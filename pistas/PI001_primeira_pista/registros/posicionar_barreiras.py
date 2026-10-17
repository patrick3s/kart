"""Executado via Blender MCP com o .blend da pista aberto.

Distribui o módulo `barreira_reta_vermelha_branca` nas duas bordas a partir do eixo
fechado. Para outra pista, troque PREFIXO/EIXO/AFASTAMENTO/ALTURA_CHAO e destinos.
"""
import bpy, json, math, pathlib
from mathutils import Vector, Matrix

ROOT = pathlib.Path('/Users/patricksoares/Documents/jogos/kart')
MODULO = ROOT/'ambiente/modelos/barreiras/barreira_reta_vermelha_branca/blender/barreira_reta_vermelha_branca.blend'
NOME_MALHA = 'Barreira_Reta_Vermelha_Branca'
PREFIXO = 'PI001'
EIXO = 'PI001_Eixo_Editavel'
COLECAO = 'PI001_07_Barreiras'
AFASTAMENTO = 5.13     # m do eixo ao centro da barreira: face (0,33 m) encostada na borda externa da zebra (4,8 m)
FOLGA_MIN = 4.75       # nenhuma parte do módulo pode invadir a zebra (borda a 4,8 m do eixo)
COMPRIMENTO = 3.5      # comprimento nominal do módulo (m)
ALTURA_CHAO = -0.1     # topo do gramado
SAIDA_JSON = ROOT/'jogo/pistas/primeira_pista/barreiras.json'

eixo = bpy.data.objects[EIXO]
pts = [(eixo.matrix_world @ Vector(p.co[:3])).to_2d() for p in eixo.data.splines[0].points]
n = len(pts)
ccw = sum(pts[i].x*pts[(i+1) % n].y - pts[(i+1) % n].x*pts[i].y for i in range(n)) > 0


def dist_eixo(q):
    melhor = 1e9
    for i in range(n):
        a, b = pts[i], pts[(i+1) % n]
        ab = b - a
        t = max(0.0, min(1.0, (q-a).dot(ab)/ab.length_squared))
        melhor = min(melhor, (a + ab*t - q).length)
    return melhor


def borda(lado):
    """lado=+1 esquerda do sentido do eixo, -1 direita. Remove trechos que invadem a pista."""
    off = []
    for i in range(n):
        t = (pts[(i+1) % n] - pts[i-1]).normalized()
        esq = Vector((-t.y, t.x))
        q = pts[i] + esq*lado*AFASTAMENTO
        if dist_eixo(q) >= AFASTAMENTO - 0.05:
            off.append(q)
    return off


def modulos(poli):
    m = len(poli)
    acum = [0.0]
    for i in range(m):
        acum.append(acum[-1] + (poli[(i+1) % m] - poli[i]).length)
    total = acum[-1]
    k = max(3, round(total/COMPRIMENTO))
    passo = total/k

    def ponto(s):
        j = 0
        while acum[j+1] < s:
            j += 1
        a, b = poli[j], poli[(j+1) % m]
        return a + (b-a)*((s-acum[j])/(acum[j+1]-acum[j]))
    ext = [ponto(i*passo) for i in range(k)]
    return [(ext[i], ext[(i+1) % k]) for i in range(k)], total


# Módulo: anexa a malha (com material e texturas relativas) se ainda não existir.
if NOME_MALHA not in bpy.data.meshes:
    with bpy.data.libraries.load(str(MODULO), link=False) as (src, dst):
        dst.meshes = [NOME_MALHA]
malha = bpy.data.meshes[NOME_MALHA]
for img in bpy.data.images:
    if img.filepath.startswith('//../texturas/barreira_'):
        img.filepath = str(MODULO.parent.parent/'texturas'/pathlib.Path(img.filepath).name)

col = bpy.data.collections.get(COLECAO) or bpy.data.collections.new(COLECAO)
if col.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(col)
for o in list(col.objects):
    bpy.data.objects.remove(o, do_unlink=True)

M = Matrix(((1, 0, 0), (0, 0, 1), (0, -1, 0)))  # Blender -> Godot (x, z, -y)
saida = {'modulo': 'res://ambiente/modelos/barreiras/barreira_reta_vermelha_branca/barreira_reta_vermelha_branca.glb',
         'origem': f'pistas/{PREFIXO}_primeira_pista/blender/primeira_pista.blend',
         'afastamento_m': AFASTAMENTO, 'comprimento_nominal_m': COMPRIMENTO,
         'altura_chao_m': ALTURA_CHAO, 'conversao': 'Blender (x,y,z) -> Godot (x,z,-y)',
         'bordas': {}}
relatorio = {}
for lado, nome in [(1, 'Interna' if ccw else 'Externa'), (-1, 'Externa' if ccw else 'Interna')]:
    pares, total = modulos(borda(lado))
    lista = []
    piores = []
    for i, (a, b) in enumerate(pares):
        d = b - a
        ang = math.atan2(d.y, d.x)
        c = (a+b)/2
        esq = Vector((-d.y, d.x)).normalized()
        # A frente do modelo (-Y local) deve olhar para a pista.
        rumo_pista = -esq*lado
        if Vector((math.sin(ang), -math.cos(ang))).dot(rumo_pista) < 0:
            ang += math.pi
        sx = d.length/COMPRIMENTO
        # Folga: cantos frontais e centro não podem invadir pista/zebra. Em curva
        # côncava a corda corta para dentro; recua o módulo só o necessário.
        for _ in range(3):
            frente = [c + rumo_pista*0.33 + d*(f/2) for f in (-1, 0, 1)]
            falta = (AFASTAMENTO - 0.33) - min(dist_eixo(q) for q in frente)
            if falta <= 0.005:
                break
            c = c - rumo_pista*falta
        piores.append(min(dist_eixo(q) for q in frente))
        o = bpy.data.objects.new(f'{PREFIXO}_Barreira_{nome}_{i:03d}', malha)
        o.location = (c.x, c.y, ALTURA_CHAO)
        o.rotation_euler = (0, 0, ang)
        o.scale = (sx, 1, 1)
        col.objects.link(o)
        B = Matrix.Rotation(ang, 3, 'Z') @ Matrix.Diagonal((sx, 1, 1))
        G = M @ B @ M.transposed()
        lista.append({'origem': [c.x, ALTURA_CHAO, -c.y],
                      'base': [[G[r][k] for r in range(3)] for k in range(3)],
                      'comprimento_m': d.length})
    saida['bordas'][nome] = lista
    relatorio[nome] = {'modulos': len(lista), 'extensao_m': total,
                       'menor_folga_frente_eixo_m': min(piores),
                       'escala_x': [min(m['comprimento_m'] for m in lista)/COMPRIMENTO,
                                    max(m['comprimento_m'] for m in lista)/COMPRIMENTO]}
    assert min(piores) >= FOLGA_MIN, (nome, min(piores))

SAIDA_JSON.write_text(json.dumps(saida, indent=1))
result = relatorio
