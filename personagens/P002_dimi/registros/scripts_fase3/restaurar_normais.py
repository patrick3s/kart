"""Restaura custom_normal (INT16_2D) de cada parte a partir do backup pré-Fase 3, via rig_original_corner.
A passagem pelo modo de edição re-codifica as normais personalizadas; topologia e posições não mudam.
Uso: Blender -b --factory-startup blender/dimi.blend --python restaurar_normais.py -- backup_pre_fase3.blend"""
import bpy, sys, numpy as np
B=sys.argv[sys.argv.index("--")+1]
antes={c:set(getattr(bpy.data,c)) for c in ("meshes","materials","images")}
with bpy.data.libraries.load(B) as (s,d): d.meshes=list(s.meshes)
rm=d.meshes[0]; ref=np.empty(len(rm.loops)*2,np.int16); rm.attributes["custom_normal"].data.foreach_get("value",ref); ref=ref.reshape(-1,2)
for o in [x for x in bpy.data.objects if x.type=="MESH" and not x.library]:
    m=o.data; nl=len(m.loops)
    ol=np.empty(nl,np.int32); m.attributes["rig_original_corner"].data.foreach_get("value",ol)
    cur=np.empty(nl*2,np.int16); m.attributes["custom_normal"].data.foreach_get("value",cur)
    dif=int((cur.reshape(-1,2)!=ref[ol]).any(1).sum())
    m.attributes["custom_normal"].data.foreach_set("value",ref[ol].ravel()); m.update()
    print("REST",o.name,"cantos_diferentes_antes",dif)
# remove tudo o que veio do backup (malha, material e imagens anexados)
for c in ("meshes","materials","images"):
    for x in [x for x in getattr(bpy.data,c) if x not in antes[c]]: getattr(bpy.data,c).remove(x)
bpy.ops.wm.save_mainfile(); print("REST_OK")
