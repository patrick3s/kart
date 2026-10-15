"""Fase 5 — validação da preparação: preservação completa (topologia, UV, materiais, normais, texturas) no estado com rig
e teste combinado de poses (raiz + torso + cabeça + rodas ao mesmo tempo). Complementa verificar_rig.py (Fase 4).
Uso no MCP: NPZ, BACKUP (backup pré-Fase 3, malha única com rig_original_*), SAIDA; exec(open(<este arquivo>).read())
Anexa a malha e as imagens do backup só na sessão; não salva. Recarregar o arquivo (wm.revert_mainfile) depois."""
import bpy, numpy as np, json, math, hashlib
from mathutils import Matrix

TOL = 1e-6
RODAS = ("Wheel_Front_Left", "Wheel_Front_Right", "Wheel_Rear_Left", "Wheel_Rear_Right")
PARTES = ("Cabeca", "Corpo_Kart") + RODAS
z = np.load(NPZ)
nv0, ne0, nf0, nl0 = len(z["co"]), len(z["edges"]), len(z["starts"]), len(z["loops"])
r = {"arquivo": bpy.data.filepath, "arquivo_sujo_no_inicio": bpy.data.is_dirty, "backup_referencia": BACKUP,
     "tolerancia_m": TOL, "partes": {}, "malha_avaliada": {}, "texturas": {}, "teste_combinado": {}}
ok = True


def g(c, a, n, dt, k=1):
    x = np.empty(n * k, dt); c.foreach_get(a, x); return x.reshape(-1, k) if k > 1 else x


def ga(m, nome, n, dt, k=1):
    x = np.empty(n * k, dt); m.attributes[nome].data.foreach_get("value", x); return x.reshape(-1, k) if k > 1 else x


def maxabs(a):
    return float(np.abs(a).max()) if np.size(a) else 0.0


def mundo(co, mw):
    mw = np.array(mw, np.float64); return co.astype(np.float64) @ mw[:3, :3].T + mw[:3, 3]


# estado do arquivo antes de anexar o backup (o anexo cria cópias .001 só nesta sessão)
MAT_LOCAL = [m.name for m in bpy.data.materials]
IMG_LOCAL = {i.name: i for i in bpy.data.images}
img_hash = {n: hashlib.sha256(bytes(i.packed_file.data)).hexdigest() if i.packed_file else None for n, i in IMG_LOCAL.items()}
img_info = {n: {"tamanho": list(i.size), "colorspace": i.colorspace_settings.name, "empacotada": bool(i.packed_file)} for n, i in IMG_LOCAL.items()}
mat = bpy.data.materials[0]
nos_img = sorted(n.image.name for n in mat.node_tree.nodes if n.type == "TEX_IMAGE" and n.image)
ligacoes = sorted(f"{l.from_node.name}.{l.from_socket.name}->{l.to_node.name}.{l.to_socket.name}" for l in mat.node_tree.links)

with bpy.data.libraries.load(BACKUP) as (src, dst):
    dst.meshes = list(src.meshes); dst.images = list(src.images); dst.materials = list(src.materials)
ref = dst.meshes[0]
rl = len(ref.loops)
ref_ol = ga(ref, "rig_original_corner", rl, np.int32); ref_of = ga(ref, "rig_original_face", len(ref.polygons), np.int32)
ref_oe = ga(ref, "rig_original_edge", len(ref.edges), np.int32)
# reordena os dados codificados do backup pelo identificador original
cn_ref = np.zeros((nl0, 2), np.int16); cn_ref[ref_ol] = ga(ref, "custom_normal", rl, np.int16, 2)
sf_ref = np.zeros(nf0, bool); sf_ref[ref_of] = ga(ref, "sharp_face", len(ref.polygons), bool) if "sharp_face" in ref.attributes else False
se_ref = np.zeros(ne0, bool); se_ref[ref_oe] = ga(ref, "sharp_edge", len(ref.edges), bool) if "sharp_edge" in ref.attributes else False
r["backup_tem_sharp"] = ["sharp_face" in ref.attributes, "sharp_edge" in ref.attributes]

# texturas: dados empacotados idênticos aos do backup pré-Fase 3
ref_img = {i.name.rsplit(".", 1)[0] if i.name.endswith(".001") else i.name: i for i in dst.images}
for n, h in img_hash.items():
    ri = ref_img.get(n); hr = hashlib.sha256(bytes(ri.packed_file.data)).hexdigest() if ri and ri.packed_file else None
    r["texturas"][n] = dict(img_info[n], sha256=h, igual_backup=(h is not None and h == hr))
r["texturas_ok"] = len(img_hash) == 3 and all(t["igual_backup"] and t["empacotada"] for t in r["texturas"].values())
r["material"] = {"nomes": MAT_LOCAL, "imagens_nos_nos": nos_img, "ligacoes": ligacoes}
ref_mat = dst.materials[0]
r["material"]["ligacoes_iguais_backup"] = ligacoes == sorted(
    f"{l.from_node.name}.{l.from_socket.name}->{l.to_node.name}.{l.to_socket.name}" for l in ref_mat.node_tree.links)
r["material_ok"] = len(MAT_LOCAL) == 1 and nos_img == sorted(img_hash) and r["material"]["ligacoes_iguais_backup"]
ok &= r["texturas_ok"] and r["material_ok"]

seen = {k: np.zeros(n, np.int32) for k, n in (("v", nv0), ("e", ne0), ("f", nf0), ("l", nl0))}
dg = bpy.context.evaluated_depsgraph_get(); dg.update()
tot = dict(v=0, e=0, f=0, l=0)
for n in PARTES:
    o = bpy.data.objects[n]; m = o.data; nv, ne, nf, nl = len(m.vertices), len(m.edges), len(m.polygons), len(m.loops)
    ov, oe, of, ol = (ga(m, a, c, np.int32) for a, c in (("rig_original_vertex", nv), ("rig_original_edge", ne),
                                                         ("rig_original_face", nf), ("rig_original_corner", nl)))
    for k, a in zip("vefl", (ov, oe, of, ol)): np.add.at(seen[k], a, 1)
    tot["v"] += nv; tot["e"] += ne; tot["f"] += nf; tot["l"] += nl
    ed = g(m.edges, "vertices", ne, np.int32, 2); lp = g(m.loops, "vertex_index", nl, np.int32)
    st = g(m.polygons, "loop_start", nf, np.int32); tt = g(m.polygons, "loop_total", nf, np.int32)
    co = mundo(g(m.vertices, "co", nv, np.float32, 3), o.matrix_world)
    p = {"v": nv, "e": ne, "f": nf, "cantos": nl, "dados_exclusivos": m.users == 1}
    p["co_mundo_base_max_desvio"] = maxabs(co - z["co"][ov])
    p["arestas_iguais"] = bool(np.array_equal(np.sort(ov[ed], 1), np.sort(z["edges"][oe], 1)))
    p["cantos_vertices_iguais"] = bool(np.array_equal(ov[lp], z["loops"][ol]))
    p["faces_inicio_ordem_iguais"] = bool(np.array_equal(ol[st], z["starts"][of])) and bool(np.array_equal(tt, z["totals"][of]))
    p["uv_camadas"] = [u.name for u in m.uv_layers]
    p["uv_iguais"] = bool(np.array_equal(g(m.uv_layers[0].data, "uv", nl, np.float32, 2), z["uv"][ol]))
    p["suavizacao_igual"] = bool(np.array_equal(g(m.polygons, "use_smooth", nf, bool), z["smooth"][of]))
    p["material_indices_iguais"] = bool(np.array_equal(g(m.polygons, "material_index", nf, np.int32), z["materials"][of]))
    p["material_slots"] = [x.name for x in m.materials]
    p["custom_normal_igual_backup"] = bool(np.array_equal(ga(m, "custom_normal", nl, np.int16, 2), cn_ref[ol]))
    p["sharp_face_igual_backup"] = bool(np.array_equal(ga(m, "sharp_face", nf, bool) if "sharp_face" in m.attributes else np.zeros(nf, bool), sf_ref[of]))
    p["sharp_edge_igual_backup"] = bool(np.array_equal(ga(m, "sharp_edge", ne, bool) if "sharp_edge" in m.attributes else np.zeros(ne, bool), se_ref[oe]))
    cnorm = g(m.corner_normals, "vector", nl, np.float32, 3)
    dn = np.abs(cnorm - z["corner_normals"][ol]).max(1)
    p["normais_canto_max_desvio_npz"] = float(dn.max())
    dots = np.clip((cnorm.astype(np.float64) * z["corner_normals"][ol]).sum(1) / np.maximum(
        np.linalg.norm(cnorm, axis=1) * np.linalg.norm(z["corner_normals"][ol], axis=1), 1e-12), -1, 1)
    p["normais_canto_max_angulo_graus"] = float(np.degrees(np.arccos(dots.min())))
    p["normais_canto_acima_1e-4"] = int((dn > 1e-4).sum())
    p["atributos"] = sorted(a.name for a in m.attributes if not a.name.startswith("."))
    p["shape_keys"] = m.shape_keys is not None
    # malha avaliada (com o modificador Armature em repouso): mesma topologia, UV e posições
    e = o.evaluated_get(dg); me = e.to_mesh()
    a = {"contagens_iguais_base": (len(me.vertices), len(me.edges), len(me.polygons), len(me.loops)) == (nv, ne, nf, nl)}
    if a["contagens_iguais_base"]:
        a["arestas_iguais_base"] = bool(np.array_equal(g(me.edges, "vertices", ne, np.int32, 2), ed))
        a["cantos_iguais_base"] = bool(np.array_equal(g(me.loops, "vertex_index", nl, np.int32), lp))
        a["uv_iguais_npz"] = bool(np.array_equal(g(me.uv_layers[0].data, "uv", nl, np.float32, 2), z["uv"][ol]))
        a["co_mundo_avaliado_max_desvio_npz"] = maxabs(mundo(g(me.vertices, "co", nv, np.float32, 3), e.matrix_world) - z["co"][ov])
        a["normais_canto_avaliadas_max_desvio_npz"] = maxabs(g(me.corner_normals, "vector", nl, np.float32, 3) - z["corner_normals"][ol])
    e.to_mesh_clear()
    r["malha_avaliada"][n] = a
    p["ok"] = bool(p["dados_exclusivos"] and p["co_mundo_base_max_desvio"] <= TOL and p["arestas_iguais"] and p["cantos_vertices_iguais"]
                   and p["faces_inicio_ordem_iguais"] and p["uv_iguais"] and p["suavizacao_igual"] and p["material_indices_iguais"]
                   and p["material_slots"] == MAT_LOCAL and p["custom_normal_igual_backup"] and p["sharp_face_igual_backup"]
                   and p["sharp_edge_igual_backup"] and p["normais_canto_max_angulo_graus"] < 0.1 and not p["shape_keys"]
                   and a["contagens_iguais_base"] and a["arestas_iguais_base"] and a["cantos_iguais_base"] and a["uv_iguais_npz"]
                   and a["co_mundo_avaliado_max_desvio_npz"] <= TOL)
    ok &= p["ok"]; r["partes"][n] = p
for k, a in seen.items():
    r[f"cada_{k}_original_uma_vez"] = bool((a == 1).all()); ok &= r[f"cada_{k}_original_uma_vez"]
r["totais"] = tot; r["totais_originais"] = dict(v=nv0, e=ne0, f=nf0, l=nl0)
r["totais_iguais"] = tot == r["totais_originais"]; ok &= r["totais_iguais"]

# remove o que foi anexado do backup antes do teste de poses
for x in list(dst.meshes): bpy.data.meshes.remove(x)
for x in list(dst.materials): bpy.data.materials.remove(x)
for x in list(dst.images): bpy.data.images.remove(x)
r["anexos_removidos"] = len(bpy.data.meshes) == 6 and len(bpy.data.images) == 3 and len(bpy.data.materials) == 1

# teste combinado: raiz Z 20°, torso Y 10°, cabeça Y 25° + Z 10°, FL giro X 90° + esterço Z 30°, RR giro X -45°
rig = bpy.data.objects["Personagem_Rig"]


def avaliado(n):
    dg.update(); e = bpy.data.objects[n].evaluated_get(dg); me = e.to_mesh()
    c = mundo(g(me.vertices, "co", len(me.vertices), np.float32, 3), e.matrix_world); e.to_mesh_clear(); return c


repouso = {n: avaliado(n) for n in PARTES}
pose0 = {pb.name: pb.matrix_basis.copy() for pb in rig.pose.bones}
mb0 = {n: bpy.data.objects[n].matrix_basis.copy() for n in RODAS}
t = {}
try:
    R = lambda gr, ax: Matrix.Rotation(math.radians(gr), 4, ax)
    rig.pose.bones["Root_Bone"].matrix_basis = R(20, "Z")
    rig.pose.bones["Torso_Bone"].matrix_basis = R(10, "Y")
    rig.pose.bones["Head_Bone"].matrix_basis = R(25, "Y") @ R(10, "Z")
    giros = {"Wheel_Front_Left": R(30, "Z") @ R(90, "X"), "Wheel_Rear_Right": R(-45, "X")}
    for n, M in giros.items(): bpy.data.objects[n].matrix_basis = mb0[n] @ M
    bpy.context.view_layer.update()

    def M_osso(nome):
        pb = rig.pose.bones[nome]; return rig.matrix_world @ pb.matrix @ pb.bone.matrix_local.inverted() @ rig.matrix_world.inverted()
    Mt, Mh = M_osso("Torso_Bone"), M_osso("Head_Bone")
    esperado = {"Corpo_Kart": Mt, "Cabeca": Mh}
    for n in RODAS:  # roda: torso aplicado à roda em repouso, depois o giro local em torno da própria origem
        esperado[n] = Mt @ (mb0[n] @ giros.get(n, Matrix.Identity(4))) @ mb0[n].inverted()
    for n in PARTES:
        A = np.array(esperado[n], np.float64); d = avaliado(n)
        t[n] = {"erro_vs_composicao_esperada": maxabs(repouso[n] @ A[:3, :3].T + A[:3, 3] - d), "movimento_max": maxabs(d - repouso[n])}
    # pivô da cabeça acompanha o fim do Neck_Bone; centros das rodas acompanham o torso
    piv_cab = rig.matrix_world @ rig.pose.bones["Head_Bone"].head
    t["pivo_cabeca_vs_fim_neck"] = (piv_cab - rig.matrix_world @ rig.pose.bones["Neck_Bone"].tail).length
    t["pivo_cabeca_vs_torso_aplicado"] = (piv_cab - Mt @ rig.data.bones["Head_Bone"].head_local).length
    t["centros_rodas_vs_torso_aplicado"] = max((bpy.data.objects[n].matrix_world.translation - Mt @ mb0[n].translation).length for n in RODAS)
    t["ok"] = bool(all(t[n]["erro_vs_composicao_esperada"] <= 1e-6 for n in PARTES) and t["pivo_cabeca_vs_fim_neck"] <= TOL
                   and t["pivo_cabeca_vs_torso_aplicado"] <= TOL and t["centros_rodas_vs_torso_aplicado"] <= TOL)
finally:
    for pb in rig.pose.bones: pb.matrix_basis = pose0[pb.name]
    for n in RODAS: bpy.data.objects[n].matrix_basis = mb0[n]
    bpy.context.view_layer.update()
r["teste_combinado"] = t
r["restaurado_apos_teste"] = max(maxabs(avaliado(n) - repouso[n]) for n in PARTES) == 0.0
ok &= t.get("ok", False) and r["restaurado_apos_teste"] and r["anexos_removidos"]
r["tudo_ok"] = bool(ok)
json.dump(r, open(SAIDA, "w"), ensure_ascii=False, indent=1, default=float)
result = {"tudo_ok": r["tudo_ok"], "partes": {n: p["ok"] for n, p in r["partes"].items()}, "texturas_ok": r["texturas_ok"],
          "material_ok": r["material_ok"], "combinado": t.get("ok"), "restaurado": r["restaurado_apos_teste"],
          "uma_vez": [r[f"cada_{k}_original_uma_vez"] for k in "vefl"]}
