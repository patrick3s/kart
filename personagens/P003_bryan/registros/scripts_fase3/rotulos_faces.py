"""Rótulos por FACE das partes do Bryan (Fase 3). Usa somente o NPZ original.
0 Corpo_Kart, 1 Cabeca, 2..5 Wheel_Front_Left, Wheel_Front_Right, Wheel_Rear_Left, Wheel_Rear_Right.
Rodas: as ilhas que tocam o cilindro do pneu são divididas por faces, pelas arestas existentes
(o Tripo fundiu o pneu com a placa do assoalho e com o preenchimento do vão do para-lama).
Fragmentos pequenos criados pelo critério geométrico são devolvidos ao rótulo vizinho.
Cabeça: ilhas inteiras (CABECA), escolhidas por posição, cor da textura e conferência visual."""
import numpy as np
NOMES = ["Corpo_Kart", "Cabeca", "Wheel_Front_Left", "Wheel_Front_Right", "Wheel_Rear_Left", "Wheel_Rear_Right"]
# eixo de cada roda (lado X, Y, Z): círculo ajustado à silhueta da face externa (|X| > 0,31); frente = -Y, esquerda = +X
CENTROS = {2: (1, -0.2694, 0.1229), 3: (-1, -0.2693, 0.1227), 4: (1, 0.2939, 0.1233), 5: (-1, 0.2938, 0.1233)}
R_PNEU = 0.1265      # raio máximo do pneu medido nas ilhas exclusivas (0,123) + folga
AX_MIN = 0.15        # |X| mínimo da face para pertencer à roda (parede interna do pneu em |X| ≈ 0,18)
Z_PLACA, TOL_PLACA = 0.0805, 0.002   # placa do assoalho fundida ao pneu (faces horizontais em Z ≈ 0,080)
PLACA_AX_MAX = 0.205                 # a placa termina em |X| ≈ 0,201; faces horizontais mais externas são do aro
# quepe (511, 510, 749, 474, 497, 611), insígnia (712), óculos (516, 522, 523), cabelo (559, 481, 536),
# orelhas (496, 758), rosto (529) e pele do pescoço (570). Ficam no corpo: gola (500, 501, 545, 556, 711, 766, 817)
# e rádio do ombro (790, 806, 829, 835, 852).
CABECA = [474, 481, 496, 497, 510, 511, 516, 522, 523, 529, 536, 559, 570, 611, 712, 749, 758]
MIN_FRAG = 60        # fragmentos de roda/corpo com menos faces que isso (dentro de uma ilha dividida) voltam ao rótulo vizinho

def geometria(z):
    co = z["co"].astype(np.float64); tri = z["loops"].reshape(-1, 3)
    assert (z["totals"] == 3).all() and np.array_equal(z["starts"], np.arange(len(tri))*3)
    p = co[tri]; n = np.cross(p[:, 1]-p[:, 0], p[:, 2]-p[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-30
    return co, tri, p, n

def rotulos_faces(z, cabeca_ilhas=CABECA):
    co, tri, p, n = geometria(z); comp = z["components"]; fcomp = comp[tri[:, 0]]
    lab = np.zeros(len(tri), np.int8)
    lab[np.isin(fcomp, cabeca_ilhas)] = 1
    placa = (np.abs(p[:, :, 2]-Z_PLACA).max(1) < TOL_PLACA) & (np.abs(n[:, 2]) > 0.95)
    for w, (sx, cy, cz) in CENTROS.items():
        r = np.hypot(p[:, :, 1]-cy, p[:, :, 2]-cz).max(1); ax = p[:, :, 0]*sx
        roda = (r <= R_PNEU) & (ax.min(1) >= AX_MIN) & ~(placa & (ax.max(1) <= PLACA_AX_MAX))
        assert not (lab[roda] != 0).any(), "face em duas partes"
        lab[roda] = w
    return limpar_fragmentos(lab, tri, fcomp)

def componentes_faces(tri, mask):
    """Componentes conexos (por aresta compartilhada) das faces em mask; devolve rótulo por face (-1 fora)."""
    f = np.where(mask)[0]; t = tri[f]
    e = np.sort(np.concatenate([t[:, [0, 1]], t[:, [1, 2]], t[:, [2, 0]]]), 1)
    fe = np.tile(np.arange(len(f)), 3)
    key = e[:, 0].astype(np.int64)*(1 << 32) + e[:, 1]
    o = np.argsort(key, kind="stable"); key, fe = key[o], fe[o]
    same = key[1:] == key[:-1]; a, b = fe[:-1][same], fe[1:][same]
    lab = np.arange(len(f))
    while True:
        mn = np.minimum(lab[a], lab[b]); new = lab.copy()
        np.minimum.at(new, lab[a], mn); np.minimum.at(new, lab[b], mn)
        while True:
            nn = new[new]
            if np.array_equal(nn, new): break
            new = nn
        if np.array_equal(new, lab): break
        lab = new
    out = np.full(len(tri), -1); out[f] = np.unique(lab, return_inverse=True)[1]
    return out

def limpar_fragmentos(lab, tri, fcomp):
    divididas = [i for i in np.unique(fcomp[lab >= 2]) if len(np.unique(lab[fcomp == i])) > 1]
    for i in divididas:
        fi = fcomp == i
        for _ in range(3):
            mudou = False
            for k in np.unique(lab[fi]):
                cc = componentes_faces(tri, fi & (lab == k))
                tam = np.bincount(cc[cc >= 0])
                for c in np.where(tam < MIN_FRAG)[0]:
                    sel = cc == c
                    # rótulo vizinho: o mais comum entre as faces da ilha que compartilham vértice com o fragmento
                    vs = np.zeros(tri.max()+1, bool); vs[tri[sel]] = True
                    viz = fi & ~sel & vs[tri].any(1)
                    if viz.any():
                        lab[sel] = np.bincount(lab[viz]).argmax(); mudou = True
            if not mudou: break
    return lab
