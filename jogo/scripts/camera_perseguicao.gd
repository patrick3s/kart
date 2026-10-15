extends Camera3D
## Câmera atrás do kart: o giro segue com atraso (mostra a lateral nas curvas),
## a distância e o FOV crescem com a velocidade e a imagem acompanha levemente a
## inclinação e a vibração da suspensão.

@export var alvo: Kart
@export var distancia := 3.4
@export var distancia_extra := 1.2
@export var altura := 1.4
@export var altura_extra := 0.3
@export var suavidade_giro := 4.0
@export var suavidade_distancia := 3.0
@export var fov_base := 68.0
@export var fov_extra := 14.0
@export var acompanhamento_rolagem := 0.15

var _giro := 0.0
var _fator := 0.0


func _ready() -> void:
	top_level = true
	_giro = alvo.global_rotation.y
	_posicionar()


func _physics_process(delta: float) -> void:
	_giro = lerp_angle(_giro, alvo.global_rotation.y, 1.0 - exp(-suavidade_giro * delta))
	_fator = lerpf(_fator, absf(alvo.velocidade) / alvo.velocidade_maxima, 1.0 - exp(-suavidade_distancia * delta))
	_posicionar()
	var vis := alvo.visual
	rotate_object_local(Vector3.BACK, -vis.rolagem * acompanhamento_rolagem)
	h_offset = vis.vibracao * 2.0 * sin(Time.get_ticks_msec() * 0.05)
	fov = fov_base + fov_extra * _fator


func _posicionar() -> void:
	var atras := Vector3(sin(_giro), 0.0, cos(_giro))
	global_position = alvo.global_position + atras * (distancia + distancia_extra * _fator) + Vector3.UP * (altura + altura_extra * _fator)
	look_at(alvo.global_position + Vector3.UP * 0.8 - atras * 2.0)
