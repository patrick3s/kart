"""Fase 3 — confere as partes separadas contra o NPZ original e o backup pré-Fase 3, pelos rig_original_*.
Executar na sessão aberta pelo Blender MCP, com o arquivo salvo e recarregado, definindo NPZ, MOD, BACKUP e OUT antes
de exec(). Anexa a malha do backup: recarregar o arquivo depois (wm.revert_mainfile), sem salvar.
Divisão por faces (decisão do usuário, 15/10/2026): faces e cantos aparecem exatamente uma vez; vértices e arestas
aparecem uma vez por parte cujas faces os usam (2 na costura entre roda e corpo)."""
import bpy, numpy as np, json, importlib.util
sp = importlib.util.spec_from_file_location("rot", MOD); rot = importlib.util.module_from_spec(sp); sp.loader.exec_module(rot)
z = np.load(NPZ); comp = z["components"]; lab = rot.rotulos_faces(z)
tri0 = z["loops"].reshape(-1, 3); nv0, ne0, nf0, nl0 = len(z["co"]), len(z["edges"]), len(tri0), len(z["loops"])
# multiplicidade esperada de vértices e arestas: nº de rótulos distintos entre as faces que os usam
def mult_esperada(n, idx_por_face):
    pares = np.unique(np.stack([idx_por_face.ravel(), np.repeat(lab, idx_por_face.shape[1])], 1), axis=0)
    return np.bincount(pares[:, 0], minlength=n)
v_esp = mult_esperada(nv0, tri0)
# arestas originais de cada face (pelos cantos): edge_index original não está no NPZ, então reconstruímos pelos pares de vértices
e0 = np.sort(z["edges"], 1); key0 = e0[:, 0].astype(np.int64)*nv0 + e0[:, 1]; o0 = np.argsort(key0)
def arestas_da_face(t):
    pares = np.sort(np.stack([t[:, [0, 1]], t[:, [1, 2]], t[:, [2, 0]]], 1), 2)
    k = pares[..., 0].astype(np.int64)*nv0 + pares[..., 1]
    i = np.searchsorted(key0[o0], k); return o0[i]
fe0 = arestas_da_face(tri0); e_esp = mult_esperada(ne0, fe0)
def g(c, attr, n, dt, k=1):
    a = np.empty(n*k, dt); c.foreach_get(attr, a); return a.reshape(-1, k) if k > 1 else a
AUSENTES = []
def ga(m, name, n, dt, k=1):
    a = np.zeros(n*k, dt)
    if name in m.attributes: m.attributes[name].data.foreach_get("value", a)
    else: AUSENTES.append((m.name, name))
    return a.reshape(-1, k) if k > 1 else a
def arrays(o, m=None):
    m = m or o.data; nv, ne, nf, nl = len(m.vertices), len(m.edges), len(m.polygons), len(m.loops)
    mw = np.array(o.matrix_world, np.float64) if o else np.eye(4)
    co = g(m.vertices, "co", nv, np.float32, 3).astype(np.float64); cow = co @ mw[:3, :3].T + mw[:3, 3]
    return dict(co=cow, edges=g(m.edges, "vertices", ne, np.int32, 2), loops=g(m.loops, "vertex_index", nl, np.int32),
                ledge=g(m.loops, "edge_index", nl, np.int32),
                uv=g(m.uv_layers[0].data, "uv", nl, np.float32, 2), starts=g(m.polygons, "loop_start", nf, np.int32),
                totals=g(m.polygons, "loop_total", nf, np.int32), smooth=g(m.polygons, "use_smooth", nf, bool),
                materials=g(m.polygons, "material_index", nf, np.int32), slots=[x.name for x in m.materials],
                se=ga(m, "sharp_edge", ne, bool), sf=ga(m, "sharp_face", nf, bool),
                cnorm=g(m.corner_normals, "vector", nl, np.float32, 3),
                ov=ga(m, "rig_original_vertex", nv, np.int32), oe=ga(m, "rig_original_edge", ne, np.int32),
                of=ga(m, "rig_original_face", nf, np.int32), ol=ga(m, "rig_original_corner", nl, np.int32))
MAT_LOCAL = [x.name for x in bpy.data.materials]
IMG_LOCAL = sorted((i.name, bool(i.packed_file)) for i in bpy.data.images)
ARQ = bpy.data.filepath; SUJO = bpy.data.is_dirty
with bpy.data.libraries.load(BACKUP) as (src, dst): dst.meshes = list(src.meshes)
ref = arrays(None, dst.meshes[0]); AUSENTES.clear()
r = {"arquivo": ARQ, "sujo_ao_verificar": SUJO, "backup": BACKUP, "partes": {}}
seen = {k: np.zeros(n, np.int32) for k, n in (("v", nv0), ("e", ne0), ("f", nf0), ("l", nl0))}
costura_v = v_esp > 1
maxdev = 0.; ok = True
partes = [o for o in bpy.data.objects if o.type == "MESH" and not o.library and o.data.name in rot.NOMES]
for o in partes:
    d = arrays(o); k = rot.NOMES.index(o.name); p = {}
    for kk, a in (("v", d["ov"]), ("e", d["oe"]), ("f", d["of"]), ("l", d["ol"])): np.add.at(seen[kk], a, 1)
    p["v"], p["e"], p["f"], p["cantos"] = len(d["ov"]), len(d["oe"]), len(d["of"]), len(d["ol"])
    p["faces_conforme_rotulo"] = bool((lab[d["of"]] == k).all()) and p["f"] == int((lab == k).sum())
    p["ids_unicos_na_parte"] = all(len(np.unique(d[x])) == len(d[x]) for x in ("ov", "oe", "of", "ol"))
    ilhas = np.unique(comp[tri0[d["of"], 0]]); p["ilhas"] = len(ilhas)
    p["ilhas_divididas"] = [int(i) for i in ilhas if (lab[comp[tri0[:, 0]] == i] != k).any()]
    dev = float(np.abs(d["co"]-z["co"][d["ov"]]).max()); maxdev = max(maxdev, dev); p["co_mundo_max_desvio"] = dev
    p["arestas_iguais"] = bool(np.array_equal(np.sort(d["ov"][d["edges"]], 1), np.sort(z["edges"][d["oe"]], 1)))
    p["cantos_vertices_iguais"] = bool(np.array_equal(d["ov"][d["loops"]], z["loops"][d["ol"]]))
    p["cantos_arestas_iguais"] = bool(np.array_equal(d["oe"][d["ledge"]], fe0.ravel()[d["ol"]]))
    p["faces_inicio_ordem_iguais"] = bool(np.array_equal(d["ol"][d["starts"]], z["starts"][d["of"]])) and bool(np.array_equal(d["totals"], z["totals"][d["of"]]))
    p["uv_iguais"] = bool(np.array_equal(d["uv"], z["uv"][d["ol"]]))
    p["suavizacao_igual"] = bool(np.array_equal(d["smooth"], z["smooth"][d["of"]]))
    p["material_igual"] = bool(np.array_equal(d["materials"], z["materials"][d["of"]])) and d["slots"] == MAT_LOCAL
    p["sharp_face_igual"] = bool(np.array_equal(d["sf"], ref["sf"][d["of"]]))
    p["sharp_edge_igual"] = bool(np.array_equal(d["se"], ref["se"][d["oe"]]))
    dn = np.abs(d["cnorm"]-z["corner_normals"][d["ol"]]).max(1)
    cc = costura_v[d["ov"][d["loops"]]]
    p["cantos_na_costura"] = int(cc.sum())
    p["normais_max_desvio_fora_costura"] = float(dn[~cc].max()) if (~cc).any() else 0.
    p["normais_max_desvio_costura"] = float(dn[cc].max()) if cc.any() else 0.
    p["normais_ok"] = p["normais_max_desvio_fora_costura"] == 0. and p["normais_max_desvio_costura"] <= 1e-3
    ve = np.zeros(p["v"], bool); ve[d["edges"].ravel()] = True; p["vertices_sem_aresta"] = int((~ve).sum())
    ef = np.zeros(p["e"], bool); ef[d["ledge"]] = True; p["arestas_sem_face"] = int((~ef).sum())
    mw = o.matrix_world; p["matriz_mundo_identidade"] = all(abs(mw[i][j]-(i == j)) < 1e-12 for i in range(4) for j in range(4))
    p["pai"] = o.parent.name if o.parent else None; p["modificadores"] = [x.type for x in o.modifiers]
    p["dados_exclusivos"] = o.data.users == 1 and o.data.name == o.name
    mn = d["co"].min(0); mx = d["co"].max(0)
    p["bbox_min"] = mn.round(4).tolist(); p["bbox_max"] = mx.round(4).tolist(); p["centro_bbox"] = ((mn+mx)/2).round(4).tolist()
    ok &= all(v for kk, v in p.items() if isinstance(v, bool)) and p["vertices_sem_aresta"] == 0 and p["arestas_sem_face"] == 0 \
        and p["pai"] is None and not p["modificadores"]
    r["partes"][o.name] = p
r["cada_face_original_uma_vez"] = bool((seen["f"] == 1).all()); r["cada_canto_original_uma_vez"] = bool((seen["l"] == 1).all())
r["vertices_multiplicidade_esperada"] = bool(np.array_equal(seen["v"], v_esp))
r["arestas_multiplicidade_esperada"] = bool(np.array_equal(seen["e"], e_esp))
r["vertices_costura"] = int((v_esp > 1).sum()); r["arestas_costura"] = int((e_esp > 1).sum())
r["vertices_totais_partes"] = int(seen["v"].sum()); r["arestas_totais_partes"] = int(seen["e"].sum())
ok &= r["cada_face_original_uma_vez"] and r["cada_canto_original_uma_vez"] and r["vertices_multiplicidade_esperada"] and r["arestas_multiplicidade_esperada"]
r["co_mundo_max_desvio_geral"] = maxdev; ok &= maxdev <= 1e-6
lados = {}
for n in rot.NOMES[2:]:
    c = r["partes"][n]["centro_bbox"]; lados[n] = bool((c[0] > 0) == ("Left" in n) and (c[1] < 0) == ("Front" in n))
r["lados_rodas_corretos"] = lados; ok &= all(lados.values())
r["objetos"] = sorted(o.name for o in bpy.data.objects if not o.library); r["nomes_padrao"] = sorted(rot.NOMES) == r["objetos"]; ok &= r["nomes_padrao"]
r["imagens_no_arquivo"] = IMG_LOCAL; r["materiais_no_arquivo"] = MAT_LOCAL
ok &= len(MAT_LOCAL) == 1 and len(IMG_LOCAL) == 3 and all(e for _, e in IMG_LOCAL) and not SUJO
r["atributos_ausentes_tratados_como_falso"] = AUSENTES
r["tolerancias"] = {"posicao_m": 1e-6, "normais_fora_da_costura": 0.0, "normais_na_costura": 1e-3}
r["tudo_ok"] = bool(ok)
json.dump(r, open(OUT, "w"), ensure_ascii=False, indent=1)
