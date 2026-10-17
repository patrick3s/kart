"""Fase 4 — mede o pivô da cabeça e os centros das rodas na cena aberta (Blender MCP).
Não altera a cena. Uso no MCP: SAIDA = "<caminho>.json"; exec(open("<este arquivo>").read())
Grava as medidas e os valores adotados (arredondados para a grade de 1/4096 m)."""
import bpy, numpy as np, json

GRADE = 4096.0
RODAS = ("Wheel_Front_Left", "Wheel_Front_Right", "Wheel_Rear_Left", "Wheel_Rear_Right")


def coords(nome):
    m = bpy.data.objects[nome].data
    a = np.empty(len(m.vertices) * 3, np.float64)
    m.vertices.foreach_get("co", a)
    return a.reshape(-1, 3)


def grade(x):
    return float(np.round(np.asarray(x) * GRADE) / GRADE) if np.ndim(x) == 0 else (np.round(np.asarray(x) * GRADE) / GRADE).tolist()


def ajustar_circulo(p):
    A = np.c_[2 * p[:, 0], 2 * p[:, 1], np.ones(len(p))]
    c = np.linalg.lstsq(A, (p ** 2).sum(1), rcond=None)[0]
    return c[:2], float(np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2))


def medir_cabeca():
    h, b = coords("Cabeca"), coords("Corpo_Kart")
    toco = h[(h[:, 2] >= 0.415) & (h[:, 2] < 0.455)]  # pele do pescoço abaixo do queixo
    gola = {}
    for z0 in (0.44, 0.45, 0.46, 0.47):
        s = b[(b[:, 2] >= z0) & (b[:, 2] < z0 + 0.01) & (np.abs(b[:, 0]) < 0.12) & (np.abs(b[:, 1] + 0.01) < 0.12)]
        sx = s[np.abs(s[:, 1] + 0.01) < 0.01][:, 0]
        neg, pos = sx[sx < 0], sx[sx >= 0]
        gola[f"{z0:.2f}"] = {"furo_x": [float(neg.max()) if len(neg) else None, float(pos.min()) if len(pos) else None]}
    queixo = h[(np.abs(h[:, 0]) < 0.004) & (h[:, 1] < -0.02) & (h[:, 1] > -0.08)]
    r = {
        "cabeca_z_min": float(h[:, 2].min()),
        "toco_pescoco": {"vertices": int(len(toco)), "centro_caixa": ((toco.min(0) + toco.max(0)) / 2).tolist(),
                          "media": toco.mean(0).tolist(), "min": toco.min(0).tolist(), "max": toco.max(0).tolist()},
        "queixo_z_min_no_plano_x0": float(queixo[:, 2].min()) if len(queixo) else None,
        "gola_furo_por_altura": gola,
    }
    # X: simetria (0); Y: centro do toco; Z: plano em que a gola fecha em volta do pescoço (entre 0,44 e 0,46)
    r["pivo_adotado"] = [0.0, grade(r["toco_pescoco"]["centro_caixa"][1] * 0.5 + r["toco_pescoco"]["media"][1] * 0.5), grade(0.4453)]
    return r


def medir_roda(nome):
    v = coords(nome)
    yz = v[:, 1:]
    c = np.array([np.median(yz[:, 0]), 0.1288])
    for _ in range(8):
        d = yz - c
        r = np.linalg.norm(d, axis=1)
        setor = np.floor((np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360) / 5).astype(int)
        rmax = np.full(72, np.nan)
        for s in range(72):
            q = r[setor == s]
            if len(q):
                rmax[s] = q.max()
        bons = np.where(rmax < np.nanmedian(rmax) + 0.003)[0]  # descarta setores com bolinhas salientes
        sel = np.isin(setor, bons) & (r >= rmax[setor] - 0.001)  # contorno externo da banda
        c, R = ajustar_circulo(yz[sel])
    res = np.linalg.norm(yz[sel] - c, axis=1) - R
    x = v[sel][:, 0]
    caixa = (v.min(0) + v.max(0)) / 2
    centro = [float((x.min() + x.max()) / 2), float(c[0]), float(c[1])]
    return {
        "criterio": "círculo de mínimos quadrados no plano YZ ajustado ao contorno externo da banda de rodagem (setores de 5°, sem picos de bolinhas); X no meio da banda",
        "centro_medido": centro, "raio": R, "residuo_desvio_padrao": float(res.std()), "residuo_max": float(np.abs(res).max()),
        "setores_usados": int(len(bons)), "setores_descartados_graus": [int(s * 5) for s in range(72) if s not in bons],
        "x_banda": [float(x.min()), float(x.max())], "z_min_malha": float(v[:, 2].min()),
        "centro_caixa_comparacao": caixa.tolist(), "diferenca_caixa_menos_ajuste": (caixa - np.array(centro)).tolist(),
        "pivo_adotado": grade(centro),
    }


medidas = {"grade_arredondamento_m": 1 / GRADE, "arquivo": bpy.data.filepath, "cabeca": medir_cabeca(),
           "rodas": {n: medir_roda(n) for n in RODAS}}
json.dump(medidas, open(SAIDA, "w"), ensure_ascii=False, indent=1)
result = {"cabeca": medidas["cabeca"]["pivo_adotado"], **{n: medidas["rodas"][n]["pivo_adotado"] for n in RODAS}}
