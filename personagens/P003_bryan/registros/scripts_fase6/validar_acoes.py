"""Fase 6 (P003 Bryan) — valida as ações da cabeça: keyframes, alças, curva amostrada, espelhamento, pivô, isolamento e rigidez.
Uso no MCP: NPZ, SAIDA, AMPLITUDE_GRAUS; exec(open(<este arquivo>).read()). Muda o quadro e a ação ativa só para medir
e devolve ao estado de entrada (ação e quadro). Não salva.
Base: script homônimo do P002, sem alterações de lógica; eixo reconferido no Bryan (Y local = +Z mundial)."""
import bpy, math, json
import numpy as np
from mathutils import Matrix, Vector
from bpy_extras import anim_utils

TOL_POS = 1e-6
RODAS = ("Wheel_Front_Left", "Wheel_Front_Right", "Wheel_Rear_Left", "Wheel_Rear_Right")
FIXAS = ("Corpo_Kart",) + RODAS
NOMES = {"Cabeca_Direita_Ida_e_Volta": -1, "Cabeca_Esquerda_Ida_e_Volta": +1}
AMOSTRA_QUADROS = (1, 13, 25, 37, 49)
sc = bpy.context.scene; rig = bpy.data.objects["Personagem_Rig"]; ad = rig.animation_data; pb = rig.pose.bones["Head_Bone"]
z = np.load(NPZ)
dg = bpy.context.evaluated_depsgraph_get()
acao0, quadro0 = ad.action, sc.frame_current
r = {"arquivo": bpy.data.filepath, "arquivo_sujo_no_inicio": bpy.data.is_dirty, "fps": [sc.render.fps, sc.render.fps_base],
     "previa": [sc.use_preview_range, sc.frame_preview_start, sc.frame_preview_end], "intervalo": [sc.frame_start, sc.frame_end],
     "nla_trilhas": len(ad.nla_tracks), "drivers": len(ad.drivers), "acoes_no_arquivo": sorted(a.name for a in bpy.data.actions), "acoes": {}}
ok = r["fps"] == [24, 1.0] and r["previa"] == [True, 1, 49] and r["intervalo"] == [1, 250] and r["nla_trilhas"] == 0 and r["drivers"] == 0
ok &= r["acoes_no_arquivo"] == sorted(NOMES)


def attr(m, nome, n):
    a = np.empty(n, np.int32); m.attributes[nome].data.foreach_get("value", a); return a


def avaliado(n):
    e = bpy.data.objects[n].evaluated_get(dg); me = e.to_mesh()
    co = np.empty(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co)
    mw = np.array(e.matrix_world, np.float64); e.to_mesh_clear()
    return co.reshape(-1, 3).astype(np.float64) @ mw[:3, :3].T + mw[:3, 3]


ov = {n: attr(bpy.data.objects[n].data, "rig_original_vertex", len(bpy.data.objects[n].data.vertices)) for n in ("Cabeca",) + FIXAS}
ref = {n: z["co"][ov[n]].astype(np.float64) for n in ov}
m = bpy.data.objects["Cabeca"].data
ed = np.empty(len(m.edges) * 2, np.int32); m.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
comp_ref = np.linalg.norm(ref["Cabeca"][ed[:, 0]] - ref["Cabeca"][ed[:, 1]], axis=1)
piv0 = rig.matrix_world @ rig.data.bones["Head_Bone"].head_local
outros = [b for b in rig.pose.bones if b.name != "Head_Bone"]
mat_obj0 = {n: bpy.data.objects[n].matrix_world.copy() for n in FIXAS + ("Cabeca",)}
curvas = {}
try:
    for nome, sinal in NOMES.items():
        act = bpy.data.actions[nome]; ad.action = act
        cb = anim_utils.action_get_channelbag_for_slot(act, ad.action_slot); fcs = list(cb.fcurves)
        a = {"use_fake_user": act.use_fake_user, "slot": ad.action_slot.identifier, "fcurves": [(f.data_path, f.array_index) for f in fcs]}
        fc = fcs[0]
        a["keyframes"] = [{"quadro": k.co[0], "graus": math.degrees(k.co[1]), "interp": k.interpolation,
                           "alcas": [k.handle_left_type, k.handle_right_type],
                           "alca_esq_graus": math.degrees(k.handle_left[1]), "alca_dir_graus": math.degrees(k.handle_right[1])} for k in fc.keyframe_points]
        a["extrapolacao"], a["modificadores_curva"] = fc.extrapolation, len(fc.modifiers)
        alvo = sinal * AMPLITUDE_GRAUS
        a["keyframes_ok"] = (len(fcs) == 1 and a["fcurves"][0] == ('pose.bones["Head_Bone"].rotation_euler', 1)
                             and [k["quadro"] for k in a["keyframes"]] == [1, 25, 49]
                             and all(abs(k["graus"] - g) < 1e-5 for k, g in zip(a["keyframes"], (0, alvo, 0)))
                             and all(k["interp"] == "BEZIER" and k["alcas"] == ["AUTO_CLAMPED"] * 2 for k in a["keyframes"])
                             # extremos com alças horizontais (sem ultrapassar 0° nem a amplitude)
                             and all(abs(k["alca_esq_graus"] - k["graus"]) < 1e-5 and abs(k["alca_dir_graus"] - k["graus"]) < 1e-5 for k in a["keyframes"])
                             and a["extrapolacao"] == "CONSTANT" and a["modificadores_curva"] == 0 and act.use_fake_user)
        # curva amostrada (481 amostras entre 1 e 49) e fora do intervalo
        xs = np.linspace(1, 49, 481); ys = np.degrees([fc.evaluate(x) for x in xs]); curvas[nome] = ys
        a["curva_min_max_graus"] = [float(ys.min()), float(ys.max())]
        a["curva_dentro_do_intervalo"] = bool((ys * sinal >= -1e-6).all() and (ys * sinal <= AMPLITUDE_GRAUS + 1e-5).all())
        a["fora_do_intervalo_graus"] = [math.degrees(fc.evaluate(0)), math.degrees(fc.evaluate(60))]
        a["curva_monotona_ida_e_volta"] = bool((np.diff(ys[:241]) * sinal >= -1e-9).all() and (np.diff(ys[240:]) * sinal <= 1e-9).all())
        # todos os quadros inteiros: pivô, outros ossos, loc/escala da cabeça, objetos
        piv, outros_d, locesc, objs, ang = 0.0, 0.0, 0.0, 0.0, []
        for f in range(1, 50):
            sc.frame_set(f)
            piv = max(piv, (rig.matrix_world @ pb.head - piv0).length)
            outros_d = max(outros_d, max(max(abs(x - y) for c1, c2 in zip(b.matrix_basis, Matrix.Identity(4)) for x, y in zip(c1, c2)) for b in outros))
            locesc = max(locesc, pb.location.length, (pb.scale - Vector((1, 1, 1))).length, abs(pb.rotation_euler.x), abs(pb.rotation_euler.z))
            objs = max(objs, max(max(abs(x - y) for c1, c2 in zip(bpy.data.objects[n].matrix_world, mat_obj0[n]) for x, y in zip(c1, c2)) for n in mat_obj0))
            ang.append(math.degrees(pb.rotation_euler.y))
        a["todos_quadros"] = {"pivo_deslocamento_max": piv, "outros_ossos_max": outros_d, "head_loc_escala_eixos_xz_max": locesc,
                              "matrizes_objetos_max": objs, "angulos_graus": [round(x, 6) for x in ang]}
        # geometria completa nos quadros de amostra
        amostras = {}
        for f in AMOSTRA_QUADROS:
            sc.frame_set(f); dg.update()
            th = pb.rotation_euler.y; Rz = np.array(Matrix.Rotation(th, 3, "Z")); p0 = np.array(piv0)
            cab = avaliado("Cabeca"); esperado = (ref["Cabeca"] - p0) @ Rz.T + p0
            frente = Matrix.Rotation(th, 3, "Z") @ Vector((0, -1, 0))
            s = {"graus": math.degrees(th), "frente_mundo": [round(x, 6) for x in frente],
                 "cabeca_erro_rigido": float(np.abs(cab - esperado).max()),
                 "cabeca_arestas_desvio": float(np.abs(np.linalg.norm(cab[ed[:, 0]] - cab[ed[:, 1]], axis=1) - comp_ref).max()),
                 "fixas_desvio_npz": max(float(np.abs(avaliado(n) - ref[n]).max()) for n in FIXAS)}
            amostras[str(f)] = s
        a["amostras"] = amostras
        s25 = amostras["25"]
        a["sentido_ok"] = (s25["frente_mundo"][0] * sinal) > 0  # direita do piloto = -X, esquerda = +X
        a["ok"] = bool(a["keyframes_ok"] and a["curva_dentro_do_intervalo"] and a["curva_monotona_ida_e_volta"] and a["sentido_ok"]
                       and piv <= TOL_POS and outros_d == 0.0 and locesc < 1e-12 and objs == 0.0
                       and all(abs(x) < 1e-9 for x in a["fora_do_intervalo_graus"])
                       and all(v["cabeca_erro_rigido"] <= 2e-7 and v["cabeca_arestas_desvio"] <= 2e-7 and v["fixas_desvio_npz"] <= TOL_POS for v in amostras.values()))
        ok &= a["ok"]; r["acoes"][nome] = a
    d, e = curvas["Cabeca_Direita_Ida_e_Volta"], curvas["Cabeca_Esquerda_Ida_e_Volta"]
    r["espelhamento_max_graus"] = float(np.abs(d + e).max()); ok &= r["espelhamento_max_graus"] < 1e-6
finally:
    ad.action = acao0; sc.frame_set(quadro0)
r["estado_restaurado"] = {"acao": ad.action.name, "quadro": sc.frame_current}
r["tudo_ok"] = bool(ok)
json.dump(r, open(SAIDA, "w"), ensure_ascii=False, indent=1, default=float)
result = {"tudo_ok": r["tudo_ok"], "espelho": r["espelhamento_max_graus"],
          "acoes": {n: {"ok": a["ok"], "kf": a["keyframes_ok"], "curva": a["curva_min_max_graus"], "sentido": a["sentido_ok"],
                        "todos": {k: v for k, v in a["todos_quadros"].items() if k != "angulos_graus"},
                        "amostras": {f: (round(s["graus"], 4), s["cabeca_erro_rigido"], s["cabeca_arestas_desvio"], s["fixas_desvio_npz"]) for f, s in a["amostras"].items()}}
                    for n, a in r["acoes"].items()}, "restaurado": r["estado_restaurado"]}
