"""Vistas de conferência da Fase 4 na cena aberta (Blender MCP). Altera a pose e a cena só para renderizar;
depois de rodar, desfazer com bpy.ops.wm.revert_mainfile() (o script não salva).
Uso no MCP: SAIDA_DIR = "<pasta>"; exec(open(<este arquivo>).read())"""
import bpy, math
from mathutils import Vector, Matrix

sc = bpy.context.scene
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "TEXTURE"
sc.render.resolution_x = sc.render.resolution_y = 700; sc.render.film_transparent = False
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


iso = Vector((2, -2, 1.6)); c0 = Vector((0, 0, 0.46))
pescoco = Vector(rig.data.bones["Head_Bone"].head_local) + Vector((0, 0, 0.06))
foto("repouso_iso", c0, iso, 1.3)
foto("repouso_pescoco_tras", pescoco, Vector((-1.5, 2, 0.6)), 0.45)
# cabeça: Y local = vertical (giro), Z local = rolagem (inclinação lateral), X local = arfagem
for eixo, graus, nome in (("Y", 40, "cabeca_giro_y_+40"), ("Y", -40, "cabeca_giro_y_-40"),
                          ("Z", 15, "cabeca_incl_z_+15"), ("Z", -15, "cabeca_incl_z_-15"), ("X", 15, "cabeca_arfagem_x_+15")):
    head.matrix_basis = Matrix.Rotation(math.radians(graus), 4, eixo)
    foto(nome + "_frente", pescoco, Vector((0, -3, 0)), 0.45)
    foto(nome + "_tras_alto", pescoco, Vector((-1.2, 2.2, 1.4)), 0.45)
    foto(nome + "_lado", pescoco, Vector((3, 0, 0.2)), 0.45)
head.matrix_basis = Matrix.Identity(4)
# rodas dianteiras esterçadas 30° (Z local) e traseira esquerda girada 90° (X local)
for n in ("Wheel_Front_Left", "Wheel_Front_Right"):
    o = bpy.data.objects[n]; o.matrix_basis = o.matrix_basis @ Matrix.Rotation(math.radians(30), 4, "Z")
o = bpy.data.objects["Wheel_Rear_Left"]; o.matrix_basis = o.matrix_basis @ Matrix.Rotation(math.radians(90), 4, "X")
foto("rodas_esterco30_giro90_topo", Vector((0, 0, 0.2)), Vector((0, 0.001, 3)), 1.3)
foto("rodas_esterco30_giro90_iso", c0, iso, 1.3)
result = {"vistas": feitas}
