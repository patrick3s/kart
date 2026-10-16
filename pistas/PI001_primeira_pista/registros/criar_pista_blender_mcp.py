"""Criação da PI001: executar exclusivamente no Blender conectado via MCP.

No MCP: exec(compile(open(CAMINHO).read(), CAMINHO, 'exec'))
Não remove objetos nem modifica malhas da cena anterior.
"""
import bpy
import bmesh
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from mathutils import Vector

RAIZ = Path('/Users/patricksoares/Documents/jogos/kart/pistas/PI001_primeira_pista')
ARQUIVO = RAIZ / 'blender/primeira_pista.blend'
FONTE = RAIZ / 'referencia/PI001_primeira_pista.jpg'
DADOS = json.loads((RAIZ / 'validacao/tracado_extraido.json').read_text())
assert not ARQUIVO.exists(), 'A pista já existe; não sobrescrever sem conferir a versão.'
assert 'PI001_Primeira_Pista' not in bpy.data.scenes, 'Cena PI001 já existente.'
assert bpy.context.mode == 'OBJECT', 'Sair do modo de edição antes de criar a pista.'
assert hashlib.sha256(FONTE.read_bytes()).hexdigest() == DADOS['sha256_referencia']

# Preserva integralmente a sessão anterior antes de trocar de projeto.
backup = RAIZ / ('backups/sessao_antes_PI001_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.blend')
estado_anterior = {'arquivo': bpy.data.filepath, 'cena': bpy.context.scene.name,
                   'objetos': sorted(o.name for o in bpy.context.scene.objects)}
bpy.ops.wm.save_as_mainfile(filepath=str(backup), copy=True, check_existing=False)

sc = bpy.data.scenes.new('PI001_Primeira_Pista')
bpy.context.window.scene = sc
sc.unit_settings.system = 'METRIC'
sc.unit_settings.scale_length = 1.0
sc['identificador'] = 'PI001'
sc['referencia_sha256'] = DADOS['sha256_referencia']
sc['largura_asfalto_m'] = DADOS['largura_asfalto_m']
sc['comprimento_eixo_m'] = DADOS['comprimento_eixo_m']
sc['observacao'] = 'Escala provisória; pista plana; ponta superior direita arredondada para permitir a largura de 8 m.'

def colecao(nome):
    c = bpy.data.collections.new(nome)
    sc.collection.children.link(c)
    return c

via = colecao('PI001_01_Pista')
amb = colecao('PI001_02_Base')
marcas = colecao('PI001_03_Sinalizacao')
guias = colecao('PI001_04_Guias_Editaveis')
refs = colecao('PI001_05_Referencia_Original')
apres = colecao('PI001_06_Apresentacao')

def material(nome, cor, aspereza=0.8):
    m = bpy.data.materials.new(nome)
    m.diffuse_color = (*cor, 1)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = (*cor, 1)
    bsdf.inputs['Roughness'].default_value = aspereza
    return m

asfalto = material('PI001_Asfalto', (0.052, 0.065, 0.078), 0.92)
n = asfalto.node_tree.nodes
l = asfalto.node_tree.links
tex = n.new('ShaderNodeTexNoise')
tex.inputs['Scale'].default_value = 16
tex.inputs['Detail'].default_value = 2
coord = n.new('ShaderNodeTexCoord')
l.new(coord.outputs['Object'], tex.inputs['Vector'])
bump = n.new('ShaderNodeBump')
bump.inputs['Strength'].default_value = 0.2
bump.inputs['Distance'].default_value = 0.025
l.new(tex.outputs['Fac'], bump.inputs['Height'])
l.new(bump.outputs['Normal'], next(node for node in n if node.type == 'BSDF_PRINCIPLED').inputs['Normal'])
vermelho = material('PI001_Zebra_Vermelha', (0.65, 0.022, 0.016))
branco = material('PI001_Tinta_Branca', (0.88, 0.90, 0.84))
escuro = material('PI001_Zebra_Lateral', (0.16, 0.18, 0.18))
preto = material('PI001_Quadriculado_Preto', (0.012, 0.016, 0.019))
grama = material('PI001_Grama', (0.17, 0.29, 0.075), 1.0)
n, l = grama.node_tree.nodes, grama.node_tree.links
coord = n.new('ShaderNodeTexCoord')
tex = n.new('ShaderNodeTexNoise')
tex.inputs['Scale'].default_value = 0.42
tex.inputs['Detail'].default_value = 3
l.new(coord.outputs['Object'], tex.inputs['Vector'])
ramp = n.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position = 0.1
ramp.color_ramp.elements[0].color = (0.10, 0.18, 0.038, 1)
ramp.color_ramp.elements[1].position = 0.9
ramp.color_ramp.elements[1].color = (0.24, 0.36, 0.10, 1)
l.new(tex.outputs['Fac'], ramp.inputs[0])
l.new(ramp.outputs['Color'], next(node for node in n if node.type == 'BSDF_PRINCIPLED').inputs['Base Color'])

xy = [Vector((x, y)) for x, y in DADOS['pontos_xy_m']]
N = len(xy)
tangentes = [(xy[(i+1) % N] - xy[(i-1) % N]).normalized() for i in range(N)]
normais = [Vector((-t.y, t.x)) for t in tangentes]
dist = [0.0]
for i in range(N):
    dist.append(dist[-1] + (xy[(i+1) % N] - xy[i]).length)

def objeto_malha(nome, vertices, faces, col, materiais):
    me = bpy.data.meshes.new(nome + '_Malha')
    me.from_pydata(vertices, [], faces)
    me.update()
    ob = bpy.data.objects.new(nome, me)
    col.objects.link(ob)
    for m in materiais:
        me.materials.append(m)
    return ob

def faixa(nome, limite_a, limite_b, topo, fundo, materiais, alternar=False):
    """Anel fechado com seção retangular e UVs contínuas no topo."""
    vertices = []
    for z, offset in ((topo, limite_a), (topo, limite_b),
                      (fundo, limite_a), (fundo, limite_b)):
        vertices.extend((p.x+n.x*offset, p.y+n.y*offset, z) for p, n in zip(xy, normais))
    faces, uvs, indices = [], [], []
    for i in range(N):
        j = (i+1) % N
        faces.extend([(i, j, N+j, N+i),
                      (2*N+i, 3*N+i, 3*N+j, 2*N+j),
                      (i, 2*N+i, 2*N+j, j),
                      (N+i, N+j, 3*N+j, 3*N+i)])
        u0, u1 = dist[i] / 8, dist[i+1] / 8
        v = (limite_b - limite_a) / 8
        uvs.extend([[(u0, 0), (u1, 0), (u1, v), (u0, v)],
                    [(u0, 0), (u0, v), (u1, v), (u1, 0)],
                    [(u0, 0), (u0, 0.1), (u1, 0.1), (u1, 0)],
                    [(u0, 0), (u1, 0), (u1, 0.1), (u0, 0.1)]])
        cor_topo = int((dist[i] + dist[i+1]) / 2 / 1.8) % 2 if alternar else 0
        indices.extend([cor_topo, len(materiais)-1, len(materiais)-1, len(materiais)-1])
    ob = objeto_malha(nome, vertices, faces, via, materiais)
    uv = ob.data.uv_layers.new(name='UV_Percurso')
    for poly, coords, idx in zip(ob.data.polygons, uvs, indices):
        poly.material_index = idx
        for li, co in zip(poly.loop_indices, coords):
            uv.data[li].uv = co
    return ob

pista = faixa('PI001_Asfalto', -4, 4, 0.10, -0.14, [asfalto])
pista['largura_m'] = 8.0
pista['eixo_fonte'] = 'PI001_Eixo_Editavel'
faixa('PI001_Zebra_Externa', -4.8, -4, 0.145, -0.12, [vermelho, branco, escuro], True)
faixa('PI001_Zebra_Interna', 4, 4.8, 0.145, -0.12, [vermelho, branco, escuro], True)
for nome, a, b in [('PI001_Linha_Externa', -3.88, -3.74),
                    ('PI001_Linha_Interna', 3.74, 3.88)]:
    faixa(nome, a, b, 0.106, 0.102, [branco])

# Base simples e independente, sem inventar cenário que o JPG não informa.
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -1.0))
base = bpy.context.object
base.name = 'PI001_Base_Gramado'
base.dimensions = (446, 284, 1.8)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
for c in list(base.users_collection):
    c.objects.unlink(base)
amb.objects.link(base)
base.data.materials.append(grama)
bev = base.modifiers.new('Cantos_arredondados', 'BEVEL')
bev.width = 3.5
bev.segments = 5
bev.affect = 'EDGES'

# Eixo fechado editável: guia sem espessura, não renderizada.
cv = bpy.data.curves.new('PI001_Eixo_Editavel', 'CURVE')
cv.dimensions = '3D'
sp = cv.splines.new('POLY')
sp.points.add(N-1)
sp.use_cyclic_u = True
for bp, p in zip(sp.points, xy):
    bp.co = (p.x, p.y, 0.11, 1)
eixo = bpy.data.objects.new('PI001_Eixo_Editavel', cv)
guias.objects.link(eixo)
eixo.hide_render = True
eixo['largura_asfalto_m'] = 8.0
eixo['nota'] = 'Fonte: tracado_extraido.json. Para alterar a largura e reconstruir, adaptar o script de criação.'
eixo.hide_set(True)

# Referência original empacotada no .blend; ativar a coleção para sobrepor.
img = bpy.data.images.load(str(FONTE), check_existing=False)
img.pack()
ref = bpy.data.objects.new('PI001_JPG_Original', None)
refs.objects.link(ref)
ref.empty_display_type = 'IMAGE'
ref.data = img
ref.empty_display_size = 679 * DADOS['metros_por_pixel']
ref.location = (0, 0, -0.2)
ref.color[3] = 0.5
ref.empty_image_depth = 'BACK'
ref.hide_render = True
ref.hide_set(True)

# Largada provisória no centro da reta inferior, orientada pelo eixo.
indice = min(range(N), key=lambda i: abs(xy[i].x) + abs(xy[i].y + 116))
p, t, normal = xy[indice], tangentes[indice], normais[indice]
verts, faces = [], []
for fila in range(2):
    for coluna in range(8):
        for longitudinal, lateral in ((fila-1, coluna-4), (fila, coluna-4),
                                      (fila, coluna-3), (fila-1, coluna-3)):
            q = p + t*longitudinal + normal*lateral
            verts.append((q.x, q.y, 0.111))
        faces.append(tuple(range(len(verts)-4, len(verts))))
largada = objeto_malha('PI001_Largada_Quadriculada', verts, faces, marcas, [branco, preto])
for i, poly in enumerate(largada.data.polygons):
    poly.material_index = (i // 8 + i % 8) % 2
spawn = bpy.data.objects.new('PI001_Posicao_Largada', None)
guias.objects.link(spawn)
spawn.empty_display_type = 'ARROWS'
spawn.empty_display_size = 3
spawn.location = (p.x, p.y, 0.3)
spawn.rotation_euler.z = math.atan2(t.y, t.x) - math.pi/2
spawn.hide_render = True
spawn['provisorio'] = True

def camera(nome, pos, alvo, escala):
    cd = bpy.data.cameras.new(nome)
    cd.type = 'ORTHO'
    cd.ortho_scale = escala
    cd.clip_end = 3000
    ob = bpy.data.objects.new(nome, cd)
    apres.objects.link(ob)
    ob.location = pos
    ob.rotation_euler = (Vector(alvo) - ob.location).to_track_quat('-Z', 'Y').to_euler()
    return ob

cam_topo = camera('PI001_Camera_Topo', (0, 0, 600), (0, 0, 0), 478)
cam_iso = camera('PI001_Camera_Perspectiva', (210, -330, 440), (0, 0, 0), 650)
sc.camera = cam_iso
ld = bpy.data.lights.new('PI001_Sol', 'SUN')
ld.energy = 2.5
ld.angle = math.radians(12)
sol = bpy.data.objects.new('PI001_Sol', ld)
apres.objects.link(sol)
sol.rotation_euler = (math.radians(25), math.radians(-22), math.radians(-30))
world = bpy.data.worlds.new('PI001_Mundo')
world.use_nodes = True
background = next(n for n in world.node_tree.nodes if n.type == 'BACKGROUND')
background.inputs['Color'].default_value = (0.22, 0.29, 0.38, 1)
background.inputs['Strength'].default_value = 0.5
sc.world = world
sc.render.engine = 'CYCLES'
sc.cycles.samples = 24
sc.cycles.use_denoising = True
sc.render.resolution_x = 1600
sc.render.resolution_y = 1000
sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'PNG'
sc.render.film_transparent = False
sc.view_settings.view_transform = 'AgX'
sc.render.filepath = str(RAIZ / 'validacao/pista_perspectiva.png')

# Validação da geometria real criada, sem corrigir silenciosamente a malha.
validacoes = []
for ob in via.objects:
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.normal_update()
    topo_malha = max(v.co.z for v in bm.verts)
    bordas_abertas = sum(not e.is_manifold for e in bm.edges)
    normais_erradas = sum(f.normal.z < 0.99 for f in bm.faces if
                          all(abs(v.co.z - topo_malha) < 1e-4 for v in f.verts))
    zero = sum(f.calc_area() < 1e-8 for f in bm.faces)
    bm.free()
    assert bordas_abertas == 0 and zero == 0 and normais_erradas == 0, ob.name
    validacoes.append({'objeto': ob.name, 'vertices': len(ob.data.vertices),
                       'faces': len(ob.data.polygons), 'arestas_nao_manifold': bordas_abertas,
                       'faces_degeneradas': zero, 'normais_topo_invertidas': normais_erradas})

for ob in sc.objects:
    ob.select_set(False)
pista.select_set(True)
sc.view_layers[0].objects.active = pista
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        space = area.spaces.active
        space.clip_end = 3000
        space.region_3d.view_distance = 480
        space.region_3d.view_location = (0, 0, 0)
        space.region_3d.view_rotation = cam_iso.rotation_euler.to_quaternion()
        space.region_3d.view_perspective = 'ORTHO'
        space.shading.type = 'MATERIAL'

bpy.context.view_layer.update()
fonte_txt = bpy.data.texts.new('LEIA_ME_PI001')
fonte_txt.write('PI001 — modelo criado pelo Blender MCP a partir do JPG.\n'
                'Largura: 8 m; zebras: 0,8 m por lado; escala provisória: 0,6 m/px.\n'
                'A ponta superior direita foi arredondada. Pista plana.\n'
                'Câmeras de topo e perspectiva na coleção Apresentação.\n'
                'JPG empacotado e eixo editável na coleção de guias.\n'
                'Integração, colisões e IA na Godot ainda pendentes.\n')
script_txt = bpy.data.texts.load(str(RAIZ / 'registros/criar_pista_blender_mcp.py'))
bpy.data.libraries.write(str(ARQUIVO), {sc, fonte_txt, script_txt},
                         path_remap='RELATIVE_ALL', fake_user=True, compress=True)
relatorio = {
    'status': 'Modelo criado e salvo pelo Blender MCP',
    'blender': bpy.app.version_string,
    'arquivo_blend': str(ARQUIVO),
    'sha256_blend': hashlib.sha256(ARQUIVO.read_bytes()).hexdigest(),
    'referencia_preservada': hashlib.sha256(FONTE.read_bytes()).hexdigest() == DADOS['sha256_referencia'],
    'backup_sessao_anterior': str(backup), 'estado_anterior': estado_anterior,
    'dimensoes_eixo_m': DADOS['dimensoes_eixo_m'],
    'comprimento_eixo_m': DADOS['comprimento_eixo_m'],
    'largura_asfalto_m': 8.0, 'largura_zebra_m': 0.8,
    'objetos': len(sc.objects), 'validacao_malhas': validacoes,
    'bordas_sem_autointersecoes': DADOS['bordas_sem_autointersecoes'],
    'integracao_godot': 'Pendente; jogo atual preservado',
    'limitacoes': ['Escala, largura e largada provisórias',
                   'Ponta superior direita arredondada para acomodar a largura',
                   'Sem relevo ou cenário detalhado: referência mostra somente o traçado'],
}
(RAIZ / 'validacao/modelo_blender.json').write_text(json.dumps(relatorio, indent=2, ensure_ascii=False) + '\n')
result = relatorio
