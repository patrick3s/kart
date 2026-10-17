# Fase 2 — diagnóstico preliminar das partes do Bryan (somente leitura do NPZ original).
# Uso: python3 -I pre_partes.py backups/geometria_original.npz validacao/diagnostico_preliminar_partes.json
import numpy as np, json, sys
z = np.load(sys.argv[1]); co = z["co"]; comp = z["components"]
nc = comp.max()+1; cnt = np.bincount(comp)
mins = np.full((nc, 3), np.inf); maxs = np.full((nc, 3), -np.inf)
for k in range(3):
    np.minimum.at(mins[:, k], comp, co[:, k]); np.maximum.at(maxs[:, k], comp, co[:, k])
res = {"criterio": "Perfil YZ da face externa (|X|>0,30, Z<0,30) por canto; cilindro com eixo X, raio da metade da altura medida + 5 mm; |X| > X_INTERNO"}
# 1) perfil da face externa de cada roda (medido neste modelo)
rodas = {}
for sx, nx in ((1, "Left"), (-1, "Right")):
    for sy, ny in ((-1, "Front"), (1, "Rear")):
        p = co[(co[:, 0]*sx > 0.30) & (co[:, 1]*sy > 0.05) & (co[:, 2] < 0.30)]
        # extensão em Y medida na faixa central de altura (exclui peças baixas que avançam para o chassi)
        mid = p[(p[:, 2] > 0.10) & (p[:, 2] < 0.15)]
        y0, y1 = float(mid[:, 1].min()), float(mid[:, 1].max()); z0, z1 = float(p[:, 2].min()), float(p[:, 2].max())
        rodas[f"Wheel_{ny}_{nx}"] = {"sx": sx, "sy": sy, "centro_yz_estimado": [round((y0+y1)/2, 4), round((z0+z1)/2, 4)],
                                    "diametro_y": round(y1-y0, 4), "diametro_z": round(z1-z0, 4)}
# 2) ilhas dentro/atravessando o cilindro de cada roda
X_INTERNO = 0.19
for nome, r in rodas.items():
    cy, cz = r["centro_yz_estimado"]; rad = max(r["diametro_y"], r["diametro_z"])/2 + 0.005
    dentro = (co[:, 0]*r["sx"] > X_INTERNO) & (np.hypot(co[:, 1]-cy, co[:, 2]-cz) <= rad)
    tot_in = np.bincount(comp[dentro], minlength=nc)
    ids = np.where(tot_in > 0)[0]
    frac = tot_in[ids]/cnt[ids]
    inteiras = ids[frac == 1.0]; parciais = ids[frac < 1.0]
    xin = co[dentro][:, 0]*r["sx"]
    r.update({"raio_usado": round(rad, 4), "x_abs_min_dentro": round(float(xin.min()), 4),
              "ilhas_inteiras": len(inteiras), "v_ilhas_inteiras": int(cnt[inteiras].sum()),
              "ilhas_parciais": len(parciais), "v_dentro_de_parciais": int(tot_in[parciais].sum()),
              "maiores_parciais": [{"id": int(i), "v": int(cnt[i]), "frac_dentro": round(float(tot_in[i]/cnt[i]), 3),
                                    "min": mins[i].round(3).tolist(), "max": maxs[i].round(3).tolist()}
                                   for i in parciais[np.argsort(-tot_in[parciais])][:8]]})
res["rodas"] = rodas
# 3) cabeça: distribuição em altura
res["ilhas_acima_de_z"] = [(t, int(cnt[mins[:, 2] >= t].sum()), int((mins[:, 2] >= t).sum())) for t in (0.40, 0.45, 0.50, 0.55)]
up = np.where(mins[:, 2] > 0.45)[0]
res["ilhas_acima_045"] = [{"id": int(i), "v": int(cnt[i]), "min": mins[i].round(3).tolist(), "max": maxs[i].round(3).tolist()}
                          for i in up[np.argsort(-cnt[up])][:40]]
json.dump(res, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "maiores_parciais"} for k, v in rodas.items()}, indent=1))
for k, v in rodas.items(): print(k, [(p["id"], p["v"], p["frac_dentro"]) for p in v["maiores_parciais"]])
print(res["ilhas_acima_de_z"])
for i in res["ilhas_acima_045"][:25]: print(i)
