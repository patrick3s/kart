# Fase 2 — atributos inteiros com o índice original de cada elemento (rastreamento para as validações).
# Executar na sessão aberta pelo Blender MCP com bryan.blend aberto e sem alterações; salva no mesmo arquivo.
import bpy, numpy as np
assert bpy.data.filepath.endswith("/P003_bryan/blender/bryan.blend") and not bpy.data.is_dirty
o = [x for x in bpy.data.objects if x.type == "MESH"][0]; m = o.data
for name, dom, n in (("rig_original_vertex", "POINT", len(m.vertices)), ("rig_original_edge", "EDGE", len(m.edges)),
                     ("rig_original_face", "FACE", len(m.polygons)), ("rig_original_corner", "CORNER", len(m.loops))):
    assert name not in m.attributes
    a = m.attributes.new(name, "INT", dom); a.data.foreach_set("value", np.arange(n, dtype=np.int32))
bpy.ops.wm.save_mainfile()
