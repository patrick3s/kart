"""Vistas de conferência da Fase 4 do Bryan na cena aberta (Blender MCP). Altera a pose e a cena só para renderizar;
depois de rodar, desfazer com bpy.ops.wm.revert_mainfile() (o script não salva).
Uso no MCP: SAIDA_DIR = "<pasta>"; exec(open(<este arquivo>).read())
Base: render_vistas.py do P002; acrescenta vistas laterais das rodas giradas para conferir a costura da Fase 3."""
import bpy, math
from mathutils import Vector, Matrix

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "TEXTURE"
sc.render.resolution_x = sc.render.resolution_y = 700; sc.render.resolution_percentage = 100; sc.render.film_transparent = False
cd = bpy.data.cameras.new("cam_conferencia"); cd.type = "ORTHO"; cd.clip_end = 20
cam = bpy.data.objects.new("cam_conferencia", cd); sc.collection.objects.link(cam); sc.camera = cam
rig = bpy.data.objects["Personagem_Rig"]; rig.hide_render = True
head = rig.pose.bones["Head_Bone"]
feitas = []


def foto(nome, centro, direcao, escala):
    cd.ortho_scale = escala
    cam.location = centro + direcao
    cam.rotation_euler = (-direcao).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    sc.render.filepath = f"{SAIDA_DIR}/{nome}.png"
    bpy.ops.render.render(write_still=True)
    feitas.append(nome)


iso = Vector((2, -2, 1.6)); c0 = Vector((0, 0, 0.40))
pescoco = Vector(rig.data.bones["Head_Bone"].head_local) + Vector((0, 0, 0.08))
foto("repouso_iso", c0, iso, 1.3)
foto("repouso_pescoco_tras", pescoco, Vector((-1.5, 2, 0.6)), 0.5)
# cabeça: Y local = vertical (giro), Z local = inclinação lateral, X local = arfagem
for eixo, graus, nome in (("Y", 40, "cabeca_giro_y_+40"), ("Y", -40, "cabeca_giro_y_-40"),
                          ("Z", 15, "cabeca_incl_z_+15"), ("Z", -15, "cabeca_incl_z_-15"), ("X", 15, "cabeca_arfagem_x_+15")):
    head.matrix_basis = Matrix.Rotation(math.radians(graus), 4, eixo)
    foto(nome + "_frente", pescoco, Vector((0, -3, 0)), 0.5)
    foto(nome + "_tras_alto", pescoco, Vector((-1.2, 2.2, 1.4)), 0.5)
    foto(nome + "_lado", pescoco, Vector((3, 0, 0.2)), 0.5)
head.matrix_basis = Matrix.Identity(4)
# rodas: dianteiras esterçadas 30° (Z local) e traseira esquerda girada 90° (X local)
mb0 = {n: bpy.data.objects[n].matrix_basis.copy() for n in ("Wheel_Front_Left", "Wheel_Front_Right", "Wheel_Rear_Left", "Wheel_Rear_Right")}
for n in ("Wheel_Front_Left", "Wheel_Front_Right"):
    o = bpy.data.objects[n]; o.matrix_basis = mb0[n] @ Matrix.Rotation(math.radians(30), 4, "Z")
o = bpy.data.objects["Wheel_Rear_Left"]; o.matrix_basis = mb0["Wheel_Rear_Left"] @ Matrix.Rotation(math.radians(90), 4, "X")
foto("rodas_esterco30_giro90_topo", Vector((0, 0, 0.2)), Vector((0, 0.001, 3)), 1.3)
foto("rodas_esterco30_giro90_iso", c0, iso, 1.3)
for n, m in mb0.items():
    bpy.data.objects[n].matrix_basis = m
# lado esquerdo (+X) com as rodas giradas 0°, 90° e 180°: costura, faixa interna do pneu e topo serrilhado
for graus in (0, 90, 180):
    for n in ("Wheel_Front_Left", "Wheel_Rear_Left"):
        bpy.data.objects[n].matrix_basis = mb0[n] @ Matrix.Rotation(math.radians(graus), 4, "X")
    foto(f"rodas_esq_giro_{graus}_lado", Vector((0, 0, 0.2)), Vector((3, 0, 0)), 1.2)
    for n in ("Wheel_Front_Left", "Wheel_Rear_Left"):
        c = bpy.data.objects[n].matrix_world.translation
        foto(f"{n}_giro_{graus}_lado", Vector(c), Vector((3, 0, 0)), 0.34)
for n, m in mb0.items():
    bpy.data.objects[n].matrix_basis = m
result = {"vistas": feitas}
