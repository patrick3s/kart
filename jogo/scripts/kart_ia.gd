class_name KartIA
extends Kart
## Piloto controlado pelo computador. Usa a mesma física do jogador e só troca a
## entrada: segue um circuito em volta da arena, desvia de blocos, muros e karts com
## três raios à frente, dá ré quando enrosca e, de vez em quando, parte para cima
## do kart mais próximo para uma batida.

@export var raio_circuito := 60.0
## Amplitude da ondulação do circuito, para ele não ser um círculo perfeito.
@export var ondulacao := 12.0
@export var pontos_circuito := 32
@export var sentido_horario := false
## Distância em que o ponto atual do circuito é dado por alcançado.
@export var alcance_ponto := 10.0
## 0..1: chance de perseguir um kart próximo a cada sorteio.
@export var agressividade := 0.35
@export var alcance_perseguicao := 28.0

## Configurar antes de add_child: nulo conserva a arena antiga.
var percurso: Path3D
var progresso_percurso := 0.0
var distancia_percorrida := 0.0
var desvio_percurso := 0.0
var velocidade_alvo := 0.0
var faixa_percurso := 0.0
var presas: Array[Kart] = []

var _circuito: PackedVector3Array
var _indice := 0
var _fase := 0.0
var _presa: Kart
var _tempo_perseguicao := 0.0
var _espera_perseguicao := 2.0
var _tempo_enroscado := 0.0
var _tempo_re := 0.0
var _sentido_re := 0.0
var _sorteio := RandomNumberGenerator.new()


func _ready() -> void:
	super()
	_sorteio.randomize()
	_fase = _sorteio.randf() * TAU
	if percurso:
		progresso_percurso = percurso.curve.get_closest_offset(percurso.to_local(global_position))
	else:
		_circuito = _gerar_circuito()
		_indice = _ponto_a_frente()
	bateu.connect(_ao_bater)


func _gerar_circuito() -> PackedVector3Array:
	var pontos := PackedVector3Array()
	for i in pontos_circuito:
		var a := TAU * i / pontos_circuito * (-1.0 if sentido_horario else 1.0)
		var r := raio_circuito + ondulacao * sin(3.0 * a + _fase)
		pontos.append(Vector3(cos(a) * r, 0.0, sin(a) * r))
	return pontos


func _ponto_a_frente() -> int:
	var frente := -global_basis.z
	var melhor := 0
	var menor := INF
	for i in _circuito.size():
		var para := _circuito[i] - global_position
		para.y = 0.0
		# Pontos atrás custam o dobro, para o kart não dar meia-volta na largada.
		var custo := para.length() * (1.0 if para.dot(frente) > 0.0 else 2.0)
		if custo < menor:
			menor = custo
			melhor = i
	return melhor


func _entrada(delta: float) -> Vector2:
	if percurso:
		return _entrada_percurso(delta)
	var alvo := _escolher_alvo(delta)
	var para := alvo - global_position
	para.y = 0.0
	var frente := -global_basis.z
	frente.y = 0.0
	var angulo := frente.signed_angle_to(para, Vector3.UP)  # + = alvo à esquerda

	if _tempo_re > 0.0:
		_tempo_re -= delta
		return Vector2(-1.0, _sentido_re)

	var direcao := clampf(angulo * 2.0, -1.0, 1.0) + _desvio()
	var acelerador := 1.0
	if absf(angulo) > 1.2 and velocidade > 10.0:
		acelerador = 0.3

	# Acelerando sem sair do lugar: dá ré esterçando para o lado contrário, o que
	# vira o bico para o alvo.
	if velocidade < 1.5:
		_tempo_enroscado += delta
	else:
		_tempo_enroscado = 0.0
	if _tempo_enroscado > 1.0:
		_tempo_enroscado = 0.0
		_tempo_re = _sorteio.randf_range(0.8, 1.4)
		_sentido_re = -signf(angulo) if absf(angulo) > 0.1 else (1.0 if _sorteio.randf() < 0.5 else -1.0)

	return Vector2(acelerador, clampf(direcao, -1.0, 1.0))


func _escolher_alvo(delta: float) -> Vector3:
	if _presa:
		_tempo_perseguicao -= delta
		var distancia := global_position.distance_to(_presa.global_position)
		if _tempo_perseguicao <= 0.0 or distancia > alcance_perseguicao * 1.5:
			_largar_presa()
		else:
			# Mira onde a presa vai estar, não onde ela está.
			var t := distancia / maxf(velocidade, 6.0)
			return _presa.global_position + _presa.velocidade_plana() * t
	else:
		_espera_perseguicao -= delta
		if _espera_perseguicao <= 0.0:
			_espera_perseguicao = _sorteio.randf_range(2.0, 4.0)
			if _sorteio.randf() < agressividade:
				_presa = _presa_proxima()
				_tempo_perseguicao = 5.0

	var ponto := _circuito[_indice]
	if Vector2(ponto.x - global_position.x, ponto.z - global_position.z).length() < alcance_ponto:
		_indice = (_indice + 1) % _circuito.size()
		ponto = _circuito[_indice]
	return ponto


func _presa_proxima() -> Kart:
	var frente := -global_basis.z
	var melhor: Kart
	var menor := alcance_perseguicao
	for k in presas:
		if not is_instance_valid(k) or k == self:
			continue
		var para := k.global_position - global_position
		var d := para.length()
		if d < menor and frente.dot(para.normalized()) > 0.3:
			menor = d
			melhor = k
	return melhor


func _largar_presa() -> void:
	_presa = null
	_espera_perseguicao = _sorteio.randf_range(3.0, 6.0)


func _ao_bater(outro: Node, _intensidade: float) -> void:
	if outro == _presa:
		_largar_presa()


## Correção de direção (+ = esquerda) a partir de três raios à frente.
func _desvio() -> float:
	var espaco := get_world_3d().direct_space_state
	var origem := global_position + Vector3.UP * 0.5
	var frente := -global_basis.z
	frente.y = 0.0
	frente = frente.normalized()
	var alcance := 6.0 + maxf(velocidade, 0.0) * 0.6
	var excluir: Array[RID] = [get_rid()]
	if _presa:
		excluir.append(_presa.get_rid())
	var correcao := 0.0
	for lado in [-1.0, 0.0, 1.0]:
		var dir := frente.rotated(Vector3.UP, lado * 0.45)
		var consulta := PhysicsRayQueryParameters3D.create(origem, origem + dir * alcance)
		consulta.exclude = excluir
		var batida := espaco.intersect_ray(consulta)
		if batida.is_empty():
			continue
		var perto := 1.0 - origem.distance_to(batida.position) / alcance
		if lado == 0.0:
			# Obstáculo bem à frente: foge para o lado em que a superfície se inclina.
			var normal: Vector3 = batida.normal
			correcao += (1.0 if frente.cross(normal).y > 0.0 else -1.0) * perto * 1.5
		else:
			# Raio da esquerda (lado = +1 gira para a esquerda) acertou: vira para a direita.
			correcao -= lado * perto * 1.2
	return correcao


## Seguimento contínuo com antecipação de curvatura e frenagem pela distância.
## Não persegue presas nem usa desvios que apontem para fora do traçado.
func _entrada_percurso(_delta: float) -> Vector2:
	var curva := percurso.curve
	var comprimento := curva.get_baked_length()
	var local := percurso.to_local(global_position)
	var atual := curva.get_closest_offset(local)
	var avanco := wrapf(atual - progresso_percurso, -comprimento * 0.5, comprimento * 0.5)
	distancia_percorrida += avanco
	progresso_percurso = atual
	var centro := curva.sample_baked(atual)
	desvio_percurso = Vector2(local.x - centro.x, local.z - centro.z).length()
	# Ultrapassa karts parados somente se a outra faixa estiver livre.
	var eixo_frente := (_amostra_percurso(atual + 1.0) - _amostra_percurso(atual - 1.0)).normalized()
	var eixo_lado := eixo_frente.cross(Vector3.UP)
	for outro in presas:
		if not is_instance_valid(outro) or outro == self: continue
		var relativo := outro.global_position - global_position
		var distancia_frente := relativo.dot(eixo_frente)
		var faixa_outro := (outro.global_position - percurso.to_global(centro)).dot(eixo_lado)
		if distancia_frente > 0.0 and distancia_frente < 16.0 and absf(faixa_outro - faixa_percurso) < 1.6 and absf(outro.velocidade) < 3.0:
			var alternativa := -faixa_percurso
			var livre := true
			for vizinho in presas:
				if not is_instance_valid(vizinho) or vizinho == self: continue
				var v := vizinho.global_position - global_position
				var faixa_vizinho := (vizinho.global_position - percurso.to_global(centro)).dot(eixo_lado)
				if absf(v.dot(eixo_frente)) < 12.0 and absf(faixa_vizinho - alternativa) < 1.6:
					livre = false
			if livre: faixa_percurso = alternativa
	var antecipa := clampf(2.0 + absf(velocidade) * 0.32, 3.0, 8.0)
	var alvo := _amostra_percurso(atual + antecipa)
	var tangente := (_amostra_percurso(atual + antecipa + 1.0) - _amostra_percurso(atual + antecipa - 1.0)).normalized()
	alvo += tangente.cross(Vector3.UP) * faixa_percurso
	var para := alvo - global_position
	para.y = 0.0
	var angulo := (-global_basis.z).signed_angle_to(para.normalized(), Vector3.UP)
	velocidade_alvo = velocidade_maxima
	# Velocidade angular disponível e aderência limitam a velocidade na curva.
	for distancia in [0.0, 5.0, 10.0, 18.0, 28.0, 40.0]:
		var a := _amostra_percurso(atual + distancia)
		var b := _amostra_percurso(atual + distancia + 3.0)
		var c := _amostra_percurso(atual + distancia + 6.0)
		var curvatura := absf((b-a).signed_angle_to(c-b, Vector3.UP)) / 3.0
		var limite := minf(velocidade_maxima, sqrt(3.0 / maxf(curvatura, 0.001)))
		velocidade_alvo = minf(velocidade_alvo, sqrt(limite * limite + 2.0 * 12.0 * distancia))
	if absf(angulo) > 0.65 or desvio_percurso > 2.5:
		velocidade_alvo = minf(velocidade_alvo, 5.0)
	# Espaçamento medido ao longo da curva: funciona também nas curvas fechadas.
	for outro in presas:
		if not is_instance_valid(outro) or outro == self: continue
		var pos_outro := percurso.to_local(outro.global_position)
		var progresso_outro := curva.get_closest_offset(pos_outro)
		var longitudinal := wrapf(progresso_outro - atual, -comprimento * 0.5, comprimento * 0.5)
		if longitudinal <= 0.0 or longitudinal > 22.0: continue
		var centro_outro := _amostra_percurso(progresso_outro)
		var tangente_outro := (_amostra_percurso(progresso_outro+1.0) - _amostra_percurso(progresso_outro-1.0)).normalized()
		var faixa_obstaculo := (outro.global_position - centro_outro).dot(tangente_outro.cross(Vector3.UP))
		var minha_faixa := (global_position - percurso.to_global(centro)).dot(eixo_lado)
		if absf(faixa_obstaculo - minha_faixa) < 1.8:
			var saindo_da_faixa := absf(faixa_obstaculo - faixa_percurso) > 1.7
			var minima := 2.0 if saindo_da_faixa and longitudinal > 1.5 else 0.0
			var velocidade_outro := maxf(0.0, outro.velocidade_plana().dot(tangente_outro))
			velocidade_alvo = minf(velocidade_alvo, maxf(minima, velocidade_outro + (longitudinal - 8.0) * 0.8))
	var acelerador := clampf((velocidade_alvo - velocidade) * 1.5, -1.0, 1.0)
	return Vector2(acelerador, clampf(angulo * 2.2, -1.0, 1.0))


func _amostra_percurso(distancia: float) -> Vector3:
	return percurso.to_global(percurso.curve.sample_baked(fposmod(distancia, percurso.curve.get_baked_length())))
