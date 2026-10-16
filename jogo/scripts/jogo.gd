extends Node
## Autoload com o catálogo de personagens e a escolha atual.

var personagens: Array[DefinicaoPersonagem] = [
	preload("res://personagens/jake/jake.tres"),
	preload("res://personagens/dimi/dimi.tres"),
]
var indice_escolhido := 0
## Karts do computador na pista. As ferramentas de validação zeram para medir o piloto sozinho.
var quantidade_adversarios := 5


func personagem_escolhido() -> DefinicaoPersonagem:
	return personagens[indice_escolhido]
