"""Fase 4 (P003 Bryan) — confere pivôs, ossos, pesos, parentesco e preservação; faz testes temporários de rotação e os desfaz.
Uso no MCP: NPZ, MEDIDAS, INSTANTANEO (npz do montar_rig.py, ou None), SAIDA; exec(open(<este arquivo>).read())
Não salva o arquivo. Posições comparadas no espaço mundial contra backups/geometria_original.npz (rig_original_vertex).
Base: verificar_rig.py do P002, acrescido da separação das normais dentro/fora da costura da Fase 3 e da conferência de sharp_*."""
import bpy, numpy as np, json, math
from mathutils import Matrix, Vector

TOL = 1e-6
RODAS = ("Wheel_Front_Left", "Wheel_Front_Right", "Wheel_Rear_Left", "Wheel_Rear_Right")
PARTES = ("Cabeca", "Corpo_Kart") + RODAS
OSSO_DA_MALHA = {"Cabeca": "Head_Bone", "Corpo_Kart": "Torso_Bone"}
HIERARQUIA = {"Root_Bone": None, "Torso_Bone": "Root_Bone", "Neck_Bone": "Torso_Bone", "Head_Bone": "Neck_Bone"}
DEFORMA = {"Root_Bone": False, "Torso_Bone": True, "Neck_Bone": False, "Head_Bone": True}
z = np.load(NPZ)
med = json.load(open(MEDIDAS))
snap = np.load(INSTANTANEO) if INSTANTANEO else None
rig = bpy.data.objects["Personagem_Rig"]
dg = bpy.context.evaluated_depsgraph_get()
r = {"arquivo": bpy.data.filepath, "arquivo_sujo_no_inicio": bpy.data.is_dirty, "tolerancia_m": TOL, "partes": {}, "ossos": {}, "testes": {}}
ok = True


TOL_NORMAL = 1e-3  # tolerância das normais decodificadas (Fase 3: costura ≤ 1e-3)


def attr(m, nome, n, dt, k=1):
    a = np.zeros(n * k, dt)
    if nome in m.attributes:  # sharp_* ausente equivale a falso
        m.attributes[nome].data.foreach_get("value", a)
    return a.reshape(-1, k) if k > 1 else a


# vértices originais que ficaram em mais de uma parte (costura da Fase 3)
_cont = np.zeros(len(z["co"]), np.int32)
for _n in PARTES:
    _m = bpy.data.objects[_n].data
    np.add.at(_cont, np.unique(attr(_m, "rig_original_vertex", len(_m.vertices), np.int32)), 1)
COSTURA = _cont > 1
r["vertices_originais_na_costura"] = int(COSTURA.sum())


def mundo_base(o):
    m = o.data
    co = np.empty(len(m.vertices) * 3, np.float32); m.vertices.foreach_get("co", co)
    mw = np.array(o.matrix_world, np.float64)
    return co.reshape(-1, 3).astype(np.float64) @ mw[:3, :3].T + mw[:3, 3]


def mundo_avaliado(o):
    dg.update()
    e = o.evaluated_get(dg); m = e.to_mesh()
    co = np.empty(len(m.vertices) * 3, np.float32); m.vertices.foreach_get("co", co)
    mw = np.array(e.matrix_world, np.float64); e.to_mesh_clear()
    return co.reshape(-1, 3).astype(np.float64) @ mw[:3, :3].T + mw[:3, 3]


def maxabs(a):
    return float(np.abs(a).max()) if np.size(a) else 0.0


# 1. partes: preservação, pivôs, pesos, parentesco
ov_cache = {}
for n in PARTES:
    o = bpy.data.objects[n]; m = o.data; p = {}
    ov = attr(m, "rig_original_vertex", len(m.vertices), np.int32); ov_cache[n] = ov
    ref = z["co"][ov].astype(np.float64)
    p["co_mundo_base_max_desvio"] = maxabs(mundo_base(o) - ref)
    p["co_mundo_avaliado_repouso_max_desvio"] = maxabs(mundo_avaliado(o) - ref)
    ol = attr(m, "rig_original_corner", len(m.loops), np.int32)
    cn = attr(m, "custom_normal", len(m.loops), np.int16, 2)
    if snap is not None:
        p["custom_normal_igual_pre_fase4"] = bool(np.array_equal(cn, snap[n + "__cn"]))
        p["sharp_edge_igual_pre_fase4"] = bool(np.array_equal(attr(m, "sharp_edge", len(m.edges), bool), snap[n + "__se"]))
        p["sharp_face_igual_pre_fase4"] = bool(np.array_equal(attr(m, "sharp_face", len(m.polygons), bool), snap[n + "__sf"]))
    cnorm = np.empty(len(m.loops) * 3, np.float32); m.corner_normals.foreach_get("vector", cnorm)
    dn = np.abs(cnorm.reshape(-1, 3) - z["corner_normals"][ol]).max(1)
    lv = np.empty(len(m.loops), np.int32); m.loops.foreach_get("vertex_index", lv)
    na_costura = COSTURA[ov[lv]]
    p["normais_canto_max_desvio_npz_fora_costura"] = maxabs(dn[~na_costura])
    p["normais_canto_max_desvio_npz_costura"] = maxabs(dn[na_costura])
    p["cantos_na_costura"] = int(na_costura.sum())
    p["normais_ok"] = p["normais_canto_max_desvio_npz_fora_costura"] <= TOL_NORMAL and p["normais_canto_max_desvio_npz_costura"] <= TOL_NORMAL
    p["origem_mundo"] = list(o.matrix_world.translation)
    alvo = med["cabeca"]["pivo_adotado"] if n == "Cabeca" else (med["rodas"][n]["pivo_adotado"] if n in RODAS else [0, 0, 0])
    p["origem_desvio_do_adotado"] = maxabs(np.array(p["origem_mundo"]) - alvo)
    # float32: com o Torso_Bone inclinado em X e Y, a compensação do parentesco das rodas deixa ruído ≈ 3e-8 na matriz
    p["rotacao_escala_desvio_identidade"] = maxabs(np.array(o.matrix_world.to_3x3()) - np.eye(3))
    p["rotacao_escala_identidade"] = p["rotacao_escala_desvio_identidade"] <= TOL
    p["pai"], p["tipo_pai"], p["osso_pai"] = (o.parent.name if o.parent else None), o.parent_type, o.parent_bone
    p["modificadores"] = [(x.name, x.type, getattr(x, "object", None) and x.object.name, getattr(x, "use_vertex_groups", None),
                           getattr(x, "use_bone_envelopes", None), getattr(x, "use_deform_preserve_volume", None)) for x in o.modifiers]
    grupos = [g.name for g in o.vertex_groups]; p["grupos"] = grupos
    if n in OSSO_DA_MALHA:
        pesos = []; sem = 0; multiplos = 0
        for v in m.vertices:
            if len(v.groups) == 0: sem += 1
            if len(v.groups) > 1: multiplos += 1
            pesos.extend(g.weight for g in v.groups)
        pesos = np.array(pesos)
        p["vertices_sem_peso"], p["vertices_com_mais_de_um_grupo"] = sem, multiplos
        p["pesos_todos_1"] = bool(len(pesos) == len(m.vertices) and (pesos == 1.0).all())
        cond = (grupos == [OSSO_DA_MALHA[n]] and p["pesos_todos_1"] and sem == 0 and multiplos == 0
                and p["pai"] == "Personagem_Rig" and p["tipo_pai"] == "OBJECT"
                and p["modificadores"] == [("Rig_Rigido_Sem_Deformacao", "ARMATURE", "Personagem_Rig", True, False, False)])
    else:
        cond = (grupos == [] and p["modificadores"] == [] and p["pai"] == "Personagem_Rig"
                and p["tipo_pai"] == "BONE" and p["osso_pai"] == "Torso_Bone")
    p["configuracao_ok"] = bool(cond)
    p["ok"] = bool(cond and p["co_mundo_base_max_desvio"] <= TOL and p["co_mundo_avaliado_repouso_max_desvio"] <= TOL
                   and p["origem_desvio_do_adotado"] <= TOL and p["rotacao_escala_identidade"]
                   and p.get("custom_normal_igual_pre_fase4", True) and p.get("sharp_edge_igual_pre_fase4", True)
                   and p.get("sharp_face_igual_pre_fase4", True) and p["normais_ok"])
    ok &= p["ok"]; r["partes"][n] = p

# 2. ossos
for b in rig.data.bones:
    r["ossos"][b.name] = {"inicio": list(b.head_local), "fim": list(b.tail_local), "pai": b.parent.name if b.parent else None,
                          "conectado": b.use_connect, "deforma": b.use_deform, "rolagem_matriz": [list(x) for x in b.matrix_local.to_3x3()]}
r["ossos_ok"] = (set(r["ossos"]) == set(HIERARQUIA) and all(r["ossos"][k]["pai"] == v for k, v in HIERARQUIA.items())
                 and all(r["ossos"][k]["deforma"] == v for k, v in DEFORMA.items()))
r["rig_matriz_identidade"] = rig.matrix_world == Matrix.Identity(4)
r["pivo_cabeca_igual_inicio_head_bone"] = maxabs(np.array(rig.data.bones["Head_Bone"].head_local) - r["partes"]["Cabeca"]["origem_mundo"])
r["fim_neck_igual_inicio_head"] = maxabs(np.array(rig.data.bones["Neck_Bone"].tail_local) - rig.data.bones["Head_Bone"].head_local)
r["pose_em_repouso"] = all(pb.matrix_basis == Matrix.Identity(4) for pb in rig.pose.bones)
ok &= r["ossos_ok"] and r["rig_matriz_identidade"] and r["pivo_cabeca_igual_inicio_head_bone"] <= TOL and r["pose_em_repouso"]
# eixo vertical do Head_Bone (Y local) em relação ao Z mundial
r["head_bone_eixo_y_local_no_mundo"] = list(rig.data.bones["Head_Bone"].matrix_local.to_3x3().col[1])


# 3. testes temporários (restaurados no finally)
def posicoes():
    return {n: mundo_avaliado(bpy.data.objects[n]) for n in PARTES}


def rigido(antes, depois, M):
    """erro em relação à transformação rígida M (4x4, mundo) aplicada às posições de antes"""
    A = np.array(M, np.float64)
    return maxabs(antes @ A[:3, :3].T + A[:3, 3] - depois)


repouso = posicoes()
pose0 = {pb.name: pb.matrix_basis.copy() for pb in rig.pose.bones}
mb0 = {n: bpy.data.objects[n].matrix_basis.copy() for n in RODAS}
try:
    for osso, eixo, graus in (("Head_Bone", "Y", 25), ("Head_Bone", "Y", -40), ("Head_Bone", "Z", 15), ("Head_Bone", "X", 15),
                              ("Torso_Bone", "Y", 10), ("Root_Bone", "Z", 20)):
        pb = rig.pose.bones[osso]
        pb.rotation_mode = "XYZ"; pb.matrix_basis = Matrix.Rotation(math.radians(graus), 4, eixo)
        bpy.context.view_layer.update()
        depois = posicoes()
        # transformação mundial do osso: pose * repouso^-1
        M = rig.matrix_world @ pb.matrix @ pb.bone.matrix_local.inverted() @ rig.matrix_world.inverted()
        piv0 = rig.matrix_world @ pb.bone.head_local; piv1 = rig.matrix_world @ pb.head
        moveis = {"Head_Bone": ["Cabeca"], "Torso_Bone": list(PARTES), "Root_Bone": list(PARTES)}[osso]
        t = {"pivo_deslocamento": (piv1 - piv0).length,
             "erro_rigido_partes_moveis": max(rigido(repouso[n], depois[n], M) for n in moveis),
             "movimento_max_partes_fixas": max([maxabs(depois[n] - repouso[n]) for n in PARTES if n not in moveis] or [0.0]),
             "movimento_max_partes_moveis": max(maxabs(depois[n] - repouso[n]) for n in moveis)}
        if osso == "Head_Bone":
            # abertura da base: menor Z da cabeça girada em relação à gola (só medição; conferência visual nas vistas)
            t["cabeca_z_min"] = float(depois["Cabeca"][:, 2].min())
        t["ok"] = t["pivo_deslocamento"] <= TOL and t["erro_rigido_partes_moveis"] <= 1e-6 and t["movimento_max_partes_fixas"] == 0.0
        ok &= t["ok"]; r["testes"][f"{osso}_{eixo}_{graus}"] = t
        pb.matrix_basis = pose0[osso]; bpy.context.view_layer.update()
    # rodas: giro (X local) e esterço (Z local) em torno da própria origem
    for n in RODAS:
        o = bpy.data.objects[n]; t = {}
        for eixo, graus in (("X", 90), ("Z", 30)):
            o.matrix_basis = mb0[n] @ Matrix.Rotation(math.radians(graus), 4, eixo); bpy.context.view_layer.update()
            d = mundo_avaliado(o)
            t[f"pivo_deslocamento_{eixo}{graus}"] = (o.matrix_world.translation - Vector(r["partes"][n]["origem_mundo"])).length
            t[f"outras_partes_movimento_{eixo}{graus}"] = max(maxabs(mundo_avaliado(bpy.data.objects[k]) - repouso[k]) for k in PARTES if k != n)
            o.matrix_basis = mb0[n]
        # oscilação do contato com o chão ao girar 360° (ovalização do pneu)
        zmin = []
        for a in range(0, 360, 15):
            o.matrix_basis = mb0[n] @ Matrix.Rotation(math.radians(a), 4, "X"); bpy.context.view_layer.update()
            zmin.append(float(mundo_avaliado(o)[:, 2].min()))
        o.matrix_basis = mb0[n]; bpy.context.view_layer.update()
        t["z_min_no_giro"] = [min(zmin), max(zmin)]; t["oscilacao_contato_m"] = max(zmin) - min(zmin)
        t["ok"] = all(v <= TOL for k, v in t.items() if k.startswith(("pivo_", "outras_")))
        ok &= t["ok"]; r["testes"][n] = t
finally:
    for pb in rig.pose.bones:
        pb.matrix_basis = pose0[pb.name]
    for n in RODAS:
        bpy.data.objects[n].matrix_basis = mb0[n]
    bpy.context.view_layer.update()
final = posicoes()
r["restaurado_apos_testes"] = max(maxabs(final[n] - repouso[n]) for n in PARTES) == 0.0
ok &= r["restaurado_apos_testes"]
r["tudo_ok"] = bool(ok)
json.dump(r, open(SAIDA, "w"), ensure_ascii=False, indent=1, default=float)
result = {"tudo_ok": r["tudo_ok"], "partes": {n: (p["ok"], p["co_mundo_base_max_desvio"], p["co_mundo_avaliado_repouso_max_desvio"]) for n, p in r["partes"].items()},
          "testes": {k: v["ok"] for k, v in r["testes"].items()}, "restaurado": r["restaurado_apos_testes"]}
