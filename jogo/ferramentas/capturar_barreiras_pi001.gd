extends SceneTree
## Capturas do renderizador real das barreiras da PI001; executar sem --headless.
const BASE := "res://../pistas/PI001_primeira_pista/validacao/barreiras_20261017/"

func _initialize() -> void:
	call_deferred("_executar")

func _foto(nome: String) -> void:
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png(BASE + nome + ".png")

func _passos(n: int) -> void:
	for i in n: await physics_frame

func _executar() -> void:
	var jogo := root.get_node("Jogo")
	jogo.quantidade_adversarios = 5
	var pista: Node = load("res://pistas/primeira_pista/primeira_pista.tscn").instantiate()
	root.add_child(pista)
	current_scene = pista
	await _passos(20)
	await _foto("largada_barreiras")
	var kart: Kart = pista.get_node("Kart")
	Input.action_press("acelerar")
	await _passos(150)
	await _foto("reta_barreiras")
	# Batida lateral: kart no eixo, acelerando para a borda.
	var eixo: PercursoPI001 = pista.get_node("Percurso")
	var d := 300.0
	kart.transform = Transform3D(Basis.looking_at(eixo.tangente(d).rotated(Vector3.UP, 0.7)), eixo.ponto(d) + Vector3.UP * 0.04)
	kart.velocidade = 0.0
	await _passos(150)
	await _foto("batida_barreiras")
	Input.action_release("acelerar")
	var camera := Camera3D.new()
	pista.add_child(camera)
	camera.position = Vector3(0, 370, 200)
	camera.look_at(Vector3.ZERO)
	camera.projection = Camera3D.PROJECTION_ORTHOGONAL
	camera.size = 470
	camera.far = 1500
	camera.make_current()
	pista.get_node("Ambiente").environment.fog_enabled = false
	await _passos(2)
	await _foto("vista_geral_barreiras")
	quit()
