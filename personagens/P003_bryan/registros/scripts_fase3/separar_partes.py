"""Fase 3 — separa UMA parte (rótulo K) do objeto de origem por seleção de FACES, sem mover vértices.
Faces da parte vão para o novo objeto; vértices e arestas na costura com outra parte são duplicados pelo
mesh.separate (não há faces novas, subdivisão nem solda). Arestas selecionadas = só as que pertencem a faces
selecionadas, para não levar arestas soltas.
Executar na sessão aberta pelo Blender MCP definindo NPZ, MOD (caminho de rotulos_faces.py) e K antes de exec().
Não salva: o salvamento é feito depois, numa chamada própria."""
import bpy, numpy as np, importlib.util
sp = importlib.util.spec_from_file_location("rot", MOD); rot = importlib.util.module_from_spec(sp); sp.loader.exec_module(rot)
z = np.load(NPZ); lab = rot.rotulos_faces(z)
fontes = [x for x in bpy.data.objects if x.type == "MESH" and x.name not in rot.NOMES[1:]]
assert len(fontes) == 1, [x.name for x in fontes]
o = fontes[0]; m = o.data
assert rot.NOMES[K] not in bpy.data.objects
if bpy.context.mode != 'OBJECT': bpy.ops.object.mode_set(mode='OBJECT')
of = np.empty(len(m.polygons), np.int32); m.attributes["rig_original_face"].data.foreach_get("value", of)
fsel = lab[of] == K
nl = len(m.loops)
le = np.empty(nl, np.int32); m.loops.foreach_get("edge_index", le)
lv = np.empty(nl, np.int32); m.loops.foreach_get("vertex_index", lv)
tt = np.empty(len(m.polygons), np.int32); m.polygons.foreach_get("loop_total", tt)
lsel = np.repeat(fsel, tt)
vsel = np.zeros(len(m.vertices), bool); vsel[lv[lsel]] = True
esel = np.zeros(len(m.edges), bool); esel[le[lsel]] = True
m.vertices.foreach_set("select", vsel); m.edges.foreach_set("select", esel); m.polygons.foreach_set("select", fsel)
for x in bpy.context.selected_objects: x.select_set(False)
o.select_set(True); bpy.context.view_layer.objects.active = o
antes = set(bpy.data.objects)
bpy.ops.object.mode_set(mode='EDIT')
bpy.context.tool_settings.mesh_select_mode = (False, False, True)
bpy.ops.mesh.separate(type='SELECTED')
bpy.ops.object.mode_set(mode='OBJECT')
novo = [x for x in bpy.data.objects if x not in antes]; assert len(novo) == 1
n = novo[0]; n.name = rot.NOMES[K]; n.data.name = rot.NOMES[K]
for x in bpy.data.objects: x.select_set(False)
res = {"parte": n.name, "faces_esperadas": int((lab == K).sum()), "v": len(n.data.vertices), "e": len(n.data.edges),
       "f": len(n.data.polygons), "origem_restante_f": len(o.data.polygons)}
