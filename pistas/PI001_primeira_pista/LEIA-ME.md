# PI001 — Primeira pista

Primeira pista, modelada em 16/10/2026 pelo **Blender MCP**, com base no [JPG fornecido](referencia/PI001_primeira_pista.jpg). O nome é provisório.

| Item | Definição |
| --- | --- |
| Identificador | PI001 |
| Nome | Primeira pista (provisório) |
| Tema e cenário | Base plana de grama; cenário detalhado a definir |
| Traçado e sentido da corrida | Circuito fechado extraído do JPG; guia em sentido anti-horário, provisório |
| Dimensões e largura da pista | Eixo de aproximadamente 395 × 227 m; extensão de 1.149 m; asfalto de 8 m e zebras de 0,8 m por lado |
| Largada, chegada e pontos de controle | Largada quadriculada provisória no centro da reta inferior; pontos de controle pendentes |
| Arquivo Blender | [blender/primeira_pista.blend](blender/primeira_pista.blend) |
| Cena na Godot | Integração pendente; a pista atual do jogo foi preservada |
| Estado | Modelo inicial criado; geometria e imagens de apresentação verificadas |

## Modelo e referência

A linha preta do JPG foi interpretada como **eixo da pista**. Como o desenho não contém medidas, adotou-se provisoriamente a escala de 0,6 m por pixel e a largura de 8 m. A ponta aguda superior direita foi encurtada e arredondada para acomodar a via; os demais cantos receberam suavização. O desenho original foi preservado e também está empacotado no `.blend`.

O arquivo contém asfalto com espessura, zebras vermelhas e brancas, linhas laterais, largada quadriculada, base de grama, eixo fechado editável e câmeras de topo e perspectiva. O eixo e a imagem de referência ficam ocultos inicialmente; podem ser ativados nas suas coleções. A geometria é estática: editar a guia não reconstrói automaticamente a malha.

- [Vista de cima](validacao/pista_topo.png).
- [Vista em perspectiva](validacao/pista_perspectiva.png).
- [Comparação do eixo e das bordas com o JPG](validacao/sobreposicao_tracado.png).
- [Validação do modelo](validacao/modelo_blender.json) e [dados do traçado](validacao/tracado_extraido.json).

As cinco malhas de pista e sinalização lateral foram verificadas: sem arestas abertas ou não manifold, sem faces degeneradas e com normais do topo voltadas para cima. As duas bordas do circuito não cruzam a si mesmas. Essa conferência não valida colisões, dirigibilidade ou IA na Godot, que ainda não foram integradas.

A sessão anterior do Blender foi preservada em `backups/sessao_antes_PI001_*.blend`. A criação e os renders foram executados na instância conectada via MCP; o script [`registros/extrair_tracado.py`](registros/extrair_tracado.py) faz apenas a análise do JPG.

## Organização

- `referencia/`: imagens, desenhos do traçado e modelos originais, com a origem e a licença registradas quando disponíveis.
- `blender/`: arquivo de trabalho da pista.
- `texturas/`: texturas e mapas específicos desta pista.
- `backups/`: cópias de segurança antes de mudanças nos arquivos de trabalho.
- `validacao/`: conferências de escala, colisão, percurso e aparência.
- `registros/`: histórico das alterações e scripts utilizados.

## Histórico

- 16/10/2026: estrutura de pastas criada. Aguardando referências e definição do traçado.
- 16/10/2026: JPG analisado; modelo inicial criado via Blender MCP e salvo em projeto próprio. Escala, largura, sentido e largada permanecem provisórios.
