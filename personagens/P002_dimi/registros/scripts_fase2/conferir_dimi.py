import bpy, json
d = {"arquivo": bpy.data.filepath, "cenas":[s.name for s in bpy.data.scenes],
 "objetos": [], "materiais": len(bpy.data.materials), "imagens": [], "acoes":[a.name for a in bpy.data.actions],
 "armatures": len(bpy.data.armatures)}
tv=tf=0
for o in bpy.data.objects:
    e={"nome":o.name,"tipo":o.type,"pai":o.parent.name if o.parent else None,
       "loc":[round(v,4) for v in o.location],"rot":[round(v,4) for v in o.rotation_euler],"esc":[round(v,4) for v in o.scale],
       "dim":[round(v,4) for v in o.dimensions]}
    if o.type=="MESH":
        m=o.data; e.update(v=len(m.vertices),f=len(m.polygons),uv=len(m.uv_layers),mats=[s.material.name if s.material else None for s in o.material_slots],
          shapekeys=len(m.shape_keys.key_blocks) if m.shape_keys else 0, mods=[x.type for x in o.modifiers])
        tv+=e["v"]; tf+=e["f"]
    d["objetos"].append(e)
for i in bpy.data.images:
    d["imagens"].append({"nome":i.name,"empacotada":bool(i.packed_file),"caminho":i.filepath,"tam":list(i.size)})
d["total_v"]=tv; d["total_f"]=tf
d["unidades"]=[bpy.context.scene.unit_settings.system, bpy.context.scene.unit_settings.scale_length]
d["faltando"]=[i.name for i in bpy.data.images if not i.packed_file and i.filepath and not __import__('os').path.exists(bpy.path.abspath(i.filepath))]
print("JSON"+json.dumps(d, ensure_ascii=False))
