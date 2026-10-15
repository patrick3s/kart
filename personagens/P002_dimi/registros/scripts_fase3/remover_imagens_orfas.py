"""Remove imagens sem usuário (cópias .001 anexadas por engano na primeira restauração de normais) e salva."""
import bpy
usadas=set()
for mat in bpy.data.materials:
    if mat.users and mat.node_tree:
        for n in mat.node_tree.nodes:
            if n.type=="TEX_IMAGE" and n.image: usadas.add(n.image)
rem=[i.name for i in bpy.data.images if i not in usadas]
for n in rem: bpy.data.images.remove(bpy.data.images[n])
for m in [m for m in bpy.data.materials if m.users==0]: bpy.data.materials.remove(m)
print("REMOVIDAS",rem,"USADAS",sorted(i.name for i in usadas))
bpy.ops.wm.save_mainfile(); print("ORF_OK")
