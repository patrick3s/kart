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
| Cena na Godot | [primeira_pista.tscn](../../jogo/pistas/primeira_pista/primeira_pista.tscn), selecionada por padrão no menu; arena disponível para testes |
| Estado | Integração jogável; importação, controles, IA e regressões executados; capturas do jogo conferidas |

## Modelo e referência

A linha preta do JPG foi interpretada como **eixo da pista**. Como o desenho não contém medidas, adotou-se provisoriamente a escala de 0,6 m por pixel e a largura de 8 m. A ponta aguda superior direita foi encurtada e arredondada para acomodar a via; os demais cantos receberam suavização. O desenho original foi preservado e também está empacotado no `.blend`.

O arquivo contém asfalto com espessura, zebras vermelhas e brancas, linhas laterais, largada quadriculada, base de grama, eixo fechado editável e câmeras de topo e perspectiva. O eixo e a imagem de referência ficam ocultos inicialmente; podem ser ativados nas suas coleções. A geometria é estática: editar a guia não reconstrói automaticamente a malha.

- [Vista de cima](validacao/pista_topo.png).
- [Vista em perspectiva](validacao/pista_perspectiva.png).
- [Comparação do eixo e das bordas com o JPG](validacao/sobreposicao_tracado.png).
- [Validação do modelo](validacao/modelo_blender.json) e [dados do traçado](validacao/tracado_extraido.json).

As cinco malhas de pista e sinalização lateral foram verificadas: sem arestas abertas ou não manifold, sem faces degeneradas e com normais do topo voltadas para cima. As duas bordas do circuito não cruzam a si mesmas. Essa conferência inicial validou somente o modelo. A integração e os ensaios posteriores na Godot estão descritos abaixo.

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

## Integração jogável — 16/10/2026

No menu, escolha o piloto, mantenha **PI001 — Primeira pista** e pressione **Jogar**. O seletor também oferece **Arena de testes**, com a IA circular anterior. W/↑ acelera, S/↓ freia e dá ré, A/D ou ←/→ esterça, Esc volta ao menu.

Os recursos estão em [`jogo/pistas/primeira_pista/`](../../jogo/pistas/primeira_pista/): GLB com sete malhas, materiais equivalentes, cena com colisões estáticas, eixo fechado e grid alinhado à reta. A IA usa esse eixo e antecipa curvas; percurso e parâmetros são configurados antes da entrada dos adversários na árvore. Asfalto e gramado usam um shader procedural da Godot; as cores das zebras e da sinalização vêm do GLB. Escala 1:1 e geometria original preservadas. O gerador de cenas inclui a PI001 e não apaga a integração.

**Validação por código:** importação e scripts na Godot 4.7.2, aceleração, frenagem, ré, giro, travessia de zebras, retorno do gramado, contato dos pneus e colisões entre os três personagens. Cinco adversários completaram uma volta em cada uma das três escolhas de jogador, com 0 quadros fora do asfalto e 0 em contramão; tempos entre 84,10 e 91,82 s. As regressões de rodas, suspensão, cabeça e câmera passaram. Os relatórios históricos permanecem preservados.

**Conferência visual:** jogo aberto com Metal / Forward+; capturas do viewport inspecionadas para menu, largada, materiais, escala, câmera, movimento e pneus dos três personagens. O ensaio dos comandos usou Input automatizado, sem pilotagem manual de uma volta inteira.

Consulte o [relatório de integração](validacao/integracao_20261016/RELATORIO.md), a [telemetria da volta](validacao/integracao_20261016/validacao_pi001.json), a [largada renderizada](validacao/integracao_20261016/largada_pi001.png) e a [vista geral](validacao/integracao_20261016/vista_geral_pi001.png). A pasta também contém as outras duas escolhas de jogador, regressões, medições dos pneus, colisões, logs, hashes e tentativas iniciais.

**Limitações:** materiais equivalentes não reproduzem exatamente o bump do Blender; suspensão permanece visual e os pneus penetram cerca de 6–10 mm no piso. Escala, sentido e largada continuam provisórios. Cenário definitivo, aprovação artística e regras de corrida (cronômetro/classificação/checkpoints) permanecem por definir. Não há etapa técnica bloqueando o uso da pista nos ensaios realizados.

- 16/10/2026: exportação via Blender MCP e integração jogável concluídas, com preservação do `.blend`/JPG por hash, arena histórica disponível e evidências separadas da modelagem inicial.

## Barreiras nas bordas — 16/10/2026

O módulo [barreira reta vermelha e branca](../../ambiente/modelos/barreiras/barreira_reta_vermelha_branca/LEIA-ME.md) foi distribuído pelo Blender MCP nas duas bordas: 317 módulos na borda interna e 340 na externa, com o centro a 6,5 m do eixo. Isso deixa cerca de 1,2 m de grama entre a zebra e a barreira. Ficam na coleção `PI001_07_Barreiras` do `.blend`, como instâncias ligadas de uma única malha. Nas curvas fechadas, os trechos que invadiriam a pista são removidos. Script: [`registros/posicionar_barreiras.py`](registros/posicionar_barreiras.py). Backup antes da mudança: `backups/primeira_pista_antes_barreiras_20261016.blend`.

Na Godot, `construir_cenas.gd` lê `jogo/pistas/primeira_pista/barreiras.json` e cria o nó `Barreiras`, com visual e colisão por módulo. Validação ([`validacao/barreiras_20261016/`](validacao/barreiras_20261016/)): 96/96 batidas contidas, dos dois lados, em retas e curvas. As cinco IAs completaram a volta sem sair do asfalto, nos mesmos tempos anteriores. Ferramentas: `validar_barreiras_pi001.gd` e `capturar_barreiras_pi001.gd`.

### Barreiras encostadas na zebra — 17/10/2026

A faixa de grama entre a zebra e a barreira foi eliminada. O `AFASTAMENTO` passou de 6,5 para 5,13 m, e agora a face da barreira encosta na borda externa da zebra, a 4,8 m do eixo. Nas curvas em S, os módulos que invadiriam a zebra são recuados só o necessário. Ficaram 319 módulos na borda interna e 338 na externa. A validação na Godot conteve 96/96 batidas, com o kart chegando no máximo a 4,15 m do eixo, e as cinco IAs completaram a volta sem sair do asfalto. Detalhes e evidências estão no [relatório](validacao/barreiras_20261017/RELATORIO.md). Backup: `backups/primeira_pista_antes_barreira_na_borda_20261017.blend`.
