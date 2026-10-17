extends SceneTree
## Fase 7 do P003 — inspeciona o GLB do Bryan importado pela Godot e compara com o Blender.
## Adaptado de inspecionar_importacao_dimi.gd: só as constantes (medidas no bryan.blend) e o nome mudam.
## Não altera cenas, fichas nem o catálogo; a ficha usada no teste de montagem existe só na memória.
## godot --headless --path jogo --script res://ferramentas/inspecionar_importacao_bryan.gd

const MODELO := "res://personagens/bryan/bryan_kart.glb"
const DESTINO := "res://../personagens/P003_bryan/validacao/importacao_godot_fase7.json"
const TOL := 1e-5
const AMPLITUDE := 25.0
const OSSOS := ["Root_Bone", "Torso_Bone", "Neck_Bone", "Head_Bone"]
const RODAS := ["Wheel_Front_Left", "Wheel_Front_Right", "Wheel_Rear_Left", "Wheel_Rear_Right"]
## Valores do bryan.blend (SHA-256 b25be23b…), em metros, já convertidos de Blender (x, y, z) para glTF (x, z, -y).
const CABECAS_OSSOS := {
	"Root_Bone": Vector3(0, 0.08056640625, 0),
	"Torso_Bone": Vector3(0, 0.25, 0),
	"Neck_Bone": Vector3(-0.007568359375, 0.4375, -0.0712890625),
	"Head_Bone": Vector3(-0.007568359375, 0.494140625, -0.0712890625),
}
const ORIGENS_RODAS := {
	"Wheel_Front_Left": Vector3(0.2602539360523224, 0.1193847730755806, 0.269287109375),
	"Wheel_Front_Right": Vector3(-0.260009765625, 0.11987302452325821, 0.26953125),
	"Wheel_Rear_Left": Vector3(0.259765625, 0.12036135047674179, -0.29443359375),
	"Wheel_Rear_Right": Vector3(-0.259521484375, 0.1203613206744194, -0.29443359375),
}
## Contagens do Blender: triângulos por objeto (a Godot duplica vértices nas costuras de UV e normais).
const TRIANGULOS := {"Cabeca": 80608, "Corpo_Kart": 1439415, "Wheel_Front_Left": 80611,
	"Wheel_Front_Right": 81386, "Wheel_Rear_Left": 87392, "Wheel_Rear_Right": 85189}
## Raio medido na Fase 4 (setores a até 2 mm da mediana da metade de baixo), por roda.
const RAIO_MEDIDO := {"Wheel_Front_Left": 0.11926, "Wheel_Front_Right": 0.11948,
	"Wheel_Rear_Left": 0.11982, "Wheel_Rear_Right": 0.11991}

func _initialize() -> void:
	call_deferred("_executar")


func _v(v: Vector3) -> Array:
	return [v.x, v.y, v.z]


func _executar() -> void:
	var r := {"modelo": MODELO, "godot": Engine.get_version_info().string, "tolerancia_m": TOL}
	var ok := true
	var cena := load(MODELO) as PackedScene
	var modelo := cena.instantiate() as Node3D
	root.add_child(modelo)
	await process_frame

	var arvore: Array = []
	for n in [modelo] + modelo.find_children("*", "", true, false):
		arvore.append({"caminho": str(modelo.get_path_to(n)), "classe": n.get_class()})
	r["arvore"] = arvore

	var esqueletos := modelo.find_children("*", "Skeleton3D", true, false)
	var esq := esqueletos[0] as Skeleton3D
	esq.force_update_all_bone_transforms()
	var ossos := {}
	var desvio_ossos := 0.0
	for i in esq.get_bone_count():
		var nome := esq.get_bone_name(i)
		var origem := modelo.global_transform.affine_inverse() * (esq.global_transform * esq.get_bone_global_rest(i).origin)
		var esperado: Vector3 = CABECAS_OSSOS.get(nome, Vector3.INF)
		var desvio := origem.distance_to(esperado)
		desvio_ossos = maxf(desvio_ossos, desvio)
		var pai := esq.get_bone_parent(i)
		ossos[nome] = {"indice": i, "pai": esq.get_bone_name(pai) if pai >= 0 else "", "origem_modelo": _v(origem),
			"desvio_do_blender": desvio, "pose_igual_repouso": esq.get_bone_pose(i).is_equal_approx(esq.get_bone_rest(i))}
	r["esqueletos"] = esqueletos.size()
	r["ossos"] = ossos
	var hierarquia_ok := esq.get_bone_count() == 4
	for i in range(1, OSSOS.size()):
		hierarquia_ok = hierarquia_ok and ossos.has(OSSOS[i]) and ossos[OSSOS[i]].pai == OSSOS[i - 1]
	r["hierarquia_ok"] = hierarquia_ok and ossos.has("Root_Bone") and ossos["Root_Bone"].pai == ""
	r["ossos_desvio_max"] = desvio_ossos
	ok = ok and esqueletos.size() == 1 and r["hierarquia_ok"] and desvio_ossos <= TOL

	var malhas := {}
	var triangulos_total := 0
	for mi in modelo.find_children("*", "MeshInstance3D", true, false):
		var m := mi as MeshInstance3D
		var tri := 0
		var vert := 0
		var materiais: Array = []
		for s in m.mesh.get_surface_count():
			var arr := m.mesh.surface_get_arrays(s)
			vert += (arr[Mesh.ARRAY_VERTEX] as PackedVector3Array).size()
			tri += (arr[Mesh.ARRAY_INDEX] as PackedInt32Array).size() / 3
			var mat := m.get_active_material(s) as StandardMaterial3D
			materiais.append({"classe": mat.get_class(), "nome": mat.resource_name,
				"albedo": mat.albedo_texture.resource_path if mat.albedo_texture else "",
				"normal": mat.normal_texture.resource_path if mat.normal_texture and mat.normal_enabled else "",
				"metallic": mat.metallic_texture.resource_path if mat.metallic_texture else "",
				"roughness": mat.roughness_texture.resource_path if mat.roughness_texture else ""})
		triangulos_total += tri
		var origem := modelo.global_transform.affine_inverse() * m.global_position
		var aabb := m.get_aabb()
		var info := {"pai": str(modelo.get_path_to(m.get_parent())), "classe_pai": m.get_parent().get_class(),
			"skin": m.skin != null, "vertices_godot": vert, "triangulos": tri, "triangulos_blender": TRIANGULOS.get(m.name, -1),
			"origem_modelo": _v(origem), "aabb_tamanho": _v(aabb.size), "materiais": materiais}
		if ORIGENS_RODAS.has(m.name):
			info["desvio_origem_do_blender"] = origem.distance_to(ORIGENS_RODAS[m.name])
			# mesmo cálculo de visual_kart.gd
			info["raio_visual_kart"] = maxf(aabb.size.y, aabb.size.z) * 0.5
		malhas[m.name] = info
		ok = ok and tri == TRIANGULOS.get(m.name, -1) and materiais.size() == 1 and materiais[0].albedo != "" \
			and materiais[0].normal != "" and materiais[0].roughness != ""
	r["malhas"] = malhas
	r["triangulos_total"] = triangulos_total
	var partes_ok := malhas.size() == 6 and malhas.has("Cabeca") and malhas.has("Corpo_Kart")
	for n in RODAS:
		partes_ok = partes_ok and malhas.has(n) and not malhas[n].skin and malhas[n].classe_pai == "BoneAttachment3D" \
			and malhas[n].desvio_origem_do_blender <= TOL
	partes_ok = partes_ok and malhas["Cabeca"].skin and malhas["Corpo_Kart"].skin
	r["partes_ok"] = partes_ok
	ok = ok and partes_ok

	# Ações da cabeça: só Head_Bone gira, em torno de Y (= Z do Blender); direita do piloto = negativo.
	var anims := {}
	var players := modelo.find_children("*", "AnimationPlayer", true, false)
	var anim_ok := players.size() == 1
	if anim_ok:
		var ap := players[0] as AnimationPlayer
		r["autoplay"] = ap.autoplay
		anim_ok = ap.autoplay == ""
		for nome in ap.get_animation_list():
			var a := ap.get_animation(nome)
			var trilhas: Array = []
			var amostras: Array = []
			for t in a.get_track_count():
				trilhas.append({"caminho": str(a.track_get_path(t)), "tipo": a.track_get_type(t), "chaves": a.track_get_key_count(t)})
				if str(a.track_get_path(t)).ends_with(":Head_Bone") and a.track_get_type(t) == Animation.TYPE_ROTATION_3D:
					for q in range(0, 9):
						var tempo := a.length * q / 8.0
						var rot := a.rotation_track_interpolate(t, tempo)
						var euler := rot.get_euler()
						amostras.append({"segundos": tempo, "y_graus": rad_to_deg(euler.y), "x_graus": rad_to_deg(euler.x), "z_graus": rad_to_deg(euler.z)})
			anims[nome] = {"duracao": a.length, "loop": a.loop_mode, "trilhas": trilhas, "cabeca": amostras}
		var esperado := {"Cabeca_Direita_Ida_e_Volta": -1.0, "Cabeca_Esquerda_Ida_e_Volta": 1.0}
		for nome in esperado:
			var sinal: float = esperado[nome]
			if not anims.has(nome):
				anim_ok = false
				continue
			var am: Array = anims[nome].cabeca
			anim_ok = anim_ok and absf(anims[nome].duracao - 2.0) < 1e-4 and am.size() == 9 and anims[nome].trilhas.size() == 1 \
				and absf(am[0].y_graus) < 1e-3 and absf(am[4].y_graus - sinal * AMPLITUDE) < 1e-3 and absf(am[8].y_graus) < 1e-3
			for s in am:
				anim_ok = anim_ok and absf(s.x_graus) < 1e-3 and absf(s.z_graus) < 1e-3
	r["animacoes"] = anims
	r["animacoes_ok"] = anim_ok
	ok = ok and anim_ok
	modelo.queue_free()

	# Montagem com o código real do jogo, com uma ficha só em memória (sem catálogo).
	var ficha := DefinicaoPersonagem.new()
	ficha.nome = "Bryan"
	ficha.modelo = cena
	var visual := VisualKart.new()
	root.add_child(visual)
	visual.montar(ficha)
	await process_frame
	var rodas: Array = []
	for roda in visual._rodas:
		rodas.append({"roda": roda.malha.name, "raio": roda.raio, "dianteira": roda.dianteira})
	var montagem := {"osso_corpo": visual._osso_corpo, "osso_cabeca": visual._osso_cabeca, "rodas": rodas,
		"raio_medido_fase4": RAIO_MEDIDO}
	montagem["ok"] = visual._osso_corpo >= 0 and visual._osso_cabeca >= 0 and rodas.size() == 4
	r["montagem_visual_kart"] = montagem
	ok = ok and montagem.ok
	visual.queue_free()

	r["tudo_ok"] = ok
	var f := FileAccess.open(DESTINO, FileAccess.WRITE)
	f.store_string(JSON.stringify(r, "\t"))
	f.close()
	print("tudo_ok=", ok, " -> ", ProjectSettings.globalize_path(DESTINO))
	quit(0)
