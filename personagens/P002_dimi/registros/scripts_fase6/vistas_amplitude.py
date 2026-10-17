"""Fase 6 — escolha da amplitude do giro da cabeça (Y local de Head_Bone = Z mundial).
Para cada ângulo, renderiza vistas do pescoço e mede, por uma grade de raios paralelos de cada direção de câmera,
quantos raios atingem primeiro uma face interna (voltada para longe da câmera) da Cabeca ou do Corpo_Kart.
Altera pose e cena só para medir/renderizar; depois desfazer com bpy.ops.wm.revert_mainfile() (o script não salva).
Uso no MCP: SAIDA_DIR, SAIDA_JSON, RENDER (bool) e, opcionalmente, SO_ANGULOS e SO_VISTAS; exec(open(<este arquivo>).read())"""
import bpy, math, json
import numpy as np
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ANGULOS = globals().get("SO_ANGULOS") or (0, 10, -10, 15, -15, 20, -20, 25, -25, 30, -30, 35, -35, 40, -40)
# direções do alvo para a câmera (frente do piloto = -Y, esquerda = +X); câmera do jogo: atrás 3.4, acima 1.4
VISTAS = {"lado_esq": Vector((3, 0, 0.2)), "lado_dir": Vector((-3, 0, 0.2)), "frente": Vector((0, -3, 0.3)),
          "jogo": Vector((0, 3.4, 1.4)), "jogo_curva_esq": Vector((1.5, 3.1, 1.4)), "jogo_curva_dir": Vector((-1.5, 3.1, 1.4))}
RENDER_VISTAS = globals().get("SO_VISTAS") or ("lado_esq", "lado_dir", "jogo")

sc = bpy.context.scene
rig = bpy.data.objects["Personagem_Rig"]; head = rig.pose.bones["Head_Bone"]
cab = bpy.data.objects["Cabeca"]; corpo = bpy.data.objects["Corpo_Kart"]

GRADE = 160          # raios por lado da janela
JANELA = 0.22        # m, quadrado centrado no pivô da cabeça + 3 cm em Z (pescoço e gola)

dg = bpy.context.evaluated_depsgraph_get(); dg.update()
bvh_corpo = BVHTree.FromObject(corpo, dg)  # Corpo_Kart: matriz identidade, pose de repouso
t_cab = cab.matrix_world.translation.copy()
alvo = Vector(rig.data.bones["Head_Bone"].head_local) + Vector((0, 0, 0.03))


def medir():
    """Para cada vista: raios paralelos (câmera ortográfica) numa grade sobre o pescoço. Conta o primeiro impacto
    em face voltada para longe da câmera (interior visível), separado por objeto."""
    dg.update()
    bvh_cab = BVHTree.FromObject(cab, dg)  # local da Cabeca = mundo - t_cab (o objeto só tem translação)
    res = {}
    for nome, d in VISTAS.items():
        d = d.normalized(); u = d.cross(Vector((0, 0, 1)))
        u = u.normalized() if u.length > 1e-6 else Vector((1, 0, 0)); w = u.cross(d).normalized()
        c = {"raios": 0, "cabeca_frente": 0, "cabeca_interior": 0, "corpo_frente": 0, "corpo_interior": 0, "vazio": 0}
        for i in range(GRADE):
            for j in range(GRADE):
                o = alvo + d * 2 + u * ((i + 0.5) / GRADE - 0.5) * JANELA + w * ((j + 0.5) / GRADE - 0.5) * JANELA
                hc = bvh_cab.ray_cast(o - t_cab, -d); hb = bvh_corpo.ray_cast(o, -d)
                c["raios"] += 1
                dc = hc[3] if hc[0] is not None else math.inf; db = hb[3] if hb[0] is not None else math.inf
                if dc == db == math.inf: c["vazio"] += 1; continue
                n, k = (hc[1], "cabeca") if dc <= db else (hb[1], "corpo")
                c[k + ("_frente" if n.dot(d) > 0 else "_interior")] += 1
        res[nome] = c
    return res


def foto(nome, centro, direcao, escala=0.45):
    cd.ortho_scale = escala
    cam.location = centro + direcao
    cam.rotation_euler = (-direcao).to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()
    sc.render.filepath = f"{SAIDA_DIR}/{nome}.png"
    bpy.ops.render.render(write_still=True)


if RENDER:
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.display.shading.light = "STUDIO"; sc.display.shading.color_type = "TEXTURE"
    sc.render.resolution_x = sc.render.resolution_y = 700; sc.render.film_transparent = False
    cd = bpy.data.cameras.new("cam_conferencia"); cd.type = "ORTHO"; cd.clip_end = 20
    cam = bpy.data.objects.new("cam_conferencia", cd); sc.collection.objects.link(cam); sc.camera = cam
    rig.hide_render = True
pescoco = Vector(rig.data.bones["Head_Bone"].head_local) + Vector((0, 0, 0.06))

r = {"grade": GRADE, "janela_m": JANELA, "alvo": list(alvo), "vistas": {k: list(v) for k, v in VISTAS.items()}, "angulos": {}}
pose0 = head.matrix_basis.copy()
try:
    for a in ANGULOS:
        head.matrix_basis = Matrix.Rotation(math.radians(a), 4, "Y"); bpy.context.view_layer.update()
        r["angulos"][str(a)] = medir()
        if RENDER:
            for v in RENDER_VISTAS:
                foto(f"giro_{a:+d}_{v}", pescoco, VISTAS[v])
finally:
    head.matrix_basis = pose0; bpy.context.view_layer.update()
json.dump(r, open(SAIDA_JSON, "w"), ensure_ascii=False, indent=1)
result = r
