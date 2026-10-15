"""Fase 6 — cria as ações de olhar para a direita e para a esquerda do piloto (ida e volta) em Personagem_Rig.
Canal único: pose.bones["Head_Bone"].rotation_euler[1] (Y local = Z mundial). Sinal: positivo vira o rosto para +X,
que é a ESQUERDA do piloto (frente -Y). Direita do piloto = negativo.
Quadros 1/25/49 a 24 FPS (2 s), 0° -> ±AMPLITUDE -> 0°, BEZIER, AUTO_CLAMPED, extrapolação CONSTANT, sem ciclos nem NLA.
Prévia 1-49; intervalo principal preservado. Não salva.
Uso no MCP: AMPLITUDE_GRAUS = 25; exec(open(<este arquivo>).read())"""
import bpy, math
from bpy_extras import anim_utils

sc = bpy.context.scene
rig = bpy.data.objects["Personagem_Rig"]
pb = rig.pose.bones["Head_Bone"]
assert sc.render.fps == 24 and sc.render.fps_base == 1.0, "FPS diferente do combinado"
assert pb.rotation_mode == "XYZ"
assert not bpy.data.actions, "já existem ações; não sobrescrever"
QUADROS = (1, 25, 49)
ACOES = {"Cabeca_Direita_Ida_e_Volta": -AMPLITUDE_GRAUS, "Cabeca_Esquerda_Ida_e_Volta": +AMPLITUDE_GRAUS}
ad = rig.animation_data_create()
criadas = {}
for nome, graus in ACOES.items():
    act = bpy.data.actions.new(nome); act.use_fake_user = True
    ad.action = act
    for f, v in zip(QUADROS, (0.0, math.radians(graus), 0.0)):
        pb.rotation_euler = (0.0, v, 0.0)
        pb.keyframe_insert("rotation_euler", index=1, frame=f, group="Head_Bone")
    slot = ad.action_slot
    cb = anim_utils.action_get_channelbag_for_slot(act, slot)
    fcs = list(cb.fcurves)
    assert len(fcs) == 1 and fcs[0].data_path == 'pose.bones["Head_Bone"].rotation_euler' and fcs[0].array_index == 1
    fc = fcs[0]; fc.extrapolation = "CONSTANT"
    for k in fc.keyframe_points:
        k.interpolation = "BEZIER"; k.handle_left_type = k.handle_right_type = "AUTO_CLAMPED"
    fc.update()
    criadas[nome] = {"slot": slot.identifier, "keys": [(k.co[0], math.degrees(k.co[1])) for k in fc.keyframe_points],
                     "modificadores": len(fc.modifiers)}
    pb.rotation_euler = (0.0, 0.0, 0.0)
# ação ativa ao salvar: direita do piloto, no quadro 1 (pose neutra)
ad.action = bpy.data.actions["Cabeca_Direita_Ida_e_Volta"]
sc.use_preview_range = True; sc.frame_preview_start, sc.frame_preview_end = 1, 49
sc.frame_set(1)
result = {"criadas": criadas, "ativa": ad.action.name, "slot_ativo": ad.action_slot and ad.action_slot.identifier,
          "previa": [sc.frame_preview_start, sc.frame_preview_end], "intervalo": [sc.frame_start, sc.frame_end], "nla": len(ad.nla_tracks)}
