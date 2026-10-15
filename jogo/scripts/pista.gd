extends Node3D

@onready var kart: Kart = $Kart
@onready var velocimetro: Label = %Velocimetro


func _process(_delta: float) -> void:
	velocimetro.text = "%d km/h" % roundi(absf(kart.velocidade) * 3.6)


func _unhandled_input(evento: InputEvent) -> void:
	if evento.is_action_pressed("voltar_menu"):
		get_tree().change_scene_to_file("res://cenas/selecao_personagem.tscn")
