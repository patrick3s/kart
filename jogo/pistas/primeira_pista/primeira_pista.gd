extends "res://scripts/pista.gd"
## A arena compartilha kart, câmera e HUD; apenas a criação da corrida é substituída.

func _criar_adversarios() -> void:
	var jogo := get_node("/root/Jogo")
	var eixo: Path3D = $Percurso
	var cena := load("res://cenas/kart.tscn") as PackedScene
	var fichas: Array[DefinicaoPersonagem] = []
	for i in jogo.personagens.size():
		if i != jogo.indice_escolhido:
			fichas.append(jogo.personagens[i])
	for i in jogo.quantidade_adversarios:
		var no := cena.instantiate()
		no.set_script(KartIA)
		var ia: KartIA = no
		ia.name = "Adversario%d" % (i + 1)
		ia.definicao = fichas[i % fichas.size()]
		ia.percurso = eixo
		ia.sentido_horario = false
		ia.agressividade = 0.0
		ia.faixa_percurso = 1.0 if i % 2 == 0 else -1.0
		ia.altura_degrau = 0.28
		ia.velocidade_maxima = 18.0
		ia.transform = eixo.largada(i + 1)
		# _ready() já recebe posição, personagem e percurso corretos.
		add_child(ia)
		adversarios.append(ia)

	var todos: Array[Kart] = [kart]
	todos.append_array(adversarios)
	for ia in adversarios:
		ia.presas = todos
