extends Node3D

@onready var kart: Kart = $Kart
@onready var velocimetro: Label = %Velocimetro

var adversarios: Array[KartIA] = []


func _ready() -> void:
	_criar_adversarios()


func _process(_delta: float) -> void:
	velocimetro.text = "%d km/h" % roundi(absf(kart.velocidade) * 3.6)


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("voltar_menu"):
		get_tree().change_scene_to_file("res://cenas/selecao_personagem.tscn")


func _criar_adversarios() -> void:
	var jogo := get_node("/root/Jogo")
	# Primeiro os pilotos que o jogador não escolheu, depois repete o catálogo.
	var fichas: Array[DefinicaoPersonagem] = []
	for i in jogo.personagens.size():
		if i != jogo.indice_escolhido:
			fichas.append(jogo.personagens[i])
	if fichas.is_empty():
		fichas.append(jogo.personagem_escolhido())

	var cena := load("res://cenas/kart.tscn") as PackedScene
	var blocos := get_node_or_null("Blocos")
	var todos: Array[Kart] = [kart]
	var quantidade: int = jogo.quantidade_adversarios
	for i in quantidade:
		var no := cena.instantiate()
		no.set_script(KartIA)
		var ia: KartIA = no
		ia.name = "Adversario%d" % (i + 1)
		ia.definicao = fichas[i % fichas.size()]
		ia.sentido_horario = i % 3 == 2  # alguns vêm na contramão
		ia.agressividade = 0.25 + 0.15 * (i % 3)
		ia.velocidade_maxima *= 0.84 + 0.03 * (i % 4)
		ia.massa = 0.9 + 0.1 * (i % 3)
		# Na contramão, a largada fica entre as dos outros e numa faixa mais aberta.
		if ia.sentido_horario:
			ia.raio_circuito += 8.0
		var angulo := TAU * (i + (0.5 if ia.sentido_horario else 0.0)) / quantidade
		ia.transform = _largada(angulo, ia.raio_circuito, ia.sentido_horario, blocos)
		add_child(ia)
		adversarios.append(ia)
		todos.append(ia)
	for ia in adversarios:
		ia.presas = todos


## Ponto do circuito livre de blocos, olhando no sentido da volta.
func _largada(angulo: float, raio: float, horario: bool, blocos: Node) -> Transform3D:
	var sentido := -1.0 if horario else 1.0
	for tentativa in 12:
		var a := angulo + tentativa * 0.08
		var pos := Vector3(cos(a), 0.0, sin(a)) * raio
		var livre := true
		if blocos:
			for b in blocos.get_children():
				if Vector2(b.position.x - pos.x, b.position.z - pos.z).length() < 4.0:
					livre = false
					break
		if livre or tentativa == 11:
			var tangente := Vector3(-sin(a), 0.0, cos(a)) * sentido
			return Transform3D(Basis.looking_at(tangente, Vector3.UP), pos + Vector3.UP * 0.1)
	return Transform3D.IDENTITY
