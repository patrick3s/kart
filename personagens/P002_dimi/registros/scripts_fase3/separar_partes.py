"""Separa Cabeca, Corpo_Kart e Wheel_* por ilhas inteiras, sem mover origem nem alterar vértices.
Uso: Blender -b --factory-startup blender/dimi.blend --python separar_partes.py -- geometria_original.npz rotulos_partes.py saida.json"""
import bpy, sys, json, numpy as np, importlib.util
a=sys.argv[sys.argv.index("--")+1:]; npz,modp,outj=a
sp=importlib.util.spec_from_file_location("rot",modp); rot=importlib.util.module_from_spec(sp); sp.loader.exec_module(rot)
z=np.load(npz); comp=z["components"]; lab=rot.rotulos(z["co"],comp)
o=[x for x in bpy.data.objects if x.type=="MESH"][0]; m=o.data
ov=np.empty(len(m.vertices),np.int32); m.attributes["rig_original_vertex"].data.foreach_get("value",ov)
vlab=lab[comp[ov]]
res={"objeto_origem":o.name,"ilhas_por_parte":{n:[int(i) for i in np.where(lab==k)[0]] for k,n in enumerate(rot.NOMES)}}
bpy.context.view_layer.objects.active=o
for k in range(1,6):
    m=o.data
    ov=np.empty(len(m.vertices),np.int32); m.attributes["rig_original_vertex"].data.foreach_get("value",ov)
    sel=(lab[comp[ov]]==k)
    bpy.ops.object.mode_set(mode='OBJECT')
    m.vertices.foreach_set("select",sel)
    ev=np.empty(len(m.edges)*2,np.int32); m.edges.foreach_get("vertices",ev); m.edges.foreach_set("select",sel[ev.reshape(-1,2)].all(1))
    lv=np.empty(len(m.loops),np.int32); m.loops.foreach_get("vertex_index",lv)
    st=np.empty(len(m.polygons),np.int32); m.polygons.foreach_get("loop_start",st)
    m.polygons.foreach_set("select",np.logical_and.reduceat(sel[lv],st))
    for x in bpy.context.selected_objects: x.select_set(False)
    o.select_set(True); bpy.context.view_layer.objects.active=o
    antes=set(bpy.data.objects)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.separate(type='SELECTED'); bpy.ops.object.mode_set(mode='OBJECT')
    novo=[x for x in bpy.data.objects if x not in antes]; assert len(novo)==1
    n=novo[0]; n.name=rot.NOMES[k]; n.data.name=rot.NOMES[k]
    res[rot.NOMES[k]]={"v":len(n.data.vertices),"f":len(n.data.polygons)}
o.name="Corpo_Kart"; o.data.name="Corpo_Kart"
res["Corpo_Kart"]={"v":len(o.data.vertices),"f":len(o.data.polygons)}
for x in bpy.data.objects: x.select_set(False)
bpy.ops.wm.save_mainfile()
res["salvo"]=bpy.data.filepath
json.dump(res,open(outj,"w"),ensure_ascii=False,indent=1); print("SEP_OK",{k:v for k,v in res.items() if k!="ilhas_por_parte"})
