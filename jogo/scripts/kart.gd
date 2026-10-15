class_name Kart
extends CharacterBody3D
## Direção arcade: W/S ou setas aceleram e freiam, A/D ou setas esterçam.

@export var definicao: DefinicaoPersonagem
@export var velocidade_maxima := 22.0
@export var velocidade_re := 8.0
@export var aceleracao := 12.0
@export var frenagem := 28.0
@export var atrito := 5.0
@export var giro_maximo := 2.2
@export var resposta_direcao := 5.0
@export var gravidade := 20.0

var velocidade := 0.0
var esterco := 0.0
var giro := 0.0
var aceleracao_atual := 0.0

@onready var visual: VisualKart = $Visual


func _ready() -> void:
	visual.montar(definicao if definicao else get_node("/root/Jogo").personagem_escolhido())


func _physics_process(delta: float) -> void:
	var entrada := Input.get_axis("frear", "acelerar")
	var direcao := Input.get_axis("direita", "esquerda")
	var anterior := velocidade

	if entrada > 0.0:
		velocidade = move_toward(velocidade, velocidade_maxima, (aceleracao if velocidade >= 0.0 else frenagem) * entrada * delta)
	elif entrada < 0.0:
		velocidade = move_toward(velocidade, -velocidade_re, (frenagem if velocidade > 0.0 else aceleracao * 0.6) * -entrada * delta)
	else:
		velocidade = move_toward(velocidade, 0.0, atrito * delta)

	esterco = move_toward(esterco, direcao, resposta_direcao * delta)
	# Sem velocidade não há giro; em ré o sentido se inverte. Em alta, o giro fica mais suave.
	var fator := clampf(velocidade / 5.0, -1.0, 1.0) * lerpf(1.0, 0.65, absf(velocidade) / velocidade_maxima)
	giro = esterco * giro_maximo * fator
	rotate_y(giro * delta)

	var plano := -global_basis.z * velocidade
	velocity.x = plano.x
	velocity.z = plano.z
	velocity.y = 0.0 if is_on_floor() else velocity.y - gravidade * delta
	move_and_slide()
	# Batidas reduzem a velocidade de verdade.
	velocidade = -global_basis.z.dot(Vector3(velocity.x, 0.0, velocity.z))

	aceleracao_atual = lerpf(aceleracao_atual, (velocidade - anterior) / delta, 1.0 - exp(-10.0 * delta))
	visual.atualizar(delta, velocidade, giro, aceleracao_atual, esterco, absf(velocidade) / velocidade_maxima)
