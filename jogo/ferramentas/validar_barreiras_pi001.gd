extends SceneTree
## Física real, 60 Hz: o kart acelera contra as barreiras da PI001 (retas e curvas, dois lados)
## e as cinco IAs completam uma volta. Saída própria; não toca os relatórios da integração.
const BASE := "res://../pistas/PI001_primeira_pista/validacao/barreiras_20261017/"
const LIMITE := 5.13 - 0.3  # face da barreira, medida do eixo
var rel: Dictionary = {"metodo": "Godot real, Input e CharacterBody3D; kart posicionado no eixo e acelerado contra a borda", "impactos": [], "adversarios": []}


func _initialize() -> void:
	call_deferred("_executar")


func passos(n: int) -> void:
	for i in n:
		await physics_frame


func distancia_eixo(eixo: Path3D, p: Vector3) -> float:
	var q := eixo.curve.get_closest_point(p)
	return Vector2(p.x - q.x, p.z - q.z).length()


func _executar() -> void:
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(BASE))
	var jogo := root.get_node("Jogo")
	jogo.quantidade_adversarios = 0
	var pista: Node = load("res://pistas/primeira_pista/primeira_pista.tscn").instantiate()
	root.add_child(pista)
	current_scene = pista
	await passos(10)
	var kart: Kart = pista.get_node("Kart")
	var eixo: PercursoPI001 = pista.get_node("Percurso")
	var total := eixo.curve.get_baked_length()
	rel.modulos = pista.get_node("Barreiras/Colisao").get_child_count()
	# 24 pontos ao longo da volta, dois lados, ataque a 90° e a 35° da tangente.
	for k in 24:
		var d := total * (k + 0.5) / 24.0
		for lado: float in [-1.0, 1.0]:
			for angulo: float in [90.0, 35.0]:
				var frente := eixo.tangente(d)
				var normal := frente.cross(Vector3.UP) * lado
				var rumo: Vector3 = frente.rotated(Vector3.UP, -deg_to_rad(angulo) * lado) if angulo < 90.0 else normal
				kart.transform = Transform3D(Basis.looking_at(rumo), eixo.ponto(d) + Vector3.UP * 0.04)
				kart.velocity = Vector3.ZERO
				kart.velocidade = 0.0
				kart.empurrao = Vector3.ZERO
				kart.rodada = 0.0
				await passos(2)
				var maior := 0.0
				var vel_max := 0.0
				Input.action_press("acelerar")
				for i in 240:
					await physics_frame
					maior = maxf(maior, distancia_eixo(eixo, kart.global_position))
					vel_max = maxf(vel_max, absf(kart.velocidade))
				Input.action_release("acelerar")
				rel.impactos.append({"distancia_m": d, "lado": lado, "angulo": angulo, "maior_afastamento_m": maior,
					"velocidade_max": vel_max, "posicao_final": str(kart.global_position), "contido": maior < LIMITE + 0.05})
	var contidos := 0
	var pior := 0.0
	for r in rel.impactos:
		contidos += int(r.contido)
		pior = maxf(pior, r.maior_afastamento_m)
	rel.impactos_contidos = "%d/%d" % [contidos, rel.impactos.size()]
	rel.maior_afastamento_m = pior
	pista.free()
	current_scene = null

	jogo.quantidade_adversarios = 5
	pista = load("res://pistas/primeira_pista/primeira_pista.tscn").instantiate()
	root.add_child(pista)
	current_scene = pista
	eixo = pista.get_node("Percurso")
	var medidas: Array[Dictionary] = []
	for ia in pista.adversarios:
		medidas.append({"nome": ia.name, "desvio_max_m": 0.0, "quadros_fora_asfalto": 0, "volta_segundos": -1.0})
	for quadro in 60 * 180:
		await physics_frame
		var todos := true
		for i in pista.adversarios.size():
			var ia: KartIA = pista.adversarios[i]
			var m: Dictionary = medidas[i]
			m.desvio_max_m = maxf(m.desvio_max_m, ia.desvio_percurso)
			if ia.desvio_percurso > 4.0: m.quadros_fora_asfalto += 1
			if ia.distancia_percorrida >= total and m.volta_segundos < 0.0: m.volta_segundos = (quadro + 1) / 60.0
			todos = todos and m.volta_segundos > 0.0
		if todos: break
	rel.adversarios = medidas
	rel.aprovado_impactos = contidos == rel.impactos.size()
	rel.aprovado_voltas = true
	for m in medidas:
		rel.aprovado_voltas = rel.aprovado_voltas and m.volta_segundos > 0.0 and m.quadros_fora_asfalto == 0
	FileAccess.open(BASE + "validacao_barreiras.json", FileAccess.WRITE).store_string(JSON.stringify(rel, "\t"))
	print("BARREIRAS ", rel.impactos_contidos, " maior=", pior, " modulos=", rel.modulos)
	print("VOLTAS ", JSON.stringify(medidas))
	pista.free()
	current_scene = null
	quit(0 if rel.aprovado_impactos and rel.aprovado_voltas else 2)
