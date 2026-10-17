class_name DefinicaoPersonagem
extends Resource
## Ficha de um personagem jogável. Para acrescentar um novo piloto, exporte o GLB
## com a mesma estrutura (ossos de corpo e cabeça + quatro rodas) e crie outra ficha.

@export var nome := ""
@export_multiline var descricao := ""
@export var modelo: PackedScene
## Fator aplicado ao modelo; o kart do Blender mede cerca de 1 unidade de comprimento.
@export var escala := 2.0
@export_group("Estrutura do modelo")
@export var osso_corpo := "Torso_Bone"
@export var osso_cabeca := "Head_Bone"
@export var rodas_dianteiras: Array[String] = ["Wheel_Front_Left", "Wheel_Front_Right"]
@export var rodas_traseiras: Array[String] = ["Wheel_Rear_Left", "Wheel_Rear_Right"]
## Raio das rodas em unidades do modelo. Zero usa a caixa de cada malha, que
## superestima o raio quando a banda de rodagem tem relevos.
@export var raio_rodas := 0.0
## Limite do giro da cabeça em relação ao corpo, em graus. Zero não limita.
@export var giro_maximo_cabeca := 0.0
