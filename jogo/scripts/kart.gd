class_name Kart
extends CharacterBody3D
## Direção arcade: W/S ou setas aceleram e freiam, A/D ou setas esterçam.
## Choques com outros karts trocam impulso (massa e restituição), empurram de lado,
## fazem o kart rodar conforme o ponto de contato e soltam faíscas.

signal bateu(outro: Node, intensidade: float)

@export var definicao: DefinicaoPersonagem
@export var velocidade_maxima := 22.0
@export var velocidade_re := 8.0
@export var aceleracao := 12.0
@export var frenagem := 28.0
@export var atrito := 5.0
@export var giro_maximo := 2.2
@export var resposta_direcao := 5.0
@export var gravidade := 20.0
## Ativado pela PI001 para transpor zebras e o desnível de 20 cm do gramado.
@export var altura_degrau := 0.0
@export_group("Colisão")
@export var massa := 1.0
## Fração da velocidade de aproximação devolvida num choque entre karts.
@export var restituicao_karts := 0.55
## Velocidade mínima com que dois karts se afastam depois de um choque (efeito "bate-bate").
@export var separacao_minima := 3.0
@export var restituicao_muros := 0.3
## Abaixo desta velocidade contra muros e blocos, o kart só desliza, como antes.
@export var velocidade_quique_muro := 4.0
## Quanto o pneu segura o empurrão lateral (1/s); menor = escorrega mais.
@export var aderencia := 3.5
@export var amortecimento_rodada := 2.5
@export var rodada_maxima := 7.0

var velocidade := 0.0
var esterco := 0.0
var giro := 0.0
var aceleracao_atual := 0.0
## Velocidade horizontal fora do eixo do kart, vinda de batidas; some com a aderência.
var empurrao := Vector3.ZERO
## Giro em Y (rad/s) causado por batidas, somado ao da direção.
var rodada := 0.0
## 0..1, decai sozinho; a câmera usa para tremer.
var tremor := 0.0

@onready var visual: VisualKart = $Visual


func _ready() -> void:
	visual.montar(definicao if definicao else get_node("/root/Jogo").personagem_escolhido())


## x = acelerador (-1 freia/ré .. 1 acelera); y = direção (+ = esquerda).
func _entrada(_delta: float) -> Vector2:
	return Vector2(Input.get_axis("frear", "acelerar"), Input.get_axis("direita", "esquerda"))


func _physics_process(delta: float) -> void:
	var comando := _entrada(delta)
	var entrada := comando.x
	var direcao := comando.y
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
	rotate_y((giro + rodada) * delta)
	rodada *= exp(-amortecimento_rodada * delta)
	empurrao *= exp(-aderencia * delta)
	tremor = move_toward(tremor, 0.0, 2.5 * delta)

	var antes := velocidade_plana()
	velocity.x = antes.x
	velocity.z = antes.z
	velocity.y = 0.0 if is_on_floor() else velocity.y - gravidade * delta
	_transpor_degrau(delta)
	move_and_slide()

	if not _resolver_choques(antes):
		# Batidas reduzem a velocidade de verdade; o que sobra de lado vira empurrão.
		_decompor(Vector3(velocity.x, 0.0, velocity.z))

	aceleracao_atual = lerpf(aceleracao_atual, (velocidade - anterior) / delta, 1.0 - exp(-10.0 * delta))
	visual.atualizar(delta, velocidade, giro, aceleracao_atual, esterco, absf(velocidade) / velocidade_maxima)


func velocidade_plana() -> Vector3:
	var frente := -global_basis.z
	return Vector3(frente.x, 0.0, frente.z).normalized() * velocidade + empurrao


## Separa uma velocidade horizontal em avanço (eixo do kart) e empurrão lateral.
func _decompor(v: Vector3) -> void:
	var frente := -global_basis.z
	frente = Vector3(frente.x, 0.0, frente.z).normalized()
	velocidade = clampf(frente.dot(v), -velocidade_maxima, velocidade_maxima * 1.2)
	empurrao = (v - frente * frente.dot(v)).limit_length(velocidade_maxima)


## Aplica um impulso (variação de velocidade em m/s) no ponto dado, em coordenadas globais.
func receber_impulso(dv: Vector3, ponto: Vector3) -> void:
	dv.y = 0.0
	_decompor(velocidade_plana() + dv)
	_girar_por(dv, ponto)
	_sacudir(dv)


func _girar_por(dv: Vector3, ponto: Vector3) -> void:
	# Caixa de 1,3 × 2 m: inércia por unidade de massa ≈ (l² + c²) / 12.
	var r := ponto - global_position
	r.y = 0.0
	rodada = clampf(rodada + r.cross(dv).y / 0.47, -rodada_maxima, rodada_maxima)


func _sacudir(dv: Vector3) -> void:
	var forca := dv.length()
	tremor = minf(1.0, tremor + forca / 12.0)
	visual.impacto(global_basis.inverse() * dv)


## Devolve true quando houve choque com quique e a velocidade já foi definida.
func _resolver_choques(antes: Vector3) -> bool:
	var v := antes
	var houve := false
	for i in get_slide_collision_count():
		var colisao := get_slide_collision(i)
		var normal := colisao.get_normal()
		if normal.y > 0.7:
			continue  # chão
		normal.y = 0.0
		normal = normal.normalized()
		var ponto := colisao.get_position()
		var outro := colisao.get_collider()
		if colisao.get_collider() is Kart:
			var outro_kart := colisao.get_collider() as Kart
			var vb := outro_kart.velocidade_plana()
			var aproximacao := (v - vb).dot(normal)  # a normal aponta do outro para este
			if aproximacao >= 0.0:
				continue
			var separacao := maxf(-aproximacao * restituicao_karts, separacao_minima)
			var j := (separacao - aproximacao) / (1.0 / massa + 1.0 / outro_kart.massa)
			var dv := normal * (j / massa)
			v += dv
			_girar_por(dv, ponto)
			_sacudir(dv)
			outro_kart.receber_impulso(-normal * (j / outro_kart.massa), ponto)
			Efeitos.faiscas(get_parent(), ponto, normal, -aproximacao)
			bateu.emit(outro, -aproximacao)
			outro_kart.bateu.emit(self, -aproximacao)
			houve = true
		else:
			var contra := v.dot(normal)
			if contra > -velocidade_quique_muro:
				continue
			var dv := -normal * contra * (1.0 + restituicao_muros)
			v += dv
			_girar_por(dv * 0.5, ponto)
			_sacudir(dv)
			Efeitos.faiscas(get_parent(), ponto, normal, -contra)
			bateu.emit(outro, -contra)
			houve = true
	if houve:
		_decompor(v)
	return houve


func _transpor_degrau(delta: float) -> void:
	if altura_degrau <= 0.0 or not is_on_floor():
		return
	var movimento := Vector3(velocity.x, 0.0, velocity.z) * delta
	var choque := KinematicCollision3D.new()
	if not test_move(global_transform, movimento, choque):
		return
	if choque.get_collider() is Kart or absf(choque.get_normal().y) > 0.5:
		return
	var elevado := global_transform
	elevado.origin.y += altura_degrau
	if not test_move(elevado, movimento):
		global_position.y += altura_degrau
