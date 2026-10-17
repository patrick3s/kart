"""Executado via Blender MCP; lê o .blend salvo em cena temporária e não o regrava."""
import bpy, json, pathlib, hashlib, shutil, tempfile
from mathutils import Vector
ROOT = pathlib.Path('/Users/patricksoares/Documents/jogos/kart')
BASE = ROOT/'pistas/PI001_primeira_pista'
OUT = ROOT/'jogo/pistas/primeira_pista'
EVID = BASE/'validacao/integracao_20261016'
original = BASE/'blender/primeira_pista.blend'
antes = hashlib.sha256(original.read_bytes()).hexdigest()
sessao = bpy.context.window.scene
selecao = list(bpy.context.selected_objects)
ativo = bpy.context.view_layer.objects.active
bpy.ops.wm.save_as_mainfile(filepath=str(EVID/'sessao_blender_antes_exportacao.blend'), copy=True)
nomes = {}
# Libera nomes temporariamente; os objetos abertos e alterações não salvas são preservados.
for o in list(bpy.data.objects):
    if o.name.startswith('PI001_'):
        nomes[o] = o.name
        o.name = 'SESSAO_' + o.name
copia = pathlib.Path(tempfile.mkdtemp(prefix='pi001_export_'))/'fonte.blend'
shutil.copy2(original, copia)
with bpy.data.libraries.load(str(copia), link=False) as (src, dst):
    dst.scenes = [src.scenes[0]]
cena = dst.scenes[0]
try:
    bpy.context.window.scene = cena
    bpy.ops.object.select_all(action='DESELECT')
    malhas = [o for o in cena.objects if o.type == 'MESH']
    for o in malhas:
        o.hide_set(False)
        o.select_set(True)
    eixo = next(o for o in cena.objects if o.name.startswith('PI001_Eixo_Editavel'))
    pts = [eixo.matrix_world @ Vector(p.co[:3]) for p in eixo.data.splines[0].points]
    fonte = json.loads((BASE/'validacao/tracado_extraido.json').read_text())['pontos_xy_m']
    erro = max((Vector((p[0],p[1],0))-Vector((q.x,q.y,0))).length for p,q in zip(fonte,pts))
    dados = {'origem':str(original.relative_to(ROOT)), 'sha256_blend':antes,
             'conversao':'Blender (x,y,z) -> Godot (x,z,-y); escala 1:1',
             'erro_maximo_eixo_json_m':erro,'largura_asfalto_m':8.0,
             'pontos':[ [p.x,0.1,-p.y] for p in pts],
             'largada':[0.1685229987,0.1,116.0999984741]}
    (OUT/'percurso.json').write_text(json.dumps(dados,indent=2))
    # glTF não transporta os nós Noise/Bump: ficam equivalentes na Godot.
    materiais=[]
    for o in malhas:
        for i,m in enumerate(o.data.materials):
            if not m: continue
            c=m.copy(); c.name=m.name.split('.')[0]+'_Jogo'
            c.use_nodes=True
            bs=next(n for n in c.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
            for socket in ['Base Color','Normal']:
                for link in list(bs.inputs[socket].links): c.node_tree.links.remove(link)
            bs.inputs['Base Color'].default_value=m.diffuse_color
            bs.inputs['Roughness'].default_value=0.88
            o.data.materials[i]=c
            materiais.append(c.name)
    bpy.context.view_layer.objects.active=malhas[0]
    bpy.ops.export_scene.gltf(filepath=str(OUT/'primeira_pista.glb'),export_format='GLB',use_selection=True,use_active_scene=True,export_cameras=False,export_lights=False,export_yup=True)
    rel={'sha256_original_antes':antes,'sha256_original_depois':hashlib.sha256(original.read_bytes()).hexdigest(),'malhas':[o.name for o in malhas],'materiais':sorted(set(materiais)),'eixo_pontos':len(pts),'erro_eixo_m':erro,'glb_bytes':(OUT/'primeira_pista.glb').stat().st_size,'excluidos':['cameras','luzes','referencia','eixo (exportado em JSON)'],'materiais_procedurais':'equivalentes em superficie.gdshader na Godot'}
    (EVID/'exportacao_blender.json').write_text(json.dumps(rel,indent=2))
finally:
    bpy.context.window.scene=sessao
    for o in list(cena.objects): bpy.data.objects.remove(o,do_unlink=True)
    bpy.data.scenes.remove(cena)
    for o,n in nomes.items(): o.name=n
    for o in selecao: o.select_set(True)
    bpy.context.view_layer.objects.active=ativo
result=rel
