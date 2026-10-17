# Barreiras encostadas na zebra — 17/10/2026

## Problema

Na primeira distribuição das barreiras, feita em 16/10/2026, o centro de cada módulo ficava a 6,5 m do eixo. Como a zebra termina a 4,8 m, sobrava uma faixa de cerca de 1,3 a 1,5 m de grama entre a zebra e a barreira, dos dois lados da pista. Nas curvas, a barreira chegava a ficar a 7,1 m do eixo. A pedida era que a barreira ficasse em cima da borda, e não afastada dela.

Medidas da pista, a partir do eixo (`PI001_Eixo_Editavel`):

| Elemento | Distância do eixo |
|---|---|
| Asfalto | 0 a 4,0 m |
| Zebra (interna e externa) | 4,0 a 4,8 m, com o topo em Z 0,145 |
| Barreira, antes | centro a 6,37–7,12 m; face a cerca de 6,1 m |
| Barreira, agora | face a 4,795 m, encostada na borda externa da zebra |

Das duas opções avaliadas, foi escolhida **barreira encostada na borda externa da zebra**, que mantém a zebra visível. A outra opção era colocar a barreira em cima da zebra.

## O que mudou

**Blender** ([`registros/posicionar_barreiras.py`](../../registros/posicionar_barreiras.py)):

- `AFASTAMENTO`: de 6,5 para **5,13 m**. O centro do módulo fica 0,33 m além da borda da zebra, que é metade da profundidade da barreira (0,65 m).
- `FOLGA_MIN`: de 5,6 para **4,75 m**. Nenhuma parte da frente do módulo pode invadir a zebra.
- **Recuo nas curvas côncavas:** nas curvas em S, a corda de um módulo reto corta para dentro e invadia a zebra em cerca de 0,14 m. Agora, cada módulo que invade é recuado para fora só o necessário, em até 3 iterações. Os demais continuam encostados.
- `ALTURA_CHAO` permanece em −0,1, o topo do gramado, porque a barreira fica na grama, ao lado da zebra.

Resultado do script: **319 módulos na borda interna e 338 na externa**, 657 no total. A menor folga entre a frente da barreira e o eixo é de 4,795 m. A escala longitudinal dos módulos vai de 0,94 a 1,00. O `.blend` foi salvo e o `jogo/pistas/primeira_pista/barreiras.json` foi regenerado.

**Godot:**

- O `construir_cenas.gd` recriou `primeira_pista.tscn` a partir do JSON novo. As barreiras ficam embutidas na cena, então esse passo é obrigatório depois de qualquer mudança no Blender.
- `validar_barreiras_pi001.gd`: `LIMITE` passou para `5.13 - 0.3`, e a saída agora vai para esta pasta.
- `capturar_barreiras_pi001.gd`: a saída agora vai para esta pasta. As evidências de 16/10, em `barreiras_20261016/`, foram preservadas.

## Validação

Física real a 60 Hz ([`validacao_barreiras.json`](validacao_barreiras.json)):

- **96/96 batidas contidas**, dos dois lados, em retas e curvas, em vários ângulos. O centro do kart chegou no máximo a **4,15 m** do eixo, ou seja, ele bate na barreira e para nela.
- **5/5 IAs completaram a volta**, entre 84,1 e 91,8 s, com **0 quadros fora do asfalto** e desvio máximo de 1,30 m do percurso. A IA não foi alterada.

Capturas no renderizador real (Metal / Forward+):

- [`largada_barreiras.png`](largada_barreiras.png): na largada, as barreiras aparecem coladas na zebra dos dois lados.
- [`reta_barreiras.png`](reta_barreiras.png): na reta em movimento, a 79 km/h.
- [`batida_barreiras.png`](batida_barreiras.png): numa curva, com as barreiras acompanhando a zebra pela borda interna e pela externa.
- [`vista_geral_barreiras.png`](vista_geral_barreiras.png): vista ortográfica de cima.

## Limitações e observações

- Apesar do nome, a captura `batida_barreiras.png` mostra o kart andando numa curva, e não o instante do impacto. A contenção das batidas está comprovada pelo teste de física, não por imagem.
- A posição foi validada por inspeção visual e pelo teste de física. Não foi feita medição vértice a vértice. Essa medição, rodada via MCP, travou o Blender e foi abandonada.
- Nas curvas côncavas, os módulos recuados podem ficar até cerca de 0,14 m afastados da zebra, para não invadi-la.

## Como refazer

1. Com o `.blend` aberto no Blender MCP, execute `registros/posicionar_barreiras.py` e salve. Para mudar a posição, ajuste `AFASTAMENTO` e `FOLGA_MIN`.
2. `godot --headless --path jogo --script res://ferramentas/construir_cenas.gd`
3. `godot --headless --path jogo --script res://ferramentas/validar_barreiras_pi001.gd` deve sair com código 0. Se o afastamento mudar, atualize o `LIMITE`.
4. `godot --path jogo --script res://ferramentas/capturar_barreiras_pi001.gd`, sem `--headless`.

Backup do `.blend` antes desta mudança: `backups/primeira_pista_antes_barreira_na_borda_20261017.blend`.
