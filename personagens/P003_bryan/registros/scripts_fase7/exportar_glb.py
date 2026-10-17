"""Fase 7 — exporta o Bryan para a Godot (GLB, mesma estrutura do Jake, com as duas ações da cabeça).
Uso no MCP: DESTINO (caminho do .glb), SAIDA (json); exec(open(<este arquivo>).read()).
Exige o bryan.blend recarregado do disco (is_dirty False). Põe o quadro 1 só para exportar e devolve o quadro e a ação ativa.
Não salva o .blend."""
import bpy, os, json, hashlib

sc = bpy.context.scene
rig = bpy.data.objects["Personagem_Rig"]
ad = rig.animation_data
assert not bpy.data.is_dirty, "recarregar o bryan.blend do disco antes de exportar"
quadro0, acao0 = sc.frame_current, ad.action
OPCOES = dict(
    export_format="GLB", use_selection=False, use_visible=False, export_yup=True, export_apply=False,
    export_texcoords=True, export_normals=True, export_tangents=False, export_attributes=False, export_extras=False,
    export_materials="EXPORT", export_image_format="AUTO", export_vertex_color="NONE",
    export_skins=True, export_def_bones=False, export_rest_position_armature=True, export_leaf_bone=False,
    export_animations=True, export_animation_mode="ACTIONS", export_anim_slide_to_zero=True,
    export_force_sampling=True, export_reset_pose_bones=True, export_optimize_animation_size=True,
    export_morph=False, export_lights=False, export_cameras=False, export_draco_mesh_compression_enable=False,
)
os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
try:
    sc.frame_set(1)
    bpy.ops.export_scene.gltf(filepath=DESTINO, **OPCOES)
finally:
    ad.action = acao0
    sc.frame_set(quadro0)
dados = open(DESTINO, "rb").read()
r = {"arquivo_blend": bpy.data.filepath, "blender": bpy.app.version_string, "destino": DESTINO, "opcoes": OPCOES,
     "bytes": len(dados), "sha256": hashlib.sha256(dados).hexdigest(), "blend_sujo_apos": bpy.data.is_dirty,
     "estado_restaurado": [sc.frame_current == quadro0, ad.action == acao0]}
json.dump(r, open(SAIDA, "w"), indent=1, ensure_ascii=False)
result = r
