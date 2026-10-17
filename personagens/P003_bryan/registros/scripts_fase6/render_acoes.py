"""Fase 6 (P003 Bryan) — vistas das ações da cabeça nos quadros 13 e 25, pela própria ação (frame_set), sem pose manual.
Altera cena e ação ativa só para renderizar; depois desfazer com bpy.ops.wm.revert_mainfile() (o script não salva).
Uso no MCP: SAIDA_DIR = "<pasta>"; exec(open(<este arquivo>).read())
Vistas (mesmas convenções de scripts_fase5/render_nuca.py):
- frente: −Y, ortográfica, cabeça inteira;
- jogo_kart: câmera da camera_perseguicao.gd no espaço do modelo (0, 1,7, 0,7), quadro do kart inteiro;
- jogo_lat30: a mesma câmera girada 30° (atraso nas curvas), ampliada no pescoço;
- tras_alto: direção da Fase 4, ortográfica, ampliada no pescoço."""
import bpy, math
from mathutils import Vector, Matrix

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "TEXTURE"
sc.render.resolution_x = sc.render.resolution_y = 500; sc.render.resolution_percentage = 100; sc.render.film_transparent = False
cd = bpy.data.cameras.new("cam_conferencia"); cd.clip_end = 20
cam = bpy.data.objects.new("cam_conferencia", cd); sc.collection.objects.link(cam); sc.camera = cam
rig = bpy.data.objects["Personagem_Rig"]; rig.hide_render = True; ad = rig.animation_data
pivo = Vector(rig.data.bones["Head_Bone"].head_local)
pescoco = pivo + Vector((0, 0, 0.08)); cabeca = pivo + Vector((0, 0, 0.14))
JOGO = Vector((0, 1.7, 0.7))
VISTAS = {"frente": ("ORTHO", cabeca, cabeca + Vector((0, -3, 0)), 0.45),
          "jogo_kart": ("PERSP", Vector((0, 0, 0.35)), JOGO.copy(), 1.1),
          "jogo_lat30": ("PERSP", pescoco, Matrix.Rotation(math.radians(30), 3, "Z") @ JOGO, 0.4),
          "tras_alto": ("ORTHO", pescoco, pescoco + Vector((-1.2, 2.2, 1.4)), 0.4)}
ACOES = {"direita": "Cabeca_Direita_Ida_e_Volta", "esquerda": "Cabeca_Esquerda_Ida_e_Volta"}
feitas = []
for rot, nome_acao in ACOES.items():
    ad.action = bpy.data.actions[nome_acao]
    for q in (13, 25):
        sc.frame_set(q)
        for vn, (tipo, alvo, pos, quadro) in VISTAS.items():
            cd.type = tipo
            if tipo == "ORTHO":
                cd.ortho_scale = quadro
            else:
                cd.angle = 2 * math.atan(quadro / 2 / (pos - alvo).length)
            cam.location = pos
            cam.rotation_euler = (alvo - pos).to_track_quat("-Z", "Y").to_euler()
            bpy.context.view_layer.update()
            sc.render.filepath = f"{SAIDA_DIR}/{rot}_q{q}__{vn}.png"
            bpy.ops.render.render(write_still=True)
            feitas.append(f"{rot}_q{q}__{vn}")
result = {"vistas": len(feitas), "graus_q25": math.degrees(rig.pose.bones["Head_Bone"].rotation_euler.y)}
