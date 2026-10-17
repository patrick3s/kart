import bpy, numpy as np, json, sys, hashlib, time
out_npz, out_json = sys.argv[sys.argv.index("--")+1:]
t0=time.time()
o=[x for x in bpy.data.objects if x.type=="MESH"][0]; m=o.data
nv,ne,nf,nl=len(m.vertices),len(m.edges),len(m.polygons),len(m.loops)
co=np.empty(nv*3,np.float32); m.vertices.foreach_get("co",co); co=co.reshape(-1,3)
ed=np.empty(ne*2,np.int32); m.edges.foreach_get("vertices",ed); ed=ed.reshape(-1,2)
lv=np.empty(nl,np.int32); m.loops.foreach_get("vertex_index",lv)
st=np.empty(nf,np.int32); m.polygons.foreach_get("loop_start",st)
tt=np.empty(nf,np.int32); m.polygons.foreach_get("loop_total",tt)
sm=np.empty(nf,bool); m.polygons.foreach_get("use_smooth",sm)
mi=np.empty(nf,np.int32); m.polygons.foreach_get("material_index",mi)
uv=np.empty(nl*2,np.float32); m.uv_layers[0].data.foreach_get("uv",uv); uv=uv.reshape(-1,2)
cn=np.empty(nl*3,np.float32); m.corner_normals.foreach_get("vector",cn); cn=cn.reshape(-1,3)
# ilhas: propagação do mínimo com salto de ponteiros
lab=np.arange(nv,dtype=np.int64); a,b=ed[:,0],ed[:,1]; it=0
while True:
    it+=1
    mn=np.minimum(lab[a],lab[b]); new=lab.copy()
    np.minimum.at(new,lab[a],mn); np.minimum.at(new,lab[b],mn)
    while True:
        nn=new[new]
        if np.array_equal(nn,new): break
        new=nn
    if np.array_equal(new,lab): break
    lab=new
u,comp=np.unique(lab,return_inverse=True); comp=comp.astype(np.int32)
nc=len(u)
cnt=np.bincount(comp,minlength=nc)
mins=np.full((nc,3),np.inf,np.float32); maxs=np.full((nc,3),-np.inf,np.float32)
for k in range(3):
    np.minimum.at(mins[:,k],comp,co[:,k]); np.maximum.at(maxs[:,k],comp,co[:,k])
# vértices coincidentes
q=np.round(co/1e-6).astype(np.int64); _,inv,qc=np.unique(q,axis=0,return_inverse=True,return_counts=True)
dup=int((qc>1).sum())
# arestas não-manifold (bordas)
fe=np.empty(len(m.loops),np.int32); m.loops.foreach_get("edge_index",fe); ec=np.bincount(fe,minlength=ne)
np.savez_compressed(out_npz,co=co,edges=ed,loops=lv,uv=uv,starts=st,totals=tt,smooth=sm,materials=mi,corner_normals=cn,components=comp)
order=np.argsort(-cnt)
islands=[{"id":int(i),"v":int(cnt[i]),"min":[round(float(x),4) for x in mins[i]],"max":[round(float(x),4) for x in maxs[i]]} for i in order]
mw=o.matrix_world
d={"objeto":o.name,"dados":m.name,"v":nv,"e":ne,"f":nf,"loops":nl,
 "tri":int((tt==3).sum()),"quad":int((tt==4).sum()),"ngon":int((tt>4).sum()),
 "matriz_mundo_identidade":all(abs(mw[i][j]-(1 if i==j else 0))<1e-9 for i in range(4) for j in range(4)),
 "bbox_min":co.min(0).round(4).tolist(),"bbox_max":co.max(0).round(4).tolist(),
 "uv_layers":[l.name for l in m.uv_layers],"uv_min":uv.min(0).round(4).tolist(),"uv_max":uv.max(0).round(4).tolist(),
 "atributos":[(x.name,x.domain,x.data_type) for x in m.attributes],
 "custom_normals":bool(m.has_custom_normals),"faces_suaves":int(sm.sum()),"material_indices":np.unique(mi).tolist(),
 "vertex_groups":[g.name for g in o.vertex_groups],"shape_keys":0 if not m.shape_keys else len(m.shape_keys.key_blocks),
 "modificadores":[x.type for x in o.modifiers],"pai":o.parent.name if o.parent else None,"acoes":len(bpy.data.actions),
 "colecoes":[c.name for c in o.users_collection],
 "ilhas":nc,"iteracoes":it,"posicoes_com_vertices_coincidentes":dup,
 "arestas_borda":int((ec==1).sum()),"arestas_mais_de_2_faces":int((ec>2).sum()),"arestas_soltas":int((ec==0).sum()),
 "hash_co_sha256":hashlib.sha256(co.tobytes()).hexdigest(),
 "hist_ilhas":{"1-10":int((cnt<=10).sum()),"11-100":int(((cnt>10)&(cnt<=100)).sum()),"101-1000":int(((cnt>100)&(cnt<=1000)).sum()),"1001-10000":int(((cnt>1000)&(cnt<=10000)).sum()),">10000":int((cnt>10000).sum())},
 "maiores_ilhas":islands[:40],"tempo_s":round(time.time()-t0,1)}
json.dump(d,open(out_json,"w"),ensure_ascii=False,indent=1)
print("OK",time.time()-t0)
