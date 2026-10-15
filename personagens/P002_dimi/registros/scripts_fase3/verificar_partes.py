"""Confere as partes separadas contra o NPZ original e o backup pré-Fase 3, pelos rig_original_*.
Uso: Blender -b --factory-startup blender/dimi.blend --python verificar_partes.py -- geometria_original.npz rotulos_partes.py backup_pre_fase3.blend saida.json"""
import bpy, numpy as np, json, sys, hashlib, importlib.util
npz,modp,backup,out=sys.argv[sys.argv.index("--")+1:]
sp=importlib.util.spec_from_file_location("rot",modp); rot=importlib.util.module_from_spec(sp); sp.loader.exec_module(rot)
z=np.load(npz); comp=z["components"]; lab=rot.rotulos(z["co"],comp)
def g(c,attr,n,dt,k=1):
    a=np.empty(n*k,dt); c.foreach_get(attr,a); return a.reshape(-1,k) if k>1 else a
def ga(m,name,n,dt,k=1):
    a=np.zeros(n*k,dt)
    if name in m.attributes: m.attributes[name].data.foreach_get("value",a)
    else: AUSENTES.append((m.name,name))  # atributo ausente = todos falsos/zero
    return a.reshape(-1,k) if k>1 else a
AUSENTES=[]
def arrays(o,m=None):
    m=m or o.data; nv,ne,nf,nl=len(m.vertices),len(m.edges),len(m.polygons),len(m.loops)
    mw=np.array(o.matrix_world,np.float64) if o else np.eye(4)
    co=g(m.vertices,"co",nv,np.float32,3).astype(np.float64); cow=co@mw[:3,:3].T+mw[:3,3]
    d=dict(co=cow,edges=g(m.edges,"vertices",ne,np.int32,2),loops=g(m.loops,"vertex_index",nl,np.int32),
      uv=g(m.uv_layers[0].data,"uv",nl,np.float32,2),starts=g(m.polygons,"loop_start",nf,np.int32),totals=g(m.polygons,"loop_total",nf,np.int32),
      smooth=g(m.polygons,"use_smooth",nf,bool),materials=g(m.polygons,"material_index",nf,np.int32),slots=[x.name for x in m.materials],
      cn=ga(m,"custom_normal",nl,np.int16,2),sf=ga(m,"sharp_face",nf,bool),se=ga(m,"sharp_edge",ne,bool),
      cnorm=g(m.corner_normals,"vector",nl,np.float32,3) if hasattr(m,"corner_normals") else None,
      ov=ga(m,"rig_original_vertex",nv,np.int32),oe=ga(m,"rig_original_edge",ne,np.int32),of=ga(m,"rig_original_face",nf,np.int32),ol=ga(m,"rig_original_corner",nl,np.int32))
    return d
nv0,ne0,nf0,nl0=len(z["co"]),len(z["edges"]),len(z["starts"]),len(z["loops"])
# estado do arquivo antes de anexar o backup (o anexo cria cópias .001 só nesta sessão)
MAT_LOCAL=[x.name for x in bpy.data.materials]
IMG_LOCAL=sorted((i.name,bool(i.packed_file)) for i in bpy.data.images)
# referência do backup pré-Fase 3 (custom_normal, sharp_*, nome do material)
with bpy.data.libraries.load(backup) as (src,dst): dst.meshes=list(src.meshes)
ref=arrays(None,dst.meshes[0]); AUSENTES.clear()
r={"arquivo":bpy.data.filepath,"backup":backup,"partes":{}}
seen={k:np.zeros(n,np.int32) for k,n in (("v",nv0),("e",ne0),("f",nf0),("l",nl0))}
maxdev=0.; ok=True
partes=[o for o in bpy.data.objects if o.type=="MESH" and not o.library]
for o in partes:
    d=arrays(o); k=rot.NOMES.index(o.name)
    np.add.at(seen["v"],d["ov"],1); np.add.at(seen["e"],d["oe"],1); np.add.at(seen["f"],d["of"],1); np.add.at(seen["l"],d["ol"],1)
    p={}
    p["v"],p["e"],p["f"],p["cantos"]=len(d["ov"]),len(d["oe"]),len(d["of"]),len(d["ol"])
    p["ilhas"]=int(len(np.unique(comp[d["ov"]])))
    p["ilhas_conforme_rotulo"]=bool((lab[comp[d["ov"]]]==k).all()) and p["ilhas"]==int((lab==k).sum())
    dev=float(np.abs(d["co"]-z["co"][d["ov"]]).max()); maxdev=max(maxdev,dev); p["co_mundo_max_desvio"]=dev
    p["arestas_iguais"]=bool(np.array_equal(np.sort(d["ov"][d["edges"]],1),np.sort(z["edges"][d["oe"]],1)))
    p["cantos_vertices_iguais"]=bool(np.array_equal(d["ov"][d["loops"]],z["loops"][d["ol"]]))
    p["faces_inicio_ordem_iguais"]=bool(np.array_equal(d["ol"][d["starts"]],z["starts"][d["of"]])) and bool(np.array_equal(d["totals"],z["totals"][d["of"]]))
    p["uv_iguais"]=bool(np.array_equal(d["uv"],z["uv"][d["ol"]]))
    p["suavizacao_igual"]=bool(np.array_equal(d["smooth"],z["smooth"][d["of"]]))
    p["material_igual"]=bool(np.array_equal(d["materials"],z["materials"][d["of"]])) and d["slots"]==MAT_LOCAL
    p["custom_normal_igual_backup"]=bool(np.array_equal(d["cn"],ref["cn"][d["ol"]]))
    p["sharp_face_igual"]=bool(np.array_equal(d["sf"],ref["sf"][d["of"]])); p["sharp_edge_igual"]=bool(np.array_equal(d["se"],ref["se"][d["oe"]]))
    p["normais_canto_max_desvio_npz"]=float(np.abs(d["cnorm"]-z["corner_normals"][d["ol"]]).max())
    mw=o.matrix_world; p["matriz_mundo_identidade"]=all(abs(mw[i][j]-(i==j))<1e-12 for i in range(4) for j in range(4))
    p["pai"]=o.parent.name if o.parent else None; p["modificadores"]=[x.type for x in o.modifiers]
    p["dados_exclusivos"]=o.data.users==1
    mn=d["co"].min(0); mx=d["co"].max(0); p["bbox_min"]=mn.round(4).tolist(); p["bbox_max"]=mx.round(4).tolist(); p["centro_bbox"]=((mn+mx)/2).round(4).tolist()
    ok&=all(v for kk,v in p.items() if isinstance(v,bool) and kk not in("dados_exclusivos",)) and p["dados_exclusivos"]
    r["partes"][o.name]=p
for k,a in seen.items(): r[f"cada_{k}_original_uma_vez"]=bool((a==1).all()); ok&=r[f"cada_{k}_original_uma_vez"]
r["co_mundo_max_desvio_geral"]=maxdev; ok&=maxdev<=1e-6
# lados das rodas: frente -Y, esquerda do piloto +X
lados={}
for n in rot.NOMES[2:]:
    c=r["partes"][n]["centro_bbox"]; lados[n]=bool((c[0]>0)==("Left" in n) and (c[1]<0)==("Front" in n))
r["lados_rodas_corretos"]=lados; ok&=all(lados.values())
r["objetos"]=sorted(o.name for o in partes); r["nomes_padrao"]=sorted(rot.NOMES)==r["objetos"]; ok&=r["nomes_padrao"]
r["imagens_no_arquivo"]=IMG_LOCAL; r["materiais_no_arquivo"]=MAT_LOCAL
ok&=len(MAT_LOCAL)==1 and len(IMG_LOCAL)==3 and all(e for _,e in IMG_LOCAL)
r["atributos_ausentes_tratados_como_falso"]=AUSENTES
r["tudo_ok"]=bool(ok)
json.dump(r,open(out,"w"),ensure_ascii=False,indent=1); print("VER_OK",r["tudo_ok"])
