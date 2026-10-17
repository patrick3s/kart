"""Analisa o JPG sem alterá-lo; não executa modelagem fora do Blender MCP.

Uso: python3 pistas/PI001_primeira_pista/registros/extrair_tracado.py
Dependências de análise: Pillow e NumPy.
"""
from pathlib import Path
import hashlib
import json
from collections import Counter

import numpy as np
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parents[1]
ORIGINAL = RAIZ / 'referencia/PI001_primeira_pista.jpg'
DESTINO = RAIZ / 'validacao'
DESTINO.mkdir(exist_ok=True)
im = Image.open(ORIGINAL).convert('RGB')
mask = np.asarray(im.convert('L')) < 110
sk = np.pad(mask, 1).astype(np.uint8)

# Afinamento Zhang–Suen: preserva a conectividade do circuito desenhado.
for rodada in range(100):
    retirados = 0
    for fase in (0, 1):
        p = [sk[1:-1, 1:-1], sk[:-2, 1:-1], sk[:-2, 2:],
             sk[1:-1, 2:], sk[2:, 2:], sk[2:, 1:-1],
             sk[2:, :-2], sk[1:-1, :-2], sk[:-2, :-2]]
        viz = sum(p[1:])
        trans = sum((p[i] == 0) & (p[1 if i == 8 else i + 1] == 1)
                    for i in range(1, 9))
        apagar = (p[0] == 1) & (viz >= 2) & (viz <= 6) & (trans == 1)
        if fase == 0:
            apagar &= (p[1] * p[3] * p[5] == 0) & (p[3] * p[5] * p[7] == 0)
        else:
            apagar &= (p[1] * p[3] * p[7] == 0) & (p[1] * p[5] * p[7] == 0)
        retirados += int(apagar.sum())
        sk[1:-1, 1:-1][apagar] = 0
    if retirados == 0:
        break

pixels = {(int(x), int(y)) for y, x in np.argwhere(sk[1:-1, 1:-1])}
grafo = {}
for x, y in pixels:
    ns = set()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1),
                   (1, 1), (-1, -1), (1, -1), (-1, 1)):
        n = (x + dx, y + dy)
        if n not in pixels:
            continue
        if dx and dy and ((x + dx, y) in pixels or (x, y + dy) in pixels):
            continue
        ns.add(n)
    grafo[x, y] = ns

# Remove pontas do esqueleto; mantém o anel fechado.
folhas = [p for p, ns in grafo.items() if len(ns) < 2]
while folhas:
    p = folhas.pop()
    if p not in grafo:
        continue
    for n in grafo.pop(p):
        grafo[n].discard(p)
        if len(grafo[n]) < 2:
            folhas.append(n)
graus = Counter(map(len, grafo.values()))
assert set(graus) == {2}, f'O desenho não produziu um circuito simples: {graus}'
inicio = min(grafo, key=lambda p: (abs(p[0] - im.width / 2) + abs(p[1] - 397)))
seq, atual, anterior = [], inicio, None
while not seq or atual != inicio:
    seq.append(atual)
    seguinte = sorted(grafo[atual] - {anterior})[0]
    anterior, atual = atual, seguinte
    assert len(seq) <= len(grafo), 'Ciclo inválido'
assert len(seq) == len(grafo), 'Mais de um circuito detectado'

pontos = np.asarray(seq, dtype=float)
originais = pontos.copy()
# A ponta aguda do desenho não acomoda uma via de 8 m. Substituímos somente
# o extremo superior direito por uma curva cúbica tangente aos dois trechos.
indices_ponta = np.flatnonzero((pontos[:, 0] > 570) & (pontos[:, 1] < 90))
assert np.all(np.diff(indices_ponta) == 1), 'Região da ponta não é contínua'
i0, i1 = int(indices_ponta[0] - 1), int(indices_ponta[-1] + 1)
a, b = pontos[i0], pontos[i1]
ta, tb = a - pontos[i0 - 8], pontos[i1 + 8] - b
ta /= np.linalg.norm(ta)
tb /= np.linalg.norm(tb)
t = np.linspace(0, 1, 120)[:, None]
curva = ((1-t)**3 * a + 3*(1-t)**2*t*(a + ta*28) +
         3*(1-t)*t*t*(b - tb*28) + t**3*b)
pontos = np.vstack([pontos[:i0], curva, pontos[i1+1:]])
comprimentos = np.linalg.norm(np.roll(pontos, -1, axis=0) - pontos, axis=1)
cum = np.r_[0, np.cumsum(comprimentos)]
dist = np.arange(0, cum[-1], 1.0)
fechados = np.vstack([pontos, pontos[0]])
uniformes = np.column_stack([np.interp(dist, cum, fechados[:, i]) for i in (0, 1)])

# Suavização periódica de 9 px: retira serrilhado e arredonda pontas estreitas.
sigma = 9.0
k = np.arange(-int(sigma * 3), int(sigma * 3) + 1)
pesos = np.exp(-0.5 * (k / sigma) ** 2)
pesos /= pesos.sum()
suaves = sum(w * np.roll(uniformes, int(i), axis=0) for i, w in zip(k, pesos))
comprimentos = np.linalg.norm(np.roll(suaves, -1, axis=0) - suaves, axis=1)
cum = np.r_[0, np.cumsum(comprimentos)]
dist = np.linspace(0, cum[-1], 1000, endpoint=False)
fechados = np.vstack([suaves, suaves[0]])
suaves = np.column_stack([np.interp(dist, cum, fechados[:, i]) for i in (0, 1)])

escala = 0.6  # metros por pixel; decisão provisória, pois o JPG não tem cotas.
centro = np.asarray([im.width / 2, im.height / 2])
xy = (suaves - centro) * [escala, -escala]
area = 0.5 * np.sum(xy[:, 0] * np.roll(xy[:, 1], -1) -
                    np.roll(xy[:, 0], -1) * xy[:, 1])
if area < 0:
    xy = xy[::-1]
    suaves = suaves[::-1]
segmentos = np.roll(xy, -1, axis=0) - xy
tan = np.roll(xy, -1, axis=0) - np.roll(xy, 1, axis=0)
tan /= np.linalg.norm(tan, axis=1)[:, None]
normais = np.column_stack([-tan[:, 1], tan[:, 0]])

largura = 8.0
zebra = 0.8
borda = largura / 2 + zebra
esq, dir = xy + normais * borda, xy - normais * borda
def cruz(a, b):
    return a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]

# As duas metades de cada quad devem apontar para cima.
tri1 = cruz(np.roll(dir, -1, axis=0) - dir, np.roll(esq, -1, axis=0) - dir)
tri2 = cruz(np.roll(esq, -1, axis=0) - dir, esq - dir)
assert min(tri1.min(), tri2.min()) > 0, 'Largura dobra a malha em curva fechada'

def intersecoes(poly):
    achadas = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        js = np.arange(i + 2, n)
        js = js[js != (i - 1) % n]
        c, d = poly[js], poly[(js + 1) % n]
        teste = ((cruz(b - a, c - a) * cruz(b - a, d - a) < -1e-10) &
                 (cruz(d - c, a - c) * cruz(d - c, b - c) < -1e-10))
        achadas.extend((i, int(j)) for j in js[teste])
    return achadas

assert not intersecoes(esq), 'Borda interna cruza a si mesma'
assert not intersecoes(dir), 'Borda externa cruza a si mesma'
distancias = np.linalg.norm(suaves[:, None, :] - originais[None, :, :], axis=2)
max_desvio = float(distancias.min(axis=1).max())
max_desvio_original = float(distancias.min(axis=0).max())
resumo = {
    'referencia': str(ORIGINAL.relative_to(RAIZ)),
    'sha256_referencia': hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(),
    'resolucao_referencia': list(im.size),
    'metodo': 'Limiar 110; esqueleto Zhang–Suen; ciclo único; arredondamento da ponta superior direita; suavização periódica de 9 px',
    'interpretacao': 'Linha preta interpretada como eixo da pista; largura e escala provisórias',
    'metros_por_pixel': escala, 'largura_asfalto_m': largura,
    'largura_zebra_m': zebra, 'amostras': len(xy),
    'comprimento_eixo_m': float(np.linalg.norm(segmentos, axis=1).sum()),
    'dimensoes_eixo_m': list(np.ptp(xy, axis=0)),
    'distancia_maxima_eixo_modelado_ao_desenhado_px': max_desvio,
    'distancia_maxima_eixo_desenhado_ao_modelado_px': max_desvio_original,
    'circuito_unico_fechado': True, 'bordas_sem_autointersecoes': True,
    'quads_sem_inversao': True,
    'pontos_xy_m': xy.round(6).tolist(),
}
(DESTINO / 'tracado_extraido.json').write_text(json.dumps(resumo, indent=2, ensure_ascii=False) + '\n')

# Sobreposição de análise; o JPG permanece intacto.
preview = im.copy().resize((im.width * 2, im.height * 2))
draw = ImageDraw.Draw(preview)
def projetar(p):
    return tuple(((p / [escala, -escala] + centro) * 2).tolist())
for linha, cor in ((xy, '#00a9d4'), (esq, '#f2472e'), (dir, '#f2472e')):
    coords = [projetar(p) for p in linha]
    draw.line(coords + coords[:1], fill=cor, width=2)
preview.save(DESTINO / 'sobreposicao_tracado.png')
print(json.dumps({k: v for k, v in resumo.items() if k != 'pontos_xy_m'}, indent=2, ensure_ascii=False))
