extends SceneTree
const BASE := "res://../pistas/PI001_primeira_pista/validacao/integracao_20261016/"
var rel: Dictionary = {"contato_pneus": [], "colisoes_karts": []}

func _initialize() -> void:
	call_deferred("_executar")

func _passos(n: int) -> void:
	for i in n: await physics_frame

func _executar() -> void:
	var jogo := root.get_node("Jogo")
	jogo.quantidade_adversarios = 0
	for i in jogo.personagens.size():
		jogo.indice_escolhido = i
		var pista = load("res://pistas/primeira_pista/primeira_pista.tscn").instantiate()
		root.add_child(pista)
		current_scene = pista
		var kart: Kart = pista.get_node("Kart")
		await _passos(30)
		var rodas: Array[Dictionary] = []
		for roda in kart.visual._rodas:
			var mi: MeshInstance3D = roda.malha
			var min_y := INF
			for s in mi.mesh.get_surface_count():
				var arrays := mi.mesh.surface_get_arrays(s)
				for v in arrays[Mesh.ARRAY_VERTEX]: min_y = minf(min_y, (mi.global_transform * v).y)
			var centro: Vector3 = roda.pivo.global_position
			var raio := PhysicsRayQueryParameters3D.create(centro + Vector3.UP, centro - Vector3.UP * 2)
			raio.exclude = [kart.get_rid()]
			var piso := kart.get_world_3d().direct_space_state.intersect_ray(raio)
			rodas.append({"roda": mi.name, "menor_y_vertices": min_y, "piso_y": piso.position.y, "folga_m": min_y - piso.position.y})
		rel.contato_pneus.append({"piloto":jogo.personagens[i].nome,"no_piso":kart.is_on_floor(),"rodas":rodas})
		# Kart parado à frente; o jogador colide usando a física e os sinais reais.
		var outro = load("res://cenas/kart.tscn").instantiate()
		outro.definicao = jogo.personagens[(i+1)%jogo.personagens.size()]
		outro.transform = kart.transform
		outro.position += -kart.basis.z * 8.0
		pista.add_child(outro)
		outro.set_physics_process(false)
		var choques: Array = []
		kart.bateu.connect(func(no: Node, intensidade: float):
			if no == outro: choques.append(intensidade))
		Input.action_press("acelerar")
		await _passos(90)
		Input.action_release("acelerar")
		rel.colisoes_karts.append({"piloto":kart.definicao.nome if kart.definicao else jogo.personagens[i].nome,"alvo":outro.definicao.nome,"batidas":choques.size(),"impulso_alvo_m_s":outro.velocidade_plana().length(),"tremor_jogador":kart.tremor})
		pista.free()
		current_scene = null
	rel.aprovado = true
	for contato in rel.contato_pneus:
		for roda in contato.rodas: rel.aprovado = rel.aprovado and absf(roda.folga_m) < 0.02
	for caso in rel.colisoes_karts: rel.aprovado = rel.aprovado and caso.batidas > 0 and caso.impulso_alvo_m_s > 0.0
	FileAccess.open(BASE + "contato_e_colisoes.json",FileAccess.WRITE).store_string(JSON.stringify(rel,"\t"))
	print("CONTATO_COLISOES ",JSON.stringify(rel))
	quit(0 if rel.aprovado else 2)
