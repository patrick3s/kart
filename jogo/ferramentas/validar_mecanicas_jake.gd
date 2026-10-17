extends SceneTree
## Executa o código real e o GLB importado, sem modificar scripts ou cenas do jogo.
## godot --headless --path jogo --fixed-fps 60 --script res://ferramentas/validar_mecanicas_jake.gd

const DESTINO := "res://../personagens/P001_jake/validacao/validacao_godot_jake.json"
var relatorio: Dictionary = {}


func _initialize() -> void:
	call_deferred("_executar")


func _novo_visual() -> VisualKart:
	var visual := VisualKart.new()
	root.add_child(visual)
	visual.montar(load("res://personagens/jake/jake.tres"))
	visual._ruido.seed = 12345
	return visual


func _inclinacao(visual: VisualKart, indice: int) -> float:
	var esqueleto := visual._esqueleto
	esqueleto.force_update_all_bone_transforms()
	var pose := esqueleto.get_bone_global_pose(indice).basis
	var repouso := esqueleto.get_bone_global_rest(indice).basis
	var cima := (pose * repouso.inverse()) * Vector3.UP
	# Positivo = direita do piloto no espaço do GLB (+Z à frente).
	return atan2(-cima.x, cima.y)


func _curvas(com_ruido: bool, fps: int) -> Dictionary:
	var visual := _novo_visual()
	if not com_ruido:
		visual.vibracao_parado = 0.0
		visual.vibracao_maxima = 0.0
		visual.rolagem_vibracao = 0.0
	var resultado := {"fps": fps, "ruido": com_ruido, "fases": []}
	var rodas_antes: Array[Vector3] = []
	for roda in visual._rodas:
		rodas_antes.append(roda.pivo.global_position)
	var deriva_roda := 0.0
	for fase in [{"nome": "esquerda", "giro": 1.0}, {"nome": "direita", "giro": -1.0}, {"nome": "reta", "giro": 0.0}]:
		var falhas := 0
		var falhas_suspensao := 0
		var primeira_falha: Dictionary = {}
		var amostras: Array[Dictionary] = []
		for i in range(fps * 3):
			visual.atualizar(1.0 / fps, 10.0, float(fase.giro), 0.0, signf(float(fase.giro)), 10.0 / 22.0)
			var corpo := _inclinacao(visual, visual._osso_corpo)
			var cabeca := _inclinacao(visual, visual._osso_cabeca)
			# Ignorar apenas a zona de +/-0,05 grau em torno da vertical.
			var mesmo_lado := absf(corpo) > deg_to_rad(0.05) and corpo * cabeca > 0.0
			if mesmo_lado:
				falhas += 1
				if primeira_falha.is_empty():
					primeira_falha = {"quadro": i + 1, "segundos": float(i + 1) / fps, "corpo_graus": rad_to_deg(corpo), "cabeca_global_graus": rad_to_deg(cabeca)}
			if float(fase.giro) != 0.0 and corpo * float(fase.giro) < 0.0:
				falhas_suspensao += 1
			if i < 20 or (i + 1) % (fps / 2) == 0:
				amostras.append({"quadro": i + 1, "corpo_graus": rad_to_deg(corpo), "cabeca_global_graus": rad_to_deg(cabeca), "cabeca_relativa_graus": rad_to_deg(visual._cabeca)})
			for j in range(visual._rodas.size()):
				deriva_roda = maxf(deriva_roda, rodas_antes[j].distance_to(visual._rodas[j].pivo.global_position))
		resultado.fases.append({"nome": fase.nome, "quadros_cabeca_mesmo_lado": falhas, "quadros_corpo_contra_sinal_curva": falhas_suspensao, "primeira_falha": primeira_falha, "corpo_final_graus": rad_to_deg(_inclinacao(visual, visual._osso_corpo)), "cabeca_final_global_graus": rad_to_deg(_inclinacao(visual, visual._osso_cabeca)), "amostras": amostras})
	resultado.deriva_maxima_pivos_rodas = deriva_roda
	visual.free()
	return resultado


func _rodas() -> Array[Dictionary]:
	var visual := _novo_visual()
	var resultado: Array[Dictionary] = []
	visual.atualizar(0.01, 5.0, 1.0, 0.0, 1.0, 0.3)
	for roda in visual._rodas:
		var esperado: float = 5.0 / visual.scale.x / float(roda.raio) * 0.01
		resultado.append({"nome": roda.malha.name, "raio_modelo": roda.raio, "giro_esperado_rad": esperado, "giro_avante_correto": roda.malha.basis.is_equal_approx(Basis(Vector3.RIGHT, esperado)), "esterco_graus": rad_to_deg(roda.pivo.rotation.y), "dianteira": roda.dianteira})
	visual.atualizar(0.01, -5.0, -1.0, 0.0, -1.0, 0.3)
	for i in range(visual._rodas.size()):
		resultado[i].re_cancela_giro = visual._rodas[i].malha.basis.is_equal_approx(Basis.IDENTITY)
	var bases: Array[Basis] = []
	for roda in visual._rodas:
		bases.append(roda.malha.basis)
	visual.atualizar(0.1, 0.0, 0.0, 0.0, 0.0, 0.0)
	for i in range(visual._rodas.size()):
		resultado[i].parada_sem_giro = visual._rodas[i].malha.basis.is_equal_approx(bases[i])
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
		if absf(corpo) > deg_to_rad(0.05) and corpo * cabeca > 0.0:
			mesmo_lado += 1
			if exemplo.is_empty():
				exemplo = {"quadro": i + 1, "corpo_graus": rad_to_deg(corpo), "cabeca_global_graus": rad_to_deg(cabeca), "cabeca_relativa_graus": rad_to_deg(visual._cabeca)}
	visual.free()
	return {"quadros": 120, "quadros_mesmo_lado": mesmo_lado, "exemplo": exemplo}


func _executar() -> void:
	relatorio.versao_godot = Engine.get_version_info().string
	relatorio.metodo = "Execucao headless dos scripts e do GLB reais; curvas manuais deterministicas e percurso com Input no motor de fisica. Sem alteracao da mecanica."
	var definicao: DefinicaoPersonagem = load("res://personagens/jake/jake.tres")
	var modelo := definicao.modelo.instantiate()
	root.add_child(modelo)
	var malhas: Array[Dictionary] = []
	for no in modelo.find_children("*", "MeshInstance3D", true, false):
		malhas.append({"nome": no.name, "skin": no.skin != null})
	var esqueleto: Skeleton3D = modelo.find_children("*", "Skeleton3D", true, false)[0]
	var ossos: Array[String] = []
	for i in range(esqueleto.get_bone_count()):
		ossos.append(esqueleto.get_bone_name(i))
	relatorio.estrutura = {"malhas": malhas, "ossos": ossos, "pilotos_cadastrados": root.get_node("Jogo").personagens.size()}
	modelo.free()
	relatorio.rodas = _rodas()
	relatorio.curvas = [_curvas(false, 60), _curvas(true, 60), _curvas(true, 120)]
	relatorio.reta_com_vibracao = _reta_com_vibracao()
	var menu = load("res://cenas/selecao_personagem.tscn").instantiate()
	root.add_child(menu)
	current_scene = menu
	await process_frame
	relatorio.selecao = {"nome_exibido": menu.nome.text, "botao_jogar": menu.jogar != null, "troca_visivel": menu.anterior.visible}
	root.get_node("Jogo").quantidade_adversarios = 0  # mede o piloto sem adversários
	menu.circuito.selected = 1  # Regressão na arena histórica.
	menu._jogar()
	await scene_changed
	await physics_frame
	var pista := current_scene
	var kart: Kart = pista.get_node("Kart")
	var cameras := pista.find_children("*", "Camera3D", true, false)
	var camera: Camera3D = cameras[0]
	var inicio := kart.global_position
	Input.action_press("acelerar")
	for i in range(120):
		await physics_frame
	var distancia := inicio.distance_to(kart.global_position)
	var fov_reta := camera.fov
	Input.action_press("esquerda")
	for i in range(120):
		await physics_frame
	Input.action_release("esquerda")
	relatorio.percurso = {"distancia_avante": distancia, "velocidade": kart.velocidade, "giro_esquerda_rad_s": kart.giro, "corpo_graus": rad_to_deg(_inclinacao(kart.visual, kart.visual._osso_corpo)), "cabeca_global_graus": rad_to_deg(_inclinacao(kart.visual, kart.visual._osso_cabeca)), "camera_atras_produto_escalar": (camera.global_position - kart.global_position).dot(kart.global_basis.z), "camera_fov_em_movimento": fov_reta, "camera_fov_base": camera.fov_base, "shader_quadriculado": str(pista.get_node("Chao/Piso").mesh.material.shader.resource_path)}
	Input.action_release("acelerar")
	var rodas_ok := true
	for roda in relatorio.rodas:
		rodas_ok = rodas_ok and roda.giro_avante_correto and roda.re_cancela_giro and roda.parada_sem_giro
		rodas_ok = rodas_ok and is_equal_approx(float(roda.esterco_graus), 28.0 if roda.dianteira else 0.0)
	var fases: Array = relatorio.curvas[0].fases
	relatorio.conclusao = {
		"status": "parcial",
		"rodas_giro_re_parada_esterco": rodas_ok,
		"suspensao_lado_correto_estabilizada": float(fases[0].corpo_final_graus) > 0.0 and float(fases[1].corpo_final_graus) < 0.0,
		"cabeca_oposta_estabilizada": float(fases[0].corpo_final_graus) * float(fases[0].cabeca_final_global_graus) < 0.0 and float(fases[1].corpo_final_graus) * float(fases[1].cabeca_final_global_graus) < 0.0,
		"cabeca_sempre_oposta": int(fases[0].quadros_cabeca_mesmo_lado) == 0 and int(fases[1].quadros_cabeca_mesmo_lado) == 0 and int(relatorio.reta_com_vibracao.quadros_mesmo_lado) == 0,
		"camera_atras_e_fov_dinamico": float(relatorio.percurso.camera_atras_produto_escalar) > 0.0 and float(relatorio.percurso.camera_fov_em_movimento) > float(relatorio.percurso.camera_fov_base),
		"menu_e_movimento": relatorio.selecao.nome_exibido == "Jake" and distancia > 1.0,
		"limites": ["Corpo_Kart reune torso do piloto e carro; Cabeca e uma malha distinta", "Quatro ossos no GLB; Torso_Bone e Head_Bone sao os dois controles usados", "Suspensao visual; sem curso individual de rodas ou contato por raycast", "Auditoria headless; sem verificacao de pixels ou aparencia renderizada"]
	}
	# O estado acompanha as medições atuais; os JSONs históricos permanecem intactos.
	var passou := true
	for valor in relatorio.conclusao.values():
		if valor is bool: passou = passou and valor
	relatorio.conclusao.status = "aprovado" if passou else "parcial"
	# Hashes permitem distinguir a versao auditada de futuras alteracoes.
	relatorio.sha256 = {}
	for caminho in ["res://scripts/kart.gd", "res://scripts/visual_kart.gd", "res://scripts/camera_perseguicao.gd", "res://personagens/jake/jake_kart.glb", "res://project.godot"]:
		relatorio.sha256[caminho] = FileAccess.get_sha256(caminho)
	var destino := DESTINO
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--saida="): destino = arg.trim_prefix("--saida=")
	var arquivo := FileAccess.open(destino, FileAccess.WRITE)
	if arquivo == null:
		push_error("Nao foi possivel gravar o relatorio: " + str(FileAccess.get_open_error()))
		quit(2)
		return
	arquivo.store_string(JSON.stringify(relatorio, "\t") + "\n")
	arquivo.close()
	print("VALIDACAO_JAKE_CONCLUIDA ", ProjectSettings.globalize_path(destino))
	print("ESTRUTURA ", JSON.stringify(relatorio.estrutura))
	print("PERCURSO ", JSON.stringify(relatorio.percurso))
	print("CONCLUSAO ", JSON.stringify(relatorio.conclusao))
	for caso in relatorio.curvas:
		for fase in caso.fases:
			print("CURVA ", caso.fps, " ruido=", caso.ruido, " ", fase.nome, " mesmo_lado=", fase.quadros_cabeca_mesmo_lado, " corpo=", fase.corpo_final_graus, " cabeca=", fase.cabeca_final_global_graus)
	current_scene.free()
	current_scene = null
	quit(0)
