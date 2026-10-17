"""Fase 5 (P003 Bryan) — comparação completa das 6 partes do rig contra o NPZ original, a divisão da Fase 3 e o arquivo da Fase 4.
Uso no MCP (arquivo salvo, recém-recarregado): B = "<pasta do personagem>/"; SAIDA = "<json>"; exec(open(<este arquivo>).read())
Carrega malhas, objetos e armature de bryan.blend1 (hash da Fase 4) e do backup pré-Fase 3: depois recarregar com
wm.revert_mainfile, sem salvar. Não altera as partes, salvo os testes combinados, desfeitos no finally.
Base: verificar_partes.py (Fase 3), sem as exigências de "sem pai/sem modificador", que a Fase 4 mudou de propósito."""
import bpy, numpy as np, json, math, hashlib, importlib.util
from mathutils import Matrix, Vector

NPZ = B + "backups/geometria_original.npz"; MOD = B + "registros/scripts_fase3/rotulos_faces.py"
FASE4 = B + "blender/bryan.blend1"; PRE3 = B + "backups/bryan_antes_fase3_20261015_192311.blend"
TOL = 1e-6; TOL_N = 1e-3
sp = importlib.util.spec_from_file_location("rot", MOD); rot = importlib.util.module_from_spec(sp); sp.loader.exec_module(rot)
z = np.load(NPZ); lab = rot.rotulos_faces(z)
tri0 = z["loops"].reshape(-1, 3); nv0, ne0, nf0, nl0 = len(z["co"]), len(z["edges"]), len(tri0), len(z["loops"])
PARTES = rot.NOMES
ARQ = bpy.data.filepath; SUJO = bpy.data.is_dirty


def mult_esperada(n, idx):
    pares = np.unique(np.stack([idx.ravel(), np.repeat(lab, idx.shape[1])], 1), axis=0)
    return np.bincount(pares[:, 0], minlength=n)


e0 = np.sort(z["edges"], 1); key0 = e0[:, 0].astype(np.int64) * nv0 + e0[:, 1]; o0 = np.argsort(key0)
pares = np.sort(np.stack([tri0[:, [0, 1]], tri0[:, [1, 2]], tri0[:, [2, 0]]], 1), 2)
fe0 = o0[np.searchsorted(key0[o0], pares[..., 0].astype(np.int64) * nv0 + pares[..., 1])]
v_esp = mult_esperada(nv0, tri0); e_esp = mult_esperada(ne0, fe0); costura_v = v_esp > 1


def g(c, a, n, dt, k=1):
    x = np.empty(n * k, dt); c.foreach_get(a, x); return x.reshape(-1, k) if k > 1 else x


def ga(m, nome, n, dt, k=1):
    x = np.zeros(n * k, dt)
    if nome in m.attributes: m.attributes[nome].data.foreach_get("value", x)
    return x.reshape(-1, k) if k > 1 else x


def arrays(m):
    nv, ne, nf, nl = len(m.vertices), len(m.edges), len(m.polygons), len(m.loops)
    d = dict(co=g(m.vertices, "co", nv, np.float32, 3), edges=g(m.edges, "vertices", ne, np.int32, 2),
             loops=g(m.loops, "vertex_index", nl, np.int32), ledge=g(m.loops, "edge_index", nl, np.int32),
             uv=g(m.uv_layers[0].data, "uv", nl, np.float32, 2), starts=g(m.polygons, "loop_start", nf, np.int32),
             totals=g(m.polygons, "loop_total", nf, np.int32), smooth=g(m.polygons, "use_smooth", nf, bool),
             materials=g(m.polygons, "material_index", nf, np.int32), slots=[x.name if x else None for x in m.materials],
             se=ga(m, "sharp_edge", ne, bool), sf=ga(m, "sharp_face", nf, bool), cn=ga(m, "custom_normal", nl, np.int16, 2),
             cnorm=g(m.corner_normals, "vector", nl, np.float32, 3), uvs=len(m.uv_layers),
             ov=ga(m, "rig_original_vertex", nv, np.int32), oe=ga(m, "rig_original_edge", ne, np.int32),
             of=ga(m, "rig_original_face", nf, np.int32), ol=ga(m, "rig_original_corner", nl, np.int32),
             attrs=sorted((a.name, a.domain, a.data_type) for a in m.attributes))
    return d


def pesos(o):
    m = o.data; idx = {vg.index: vg.name for vg in o.vertex_groups}
    return [(v.index, tuple((idx[x.group], x.weight) for x in v.groups)) for v in m.vertices]


def h(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def maxabs(a): return float(np.abs(a).max()) if np.size(a) else 0.0


# estado atual (antes de anexar qualquer coisa)
atual = {}
for n in PARTES:
    o = bpy.data.objects[n]; d = arrays(o.data)
    d["mw"] = np.array(o.matrix_world, np.float64); d["mb"] = np.array(o.matrix_basis, np.float64)
    d["pai"] = (o.parent.name if o.parent else None, o.parent_type, o.parent_bone)
    d["mpi"] = np.array(o.matrix_parent_inverse, np.float64)
    d["mods"] = [(x.name, x.type, getattr(x, "object", None) and x.object.name, getattr(x, "use_vertex_groups", None),
                  getattr(x, "use_bone_envelopes", None)) for x in o.modifiers]
    d["pesos"] = pesos(o) if o.vertex_groups else []
    atual[n] = d
rig = bpy.data.objects["Personagem_Rig"]
ossos_atual = {b.name: (tuple(b.head_local), tuple(b.tail_local), b.roll if hasattr(b, "roll") else None,
                        b.parent.name if b.parent else None, b.use_deform, b.use_connect) for b in rig.data.bones}
MATS = [(m.name, sorted(n.image.name for n in m.node_tree.nodes if n.type == "TEX_IMAGE" and n.image)) for m in bpy.data.materials]
IMGS = {i.name: (bool(i.packed_file), i.packed_file.size if i.packed_file else 0,
                 hashlib.sha256(i.packed_file.data).hexdigest()[:16] if i.packed_file else None, tuple(i.size)) for i in bpy.data.images}
CENA = {"fps": bpy.context.scene.render.fps, "unidade": bpy.context.scene.unit_settings.system,
        "escala_unidade": bpy.context.scene.unit_settings.scale_length, "acoes": [a.name for a in bpy.data.actions]}

r = {"arquivo": ARQ, "sujo_ao_verificar": SUJO, "tolerancias": {"posicao_m": TOL, "normais": TOL_N}, "partes": {}}
ok = True
seen = {k: np.zeros(n, np.int32) for k, n in (("v", nv0), ("e", ne0), ("f", nf0), ("l", nl0))}
for k, n in enumerate(PARTES):
    d = atual[n]; p = {}
    for kk, a in (("v", d["ov"]), ("e", d["oe"]), ("f", d["of"]), ("l", d["ol"])): np.add.at(seen[kk], a, 1)
    p["v"], p["e"], p["f"], p["cantos"] = len(d["ov"]), len(d["oe"]), len(d["of"]), len(d["ol"])
    p["faces_conforme_divisao_fase3"] = bool((lab[d["of"]] == k).all()) and p["f"] == int((lab == k).sum())
    p["ids_unicos"] = all(len(np.unique(d[x])) == len(d[x]) for x in ("ov", "oe", "of", "ol"))
    # posições: mundo (float64) e local+origem; arredondamento de float32 registrado separadamente
    mw = d["mw"]; co64 = d["co"].astype(np.float64)
    ref = z["co"][d["ov"]].astype(np.float64)
    p["co_mundo_max_desvio"] = maxabs(co64 @ mw[:3, :3].T + mw[:3, 3] - ref)
    p["co_local_mais_origem_max_desvio"] = maxabs(co64 + mw[:3, 3] - ref)
    # informativo (não é critério): co local é float32 relativo à origem deslocada na Fase 4; recompor e arredondar
    # para float32 pode mudar o último bit, sempre dentro de TOL
    p["co_vertices_diferentes_apos_float32"] = int(((co64 + mw[:3, 3]).astype(np.float32) != z["co"][d["ov"]]).any(1).sum())
    p["arestas_iguais"] = bool(np.array_equal(np.sort(d["ov"][d["edges"]], 1), np.sort(z["edges"][d["oe"]], 1)))
    p["cantos_vertices_iguais"] = bool(np.array_equal(d["ov"][d["loops"]], z["loops"][d["ol"]]))
    p["cantos_arestas_iguais"] = bool(np.array_equal(d["oe"][d["ledge"]], fe0.ravel()[d["ol"]]))
    p["faces_inicio_ordem_iguais"] = bool(np.array_equal(d["ol"][d["starts"]], z["starts"][d["of"]])) and bool(np.array_equal(d["totals"], z["totals"][d["of"]]))
    p["uv_camadas"] = d["uvs"]; p["uv_iguais"] = bool(np.array_equal(d["uv"], z["uv"][d["ol"]])) and d["uvs"] == 1
    p["suavizacao_igual"] = bool(np.array_equal(d["smooth"], z["smooth"][d["of"]]))
    p["material_igual"] = bool(np.array_equal(d["materials"], z["materials"][d["of"]])) and d["slots"] == [m for m, _ in MATS]
    dn = np.abs(d["cnorm"] - z["corner_normals"][d["ol"]]).max(1); cc = costura_v[d["ov"][d["loops"]]]
    p["normais_max_desvio_fora_costura"] = maxabs(dn[~cc]); p["normais_max_desvio_costura"] = maxabs(dn[cc])
    p["normais_ok"] = max(p["normais_max_desvio_fora_costura"], p["normais_max_desvio_costura"]) <= TOL_N
    ve = np.zeros(p["v"], bool); ve[d["edges"].ravel()] = True; p["vertices_sem_aresta"] = int((~ve).sum())
    ef = np.zeros(p["e"], bool); ef[d["ledge"]] = True; p["arestas_sem_face"] = int((~ef).sum())
    p["pai"] = list(d["pai"]); p["modificadores"] = d["mods"]
    p["dados_exclusivos"] = bpy.data.objects[n].data.users == 1
    ok &= (all(v for kk, v in p.items() if isinstance(v, bool)) and p["co_mundo_max_desvio"] <= TOL
           and p["co_local_mais_origem_max_desvio"] <= TOL and p["vertices_sem_aresta"] == 0 and p["arestas_sem_face"] == 0)
    r["partes"][n] = p
r["cada_face_original_uma_vez"] = bool((seen["f"] == 1).all()); r["cada_canto_original_uma_vez"] = bool((seen["l"] == 1).all())
r["vertices_multiplicidade_esperada"] = bool(np.array_equal(seen["v"], v_esp))
r["arestas_multiplicidade_esperada"] = bool(np.array_equal(seen["e"], e_esp))
r["totais"] = {"v_partes": int(seen["v"].sum()), "e_partes": int(seen["e"].sum()), "f": nf0, "cantos": nl0,
               "v_original": nv0, "e_original": ne0, "v_costura": int((v_esp > 1).sum()), "e_costura": int((e_esp > 1).sum())}
ok &= r["cada_face_original_uma_vez"] and r["cada_canto_original_uma_vez"] and r["vertices_multiplicidade_esperada"] and r["arestas_multiplicidade_esperada"]
r["materiais"] = MATS; r["imagens"] = {k: list(v) for k, v in IMGS.items()}; r["cena"] = CENA
ok &= len(MATS) == 1 and len(IMGS) == 3 and all(v[0] for v in IMGS.values()) and not CENA["acoes"]

# 2. sharp_* contra a malha única do backup pré-Fase 3 (por índice original)
with bpy.data.libraries.load(PRE3) as (src, dst): dst.meshes = list(src.meshes)
m3 = dst.meshes[0]; se3 = ga(m3, "sharp_edge", len(m3.edges), bool); sf3 = ga(m3, "sharp_face", len(m3.polygons), bool)
for n in PARTES:
    d = atual[n]; p = r["partes"][n]
    p["sharp_edge_igual_pre_fase3"] = bool(np.array_equal(d["se"], se3[d["oe"]]))
    p["sharp_face_igual_pre_fase3"] = bool(np.array_equal(d["sf"], sf3[d["of"]]))
    ok &= p["sharp_edge_igual_pre_fase3"] and p["sharp_face_igual_pre_fase3"]

# 3. igualdade exata com o arquivo da Fase 4 (bryan.blend1): o que mudou no salvamento de 15/10 21:20?
with bpy.data.libraries.load(FASE4) as (src, dst):
    dst.objects = [x for x in src.objects]; dst.images = list(src.images); dst.actions = list(src.actions)
ant = {o.name.rsplit(".", 1)[0] if o.name.rsplit(".", 1)[0] in PARTES + ["Personagem_Rig"] else o.name: o for o in dst.objects}
c4 = {}
for n in PARTES:
    o4 = ant[n]; d4 = arrays(o4.data); d = atual[n]; c = {}
    for kk in ("co", "edges", "loops", "ledge", "uv", "starts", "totals", "smooth", "materials", "se", "sf", "cn", "ov", "oe", "of", "ol"):
        c[kk] = bool(np.array_equal(d[kk], d4[kk]))
    c["normais_canto_iguais"] = bool(np.array_equal(d["cnorm"], d4["cnorm"]))
    c["atributos_iguais"] = d["attrs"] == d4["attrs"]
    # matrix_world de objeto anexado fora da cena não é avaliada (vem identidade); a mundial decorre de base, pai, inversa e ossos
    c["matriz_base_igual"] = bool(np.array_equal(d["mb"], np.array(o4.matrix_basis, np.float64)))
    c["matriz_pai_inversa_igual"] = bool(np.array_equal(d["mpi"], np.array(o4.matrix_parent_inverse, np.float64)))
    c["pai_igual"] = d["pai"] == ((o4.parent.name.rsplit(".", 1)[0] if o4.parent else None), o4.parent_type, o4.parent_bone)
    c["pesos_iguais"] = d["pesos"] == (pesos(o4) if o4.vertex_groups else [])
    c4[n] = c
r4 = ant["Personagem_Rig"]
oss4 = {b.name: (tuple(b.head_local), tuple(b.tail_local), b.roll if hasattr(b, "roll") else None,
                 b.parent.name if b.parent else None, b.use_deform, b.use_connect) for b in r4.data.bones}
r["comparacao_fase4"] = {"arquivo": FASE4, "partes": c4, "ossos_iguais": oss4 == ossos_atual,
                         "rig_matriz_igual": bool(np.array_equal(np.array(rig.matrix_world), np.array(r4.matrix_world))),
                         "pose_igual": all(np.array_equal(np.array(rig.pose.bones[b.name].matrix_basis), np.array(b.matrix_basis)) for b in r4.pose.bones),
                         "acoes_fase4": [a.name for a in dst.actions],
                         "imagens_iguais": all(IMGS.get(i.name.rsplit(".", 1)[0] if i.name not in IMGS else i.name, (None,))[2] ==
                                               (hashlib.sha256(i.packed_file.data).hexdigest()[:16] if i.packed_file else None) for i in dst.images)}
r["comparacao_fase4"]["tudo_igual"] = bool(all(all(c.values()) for c in c4.values()) and r["comparacao_fase4"]["ossos_iguais"]
                                           and r["comparacao_fase4"]["rig_matriz_igual"] and r["comparacao_fase4"]["pose_igual"]
                                           and r["comparacao_fase4"]["imagens_iguais"])

# 4. testes combinados (temporários): cabeça girada com o corpo inclinado; roda dianteira esterçada e girada ao mesmo tempo
dg = bpy.context.evaluated_depsgraph_get()


def mundo(n):
    dg.update(); e = bpy.data.objects[n].evaluated_get(dg); m = e.to_mesh()
    co = g(m.vertices, "co", len(m.vertices), np.float32, 3).astype(np.float64); mw = np.array(e.matrix_world, np.float64); e.to_mesh_clear()
    return co @ mw[:3, :3].T + mw[:3, 3]


def M_osso(nome):
    pb = rig.pose.bones[nome]
    return rig.matrix_world @ pb.matrix @ pb.bone.matrix_local.inverted() @ rig.matrix_world.inverted()


def rigido(a, b, M):
    A = np.array(M, np.float64); return maxabs(a @ A[:3, :3].T + A[:3, 3] - b)


rep = {n: mundo(n) for n in PARTES}
pose0 = {pb.name: pb.matrix_basis.copy() for pb in rig.pose.bones}; modo0 = {pb.name: pb.rotation_mode for pb in rig.pose.bones}
mb0 = {n: bpy.data.objects[n].matrix_basis.copy() for n in PARTES[2:]}
testes = {}
try:
    for pb in rig.pose.bones: pb.rotation_mode = "XYZ"
    # corpo inclinado 10° (Y local do Torso_Bone) + cabeça 15° na rolagem (Z local) e −10° no giro
    rig.pose.bones["Torso_Bone"].matrix_basis = Matrix.Rotation(math.radians(10), 4, "Y")
    rig.pose.bones["Head_Bone"].matrix_basis = Matrix.Rotation(math.radians(15), 4, "Z") @ Matrix.Rotation(math.radians(-10), 4, "Y")
    bpy.context.view_layer.update()
    Mt, Mh = M_osso("Torso_Bone"), M_osso("Head_Bone"); dep = {n: mundo(n) for n in PARTES}
    piv = rig.matrix_world @ rig.pose.bones["Head_Bone"].head; piv_esp = Mt @ Vector(rig.data.bones["Head_Bone"].head_local)
    testes["torso_Y10_cabeca_Z15_Yneg10"] = {
        "erro_rigido_cabeca": rigido(rep["Cabeca"], dep["Cabeca"], Mh),
        "erro_rigido_corpo_e_rodas": max(rigido(rep[n], dep[n], Mt) for n in PARTES if n != "Cabeca"),
        "pivo_cabeca_segue_torso": (piv - piv_esp).length}
    for pb in rig.pose.bones: pb.matrix_basis = pose0[pb.name]
    # rodas dianteiras: esterço 28° (máximo do jogo, Z local) seguido do giro 120° (X local), corpo inclinado 6° em X
    rig.pose.bones["Torso_Bone"].matrix_basis = Matrix.Rotation(math.radians(6), 4, "X")
    for n in ("Wheel_Front_Left", "Wheel_Front_Right"):
        bpy.data.objects[n].matrix_basis = mb0[n] @ Matrix.Rotation(math.radians(28), 4, "Z") @ Matrix.Rotation(math.radians(120), 4, "X")
    bpy.context.view_layer.update()
    Mt = M_osso("Torso_Bone")
    for n in ("Wheel_Front_Left", "Wheel_Front_Right"):
        o = bpy.data.objects[n]; d = mundo(n)
        centro_esp = Mt @ Vector(atual[n]["mw"][:3, 3])
        M = o.matrix_world @ Matrix(atual[n]["mw"].tolist()).inverted()
        testes[f"{n}_esterco28_giro120_torso_X6"] = {"pivo_desvio": (o.matrix_world.translation - centro_esp).length,
                                                      "erro_rigido": rigido(rep[n], d, M),
                                                      "cabeca_movimento_alem_do_torso": rigido(rep["Cabeca"], mundo("Cabeca"), Mt)}
finally:
    for pb in rig.pose.bones: pb.matrix_basis = pose0[pb.name]; pb.rotation_mode = modo0[pb.name]
    for n, m in mb0.items(): bpy.data.objects[n].matrix_basis = m
    bpy.context.view_layer.update()
for t in testes.values():
    t["ok"] = all(v <= TOL for v in t.values()); ok &= t["ok"]
r["testes_combinados"] = testes
fin = {n: mundo(n) for n in PARTES}
r["restaurado_apos_testes"] = max(maxabs(fin[n] - rep[n]) for n in PARTES) == 0.0; ok &= r["restaurado_apos_testes"]
r["tudo_ok"] = bool(ok)
json.dump(r, open(SAIDA, "w"), ensure_ascii=False, indent=1, default=float)
result = {"tudo_ok": r["tudo_ok"], "fase4_tudo_igual": r["comparacao_fase4"]["tudo_igual"],
          "fase4_diferencas": {n: [k for k, v in c.items() if not v] for n, c in c4.items()},
          "fase4_outros": {k: v for k, v in r["comparacao_fase4"].items() if k not in ("partes", "arquivo")},
          "falhas_partes": {n: [k for k, v in p.items() if v is False] for n, p in r["partes"].items()},
          "co": {n: (p["co_mundo_max_desvio"], p["co_local_mais_origem_max_desvio"], p["co_vertices_diferentes_apos_float32"]) for n, p in r["partes"].items()},
          "normais": {n: (p["normais_max_desvio_fora_costura"], p["normais_max_desvio_costura"]) for n, p in r["partes"].items()},
          "globais": [r["cada_face_original_uma_vez"], r["cada_canto_original_uma_vez"], r["vertices_multiplicidade_esperada"], r["arestas_multiplicidade_esperada"]],
          "testes": testes, "restaurado": r["restaurado_apos_testes"], "imgs": IMGS, "mats": MATS}
