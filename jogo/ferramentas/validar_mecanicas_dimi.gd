extends SceneTree
## Fase 8 do P002 — executa o código real do jogo com a ficha e o GLB do Dimi.
## Não altera scripts, cenas nem fichas; só grava o relatório.
## godot --headless --path jogo --fixed-fps 60 --script res://ferramentas/validar_mecanicas_dimi.gd [-- --saida=res://...json]

const FICHA := "res://personagens/dimi/dimi.tres"
const DESTINO_PADRAO := "res://../personagens/P002_dimi/validacao/validacao_mecanicas_fase8.json"
const RAIO_MEDIDO := 0.1297
## Teto decidido na Fase 6 para o giro da cabeça (base aberta escondida pela gola).
const TETO_CABECA := 25.0
const ZONA_NEUTRA := 0.05
var relatorio: Dictionary = {}


func _initialize() -> void:
	call_deferred("_executar")


## Destino do relatório: `--saida=` depois de `--` na linha de comando, ou o da Fase 8.
func _destino() -> String:
	for argumento in OS.get_cmdline_user_args():
		if argumento.begins_with("--saida="):
			return argumento.trim_prefix("--saida=")
	return DESTINO_PADRAO


func _novo_visual(sem_ruido := false) -> VisualKart:
	var visual := VisualKart.new()
	root.add_child(visual)
	visual.montar(load(FICHA))
	visual._ruido.seed = 12345
	if sem_ruido:
		visual.vibracao_parado = 0.0
		visual.vibracao_maxima = 0.0
		visual.rolagem_vibracao = 0.0
	return visual


## Inclinação lateral do osso no espaço do esqueleto, incluindo o que herda dos pais.
## Positivo = direita do piloto (o GLB olha para +Z).
func _inclinacao(visual: VisualKart, indice: int) -> float:
	var esqueleto := visual._esqueleto
	esqueleto.force_update_all_bone_transforms()
	var pose := esqueleto.get_bone_global_pose(indice).basis
	var repouso := esqueleto.get_bone_global_rest(indice).basis
	var cima := (pose * repouso.inverse()) * Vector3.UP
	return atan2(-cima.x, cima.y)


func _mesmo_lado(corpo: float, cabeca: float) -> bool:
	return absf(corpo) > deg_to_rad(ZONA_NEUTRA) and corpo * cabeca > 0.0


## Entrada, inversão e saída de curva, depois parada; cada trecho dura 3 s.
func _curvas(com_ruido: bool, fps: int) -> Dictionary:
	var visual := _novo_visual(not com_ruido)
	var resultado := {"fps": fps, "ruido": com_ruido, "fases": []}
	var rodas_antes: Array[Vector3] = []
	for roda in visual._rodas:
		rodas_antes.append(roda.pivo.global_position)
	var deriva_roda := 0.0
	var pivo_cabeca := visual._esqueleto.get_bone_global_rest(visual._osso_cabeca).origin
	var deriva_pivo := 0.0
	var trechos := [
		{"nome": "esquerda", "velocidade": 10.0, "giro": 1.0},
		{"nome": "direita", "velocidade": 10.0, "giro": -1.0},
		{"nome": "reta", "velocidade": 10.0, "giro": 0.0},
		{"nome": "parada", "velocidade": 0.0, "giro": 0.0},
	]
	for fase in trechos:
		var falhas := 0
		var falhas_suspensao := 0
		var ultima_falha := 0
		var primeira_falha: Dictionary = {}
		var maior_relativa := 0.0
		var maior_global := 0.0
		var maior_salto := 0.0
		var cabeca_anterior := visual._cabeca
		var amostras: Array[Dictionary] = []
		for i in range(fps * 3):
			var v: float = fase.velocidade
			var g: float = fase.giro
			visual.atualizar(1.0 / fps, v, g, 0.0, signf(g), absf(v) / 22.0)
			var corpo := _inclinacao(visual, visual._osso_corpo)
			var cabeca := _inclinacao(visual, visual._osso_cabeca)
			maior_relativa = maxf(maior_relativa, absf(rad_to_deg(visual._cabeca)))
			maior_salto = maxf(maior_salto, absf(rad_to_deg(visual._cabeca - cabeca_anterior)))
			cabeca_anterior = visual._cabeca
			maior_global = maxf(maior_global, absf(rad_to_deg(cabeca)))
			if _mesmo_lado(corpo, cabeca):
				falhas += 1
				ultima_falha = i + 1
				if primeira_falha.is_empty():
					primeira_falha = {"quadro": i + 1, "segundos": float(i + 1) / fps, "corpo_graus": rad_to_deg(corpo), "cabeca_global_graus": rad_to_deg(cabeca)}
			if g != 0.0 and corpo * g < 0.0:
				falhas_suspensao += 1
			if i < 20 or (i + 1) % (fps / 2) == 0:
				amostras.append({"quadro": i + 1, "corpo_graus": rad_to_deg(corpo), "cabeca_global_graus": rad_to_deg(cabeca), "cabeca_relativa_graus": rad_to_deg(visual._cabeca)})
			for j in range(visual._rodas.size()):
				deriva_roda = maxf(deriva_roda, rodas_antes[j].distance_to(visual._rodas[j].pivo.global_position))
			deriva_pivo = maxf(deriva_pivo, visual._esqueleto.get_bone_global_pose(visual._osso_cabeca).origin.distance_to(pivo_cabeca))
		resultado.fases.append({
			"nome": fase.nome,
			"quadros_cabeca_mesmo_lado": falhas,
			"ultimo_quadro_mesmo_lado": ultima_falha,
			"quadros_corpo_contra_sinal_curva": falhas_suspensao,
			"primeira_falha": primeira_falha,
			"cabeca_relativa_max_graus": maior_relativa,
			"cabeca_global_max_graus": maior_global,
			"cabeca_variacao_max_por_quadro_graus": maior_salto,
			"corpo_final_graus": rad_to_deg(_inclinacao(visual, visual._osso_corpo)),
			"cabeca_final_global_graus": rad_to_deg(_inclinacao(visual, visual._osso_cabeca)),
			"amostras": amostras,
		})
	resultado.deriva_maxima_pivos_rodas = deriva_roda
	# O pivô da cabeça acompanha o corpo; a deriva mede só o salto da vibração e a rolagem.
	resultado.deriva_maxima_pivo_cabeca_esqueleto = deriva_pivo
	visual.free()
	return resultado


func _rodas() -> Dictionary:
	var visual := _novo_visual()
	var lista: Array[Dictionary] = []
	var modelo := visual.get_child(0) as Node3D
	visual.atualizar(0.01, 5.0, 1.0, 0.0, 1.0, 0.3)
	for roda in visual._rodas:
		var esperado: float = 5.0 / visual.scale.x / float(roda.raio) * 0.01
		var pivo: Node3D = roda.pivo
		lista.append({
			"nome": roda.malha.name,
			"raio_modelo": roda.raio,
			"raio_caixa_modelo": maxf(roda.malha.get_aabb().size.y, roda.malha.get_aabb().size.z) * 0.5,
			"altura_banda_no_chao_modelo": modelo.position.y + pivo.position.y - float(roda.raio),
			"giro_esperado_rad": esperado,
			"giro_avante_correto": roda.malha.basis.is_equal_approx(Basis(Vector3.RIGHT, esperado)),
			"esterco_graus": rad_to_deg(pivo.rotation.y),
			"dianteira": roda.dianteira,
		})
	visual.atualizar(0.01, -5.0, -1.0, 0.0, -1.0, 0.3)
	for i in range(visual._rodas.size()):
		lista[i].re_cancela_giro = visual._rodas[i].malha.basis.is_equal_approx(Basis.IDENTITY)
		lista[i].esterco_oposto_graus = rad_to_deg(visual._rodas[i].pivo.rotation.y)
	var bases: Array[Basis] = []
	for roda in visual._rodas:
		bases.append(roda.malha.basis)
	visual.atualizar(0.1, 0.0, 0.0, 0.0, 0.0, 0.0)
	for i in range(visual._rodas.size()):
		lista[i].parada_sem_giro = visual._rodas[i].malha.basis.is_equal_approx(bases[i])
	var resultado := {"rodas": lista, "deslocamento_modelo_y": modelo.position.y, "escala": visual.scale.x}
	visual.free()
	return resultado


func _reta_com_vibracao() -> Dictionary:
	var visual := _novo_visual()
	var mesmo_lado := 0
	var exemplo: Dictionary = {}
	for i in range(120):
		visual.atualizar(1.0 / 60.0, 10.0, 0.0, 0.0, 0.0, 10.0 / 22.0)
		var corpo := _inclinacao(visual, visual._osso_corpo)
		var cabeca := _inclinacao(visual, visual._osso_cabeca)
		if _mesmo_lado(corpo, cabeca):
			mesmo_lado += 1
			if exemplo.is_empty():
				exemplo = {"quadro": i + 1, "corpo_graus": rad_to_deg(corpo), "cabeca_global_graus": rad_to_deg(cabeca), "cabeca_relativa_graus": rad_to_deg(visual._cabeca)}
	visual.free()
	return {"quadros": 120, "quadros_mesmo_lado": mesmo_lado, "exemplo": exemplo}


## Compara o comprimento e a altura do modelo do Dimi com os do Jake, na mesma escala.
func _dimensoes() -> Dictionary:
	var resultado := {}
	for caminho in ["res://personagens/jake/jake.tres", FICHA]:
		var definicao: DefinicaoPersonagem = load(caminho)
		var modelo := definicao.modelo.instantiate() as Node3D
		root.add_child(modelo)
		var caixa := AABB()
		var primeira := true
		for malha in modelo.find_children("*", "MeshInstance3D", true, false):
			var c: AABB = (malha as MeshInstance3D).global_transform * (malha as MeshInstance3D).get_aabb()
			caixa = c if primeira else caixa.merge(c)
			primeira = false
		resultado[definicao.nome] = {"tamanho_modelo": [caixa.size.x, caixa.size.y, caixa.size.z], "escala": definicao.escala, "comprimento_jogo": caixa.size.z * definicao.escala, "altura_jogo": caixa.size.y * definicao.escala}
		modelo.free()
	return resultado


func _passos(n: int) -> void:
	for i in range(n):
		await physics_frame


func _angulo_camera(camera: Camera3D, kart: Kart) -> float:
	var para_kart := kart.global_position - camera.global_position
	para_kart.y = 0.0
	var frente := -kart.global_basis.z
	frente.y = 0.0
	return rad_to_deg(frente.signed_angle_to(para_kart, Vector3.UP))


func _executar() -> void:
	relatorio.versao_godot = Engine.get_version_info().string
	relatorio.metodo = "Execucao headless dos scripts, da ficha e do GLB reais do Dimi; curvas manuais deterministicas e percurso com Input no motor de fisica a 60 passos/s."
	var jogo = root.get_node("Jogo")
	var nomes: Array[String] = []
	for definicao in jogo.personagens:
		nomes.append(definicao.nome)
	var ficha: DefinicaoPersonagem = load(FICHA)
	var modelo := ficha.modelo.instantiate()
	root.add_child(modelo)
	var malhas: Array[Dictionary] = []
	for no in modelo.find_children("*", "MeshInstance3D", true, false):
		malhas.append({"nome": no.name, "skin": no.skin != null})
	var esqueleto: Skeleton3D = modelo.find_children("*", "Skeleton3D", true, false)[0]
	var ossos: Array[String] = []
	for i in range(esqueleto.get_bone_count()):
		ossos.append(esqueleto.get_bone_name(i))
	var reprodutores := modelo.find_children("*", "AnimationPlayer", true, false)
	relatorio.estrutura = {"malhas": malhas, "ossos": ossos, "catalogo": nomes, "animation_player_autoplay": "" if reprodutores.is_empty() else str(reprodutores[0].autoplay), "ficha": {"nome": ficha.nome, "escala": ficha.escala, "raio_rodas": ficha.raio_rodas}}
	modelo.free()
	relatorio.dimensoes = _dimensoes()
	relatorio.rodas = _rodas()
	relatorio.curvas = [_curvas(false, 60), _curvas(true, 60), _curvas(true, 120)]
	relatorio.reta_com_vibracao = _reta_com_vibracao()

	# Tela de escolha: começa no Jake, troca para o Dimi e volta.
	jogo.indice_escolhido = 0
	var menu = load("res://cenas/selecao_personagem.tscn").instantiate()
	root.add_child(menu)
	current_scene = menu
	await process_frame
	var selecao := {"inicial": menu.nome.text, "botoes_troca_visiveis": menu.anterior.visible and menu.proximo.visible}
	menu._trocar(1)
	await process_frame
	selecao.apos_proximo = menu.nome.text
	selecao.descricao_dimi = menu.descricao.text
	menu._trocar(jogo.personagens.size() - 1)
	await process_frame
	selecao.apos_volta_completa = menu.nome.text
	menu._trocar(-1)
	await process_frame
	selecao.apos_anterior = menu.nome.text
	menu._trocar(1 - jogo.indice_escolhido)
	await process_frame
	selecao.indice_escolhido = jogo.indice_escolhido
	relatorio.selecao = selecao
	root.get_node("Jogo").quantidade_adversarios = 0  # mede o piloto sem adversários
	menu.circuito.selected = 1  # Regressão na arena histórica.
	menu._jogar()
	await scene_changed
	await physics_frame

	var pista := current_scene
	var kart: Kart = pista.get_node("Kart")
	var camera: Camera3D = pista.find_children("*", "Camera3D", true, false)[0]
	var modelo_pista := kart.visual.get_child(0)
	var percurso := {"modelo_na_pista": modelo_pista.scene_file_path, "shader_quadriculado": str(pista.get_node("Chao/Piso").mesh.material.shader.resource_path)}
	var maior_cabeca := 0.0
	var inicio := kart.global_position

	Input.action_press("acelerar")
	await _passos(120)
	percurso.avante = {"distancia": inicio.distance_to(kart.global_position), "velocidade": kart.velocidade, "camera_atras_produto_escalar": (camera.global_position - kart.global_position).dot(kart.global_basis.z), "camera_fov": camera.fov, "camera_fov_base": camera.fov_base}

	Input.action_press("esquerda")
	var maior_atraso := 0.0
	for i in range(120):
		await physics_frame
		maior_atraso = maxf(maior_atraso, absf(_angulo_camera(camera, kart)))
		maior_cabeca = maxf(maior_cabeca, absf(rad_to_deg(kart.visual._cabeca)))
	percurso.curva_esquerda = {"velocidade": kart.velocidade, "giro_rad_s": kart.giro, "esterco": kart.esterco, "corpo_graus": rad_to_deg(_inclinacao(kart.visual, kart.visual._osso_corpo)), "cabeca_global_graus": rad_to_deg(_inclinacao(kart.visual, kart.visual._osso_cabeca)), "camera_atraso_max_graus": maior_atraso, "rolagem_camera_graus": rad_to_deg(camera.rotation.z)}
	Input.action_release("esquerda")

	Input.action_press("direita")
	for i in range(120):
		await physics_frame
		maior_cabeca = maxf(maior_cabeca, absf(rad_to_deg(kart.visual._cabeca)))
	percurso.curva_direita = {"velocidade": kart.velocidade, "giro_rad_s": kart.giro, "esterco": kart.esterco, "corpo_graus": rad_to_deg(_inclinacao(kart.visual, kart.visual._osso_corpo)), "cabeca_global_graus": rad_to_deg(_inclinacao(kart.visual, kart.visual._osso_cabeca))}
	Input.action_release("direita")
	Input.action_release("acelerar")

	# Frenagem até parar, depois ré com a mesma tecla.
	var velocidade_inicial := kart.velocidade
	var fov_rapido := camera.fov
	var quadros_frenagem := 0
	var arfagem_frenagem := 0.0
	Input.action_press("frear")
	while kart.velocidade > 0.0 and quadros_frenagem < 600:
		await physics_frame
		quadros_frenagem += 1
		arfagem_frenagem = maxf(arfagem_frenagem, rad_to_deg(kart.visual.arfagem))
	var parada := kart.global_position
	var frente := -kart.global_basis.z
	await _passos(120)
	percurso.frenagem = {"velocidade_inicial": velocidade_inicial, "segundos_ate_parar": quadros_frenagem / 60.0, "bico_mergulha_max_graus": arfagem_frenagem}
	percurso.re = {"velocidade": kart.velocidade, "deslocamento_ao_longo_da_frente": (kart.global_position - parada).dot(frente), "camera_fov": camera.fov, "fov_em_alta": fov_rapido}
	Input.action_release("frear")
	await _passos(240)
	percurso.parado = {"velocidade": kart.velocidade, "cabeca_relativa_graus": rad_to_deg(kart.visual._cabeca), "rolagem_graus": rad_to_deg(kart.visual.rolagem)}
	percurso.cabeca_relativa_max_graus = maior_cabeca
	relatorio.percurso = percurso

	var rodas_ok := true
	for roda in relatorio.rodas.rodas:
		rodas_ok = rodas_ok and roda.giro_avante_correto and roda.re_cancela_giro and roda.parada_sem_giro
		rodas_ok = rodas_ok and is_equal_approx(float(roda.raio_modelo), RAIO_MEDIDO)
		rodas_ok = rodas_ok and is_equal_approx(float(roda.esterco_graus), 28.0 if roda.dianteira else 0.0)
		rodas_ok = rodas_ok and is_equal_approx(float(roda.esterco_oposto_graus), -28.0 if roda.dianteira else 0.0)
	var fases: Array = relatorio.curvas[0].fases
	var maior_relativa := float(percurso.cabeca_relativa_max_graus)
	var falhas_transicao := 0
	for caso in relatorio.curvas:
		for fase in caso.fases:
			maior_relativa = maxf(maior_relativa, float(fase.cabeca_relativa_max_graus))
			falhas_transicao += int(fase.quadros_cabeca_mesmo_lado)
	relatorio.conclusao = {
		"catalogo_jake_e_dimi": nomes.has("Jake") and nomes.has("Dimi"),
		"selecao_troca_e_volta": selecao.inicial == "Jake" and selecao.apos_proximo == "Dimi" and selecao.apos_volta_completa == "Jake" and selecao.apos_anterior == nomes.back() and selecao.botoes_troca_visiveis,
		"pista_usa_modelo_dimi": percurso.modelo_na_pista == "res://personagens/dimi/dimi_kart.glb",
		"movimento_frenagem_re": float(percurso.avante.distancia) > 1.0 and float(percurso.re.velocidade) < 0.0 and float(percurso.re.deslocamento_ao_longo_da_frente) < 0.0 and absf(float(percurso.parado.velocidade)) < 0.01,
		"direcao_dois_sentidos": float(percurso.curva_esquerda.giro_rad_s) > 0.0 and float(percurso.curva_direita.giro_rad_s) < 0.0,
		"camera_atras_atraso_e_fov_dinamico": float(percurso.avante.camera_atras_produto_escalar) > 0.0 and float(percurso.avante.camera_fov) > float(percurso.avante.camera_fov_base) and float(percurso.curva_esquerda.camera_atraso_max_graus) > 1.0,
		"rodas_raio_giro_re_parada_esterco": rodas_ok,
		"suspensao_lado_correto_estabilizada": float(fases[0].corpo_final_graus) > 0.0 and float(fases[1].corpo_final_graus) < 0.0,
		"cabeca_oposta_estabilizada": float(fases[0].corpo_final_graus) * float(fases[0].cabeca_final_global_graus) < 0.0 and float(fases[1].corpo_final_graus) * float(fases[1].cabeca_final_global_graus) < 0.0,
		"cabeca_sempre_oposta": falhas_transicao == 0 and int(relatorio.reta_com_vibracao.quadros_mesmo_lado) == 0,
		"cabeca_relativa_max_graus": maior_relativa,
		"cabeca_dentro_do_teto_25": maior_relativa <= TETO_CABECA,
	}
	relatorio.sha256 = {}
	for caminho in ["res://scripts/kart.gd", "res://scripts/visual_kart.gd", "res://scripts/camera_perseguicao.gd", "res://scripts/definicao_personagem.gd", "res://scripts/jogo.gd", "res://scripts/selecao_personagem.gd", FICHA, "res://personagens/dimi/dimi_kart.glb", "res://personagens/jake/jake.tres", "res://project.godot"]:
		relatorio.sha256[caminho] = FileAccess.get_sha256(caminho)
	var destino := _destino()
	var arquivo := FileAccess.open(destino, FileAccess.WRITE)
	if arquivo == null:
		push_error("Nao foi possivel gravar o relatorio: " + str(FileAccess.get_open_error()))
		quit(2)
		return
	arquivo.store_string(JSON.stringify(relatorio, "\t") + "\n")
	arquivo.close()
	print("VALIDACAO_DIMI_CONCLUIDA ", ProjectSettings.globalize_path(destino))
	print("SELECAO ", JSON.stringify(relatorio.selecao))
	print("PERCURSO ", JSON.stringify(relatorio.percurso))
	print("CONCLUSAO ", JSON.stringify(relatorio.conclusao))
	for caso in relatorio.curvas:
		for fase in caso.fases:
			print("CURVA ", caso.fps, " ruido=", caso.ruido, " ", fase.nome, " mesmo_lado=", fase.quadros_cabeca_mesmo_lado, " ultimo=", fase.ultimo_quadro_mesmo_lado, " corpo=", fase.corpo_final_graus, " cabeca=", fase.cabeca_final_global_graus, " rel_max=", fase.cabeca_relativa_max_graus, " salto_max=", fase.cabeca_variacao_max_por_quadro_graus)
	current_scene.free()
	current_scene = null
	quit(0)
