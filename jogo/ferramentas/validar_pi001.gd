extends SceneTree
## Física real, 60 Hz. Saída exclusiva da integração; não toca relatórios históricos.
const BASE := "res://../pistas/PI001_primeira_pista/validacao/integracao_20261016/"
var rel: Dictionary = {"metodo": "Godot real, Input e CharacterBody3D; sem teletransporte na medição da volta", "controles": {}, "adversarios": [], "amostras": []}

func _initialize() -> void:
	call_deferred("_executar")

func passos(n: int) -> void:
	for i in n:
		await physics_frame

func _executar() -> void:
	var jogo := root.get_node("Jogo")
	var sufixo := ""
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--personagem="):
			jogo.indice_escolhido = int(arg.trim_prefix("--personagem="))
			sufixo = "_piloto%d" % jogo.indice_escolhido
	jogo.quantidade_adversarios = 0
	var menu = load("res://cenas/selecao_personagem.tscn").instantiate()
	root.add_child(menu)
	current_scene = menu
	await process_frame
	rel.menu = {"circuitos": menu.circuito.item_count, "padrao": menu.circuito.get_item_text(0)}
	menu._jogar()
	await scene_changed
	await passos(30)
	var pista := current_scene
	var kart: Kart = pista.get_node("Kart")
	var eixo: Path3D = pista.get_node("Percurso")
	rel.comprimento_m = eixo.curve.get_baked_length()
	rel.colisoes = pista.get_node("Colisoes").get_child_count()
	rel.controles.no_piso = kart.is_on_floor()
	var inicio := kart.position
	Input.action_press("acelerar")
	await passos(120)
	rel.controles.aceleracao = {"velocidade": kart.velocidade, "distancia_m": inicio.distance_to(kart.position)}
	Input.action_release("acelerar")
	Input.action_press("frear")
	await passos(48)
	rel.controles.frenagem_velocidade = kart.velocidade
	await passos(100)
	rel.controles.re_velocidade = kart.velocidade
	Input.action_press("esquerda")
	await passos(30)
	rel.controles.giro_re = kart.giro
	Input.action_release("esquerda")
	Input.action_release("frear")
	# Travessia da zebra numa reta: inclui subida e descida reais.
	kart.transform = Transform3D(Basis.looking_at(Vector3(0,0,1)), eixo.ponto(35.0) + Vector3.UP * 0.04)
	kart.velocidade = 0.0
	kart.empurrao = Vector3.ZERO
	kart.rodada = 0.0
	var alturas: Array[float] = []
	Input.action_press("acelerar")
	for i in 75:
		await physics_frame
		alturas.append(kart.position.y)
	Input.action_release("acelerar")
	rel.controles.zebra = {"y_min": alturas.min(), "y_max": alturas.max(), "posicao_final": str(kart.position), "velocidade_final": kart.velocidade}
	kart.rotation.y += PI
	kart.velocidade = 0.0
	Input.action_press("acelerar")
	var atravessou_asfalto := false
	var maior_y_retorno := -INF
	for i in 95:
		await physics_frame
		maior_y_retorno = maxf(maior_y_retorno, kart.position.y)
		if absf(kart.position.z - 116.1) < 1.0 and kart.is_on_floor(): atravessou_asfalto = true
	Input.action_release("acelerar")
	rel.controles.retorno_do_gramado = {"atravessou_asfalto": atravessou_asfalto, "maior_y": maior_y_retorno}
	pista.free()
	current_scene = null
	# Ensaio da corrida completa com as cinco IAs e colisões entre todos.
	jogo.quantidade_adversarios = 5
	pista = load("res://pistas/primeira_pista/primeira_pista.tscn").instantiate()
	root.add_child(pista)
	current_scene = pista
	kart = pista.get_node("Kart")
	eixo = pista.get_node("Percurso")
	# Jogador estacionado na sua vaga; as IAs largam normalmente.
	var medidas: Array[Dictionary] = []
	for ia in pista.adversarios:
		medidas.append({"nome": ia.name, "piloto": ia.definicao.nome, "desvio_max_m": 0.0, "quadros_fora_asfalto": 0, "quadros_contramao": 0, "volta_segundos": -1.0, "progresso_m": 0.0})
	var minimo := INF
	var karts: Array = [kart]
	karts.append_array(pista.adversarios)
	for a in karts:
		for b in karts:
			if a != b: minimo = minf(minimo, a.position.distance_to(b.position))
	rel.distancia_minima_largada_m = minimo
	for quadro in 60 * 180:
		await physics_frame
		var todos := true
		for i in pista.adversarios.size():
			var ia: KartIA = pista.adversarios[i]
			var m: Dictionary = medidas[i]
			m.desvio_max_m = maxf(m.desvio_max_m, ia.desvio_percurso)
			if ia.desvio_percurso > 4.0: m.quadros_fora_asfalto += 1
			if ia.velocidade > 1.0 and (-ia.global_basis.z).dot(eixo.tangente(ia.progresso_percurso)) < 0.0: m.quadros_contramao += 1
			m.progresso_m = ia.distancia_percorrida
			if ia.distancia_percorrida >= eixo.curve.get_baked_length() and m.volta_segundos < 0.0: m.volta_segundos = (quadro + 1) / 60.0
			todos = todos and m.volta_segundos > 0.0
		if quadro % 60 == 0:
			var amostra: Dictionary = {"segundos": quadro / 60.0, "karts": []}
			for ia in pista.adversarios:
				amostra.karts.append({"nome":ia.name,"progresso_m":ia.distancia_percorrida,"velocidade":ia.velocidade,"desvio_m":ia.desvio_percurso,"faixa":ia.faixa_percurso,"posicao":str(ia.position)})
			rel.amostras.append(amostra)
		if todos: break
	rel.adversarios = medidas
	rel.aprovado_controles = rel.controles.no_piso and float(rel.controles.aceleracao.velocidade) > 20.0 and float(rel.controles.aceleracao.distancia_m) > 20.0 and absf(float(rel.controles.frenagem_velocidade)) < 1.0 and float(rel.controles.re_velocidade) < -7.0 and float(rel.controles.giro_re) < 0.0 and float(rel.controles.zebra.y_max) > 0.12 and float(rel.controles.zebra.y_min) < 0.0 and rel.controles.retorno_do_gramado.atravessou_asfalto
	rel.aprovado_voltas = true
	for m in medidas:
		rel.aprovado_voltas = rel.aprovado_voltas and m.volta_segundos > 0.0 and m.quadros_fora_asfalto == 0 and m.quadros_contramao == 0
	FileAccess.open(BASE + "validacao_pi001" + sufixo + ".json", FileAccess.WRITE).store_string(JSON.stringify(rel,"\t"))
	print("PI001_RESULTADO ", JSON.stringify(medidas))
	print("CONTROLES ", JSON.stringify(rel.controles))
	pista.free()
	current_scene = null
	quit(0 if rel.aprovado_voltas and rel.aprovado_controles else 2)
