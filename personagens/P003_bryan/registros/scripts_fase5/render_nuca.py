"""Fase 5 (P003 Bryan) — vistas da nuca em amplitudes candidatas do Head_Bone, para definir o limite (decisão do usuário: limitar).
Altera pose e cena só para renderizar; depois desfazer com bpy.ops.wm.revert_mainfile() (o script não salva).
Uso no MCP: SAIDA_DIR = "<pasta>"; exec(open(<este arquivo>).read())
Vistas:
- jogo: posição da camera_perseguicao.gd (3,4 m atrás, 1,4 m acima) dividida pela escala 2,0 do catálogo → (0, 1,7, 0,7)
  no espaço do modelo; perspectiva estreita apontada ao pescoço (mesmo ângulo de visão, só ampliado);
- jogo_lat30: a mesma câmera girada 30° em torno do kart (atraso do giro da câmera nas curvas);
- tras_alto: direção da Fase 4 (−1,2, 2,2, 1,4), ortográfica;
- lado: +X, ortográfica.
Eixos locais do Head_Bone (Fase 4): Y = giro horizontal, Z = inclinação lateral (rolagem), X = arfagem."""
import bpy, math
from mathutils import Vector, Matrix

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "TEXTURE"
sc.render.resolution_x = sc.render.resolution_y = 500; sc.render.resolution_percentage = 100; sc.render.film_transparent = False
cd = bpy.data.cameras.new("cam_conferencia"); cd.clip_end = 20
cam = bpy.data.objects.new("cam_conferencia", cd); sc.collection.objects.link(cam); sc.camera = cam
rig = bpy.data.objects["Personagem_Rig"]; rig.hide_render = True
head = rig.pose.bones["Head_Bone"]; head.rotation_mode = "XYZ"
pescoco = Vector(rig.data.bones["Head_Bone"].head_local) + Vector((0, 0, 0.08))
JOGO = Vector((0, 1.7, 0.7))


def girar_z(v, graus):
    return Matrix.Rotation(math.radians(graus), 3, "Z") @ v


VISTAS = {"jogo": ("PERSP", JOGO.copy()),
          "jogo_lat30": ("PERSP", girar_z(JOGO, 30)),
          "tras_alto": ("ORTHO", pescoco + Vector((-1.2, 2.2, 1.4))),
          "lado": ("ORTHO", pescoco + Vector((3, 0, 0.2)))}
PREFIXO = {"Y": "giro_y", "Z": "rolagem_z", "X": "arfagem_x"}
# 1ª rodada: amplitudes da Fase 4 e do jogo; 2ª rodada (ANGULOS definido antes do exec): amplitudes menores
ANGULOS = globals().get("ANGULOS") or {"Y": (20, -20, 25, -25, 30, -30, 40, -40), "Z": (15, -15, 20, -20, 25, -25), "X": (6, -6, 10, -10, 15)}
POSES = [("repouso", None, 0)] + [(f"{PREFIXO[e]}_{g:+d}", e, g) for e, gs in ANGULOS.items() for g in gs]
feitas = []
try:
    for nome, eixo, g in POSES:
        head.matrix_basis = Matrix.Rotation(math.radians(g), 4, eixo) if eixo else Matrix.Identity(4)
        for vn, (tipo, pos) in VISTAS.items():
            cd.type = tipo
            if tipo == "ORTHO":
                cd.ortho_scale = 0.4
            else:
                d = (pos - pescoco).length; cd.angle = 2 * math.atan(0.2 / d)  # ~0,4 m de quadro no pescoço
            cam.location = pos
            cam.rotation_euler = (pescoco - pos).to_track_quat("-Z", "Y").to_euler()
            bpy.context.view_layer.update()
            sc.render.filepath = f"{SAIDA_DIR}/{nome}__{vn}.png"
            bpy.ops.render.render(write_still=True)
            feitas.append(f"{nome}__{vn}")
finally:
    head.matrix_basis = Matrix.Identity(4)
result = {"vistas": len(feitas)}
