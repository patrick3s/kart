# Pistas na Godot

Crie uma subpasta por pista, como `nome_da_pista/`, para a cena `.tscn`, os modelos exportados e os materiais utilizados pelo jogo.

Referências, arquivos Blender, backups e registros de produção ficam em [`pistas/`](../../pistas/LEIA-ME.md), fora do projeto Godot.

A PI001 está em [`primeira_pista/primeira_pista.tscn`](primeira_pista/primeira_pista.tscn), disponível por padrão no menu. A arena original continua em `res://cenas/pista.tscn`, acessível como “Arena de testes”.

O gerador `res://ferramentas/construir_cenas.gd` recria ambas e o seletor. Recursos, percurso e materiais da PI001 ficam em `primeira_pista/`; evidências e limitações estão no [relatório de integração](../../pistas/PI001_primeira_pista/validacao/integracao_20261016/RELATORIO.md).


Para criar outra pista, use o [prompt de nova pista](../../documentacao/PROMPT_NOVA_PISTA.md) e a [receita](../../documentacao/RECEITA_PISTA.md). A nova cena deve usar o eixo real para a IA, preservar as pistas existentes no menu e fazer parte do gerador. Adapte caminhos e destinos das ferramentas da PI001 antes de reutilizá-las; seus relatórios pertencem à versão auditada da primeira pista.
