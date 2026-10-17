extends SceneTree
## Gera as cenas do jogo pela linha de comando:
##   godot --headless --path . --script res://ferramentas/construir_cenas.gd


func _init() -> void:
	_salvar(_kart(), "res://cenas/kart.tscn")
	_salvar(_pista(), "res://cenas/pista.tscn")
	_salvar(_selecao(), "res://cenas/selecao_personagem.tscn")
	quit()


func _salvar(raiz: Node, caminho: String) -> void:
	_definir_dono(raiz, raiz)
	var cena := PackedScene.new()
	var erro := cena.pack(raiz)
	if erro == OK:
		erro = ResourceSaver.save(cena, caminho)
	print("%s: %s" % [caminho, error_string(erro)])
	raiz.free()


func _definir_dono(no: Node, dono: Node) -> void:
	for filho in no.get_children():
		filho.owner = dono
		if filho.scene_file_path.is_empty():
			_definir_dono(filho, dono)


func _filho(pai: Node, no: Node, nome: String) -> Node:
	no.name = nome
	pai.add_child(no)
	return no


func _ambiente(pai: Node) -> void:
	# HDRI "Kloofendal 48d Partly Cloudy (Pure Sky)", referência em ambiente/referencia/ceu/.
	var ceu := PanoramaSkyMaterial.new()
	ceu.panorama = load("res://ambiente/kloofendal_48d_partly_cloudy_puresky_4k.exr")
	var sky := Sky.new()
	sky.sky_material = ceu
	var amb := Environment.new()
	amb.background_mode = Environment.BG_SKY
	amb.sky = sky
	amb.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
	amb.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	amb.fog_enabled = true
	# Cor média da faixa do horizonte no HDRI; a neblina não cobre o céu.
	amb.fog_light_color = Color(0.4361, 0.4685, 0.5671).linear_to_srgb()
	amb.fog_density = 0.004
	amb.fog_sky_affect = 0.0
	var we := WorldEnvironment.new()
	we.environment = amb
	_filho(pai, we, "Ambiente")

	# Altura (47,9°) e direção do sol medidas no HDRI; renderizado, o sol do céu fica a < 0,5° desta luz.
	var sol := DirectionalLight3D.new()
	sol.rotation_degrees = Vector3(-47.9, -34.3, 0)
	sol.light_energy = 1.2
	sol.shadow_enabled = true
	sol.directional_shadow_max_distance = 60.0
	_filho(pai, sol, "Sol")


func _caixa(pai: Node, nome: String, tamanho: Vector3, posicao: Vector3, cor: Color) -> void:
	var corpo := _filho(pai, StaticBody3D.new(), nome) as StaticBody3D
	corpo.position = posicao
	var forma := BoxShape3D.new()
	forma.size = tamanho
	var colisao := CollisionShape3D.new()
	colisao.shape = forma
	_filho(corpo, colisao, "Colisao")
	var malha := BoxMesh.new()
	malha.size = tamanho
	var material := StandardMaterial3D.new()
	material.albedo_color = cor
	malha.material = material
	var mi := MeshInstance3D.new()
	mi.mesh = malha
	_filho(corpo, mi, "Malha")


func _kart() -> Node:
	var kart := CharacterBody3D.new()
	kart.name = "Kart"
	kart.set_script(load("res://scripts/kart.gd"))
	kart.floor_snap_length = 0.3
	var forma := BoxShape3D.new()
	forma.size = Vector3(1.3, 0.7, 2.0)
	var colisao := CollisionShape3D.new()
	colisao.shape = forma
	colisao.position.y = 0.36
	_filho(kart, colisao, "Colisao")
	var visual := Node3D.new()
	visual.set_script(load("res://scripts/visual_kart.gd"))
	_filho(kart, visual, "Visual")
	return kart


func _pista() -> Node:
	var raiz := Node3D.new()
	raiz.name = "Pista"
	raiz.set_script(load("res://scripts/pista.gd"))
	_ambiente(raiz)

	var chao := _filho(raiz, StaticBody3D.new(), "Chao")
	var limite := CollisionShape3D.new()
	limite.shape = WorldBoundaryShape3D.new()
	_filho(chao, limite, "Colisao")
	var plano := PlaneMesh.new()
	plano.size = Vector2(800, 800)
	var material := ShaderMaterial.new()
	material.shader = load("res://shaders/quadriculado.gdshader")
	plano.material = material
	var piso := MeshInstance3D.new()
	piso.mesh = plano
	_filho(chao, piso, "Piso")

	# Muros nas bordas e alguns blocos para referência de movimento.
	var muros := _filho(raiz, Node3D.new(), "Muros")
	var cor_muro := Color(0.85, 0.3, 0.25)
	_caixa(muros, "Norte", Vector3(200, 2, 1), Vector3(0, 1, -100), cor_muro)
	_caixa(muros, "Sul", Vector3(200, 2, 1), Vector3(0, 1, 100), cor_muro)
	_caixa(muros, "Leste", Vector3(1, 2, 200), Vector3(100, 1, 0), cor_muro)
	_caixa(muros, "Oeste", Vector3(1, 2, 200), Vector3(-100, 1, 0), cor_muro)
	var blocos := _filho(raiz, Node3D.new(), "Blocos")
	var sorteio := RandomNumberGenerator.new()
	sorteio.seed = 7
	for i in 24:
		var pos := Vector3(sorteio.randf_range(-85, 85), 0, sorteio.randf_range(-85, 85))
		if pos.length() < 12.0:
			continue
		var altura := sorteio.randf_range(0.8, 3.0)
		pos.y = altura * 0.5
		var cor := Color.from_hsv(sorteio.randf(), 0.55, 0.9)
		_caixa(blocos, "Bloco%d" % i, Vector3(2, altura, 2), pos, cor)

	var kart := (load("res://cenas/kart.tscn") as PackedScene).instantiate()
	_filho(raiz, kart, "Kart")

	var camera := Camera3D.new()
	camera.set_script(load("res://scripts/camera_perseguicao.gd"))
	camera.position = Vector3(0, 2, 5)
	_filho(raiz, camera, "Camera")
	camera.alvo = kart

	var hud := _filho(raiz, CanvasLayer.new(), "HUD")
	var velocimetro := Label.new()
	velocimetro.unique_name_in_owner = true
	velocimetro.add_theme_font_size_override("font_size", 40)
	velocimetro.add_theme_constant_override("outline_size", 8)
	velocimetro.add_theme_color_override("font_outline_color", Color.BLACK)
	velocimetro.set_anchors_and_offsets_preset(Control.PRESET_BOTTOM_RIGHT)
	velocimetro.grow_horizontal = Control.GROW_DIRECTION_BEGIN
	velocimetro.grow_vertical = Control.GROW_DIRECTION_BEGIN
	velocimetro.position -= Vector2(24, 16)
	_filho(hud, velocimetro, "Velocimetro")
	var ajuda := Label.new()
	ajuda.text = "W/↑ acelera · S/↓ freia e dá ré · A/D ou ←/→ esterça · Esc volta à escolha"
	ajuda.add_theme_constant_override("outline_size", 6)
	ajuda.add_theme_color_override("font_outline_color", Color.BLACK)
	ajuda.position = Vector2(16, 12)
	_filho(hud, ajuda, "Ajuda")
	return raiz


func _selecao() -> Node:
	var raiz := Node3D.new()
	raiz.name = "SelecaoPersonagem"
	raiz.set_script(load("res://scripts/selecao_personagem.gd"))
	_ambiente(raiz)

	var pedestal := CylinderMesh.new()
	pedestal.top_radius = 2.0
	pedestal.bottom_radius = 2.2
	pedestal.height = 0.3
	var material := ShaderMaterial.new()
	material.shader = load("res://shaders/quadriculado.gdshader")
	material.set_shader_parameter("tamanho", 0.5)
	pedestal.material = material
	var base := MeshInstance3D.new()
	base.mesh = pedestal
	base.position.y = -0.15
	_filho(raiz, base, "Pedestal")
	var vitrine := _filho(raiz, Node3D.new(), "Vitrine") as Node3D
	vitrine.rotation_degrees.y = 210  # começa de frente para a câmera, em três quartos

	var camera := Camera3D.new()
	camera.position = Vector3(0, 1.6, 3.6)
	camera.rotation_degrees.x = -14
	camera.fov = 50
	_filho(raiz, camera, "Camera")

	var ui := _filho(raiz, CanvasLayer.new(), "UI")
	var coluna := VBoxContainer.new()
	coluna.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	coluna.offset_left = 32
	coluna.offset_right = -32
	coluna.offset_top = 24
	coluna.offset_bottom = -32
	_filho(ui, coluna, "Coluna")
	var titulo := Label.new()
	titulo.text = "Escolha seu piloto"
	titulo.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	titulo.add_theme_font_size_override("font_size", 44)
	titulo.add_theme_constant_override("outline_size", 10)
	titulo.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.8))
	_filho(coluna, titulo, "Titulo")
	var espaco := Control.new()
	espaco.size_flags_vertical = Control.SIZE_EXPAND_FILL
	_filho(coluna, espaco, "Espaco")
	var nome := Label.new()
	nome.unique_name_in_owner = true
	nome.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	nome.add_theme_font_size_override("font_size", 36)
	nome.add_theme_constant_override("outline_size", 8)
	nome.add_theme_color_override("font_outline_color", Color.BLACK)
	_filho(coluna, nome, "Nome")
	var descricao := Label.new()
	descricao.unique_name_in_owner = true
	descricao.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	descricao.add_theme_constant_override("outline_size", 6)
	descricao.add_theme_color_override("font_outline_color", Color.BLACK)
	_filho(coluna, descricao, "Descricao")
	var botoes := HBoxContainer.new()
	botoes.alignment = BoxContainer.ALIGNMENT_CENTER
	botoes.add_theme_constant_override("separation", 16)
	_filho(coluna, botoes, "Botoes")
	for dados in [["Anterior", "◀"], ["Jogar", "Jogar"], ["Proximo", "▶"]]:
		var botao := Button.new()
		botao.text = dados[1]
		botao.unique_name_in_owner = true
		botao.custom_minimum_size = Vector2(200 if dados[0] == "Jogar" else 64, 56)
		botao.add_theme_font_size_override("font_size", 26)
		_filho(botoes, botao, dados[0])
	return raiz
