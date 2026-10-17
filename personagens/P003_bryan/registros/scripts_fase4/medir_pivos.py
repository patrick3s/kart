"""Fase 4 — mede o pivô da cabeça e os centros das rodas do Bryan na cena aberta (Blender MCP).
Não altera a cena. Uso no MCP: SAIDA = "<caminho>.json"; exec(open("<este arquivo>").read())
Grava as medidas e os valores adotados (arredondados para a grade de 1/4096 m).
Critérios próprios deste modelo; nenhum limite do Jake ou do Dimi foi reaproveitado."""
import bpy, numpy as np, json

GRADE = 4096.0
RODAS = ("Wheel_Front_Left", "Wheel_Front_Right", "Wheel_Rear_Left", "Wheel_Rear_Right")
# ponto de partida: eixos (Y, Z) ajustados na Fase 3 (registro-fase3, seção 5)
EIXO_FASE3 = {"Wheel_Front_Left": (-0.2694, 0.1229), "Wheel_Front_Right": (-0.2693, 0.1227),
              "Wheel_Rear_Left": (0.2939, 0.1233), "Wheel_Rear_Right": (0.2938, 0.1233)}
Z_QUEIXO = 0.525  # acima disso a ilha do pescoço se alarga no queixo/mandíbula
TOL_SETOR = globals().get("TOL_SETOR", 0.002)  # setor aceito se o raio máximo fica a até 2 mm da mediana da metade de baixo


def coords(nome):
    m = bpy.data.objects[nome].data
    a = np.empty(len(m.vertices) * 3, np.float64)
    m.vertices.foreach_get("co", a)
    return a.reshape(-1, 3)


def grade(x):
    a = np.round(np.asarray(x, np.float64) * GRADE) / GRADE
    return float(a) if a.ndim == 0 else a.tolist()


def ajustar_circulo(p):
    A = np.c_[2 * p[:, 0], 2 * p[:, 1], np.ones(len(p))]
    c = np.linalg.lstsq(A, (p ** 2).sum(1), rcond=None)[0]
    return c[:2], float(np.sqrt(c[2] + c[0] ** 2 + c[1] ** 2))


def ilhas(nome):
    m = bpy.data.objects[nome].data
    n = len(m.vertices)
    e = np.empty(len(m.edges) * 2, np.int64); m.edges.foreach_get("vertices", e)
    p = np.arange(n)

    def raiz(x):
        while p[x] != x:
            p[x] = p[p[x]]; x = p[x]
        return x
    for a, b in e.reshape(-1, 2):
        ra, rb = raiz(a), raiz(b)
        if ra != rb:
            p[ra] = rb
    return np.array([raiz(i) for i in range(n)])


def medir_cabeca():
    h, b = coords("Cabeca"), coords("Corpo_Kart")
    rot = ilhas("Cabeca")
    pescoco = h[rot == rot[np.argmin(h[:, 2])]]  # ilha que desce mais: pele do pescoço
    toco = pescoco[pescoco[:, 2] < Z_QUEIXO]
    cx, cy = ((toco.min(0) + toco.max(0)) / 2 * 0.5 + toco.mean(0) * 0.5)[:2]
    fatias = {}
    for z0 in np.arange(0.48, 0.535, 0.005):
        s = b[(b[:, 2] >= z0) & (b[:, 2] < z0 + 0.005)]
        sx = s[(np.abs(s[:, 1] - cy) < 0.004) & (np.abs(s[:, 0] - cx) < 0.1)][:, 0] - cx
        neg, pos = sx[sx < 0], sx[sx >= 0]
        fatias[f"{z0:.3f}"] = [float(neg.max()) if len(neg) else None, float(pos.min()) if len(pos) else None]
    r = {
        "cabeca_z_min": float(h[:, 2].min()),
        "ilha_pescoco": {"vertices": int(len(pescoco)), "min": pescoco.min(0).tolist(), "max": pescoco.max(0).tolist()},
        "toco_abaixo_do_queixo": {"z_max_considerado": Z_QUEIXO, "vertices": int(len(toco)), "min": toco.min(0).tolist(),
                                  "max": toco.max(0).tolist(), "media": toco.mean(0).tolist(),
                                  "centro_caixa": ((toco.min(0) + toco.max(0)) / 2).tolist()},
        "corpo_furo_x_em_volta_do_toco": fatias,
        "criterio": "X, Y: média entre centro da caixa e média dos vértices do toco do pescoço abaixo do queixo; "
                    "Z: base do toco (menor Z da cabeça), onde a superfície do corpo fecha sob o pescoço (furo ≈ 0 entre Z 0,485 e 0,495)",
    }
    r["pivo_adotado"] = [grade(cx), grade(cy), grade(h[:, 2].min())]
    return r


def medir_roda(nome):
    v = coords(nome)
    yz = v[:, 1:]
    c = np.array(EIXO_FASE3[nome])
    for _ in range(12):
        d = yz - c
        r = np.linalg.norm(d, axis=1)
        setor = np.floor((np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360) / 5).astype(int)  # 0° = +Y, 90° = +Z
        rmax = np.full(72, np.nan)
        for s in range(72):
            q = r[setor == s]
            if len(q):
                rmax[s] = q.max()
        ref = np.nanmedian(rmax[36:])  # metade de baixo: sem preenchimento do para-lama
        bons = np.where(np.abs(rmax - ref) < TOL_SETOR)[0]
        sel = np.isin(setor, bons) & (r >= rmax[setor] - 0.001)
        c, R = ajustar_circulo(yz[sel])
    res = np.linalg.norm(yz[sel] - c, axis=1) - R
    d = yz - c
    ang = np.degrees(np.arctan2(d[:, 1], d[:, 0])) % 360
    banda = v[(np.linalg.norm(d, axis=1) > R - 0.008) & (ang > 200) & (ang < 340)][:, 0]
    p1, p99 = np.percentile(banda, [1, 99])
    centro = [float((p1 + p99) / 2), float(c[0]), float(c[1])]
    caixa = (v.min(0) + v.max(0)) / 2
    return {
        "criterio": "círculo de mínimos quadrados no plano YZ ajustado ao contorno externo da banda (setores de 5°, só os setores com raio "
                    "máximo a até 2 mm da mediana da metade de baixo; exclui o preenchimento do para-lama no topo); X no meio da banda (percentis 1–99)",
        "centro_medido": centro, "raio": R, "residuo_desvio_padrao": float(res.std()), "residuo_max": float(np.abs(res).max()),
        "setores_usados": int(len(bons)), "setores_descartados_graus": [int(s * 5) for s in range(72) if s not in bons],
        "raio_max_por_setor": [None if np.isnan(x) else float(x) for x in rmax],
        "x_banda_p1_p99": [float(p1), float(p99)], "x_malha": [float(v[:, 0].min()), float(v[:, 0].max())],
        "z_min_malha": float(v[:, 2].min()), "folga_chao_no_circulo": float(c[1] - R - v[:, 2].min()),
        "centro_caixa_comparacao": caixa.tolist(), "diferenca_caixa_menos_ajuste": (caixa - np.array(centro)).tolist(),
        "eixo_fase3_partida": list(EIXO_FASE3[nome]),
        "pivo_adotado": grade(centro),
    }


medidas = {"grade_arredondamento_m": 1 / GRADE, "arquivo": bpy.data.filepath, "arquivo_sujo": bpy.data.is_dirty,
           "cabeca": medir_cabeca(), "rodas": {n: medir_roda(n) for n in RODAS}}
json.dump(medidas, open(SAIDA, "w"), ensure_ascii=False, indent=1)
result = {"cabeca": medidas["cabeca"]["pivo_adotado"],
          **{n: [medidas["rodas"][n]["pivo_adotado"], round(medidas["rodas"][n]["raio"], 5), round(medidas["rodas"][n]["residuo_desvio_padrao"], 5),
                 medidas["rodas"][n]["setores_usados"], round(medidas["rodas"][n]["folga_chao_no_circulo"], 5)] for n in RODAS}}
