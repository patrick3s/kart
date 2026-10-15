class_name VisualKart
extends Node3D
## Monta o modelo do personagem e anima rodas, suspensão, vibração e cabeça.
##
## Convenções no espaço do modelo (o GLB olha para +Z):
## - rolagem positiva = carroceria pende para a direita do piloto;
## - arfagem positiva = bico mergulha.

@export_group("Suspensão")
@export var rigidez := 90.0
@export var amortecimento := 11.0
## Radianos de rolagem por m/s² de aceleração lateral.
@export var ganho_rolagem := 0.012
## Radianos de arfagem por m/s² de aceleração longitudinal.
@export var ganho_arfagem := 0.008
@export var rolagem_maxima := deg_to_rad(14.0)
@export var arfagem_maxima := deg_to_rad(6.0)
@export_group("Vibração")
## Amplitude (unidades do modelo) com o motor parado e em velocidade máxima.
@export var vibracao_parado := 0.0015
@export var vibracao_maxima := 0.007
@export var rolagem_vibracao := deg_to_rad(0.8)
@export_group("Cabeça")
## A cabeça gira no sentido inverso da suspensão; 1.0 apenas cancela a rolagem.
@export var compensacao_cabeca := 1.7
@export var rigidez_cabeca := 55.0
@export var amortecimento_cabeca := 7.0
## Fração mínima da inclinação do corpo que a cabeça mantém do lado oposto em todo
## quadro, mesmo enquanto a mola ainda não chegou (0.2 = 20% da inclinação do corpo).
@export var oposicao_minima_cabeca := 0.2
## Fração máxima: limita o quanto a cabeça pode passar do lado oposto. Faz a cabeça
## cruzar o centro junto com o corpo, sem saltar de um lado para o outro.
@export var oposicao_maxima_cabeca := 1.0
@export_group("Rodas")
@export var esterco_maximo := deg_to_rad(28.0)

var rolagem := 0.0
var arfagem := 0.0
var vibracao := 0.0

var _vel_rolagem := 0.0
var _vel_arfagem := 0.0
var _cabeca := 0.0
var _vel_cabeca := 0.0
var _limite_cabeca := 0.0
var _tempo := 0.0
var _esqueleto: Skeleton3D
var _osso_corpo := -1
var _osso_cabeca := -1
var _rodas: Array[Dictionary] = []
var _ruido := FastNoiseLite.new()


## Deve ser chamado com o nó já na árvore.
func montar(definicao: DefinicaoPersonagem) -> void:
	scale = Vector3.ONE * definicao.escala
	_limite_cabeca = deg_to_rad(definicao.giro_maximo_cabeca)
	var modelo := definicao.modelo.instantiate() as Node3D
	modelo.rotation.y = PI  # o kart anda para -Z, padrão da Godot
	add_child(modelo)

	_esqueleto = modelo.find_children("*", "Skeleton3D", true, false)[0]
	_osso_corpo = _esqueleto.find_bone(definicao.osso_corpo)
	_osso_cabeca = _esqueleto.find_bone(definicao.osso_cabeca)

	# No Blender as rodas acompanham o osso do corpo; aqui elas saem do esqueleto
	# para ficarem no chão enquanto a carroceria inclina sobre a suspensão.
	var base := INF
	var para_modelo := modelo.global_transform.affine_inverse()
	for nome in definicao.rodas_dianteiras + definicao.rodas_traseiras:
		var malha := modelo.find_child(nome, true, false) as MeshInstance3D
		var aabb := malha.get_aabb()
		var raio := definicao.raio_rodas if definicao.raio_rodas > 0.0 else maxf(aabb.size.y, aabb.size.z) * 0.5
		var pivo := Node3D.new()
		pivo.name = nome + "_Pivo"
		pivo.position = para_modelo * malha.global_position
		modelo.add_child(pivo)
		malha.reparent(pivo, false)
		malha.transform = Transform3D.IDENTITY
		base = minf(base, pivo.position.y - raio)
		_rodas.append({pivo = pivo, malha = malha, raio = raio, dianteira = nome in definicao.rodas_dianteiras})
	modelo.position.y = -base

	_ruido.seed = randi()
	_ruido.frequency = 1.0


## velocidade: m/s para a frente; giro: rad/s em Y (+ = esquerda);
## aceleracao: m/s² longitudinal; esterco: -1..1 (+ = esquerda); fator_velocidade: 0..1.
func atualizar(delta: float, velocidade: float, giro: float, aceleracao: float, esterco: float, fator_velocidade: float) -> void:
	if _esqueleto == null:
		return
	_tempo += delta

	# Inércia: numa curva para a esquerda a aceleração centrípeta aponta para a
	# esquerda, então a carroceria pende para a direita (e vice-versa).
	var aceleracao_lateral := giro * velocidade
	var alvo_rolagem := clampf(ganho_rolagem * aceleracao_lateral, -rolagem_maxima, rolagem_maxima)
	var alvo_arfagem := clampf(-ganho_arfagem * aceleracao, -arfagem_maxima, arfagem_maxima)
	_vel_rolagem += (rigidez * (alvo_rolagem - rolagem) - amortecimento * _vel_rolagem) * delta
	_vel_arfagem += (rigidez * (alvo_arfagem - arfagem) - amortecimento * _vel_arfagem) * delta
	rolagem += _vel_rolagem * delta
	arfagem += _vel_arfagem * delta

	# Vibração do motor e do piso, mais forte e mais rápida com a velocidade.
	vibracao = lerpf(vibracao_parado, vibracao_maxima, fator_velocidade)
	var t := _tempo * lerpf(12.0, 35.0, fator_velocidade)
	var salto := vibracao * _ruido.get_noise_1d(t)
	var tremor := rolagem_vibracao * fator_velocidade * _ruido.get_noise_1d(t + 500.0)

	var rolagem_total := rolagem + tremor
	var giro_corpo := Basis(Vector3.BACK, rolagem_total) * Basis(Vector3.RIGHT, arfagem)
	_girar_osso(_osso_corpo, giro_corpo)
	_esqueleto.set_bone_pose_position(_osso_corpo, _esqueleto.get_bone_rest(_osso_corpo).origin + Vector3(0, salto, 0))

	# A cabeça busca o lado inverso da inclinação total (com o tremor), com um
	# pequeno atraso de mola. A cabeça herda a inclinação do corpo, então a global
	# é rolagem_total + _cabeca.
	var alvo_cabeca := -compensacao_cabeca * rolagem_total
	_vel_cabeca += (rigidez_cabeca * (alvo_cabeca - _cabeca) - amortecimento_cabeca * _vel_cabeca) * delta
	_cabeca += _vel_cabeca * delta
	# Em todo quadro a global fica do lado oposto ao corpo, entre as frações mínima e
	# máxima da inclinação dele; a velocidade que insiste contra a faixa é descartada.
	var perto := -(1.0 + oposicao_minima_cabeca) * rolagem_total
	var longe := -(1.0 + oposicao_maxima_cabeca) * rolagem_total
	var limitada := clampf(_cabeca, minf(perto, longe), maxf(perto, longe))
	if limitada != _cabeca:
		_vel_cabeca = 0.0 if signf(_vel_cabeca) == signf(_cabeca - limitada) else _vel_cabeca
		_cabeca = limitada
	if _limite_cabeca > 0.0 and absf(_cabeca) > _limite_cabeca:
		_cabeca = signf(_cabeca) * _limite_cabeca
		_vel_cabeca = 0.0
	_girar_osso(_osso_cabeca, Basis(Vector3.BACK, _cabeca) * Basis(Vector3.RIGHT, -arfagem))

	for roda in _rodas:
		var malha: Node3D = roda.malha
		malha.rotate_x(velocidade / scale.x / roda.raio * delta)
		if roda.dianteira:
			roda.pivo.rotation.y = esterco * esterco_maximo


## Aplica uma rotação expressa no espaço do esqueleto em torno da origem do osso.
func _girar_osso(osso: int, rotacao: Basis) -> void:
	var pai := _esqueleto.get_bone_parent(osso)
	var p := Basis() if pai < 0 else _esqueleto.get_bone_global_rest(pai).basis.orthonormalized()
	var local := _esqueleto.get_bone_rest(osso).basis.orthonormalized()
	_esqueleto.set_bone_pose_rotation(osso, (p.inverse() * rotacao * p * local).get_rotation_quaternion())
