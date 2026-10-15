import bpy, sys, math
from mathutils import Vector
outdir=sys.argv[sys.argv.index("--")+1]
sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='FLAT'; sc.display.shading.color_type='TEXTURE'
sc.render.resolution_x=sc.render.resolution_y=900
sc.render.film_transparent=True
cam_d=bpy.data.cameras.new("c"); cam_d.type='ORTHO'; cam_d.ortho_scale=1.15
cam=bpy.data.objects.new("c",cam_d); sc.collection.objects.link(cam); sc.camera=cam
c=Vector((0,0,0.46))
views={"pos_y":Vector((0,3,0)),"neg_y":Vector((0,-3,0)),"pos_x":Vector((3,0,0)),"neg_x":Vector((-3,0,0)),"topo":Vector((0,0.001,3)),"iso":Vector((2,-2,1.6))}
for n,d in views.items():
    cam.location=c+d
    cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=f"{outdir}/vista_{n}.png"; bpy.ops.render.render(write_still=True)
print("RENDER_OK")
