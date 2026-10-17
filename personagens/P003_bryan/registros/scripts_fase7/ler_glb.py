"""Fase 7 — lê o GLB exportado e resume nós, skin, triângulos, imagens e animações. Uso: python3 ler_glb.py <glb>"""
import json, struct, sys, hashlib, math
d = open(sys.argv[1], "rb").read()
jl = struct.unpack_from("<I", d, 12)[0]
j = json.loads(d[20:20 + jl])
binoff = 20 + jl + 8
def acc(i):
    a = j["accessors"][i]; bv = j["bufferViews"][a["bufferView"]]
    n = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}[a["type"]]
    fmt = {5126: "f", 5125: "I", 5123: "H"}[a["componentType"]]
    o = binoff + bv.get("byteOffset", 0) + a.get("byteOffset", 0)
    v = struct.unpack_from("<%d%s" % (a["count"] * n, fmt), d, o)
    return [v[k:k + n] for k in range(0, len(v), n)] if n > 1 else list(v)
nos = [{"nome": n["name"], "filhos": [j["nodes"][c]["name"] for c in n.get("children", [])],
        "malha": "mesh" in n, "skin": "skin" in n, "t": n.get("translation")} for n in j["nodes"]]
tri = {}
for n in j["nodes"]:
    if "mesh" in n:
        tri[n["name"]] = sum(j["accessors"][p["indices"]]["count"] // 3 for p in j["meshes"][n["mesh"]]["primitives"])
imgs = {}
for im in j.get("images", []):
    bv = j["bufferViews"][im["bufferView"]]; o = binoff + bv.get("byteOffset", 0)
    imgs[im["name"]] = hashlib.sha256(d[o:o + bv["byteLength"]]).hexdigest()
anims = {}
for a in j.get("animations", []):
    canais = []
    for c in a["channels"]:
        s = a["samplers"][c["sampler"]]; t = acc(s["input"]); v = acc(s["output"])
        alvo = j["nodes"][c["target"]["node"]]["name"] + "." + c["target"]["path"]
        info = {"alvo": alvo, "interp": s.get("interpolation", "LINEAR"), "chaves": len(t), "t": [t[0], t[-1]]}
        if alvo == "Head_Bone.rotation":
            # ângulo em Y (quaternion x,y,z,w) no meio e nas pontas
            ang = lambda q: math.degrees(2 * math.atan2(q[1], q[3]))
            info["y_graus"] = [ang(v[0]), ang(v[len(v) // 2]), ang(v[-1])]
            info["xz_max"] = max(max(abs(q[0]), abs(q[2])) for q in v)
        canais.append(info)
    anims[a["name"]] = canais
print(json.dumps({"bytes": len(d), "sha256": hashlib.sha256(d).hexdigest(), "asset": j["asset"], "nos": nos,
  "skins": [{"nome": s.get("name"), "juntas": [j["nodes"][k]["name"] for k in s["joints"]]} for s in j.get("skins", [])],
  "triangulos": tri, "triangulos_total": sum(tri.values()), "materiais": [m["name"] for m in j["materials"]],
  "imagens_sha256": imgs, "animacoes": anims}, indent=1, ensure_ascii=False))
