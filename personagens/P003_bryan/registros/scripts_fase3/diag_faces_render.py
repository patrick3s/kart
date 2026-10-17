# Fase 3 — diagnóstico visual por FACE: cores lidas de um .npy (n_faces originais × 3) e vistas renderizadas.
# Executar na sessão aberta pelo Blender MCP definindo FCORES (caminho .npy), OUTDIR, VISTAS e TEXTURA (bool) antes de exec().
# Altera a cena só temporariamente: recarregar o arquivo depois (wm.revert_mainfile), sem salvar.
import bpy, numpy as np
from mathutils import Vector
fc = np.load(FCORES).astype(np.float32)
o = [x for x in bpy.data.objects if x.type == "MESH"][0]; m = o.data
of = np.empty(len(m.polygons), np.int32); m.attributes["rig_original_face"].data.foreach_get("value", of)
st = np.empty(len(m.polygons), np.int32); m.polygons.foreach_get("loop_start", st)
tt = np.empty(len(m.polygons), np.int32); m.polygons.foreach_get("loop_total", tt)
cor = np.ones((len(m.loops), 4), np.float32); cor[:, :3] = np.repeat(fc[of], tt, axis=0)
a = m.color_attributes.new("diag_temp", "FLOAT_COLOR", "CORNER"); a.data.foreach_set("color", cor.ravel())
m.color_attributes.active_color = a
sc = bpy.context.scene; sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'
sc.render.resolution_x = sc.render.resolution_y = 600; sc.render.resolution_percentage = 100
sc.render.film_transparent = False
cd = bpy.data.cameras.new("cam_temp"); cd.type = 'ORTHO'; cd.clip_end = 20
cam = bpy.data.objects.new("cam_temp", cd); sc.collection.objects.link(cam); sc.camera = cam
for tipo in (["VERTEX", "TEXTURE"] if TEXTURA else ["VERTEX"]):
    sc.display.shading.color_type = tipo
    for nome, c, d, esc in VISTAS:
        c = Vector(c); d = Vector(d)
        cd.ortho_scale = esc; cam.location = c + d; cam.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
        sc.render.filepath = f"{OUTDIR}/{nome}_{tipo.lower()}.png"; bpy.ops.render.render(write_still=True)
