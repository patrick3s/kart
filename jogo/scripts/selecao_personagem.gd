extends Node3D
## Tela de escolha: mostra o piloto girando sobre um pedestal.

@onready var vitrine: Node3D = $Vitrine
@onready var nome: Label = %Nome
@onready var descricao: Label = %Descricao
@onready var anterior: Button = %Anterior
@onready var proximo: Button = %Proximo
@onready var jogar: Button = %Jogar

@onready var circuito: OptionButton = %Circuito

var _visual: VisualKart

@onready var jogo := get_node("/root/Jogo")


func _ready() -> void:
	anterior.pressed.connect(_trocar.bind(-1))
	proximo.pressed.connect(_trocar.bind(1))
	jogar.pressed.connect(_jogar)
	var varios: bool = jogo.personagens.size() > 1
	anterior.visible = varios
	proximo.visible = varios
	circuito.selected = jogo.indice_pista
	_mostrar()
	jogar.grab_focus()


func _process(delta: float) -> void:
	vitrine.rotate_y(delta * 0.6)
	if _visual:
		_visual.atualizar(delta, 0.0, 0.0, 0.0, 0.0, 0.0)


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("ui_left"):
		_trocar(-1)
	elif evento.is_action_pressed("ui_right"):
		_trocar(1)


func _trocar(passo: int) -> void:
	jogo.indice_escolhido = posmod(jogo.indice_escolhido + passo, jogo.personagens.size())
	_mostrar()


func _mostrar() -> void:
	if _visual:
		_visual.queue_free()
	var definicao: DefinicaoPersonagem = jogo.personagem_escolhido()
	_visual = VisualKart.new()
	vitrine.add_child(_visual)
	_visual.montar(definicao)
	nome.text = definicao.nome
	descricao.text = definicao.descricao


func _jogar() -> void:
	jogo.indice_pista = circuito.selected
	get_tree().change_scene_to_file("res://pistas/primeira_pista/primeira_pista.tscn" if circuito.selected == 0 else "res://cenas/pista.tscn")
