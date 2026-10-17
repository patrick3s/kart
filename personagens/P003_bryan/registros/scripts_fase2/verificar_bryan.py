# Fase 2 — confere o arquivo de trabalho contra o NPZ original e o backup anterior à edição.
# Executar na sessão aberta pelo Blender MCP definindo NPZ, BACKUP e OUT antes de exec().
# Carrega a malha do backup na sessão: recarregar o arquivo depois (wm.revert_mainfile).
import bpy, numpy as np, json, hashlib
z = np.load(NPZ)
def arrays(m):
    nv, ne, nf, nl = len(m.vertices), len(m.edges), len(m.polygons), len(m.loops)
    def g(c, attr, n, dt, k=1):
        a = np.empty(n*k, dt); c.foreach_get(attr, a); return a.reshape(-1, k) if k > 1 else a
    cn = np.empty(nl*2, np.int16); m.attributes["custom_normal"].data.foreach_get("value", cn)
    sf = np.empty(nf, bool); m.attributes["sharp_face"].data.foreach_get("value", sf)
    se = np.empty(ne, bool); m.attributes["sharp_edge"].data.foreach_get("value", se)
    return dict(co=g(m.vertices, "co", nv, np.float32, 3), edges=g(m.edges, "vertices", ne, np.int32, 2),
                loops=g(m.loops, "vertex_index", nl, np.int32), uv=g(m.uv_layers[0].data, "uv", nl, np.float32, 2),
                starts=g(m.polygons, "loop_start", nf, np.int32), totals=g(m.polygons, "loop_total", nf, np.int32),
                smooth=g(m.polygons, "use_smooth", nf, bool), materials=g(m.polygons, "material_index", nf, np.int32),
                custom_normal=cn, sharp_face=sf, sharp_edge=se)
o = [x for x in bpy.data.objects if x.type == "MESH"][0]; m = o.data
mats_arquivo = [x.name for x in bpy.data.materials]; imgs_arquivo = [(i.name, bool(i.packed_file)) for i in bpy.data.images]
cur = arrays(m)
with bpy.data.libraries.load(BACKUP) as (src, dst): dst.meshes = list(src.meshes)
ref = arrays(dst.meshes[0])
r = {"arquivo": bpy.data.filepath, "backup": BACKUP}
for k in ("co", "edges", "loops", "uv", "starts", "totals", "smooth", "materials"):
    r[f"{k}_igual_npz"] = bool(np.array_equal(cur[k], z[k]))
for k in ("custom_normal", "sharp_face", "sharp_edge"):
    r[f"{k}_igual_backup"] = bool(np.array_equal(cur[k], ref[k]))
r["co_max_desvio_npz"] = float(np.abs(cur["co"]-z["co"]).max())
r["hash_co_sha256"] = hashlib.sha256(cur["co"].tobytes()).hexdigest()
mw = o.matrix_world; r["matriz_mundo_identidade"] = all(abs(mw[i][j]-(i == j)) < 1e-12 for i in range(4) for j in range(4))
for name, n in (("rig_original_vertex", len(m.vertices)), ("rig_original_edge", len(m.edges)),
                ("rig_original_face", len(m.polygons)), ("rig_original_corner", len(m.loops))):
    a = np.empty(n, np.int32); m.attributes[name].data.foreach_get("value", a); r[name] = bool(np.array_equal(a, np.arange(n)))
r["materiais_no_arquivo"] = mats_arquivo; r["imagens_no_arquivo"] = imgs_arquivo
json.dump(r, open(OUT, "w"), ensure_ascii=False, indent=1)
