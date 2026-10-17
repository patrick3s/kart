"""Fase 4 — origens, Personagem_Rig, pesos rígidos, parentesco e modificadores do Bryan (cena aberta, Blender MCP).
Uso no MCP: MEDIDAS = "<validacao/medidas_pivos_fase4.json>"; INSTANTANEO = "<npz temporário>"; exec(open(<este arquivo>).read())
Não salva o arquivo. Guarda antes, em INSTANTANEO, as posições mundiais, o custom_normal e os sharp_* de cada parte.
Mesmo método do P002 (registro-fase4 do Dimi), com pivôs e alturas medidos neste modelo."""
import bpy, numpy as np, json
from mathutils import Matrix, Vector

G = 1 / 4096
med = json.load(open(MEDIDAS))
PIVO_CABECA = Vector(med["cabeca"]["pivo_adotado"])
RODAS = ("Wheel_Front_Left", "Wheel_Front_Right", "Wheel_Rear_Left", "Wheel_Rear_Right")
PARTES = ("Cabeca", "Corpo_Kart") + RODAS
assert not any(o.type == "ARMATURE" for o in bpy.data.objects), "já existe armature na cena"
assert all(bpy.data.objects[n].parent is None and bpy.data.objects[n].matrix_world == Matrix.Identity(4) for n in PARTES)
if bpy.context.mode != "OBJECT":
    bpy.ops.object.mode_set(mode="OBJECT")


def ler(m, nome, n, dt, k=1):
    a = np.zeros(n * k, dt)
    if nome in m.attributes:
        m.attributes[nome].data.foreach_get("value", a)
    return a.reshape(-1, k) if k > 1 else a


# 1. instantâneo para a comparação posterior
snap = {}
for n in PARTES:
    m = bpy.data.objects[n].data
    co = np.empty(len(m.vertices) * 3, np.float32); m.vertices.foreach_get("co", co)
    snap[n + "__co"] = co.reshape(-1, 3)
    snap[n + "__cn"] = ler(m, "custom_normal", len(m.loops), np.int16, 2)
    snap[n + "__se"] = ler(m, "sharp_edge", len(m.edges), bool)
    snap[n + "__sf"] = ler(m, "sharp_face", len(m.polygons), bool)
np.savez(INSTANTANEO, **snap)


# 2. origens: desloca a malha por -p e o objeto por +p (equivale a origin_set com compensação, sem modo de edição)
def mover_origem(nome, p):
    o = bpy.data.objects[nome]
    o.data.transform(Matrix.Translation(-p))
    o.location = p
    o.data.update()


mover_origem("Cabeca", PIVO_CABECA)
for n in RODAS:
    mover_origem(n, Vector(med["rodas"][n]["pivo_adotado"]))

# 3. armature: Root -> Torso -> Neck -> Head (rig com matriz identidade: espaço do rig = mundo)
x, y = PIVO_CABECA.x, PIVO_CABECA.y
Z_ASSOALHO = 330 * G   # 0,0805664: placa do assoalho (Z ≈ 0,0805)
Z_ASSENTO = 1024 * G   # 0,25: altura do assento/quadril do piloto
Z_PESCOCO = 1792 * G   # 0,4375: dentro do tronco, abaixo da superfície que fecha sob o pescoço (≈ 0,486)
Z_TOPO = 3008 * G      # 0,734375: topo do quepe (Z máx. da cabeça ≈ 0,7336)
OSSOS = [  # nome, início, fim, pai, deforma
    ("Root_Bone", (0, 0, Z_ASSOALHO), (0, 0, Z_ASSENTO), None, False),
    ("Torso_Bone", (0, 0, Z_ASSENTO), (x, y, Z_PESCOCO), "Root_Bone", True),
    ("Neck_Bone", (x, y, Z_PESCOCO), tuple(PIVO_CABECA), "Torso_Bone", False),
    ("Head_Bone", tuple(PIVO_CABECA), (x, y, Z_TOPO), "Neck_Bone", True),
]
arm = bpy.data.armatures.new("Personagem_Rig_Armature")
arm.display_type = "OCTAHEDRAL"
rig = bpy.data.objects.new("Personagem_Rig", arm)
rig.show_in_front = True
bpy.data.objects["Cabeca"].users_collection[0].objects.link(rig)
for o in bpy.context.view_layer.objects:
    o.select_set(False)
rig.select_set(True); bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="EDIT")
for nome, ini, fim, pai, deforma in OSSOS:
    b = arm.edit_bones.new(nome)
    b.head, b.tail, b.roll = Vector(ini), Vector(fim), 0.0
    b.use_deform = deforma
    if pai:
        b.parent = arm.edit_bones[pai]
        b.use_connect = (b.parent.tail - b.head).length < 1e-9
bpy.ops.object.mode_set(mode="OBJECT")

# 4. pesos rígidos e modificador Armature (Cabeca -> Head_Bone, Corpo_Kart -> Torso_Bone)
for nome, osso in (("Cabeca", "Head_Bone"), ("Corpo_Kart", "Torso_Bone")):
    o = bpy.data.objects[nome]
    g = o.vertex_groups.new(name=osso)
    g.add(list(range(len(o.data.vertices))), 1.0, "REPLACE")
    mw = o.matrix_world.copy()
    o.parent = rig
    o.matrix_parent_inverse = rig.matrix_world.inverted()
    o.matrix_world = mw
    mod = o.modifiers.new("Rig_Rigido_Sem_Deformacao", "ARMATURE")
    mod.object = rig
    mod.use_vertex_groups, mod.use_bone_envelopes, mod.use_deform_preserve_volume = True, False, False

# 5. rodas: parentesco direto com Torso_Bone, compensando a matriz do osso (sem modificador)
for n in RODAS:
    o = bpy.data.objects[n]
    base = o.matrix_basis.copy()
    o.parent, o.parent_type, o.parent_bone = rig, "BONE", "Torso_Bone"
    o.matrix_parent_inverse = Matrix.Identity(4)
    bpy.context.view_layer.update()
    pai = o.matrix_world @ o.matrix_basis.inverted()  # matriz do osso (cauda) no mundo
    o.matrix_parent_inverse = pai.inverted()
    o.matrix_basis = base
bpy.context.view_layer.update()
result = {"rig": rig.name, "ossos": [(b.name, list(b.head_local), list(b.tail_local)) for b in arm.bones],
          "origens": {n: list(bpy.data.objects[n].matrix_world.translation) for n in PARTES}}
