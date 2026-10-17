"""Fase 3 — restaura custom_normal (INT16_2D), sharp_edge e sharp_face de cada parte a partir do backup pré-Fase 3,
via rig_original_corner/edge/face. A passagem pelo modo de edição recodifica as normais personalizadas e, no Bryan,
marcou 3 arestas do corpo como sharp (faces quase degeneradas da ilha 257); topologia e posições não mudam.
Executar na sessão aberta pelo Blender MCP definindo BACKUP antes de exec(). Remove tudo o que anexar do backup."""
import bpy, numpy as np
antes = {c: set(getattr(bpy.data, c)) for c in ("meshes", "materials", "images")}
with bpy.data.libraries.load(BACKUP) as (s, d): d.meshes = list(s.meshes)
rm = d.meshes[0]; ref = np.empty(len(rm.loops)*2, np.int16); rm.attributes["custom_normal"].data.foreach_get("value", ref); ref = ref.reshape(-1, 2)
se0 = np.zeros(len(rm.edges), bool); rm.attributes["sharp_edge"].data.foreach_get("value", se0)
sf0 = np.zeros(len(rm.polygons), bool); rm.attributes["sharp_face"].data.foreach_get("value", sf0)
rest = {}; sharp = {}
for o in [x for x in bpy.data.objects if x.type == "MESH" and not x.library]:
    m = o.data; nl = len(m.loops)
    ol = np.empty(nl, np.int32); m.attributes["rig_original_corner"].data.foreach_get("value", ol)
    cur = np.empty(nl*2, np.int16); m.attributes["custom_normal"].data.foreach_get("value", cur)
    rest[o.name] = int((cur.reshape(-1, 2) != ref[ol]).any(1).sum())
    m.attributes["custom_normal"].data.foreach_set("value", ref[ol].ravel())
    for nome, ref_b, dom, attr in (("sharp_edge", se0, m.edges, "rig_original_edge"), ("sharp_face", sf0, m.polygons, "rig_original_face")):
        oi = np.empty(len(dom), np.int32); m.attributes[attr].data.foreach_get("value", oi)
        alvo = ref_b[oi]; atual = np.zeros(len(dom), bool)
        if nome in m.attributes: m.attributes[nome].data.foreach_get("value", atual)
        sharp[f"{o.name}.{nome}"] = int((atual != alvo).sum())
        if (atual != alvo).any():
            if nome not in m.attributes: m.attributes.new(nome, "BOOLEAN", "EDGE" if nome == "sharp_edge" else "FACE")
            m.attributes[nome].data.foreach_set("value", alvo)
    m.update()
for c in ("meshes", "materials", "images"):
    for x in [x for x in getattr(bpy.data, c) if x not in antes[c]]: getattr(bpy.data, c).remove(x)
res = {"cantos_diferentes_antes": rest, "sharp_diferentes_antes": {k: v for k, v in sharp.items() if v},
       "sobras": {c: [x.name for x in getattr(bpy.data, c) if x not in antes[c]] for c in ("meshes", "materials", "images")}}

# Cantos na costura (vértices duplicados ao dividir ilhas por faces): o código INT16 original é relativo ao
# espaço de normais do vértice inteiro e decodifica outra direção depois da divisão. Para esses cantos, e só
# para eles, o código é refeito a partir do vetor original do NPZ (corner_normals) com normals_split_custom_set;
# os demais cantos mantêm o código original do backup (decodificação exata).
# normals_split_custom_set marca como sharp as 3 arestas das faces quase degeneradas do corpo; por isso sharp_edge
# e sharp_face são restaurados de novo ao fim, a partir do backup, e só então a decodificação é medida.
# Chamar regravar_costura(NPZ, PARTES) depois do bloco acima.
def regravar_costura(NPZ, PARTES):
    cn0 = np.load(NPZ)["corner_normals"]; out = {}
    for nome in PARTES:
        m = bpy.data.objects[nome].data; nl = len(m.loops)
        ol = np.empty(nl, np.int32); m.attributes["rig_original_corner"].data.foreach_get("value", ol)
        def decod():
            cn = np.empty(nl*3, np.float32); m.corner_normals.foreach_get("vector", cn)
            return np.abs(cn.reshape(-1, 3)-cn0[ol]).max(1)
        orig = np.empty(nl*2, np.int16); m.attributes["custom_normal"].data.foreach_get("value", orig); orig = orig.reshape(-1, 2)
        d0 = decod(); costura = d0 > 0
        m.normals_split_custom_set([tuple(v) for v in cn0[ol]]); m.update()
        novo = np.empty(nl*2, np.int16); m.attributes["custom_normal"].data.foreach_get("value", novo); novo = novo.reshape(-1, 2)
        final = np.where(costura[:, None], novo, orig)
        m.attributes["custom_normal"].data.foreach_set("value", final.ravel())
        oe = np.empty(len(m.edges), np.int32); m.attributes["rig_original_edge"].data.foreach_get("value", oe)
        of = np.empty(len(m.polygons), np.int32); m.attributes["rig_original_face"].data.foreach_get("value", of)
        se = np.zeros(len(m.edges), bool); m.attributes["sharp_edge"].data.foreach_get("value", se)
        sharp_refeitas = int((se != se0[oe]).sum())
        m.attributes["sharp_edge"].data.foreach_set("value", se0[oe])
        if "sharp_face" in m.attributes: m.attributes["sharp_face"].data.foreach_set("value", sf0[of])
        m.update()
        d = decod()
        out[nome] = {"cantos_costura": int(costura.sum()), "sharp_edge_restauradas_apos_recodificar": sharp_refeitas, "desvio_max_costura_antes": float(d0.max()),
                     "desvio_max_final": float(d.max()), "desvio_max_fora_da_costura": float(d[~costura].max()),
                     "cantos_final_>1e-6": int((d > 1e-6).sum())}
    return out
