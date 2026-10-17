# Fase 2 — vistas ortográficas texturizadas (Workbench) para conferir a orientação.
# Executar na sessão aberta pelo Blender MCP definindo OUTDIR antes de exec();
# a câmera e os ajustes de render são temporários: recarregar o arquivo depois (wm.revert_mainfile).
import bpy
from mathutils import Vector
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'FLAT'; sc.display.shading.color_type = 'TEXTURE'
sc.render.resolution_x = sc.render.resolution_y = 900
sc.render.resolution_percentage = 100
sc.render.film_transparent = True
cam_d = bpy.data.cameras.new("cam_temp"); cam_d.type = 'ORTHO'; cam_d.ortho_scale = 1.15
cam = bpy.data.objects.new("cam_temp", cam_d); sc.collection.objects.link(cam); sc.camera = cam
c = Vector((0, 0, 0.385))
views = {"pos_y": Vector((0, 3, 0)), "neg_y": Vector((0, -3, 0)), "pos_x": Vector((3, 0, 0)),
         "neg_x": Vector((-3, 0, 0)), "topo": Vector((0, 0.001, 3)), "iso": Vector((2, -2, 1.6))}
for n, d in views.items():
    cam.location = c + d
    cam.rotation_euler = (c - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = f"{OUTDIR}/vista_{n}.png"
    bpy.ops.render.render(write_still=True)
