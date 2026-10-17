"""Vistas de conferência da Fase 3 (não salva o arquivo): reunidas, explodidas e cada parte isolada."""
import bpy, sys
from mathutils import Vector
out=sys.argv[sys.argv.index("--")+1]
sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='STUDIO'; sc.display.shading.color_type='TEXTURE'
sc.render.resolution_x=sc.render.resolution_y=700; sc.render.film_transparent=False
cd=bpy.data.cameras.new("c"); cd.type='ORTHO'; cd.clip_end=20
cam=bpy.data.objects.new("c",cd); sc.collection.objects.link(cam); sc.camera=cam
P={o.name:o for o in bpy.data.objects if o.type=="MESH"}
def shot(nome,c,d,esc):
    cd.ortho_scale=esc; cam.location=c+d; cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler()
    sc.render.filepath=f"{out}/{nome}.png"; bpy.ops.render.render(write_still=True)
iso=Vector((2,-2,1.6)); c0=Vector((0,0,0.46))
shot("reunidas_iso",c0,iso,1.3)
off={"Cabeca":(0,0,0.25),"Wheel_Front_Left":(0.25,-0.1,0),"Wheel_Front_Right":(-0.25,-0.1,0),"Wheel_Rear_Left":(0.25,0.1,0),"Wheel_Rear_Right":(-0.25,0.1,0)}
for n,v in off.items(): P[n].location=v
shot("explodida_iso",Vector((0,0,0.5)),iso,1.8); shot("explodida_tras",Vector((0,0,0.5)),Vector((-2,2,1.2)),1.8)
for n,v in off.items(): P[n].location=(0,0,0)
bpy.context.view_layer.update()
for n,o in P.items():
    for x in P.values(): x.hide_render=(x is not o)
    c=sum((o.matrix_world@Vector(b) for b in o.bound_box),Vector())/8
    if n.startswith("Wheel"):
        sx=1 if c.x>0 else -1
        shot(f"{n}_fora",c,Vector((sx*3,0,0)),0.36); shot(f"{n}_dentro",c,Vector((-sx*3,0,0)),0.36)
    elif n=="Cabeca":
        shot("Cabeca_frente",c,Vector((0,-3,0)),0.4); shot("Cabeca_lado_esq",c,Vector((3,0,0)),0.4); shot("Cabeca_baixo",c,Vector((0,0.001,-3)),0.4)
    else:
        shot("Corpo_Kart_iso",c,iso,1.3); shot("Corpo_Kart_lado_esq",c,Vector((3,0,0)),1.3)
print("RENDER_OK")
