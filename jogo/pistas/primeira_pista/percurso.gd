class_name PercursoPI001
extends Path3D
## Eixo do .blend, conferido contra tracado_extraido.json. Não altera escala.

func _init() -> void:
	var dados: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://pistas/primeira_pista/percurso.json"))
	curve = Curve3D.new()
	curve.bake_interval = 0.5
	for p in dados.pontos:
		curve.add_point(Vector3(p[0], p[1], p[2]))
	curve.add_point(curve.get_point_position(0))


func ponto(distancia: float) -> Vector3:
	return curve.sample_baked(fposmod(distancia, curve.get_baked_length()))


func tangente(distancia: float) -> Vector3:
	return (ponto(distancia + 0.5) - ponto(distancia - 0.5)).normalized()


func largada(indice: int) -> Transform3D:
	# Seis posições, duas colunas; a primeira fila fica antes da faixa.
	var d := -6.0 - floori(indice / 2.0) * 7.0
	var frente := tangente(d)
	var lado := frente.cross(Vector3.UP)
	var pos := ponto(d) + lado * (-1.25 if indice % 2 == 0 else 1.25)
	pos.y += 0.04
	return Transform3D(Basis.looking_at(frente), pos)
