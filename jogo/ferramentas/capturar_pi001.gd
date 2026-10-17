extends SceneTree
## Capturas do renderizador real; executar sem --headless.
const BASE := "res://../pistas/PI001_primeira_pista/validacao/integracao_20261016/"

func _initialize() -> void:
	call_deferred("_executar")

func _foto(nome: String) -> void:
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(BASE + nome + ".png")

func _passos(n: int) -> void:
	for i in n: await physics_frame

func _executar() -> void:
	var jogo := root.get_node("Jogo")
	var menu = load("res://cenas/selecao_personagem.tscn").instantiate()
	root.add_child(menu)
	current_scene = menu
	await _passos(30)
	await _foto("menu_pi001")
	menu._jogar()
	await scene_changed
	await _passos(10)
	await _foto("largada_pi001")
	var pista := current_scene
	var kart: Kart = pista.get_node("Kart")
	Input.action_press("acelerar")
	await _passos(150)
	await _foto("aceleracao_pi001")
	Input.action_press("esquerda")
	await _passos(24)
	await _foto("curva_pi001")
	Input.action_release("esquerda")
	Input.action_release("acelerar")
	Input.action_press("frear")
	await _passos(120)
	await _foto("re_pi001")
	Input.action_release("frear")
	# Vista elevada da cena completa, sem alterar as câmeras do projeto.
	var camera := Camera3D.new()
	pista.add_child(camera)
	camera.position = Vector3(0, 370, 200)
	camera.look_at(Vector3.ZERO)
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 470
	camera.far = 1500
	camera.make_current()
	# Só a captura de inspeção geral suspende a neblina, para mostrar o modelo inteiro.
	pista.get_node("Ambiente").environment.fog_enabled = false
	await _passos(2)
	await _foto("vista_geral_pi001")
	# Contato em repouso, os três personagens com a câmera existente.
	pista.get_node("Ambiente").environment.fog_enabled = true
	camera.queue_free()
	pista.get_node("Camera").make_current()
	for i in jogo.personagens.size():
		kart.definicao = jogo.personagens[i]
		kart.remove_child(kart.visual)
		kart.visual.free()
		kart.visual = VisualKart.new()
		kart.visual.name = "Visual"
		kart.add_child(kart.visual)
		kart.visual.montar(kart.definicao)
		kart.transform = pista.get_node("Percurso").largada(0)
		kart.velocidade = 0.0
		kart.empurrao = Vector3.ZERO
		kart.rodada = 0.0
		await _passos(30)
		await _foto("contato_" + kart.definicao.nome.to_lower())
		var lateral := Camera3D.new()
		pista.add_child(lateral)
		lateral.global_position = kart.global_position + kart.global_basis.x * 3.0 + Vector3.UP * 0.5
		lateral.look_at(kart.global_position + Vector3.UP * 0.4)
		lateral.fov = 55
		lateral.make_current()
		await _passos(2)
		await _foto("pneus_lateral_" + kart.definicao.nome.to_lower())
		lateral.queue_free()
		pista.get_node("Camera").make_current()
	print("CAPTURAS_PI001_CONCLUIDAS")
	pista.free()
	current_scene = null
	quit()
