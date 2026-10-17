"""Fase 3 — vistas de conferência (não salva): reunidas, explodidas e cada parte isolada, com textura.
Executar na sessão aberta pelo Blender MCP definindo OUTDIR antes de exec(); recarregar o arquivo depois (wm.revert_mainfile)."""
import bpy
from mathutils import Vector
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'TEXTURE'
sc.render.resolution_x = sc.render.resolution_y = 700; sc.render.resolution_percentage = 100; sc.render.film_transparent = False
cd = bpy.data.cameras.new("cam_temp"); cd.type = 'ORTHO'; cd.clip_end = 20
cam = bpy.data.objects.new("cam_temp", cd); sc.collection.objects.link(cam); sc.camera = cam
P = {o.name: o for o in bpy.data.objects if o.type == "MESH"}
def shot(nome, c, d, esc):
    cd.ortho_scale = esc; cam.location = c + d; cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = f"{OUTDIR}/{nome}.png"; bpy.ops.render.render(write_still=True)
iso = Vector((2, -2, 1.6)); c0 = Vector((0, 0, 0.385))
shot("reunidas_iso", c0, iso, 1.25)
off = {"Cabeca": (0, 0, 0.22), "Wheel_Front_Left": (0.22, -0.08, 0), "Wheel_Front_Right": (-0.22, -0.08, 0),
       "Wheel_Rear_Left": (0.22, 0.08, 0), "Wheel_Rear_Right": (-0.22, 0.08, 0)}
for n, v in off.items(): P[n].location = v
bpy.context.view_layer.update()
shot("explodida_iso", Vector((0, 0, 0.42)), iso, 1.7); shot("explodida_tras", Vector((0, 0, 0.42)), Vector((-2, 2, 1.2)), 1.7)
shot("explodida_baixo", Vector((0, 0, 0.1)), Vector((0, 0.001, -3)), 1.6)
for n in off: P[n].location = (0, 0, 0)
bpy.context.view_layer.update()
for n, o in P.items():
    for x in P.values(): x.hide_render = (x is not o)
    c = sum((o.matrix_world @ Vector(b) for b in o.bound_box), Vector())/8
    if n.startswith("Wheel"):
        sx = 1 if c.x > 0 else -1
        shot(f"{n}_fora", c, Vector((sx*3, 0, 0)), 0.32); shot(f"{n}_dentro", c, Vector((-sx*3, 0, 0)), 0.32)
    elif n == "Cabeca":
        shot("Cabeca_frente", c, Vector((0, -3, 0)), 0.3); shot("Cabeca_lado_esq", c, Vector((3, 0, 0)), 0.3)
        shot("Cabeca_baixo", c, Vector((0, 0.001, -3)), 0.3)
    else:
        shot("Corpo_Kart_iso", c, iso, 1.25); shot("Corpo_Kart_lado_esq", c, Vector((3, 0, 0)), 1.25)
        shot("Corpo_Kart_baixo", c, Vector((0, 0.001, -3)), 1.25)
