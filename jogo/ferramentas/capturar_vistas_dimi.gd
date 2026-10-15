extends SceneTree
## Fase 8 do P002 — captura imagens renderizadas do menu e da pista com o Dimi.
## Precisa de janela (sem --headless). Não altera scripts, cenas nem fichas.
## godot --path jogo --fixed-fps 60 --script res://ferramentas/capturar_vistas_dimi.gd [-- --pasta=res://.../]

const PASTA_PADRAO := "res://../personagens/P002_dimi/registros/vistas_fase8/"
var PASTA := PASTA_PADRAO
var _lateral: Camera3D
var _seguidora: Camera3D
var _salvas: Array[String] = []


func _initialize() -> void:
	call_deferred("_executar")


func _salvar(nome: String) -> void:
	await RenderingServer.frame_post_draw
	var caminho := PASTA + nome + ".png"
	root.get_texture().get_image().save_png(caminho)
	_salvas.append(nome)


## Vista lateral fechada da cabeça, pelo lado direito do piloto.
func _capturar_lateral(kart: Kart, nome: String) -> void:
	var cabeca := kart.visual.global_transform * Vector3(0, 0.62, 0)
	_lateral.global_position = cabeca + kart.global_basis.x * 2.2 + Vector3.UP * 0.15
	_lateral.look_at(cabeca)
	_lateral.make_current()
	await _salvar(nome)
	_seguidora.make_current()


func _executar() -> void:
	for argumento in OS.get_cmdline_user_args():
		if argumento.begins_with("--pasta="):
			PASTA = argumento.trim_prefix("--pasta=")
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(PASTA))
	var jogo = root.get_node("Jogo")
	jogo.indice_escolhido = 0
	var menu = load("res://cenas/selecao_personagem.tscn").instantiate()
	root.add_child(menu)
	current_scene = menu
	for i in range(30):
		await process_frame
	await _salvar("menu_jake")
	menu._trocar(1)
	for i in range(30):
		await process_frame
	await _salvar("menu_dimi")
	menu._jogar()
	await scene_changed
	var pista := current_scene
	var kart: Kart = pista.get_node("Kart")
	_seguidora = pista.find_children("*", "Camera3D", true, false)[0]
	_lateral = Camera3D.new()
	_lateral.fov = 35.0
	pista.add_child(_lateral)
	_lateral.top_level = true
	await _salvar("pista_parado")
	await _capturar_lateral(kart, "lateral_parado")

	Input.action_press("acelerar")
	for i in range(120):
		await physics_frame
	await _salvar("pista_reta")

	Input.action_press("esquerda")
	for i in range(90):
		await physics_frame
	await _salvar("pista_curva_esquerda")
	await _capturar_lateral(kart, "lateral_curva_esquerda")
	Input.action_release("esquerda")

	# Inverte e captura no pico do giro relativo da cabeça.
	Input.action_press("direita")
	# Antes do pico a cabeça passa pelo centro; só depois disso o máximo conta.
	var maior := 0.0
	var quadro_pico := -10
	var cruzou := false
	var sinal_inicial := signf(kart.visual._cabeca)
	for i in range(90):
		await physics_frame
		var atual := absf(kart.visual._cabeca)
		cruzou = cruzou or atual < deg_to_rad(1.0) or signf(kart.visual._cabeca) != sinal_inicial
		if not cruzou:
			continue
		if atual > maior:
			maior = atual
			quadro_pico = i
		elif quadro_pico == i - 1:
			await _capturar_lateral(kart, "lateral_pico_cabeca_%.1f_graus" % rad_to_deg(maior))
			await _salvar("pista_pico_cabeca")
	await _salvar("pista_curva_direita")
	Input.action_release("direita")
	Input.action_release("acelerar")

	Input.action_press("frear")
	for i in range(150):
		await physics_frame
	await _salvar("pista_re")
	Input.action_release("frear")
	print("VISTAS_DIMI ", JSON.stringify(_salvas), " pico_graus=", rad_to_deg(maior))
	current_scene.free()
	current_scene = null
	quit(0)
