"""Fase 5 (P003 Bryan) — mede a exposição da borda aberta da nuca para cada rotação do Head_Bone e propõe a amplitude segura.
Decisão do usuário (16/10/2026): limitar a amplitude em vez de criar tampa. Não altera geometria nem salva.
Uso no MCP: SAIDA = "<json>"; exec(open(<este arquivo>).read())
Método: vértices de borda (arestas com uma face) da Cabeca até ALTURA_NUCA acima do pivô. Para cada pose, raio de cada ponto
de vista até cada vértice; o vértice está visível se nada (Corpo_Kart ou a própria Cabeca posada) o cobre antes de chegar.
Conta-se só o que fica visível na pose e não estava visível no repouso, pelo mesmo ponto de vista ("novos expostos").
A transformação da cabeça vem do osso posado de fato (pb.matrix); a Fase 4 já mediu que a Cabeca segue o osso rigidamente."""
import bpy, bmesh, numpy as np, json, math
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree

ALTURA_NUCA = 0.04       # m acima do pivô da cabeça
DIST_VISTA = 2.5         # m do centro do pescoço
AZIMUTES = range(0, 360, 30)   # 0 = atrás (+Y), 90 = esquerda do piloto (+X), 180 = frente
ELEVACOES = (10, 30, 50)
EPS = 1e-4               # m antes do vértice
POSES = ([("Y", g) for g in (5, 10, 15, 20, 25, 30, 35, 40, -5, -10, -15, -20, -25, -30, -35, -40)]
         + [("X", g) for g in (5, 10, 15, 20, -5, -10, -15, -20)] + [("Z", g) for g in (5, 10, 15, -5, -10, -15)])

dg = bpy.context.evaluated_depsgraph_get()
rig = bpy.data.objects["Personagem_Rig"]; pb = rig.pose.bones["Head_Bone"]
cab = bpy.data.objects["Cabeca"]


def malha(o, mundo):
    e = o.evaluated_get(dg); m = e.to_mesh()
    co = np.empty(len(m.vertices) * 3, np.float32); m.vertices.foreach_get("co", co); co = co.reshape(-1, 3).astype(np.float64)
    if mundo:
        mw = np.array(e.matrix_world); co = co @ mw[:3, :3].T + mw[:3, 3]
    m.calc_loop_triangles()
    tri = np.empty(len(m.loop_triangles) * 3, np.int32); m.loop_triangles.foreach_get("vertices", tri)
    e.to_mesh_clear()
    return co, tri.reshape(-1, 3)


co_c, tri_c = malha(bpy.data.objects["Corpo_Kart"], True)
arv_corpo = BVHTree.FromPolygons(co_c.tolist(), tri_c.tolist(), epsilon=0.0)
co_h, tri_h = malha(cab, False)
arv_cab = BVHTree.FromPolygons(co_h.tolist(), tri_h.tolist(), epsilon=0.0)  # espaço local da Cabeca

bm = bmesh.new(); bm.from_mesh(cab.data)
borda = sorted({v.index for e in bm.edges if len(e.link_faces) < 2 for v in e.verts}); bm.free()
mw0 = cab.matrix_world.copy()
piv = Vector(rig.data.bones["Head_Bone"].head_local)
loc = [Vector(co_h[i]) for i in borda]
nuca = [i for i, p in zip(borda, loc) if (mw0 @ p).z < piv.z + ALTURA_NUCA]
p_loc = [Vector(co_h[i]) for i in nuca]
centro = piv + Vector((0, 0, 0.06))
vistas = []
for el in ELEVACOES:
    for az in AZIMUTES:
        a, e = math.radians(az), math.radians(el)
        vistas.append((az, el, centro + DIST_VISTA * Vector((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e)))))


def visiveis(M_cab):
    """matriz booleana [vista, vértice] para a Cabeca com matriz mundial M_cab"""
    inv = M_cab.inverted(); R = inv.to_3x3()
    vis = np.zeros((len(vistas), len(p_loc)), bool)
    pw = [M_cab @ p for p in p_loc]
    for k, (_, _, c) in enumerate(vistas):
        c_loc = inv @ c
        for j, p in enumerate(pw):
            d = p - c; dist = d.length; d.normalize()
            if arv_corpo.ray_cast(c, d, dist - EPS)[0] is not None:
                continue
            if arv_cab.ray_cast(c_loc, (R @ d).normalized(), dist - EPS)[0] is not None:
                continue
            vis[k, j] = True
    return vis


def M_osso():
    bpy.context.view_layer.update()
    return rig.matrix_world @ pb.matrix @ pb.bone.matrix_local.inverted() @ rig.matrix_world.inverted()


base0 = pb.matrix_basis.copy(); modo0 = pb.rotation_mode
r = {"arquivo": bpy.data.filepath, "parametros": {"altura_nuca_m": ALTURA_NUCA, "dist_vista_m": DIST_VISTA, "azimutes": list(AZIMUTES),
     "elevacoes": list(ELEVACOES), "eps_m": EPS, "azimute_0": "atrás (+Y)", "azimute_90": "esquerda do piloto (+X)"},
     "vertices_borda_cabeca": len(borda), "vertices_borda_nuca": len(nuca), "vistas": len(vistas), "poses": {}}
try:
    rep = visiveis(M_osso() @ mw0)
    r["repouso_visiveis_pares"] = int(rep.sum()); r["repouso_vertices_visiveis"] = int(rep.any(0).sum())
    for eixo, g in POSES:
        pb.rotation_mode = "XYZ"; pb.matrix_basis = Matrix.Rotation(math.radians(g), 4, eixo)
        v = visiveis(M_osso() @ mw0); novo = v & ~rep
        por_vista = novo.sum(1)
        r["poses"][f"{eixo}{g:+d}"] = {
            "novos_pares": int(novo.sum()), "novos_vertices": int(novo.any(0).sum()),
            "vistas_com_exposicao": [[vistas[k][0], vistas[k][1], int(por_vista[k])] for k in np.nonzero(por_vista)[0]],
            "novos_vertices_vistas_traseiras": int(novo[[k for k, x in enumerate(vistas) if x[0] in (0, 30, 330)]].any(0).sum())}
        pb.matrix_basis = base0
finally:
    pb.matrix_basis = base0; pb.rotation_mode = modo0; bpy.context.view_layer.update()
r["pose_restaurada"] = pb.matrix_basis == Matrix.Identity(4)
json.dump(r, open(SAIDA, "w"), ensure_ascii=False, indent=1)
result = {"nuca": len(nuca), "repouso": r["repouso_vertices_visiveis"], "restaurada": r["pose_restaurada"],
          "poses": {k: (p["novos_vertices"], p["novos_vertices_vistas_traseiras"]) for k, p in r["poses"].items()}}
