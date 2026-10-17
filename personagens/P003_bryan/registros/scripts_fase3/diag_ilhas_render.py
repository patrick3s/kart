# Fase 3 — diagnóstico visual: pinta ilhas escolhidas com cores temporárias e renderiza vistas.
# Executar na sessão aberta pelo Blender MCP definindo NPZ, OUTDIR, CORES {ilha: (r,g,b)} e VISTAS
# [(nome, centro, direção, escala)] antes de exec(). Altera a cena só temporariamente:
# recarregar o arquivo depois (wm.revert_mainfile), sem salvar.
import bpy, numpy as np
from mathutils import Vector
z = np.load(NPZ); comp = z["components"]
o = [x for x in bpy.data.objects if x.type == "MESH"][0]; m = o.data
ov = np.empty(len(m.vertices), np.int32); m.attributes["rig_original_vertex"].data.foreach_get("value", ov)
cor = np.full((len(ov), 4), 0.55, np.float32); cor[:, 3] = 1
ilha = comp[ov]
for i, c in CORES.items():
    cor[ilha == i, :3] = c
a = m.color_attributes.new("diag_temp", "FLOAT_COLOR", "POINT"); a.data.foreach_set("color", cor.ravel())
m.color_attributes.active_color = a
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'VERTEX'
sc.render.resolution_x = sc.render.resolution_y = 800; sc.render.resolution_percentage = 100
sc.render.film_transparent = False
cd = bpy.data.cameras.new("cam_temp"); cd.type = 'ORTHO'; cd.clip_end = 20
cam = bpy.data.objects.new("cam_temp", cd); sc.collection.objects.link(cam); sc.camera = cam
for nome, c, d, esc in VISTAS:
    c = Vector(c); d = Vector(d)
    cd.ortho_scale = esc; cam.location = c + d; cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = f"{OUTDIR}/{nome}.png"; bpy.ops.render.render(write_still=True)
