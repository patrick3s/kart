import bpy, sys, os
argv = sys.argv[sys.argv.index("--")+1:]
glb, out = argv
assert not os.path.exists(out), "destino já existe"
bpy.ops.wm.read_homefile(use_empty=True)
r = bpy.ops.import_scene.gltf(filepath=glb)
print("IMPORT", r)
bpy.ops.wm.save_as_mainfile(filepath=out, relative_remap=True)
print("SAVED", out)
