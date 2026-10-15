# Registro — Fase 8 — personagem jogável e mecânicas — P002 Dimi

Data: 15/10/2026 (−03:00). Ferramenta: Godot 4.7.2.stable pela CLI (`--headless` para as medições; com janela, Metal/Forward+, para as imagens). Pedido do usuário: “inicie a fase 8 do dimi”. O Blender não foi usado e `dimi.blend` não mudou (SHA-256 `e28bf878…49e1`).

## 1. Estado de entrada

- `dimi_kart.glb` com SHA-256 `2b25281b…e606258b`, igual ao da Fase 7; `.import` sem mudança.
- Catálogo `scripts/jogo.gd` só com o Jake. Pendência herdada: `visual_kart.gd` media o raio das rodas pela caixa da malha (RL 0,1429 contra 0,1297).

## 2. Alterações no jogo

| Arquivo | Mudança | Efeito no Jake |
| --- | --- | --- |
| `jogo/personagens/dimi/dimi.tres` (novo) | Ficha `DefinicaoPersonagem`: nome “Dimi”, `escala = 2.0`, `raio_rodas = 0.1297`, `giro_maximo_cabeca = 25.0` | — |
| `jogo/scripts/jogo.gd` | Dimi acrescentado **depois** do Jake no catálogo | Jake continua no índice 0 |
| `jogo/scripts/definicao_personagem.gd` | Campos opcionais `raio_rodas` e `giro_maximo_cabeca`; zero mantém o comportamento anterior | Nenhum (a ficha do Jake não usa os campos) |
| `jogo/scripts/visual_kart.gd` | Usa `raio_rodas` quando a ficha informa; limita `_cabeca` a `giro_maximo_cabeca` e zera a velocidade da mola no limite | Nenhum |

**Por que o raio fixo:** as bolinhas da banda inflam a caixa da malha. Com 0,1297, giro e apoio usam o círculo da banda medido na Fase 4. As quatro bandas ficaram exatamente no chão (`altura_banda_no_chao` ≤ 3e-8). O modelo sobe 1,77 mm, porque o pivô medido fica a 0,1279 m. Como registrado na Fase 4, as bolinhas passam até 2,5 cm abaixo do chão durante o giro.

**Por que o teto de 25°:** o checkpoint registrava que o teto da Fase 6 valia também para a compensação. Sem o limite, a primeira execução mediu **32,74°** de giro relativo da cabeça no percurso real, a 22 m/s, no pico da mola ao inverter a curva. A meta estabilizada é 1,7 × 14° = 23,8°. Com o teto, o máximo ficou em 25,0°. O limite só corta o excesso da mola e não muda o sinal da cabeça, por isso não altera as contagens de quadros “no mesmo lado”.

**Atenção:** o teto da Fase 6 foi medido para o giro em **Y** (olhar para os lados). No jogo, a cabeça **inclina** em torno do eixo da frente (rolagem) e acompanha a arfagem. Ela não gira em Y. Aplicar o mesmo valor à inclinação é a interpretação adotada aqui, não uma medida da abertura da base nessa direção (ver seção 5).

## 3. Verificador e comandos

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --fixed-fps 60 --script res://ferramentas/validar_mecanicas_dimi.gd
/Applications/Godot.app/Contents/MacOS/Godot --path jogo --fixed-fps 60 --script res://ferramentas/capturar_vistas_dimi.gd
```

O primeiro grava [`validacao_mecanicas_fase8.json`](../validacao/validacao_mecanicas_fase8.json) e o segundo, as imagens em [`vistas_fase8/`](vistas_fase8/). Nenhum dos dois altera scripts, cenas ou fichas. O verificador segue o do Jake e acrescenta a troca de piloto, frenagem, ré, parada, atraso da câmera, apoio das rodas, teto da cabeça e um trecho “parada” depois das curvas.

## 4. Resultados no motor (relatório final, com o teto)

| Verificação | Resultado |
| --- | --- |
| Catálogo | `["Jake", "Dimi"]` |
| Escolha | Menu começa no Jake; ▶ mostra Dimi, ▶ volta ao Jake, ◀ volta ao Dimi; botões de troca visíveis (antes ficavam ocultos com um só piloto). “Jogar” carrega `dimi_kart.glb` na pista quadriculada |
| Tamanho | Comprimento no jogo 1,961 m (Jake 1,962 m), altura 1,828 m (Jake 1,659 m), ambos com escala 2,0 |
| Movimento | 24,0 m em 2 s acelerando; velocidade máxima de 22 m/s |
| Direção | Giro +1,43 rad/s à esquerda e −1,43 rad/s à direita a 22 m/s; esterço ±1 |
| Frenagem e ré | De 22 m/s a 0 em 0,80 s; bico mergulha até 6,53° (limite 6°, mais o excesso da mola); ré a −8,0 m/s, 12,06 m para trás; parado 4 s depois: velocidade 0, rolagem e cabeça em 0 |
| Câmera | Atrás do kart (produto escalar +4,47); FOV 68° → 80,5° acelerando, 82° no máximo e 73° em ré; na curva fica até 19,8° atrás do kart; rolagem da imagem −2,1° |
| Rodas | Raio 0,1297 nas quatro; giro avante = `v / escala / raio · dt`; a ré cancela o giro; parado não gira; dianteiras ±28°, traseiras 0°; pivôs das rodas sem deriva (0,0) com o corpo inclinando |
| Suspensão | Curva à esquerda: corpo +6,88° (pende para a direita); à direita: −6,88°; nenhum quadro contra o sinal da curva; no percurso a 22 m/s, ±13,8° a 14,0° |
| Cabeça estabilizada | Oposta ao corpo nos dois sentidos: −4,81° / +4,81° globais (sem ruído, 60 passos/s); no percurso −10,0° / +9,8° |
| Cabeça em todo quadro | **Falha.** Quadros no mesmo lado do corpo, a 60 passos/s sem ruído: entrada 18 (até 0,30 s), inversão 15 (até o quadro 22), saída 16 (até o quadro 50); parada 0. Com ruído, a reta tem 78 de 180 quadros; a 120 passos/s, 40/31/148. Reta com vibração: 84 de 120 |
| Teto da cabeça | Máximo relativo de 25,0° (antes do teto: 32,74°) |

`conclusao`: tudo `true`, exceto `cabeca_sempre_oposta: false`.

**Causa da falha, igual à do Jake:** a cabeça segue a rolagem por uma mola (atraso) e ignora o tremor da carroceria (`tremor` entra no corpo, não na meta da cabeça). Na saída da curva, a cabeça volta mais devagar que o corpo e fica do mesmo lado enquanto o corpo cruza o zero. Os números sem ruído são **idênticos** aos do Jake (18 e 15 quadros), porque a mecânica é a mesma. A diferença de geometria não muda a medida feita no espaço do esqueleto.

## 5. Inspeção visual (Godot com janela)

Imagens em [`vistas_fase8/`](vistas_fase8/), todas do executável real, com a ficha final:

- `menu_jake.png`, `menu_dimi.png`: o Dimi aparece texturizado no pedestal, com nome, descrição e as setas de troca.
- `pista_parado`, `pista_reta`, `pista_curva_esquerda`, `pista_pico_cabeca`, `pista_curva_direita`, `pista_re`: câmera atrás do kart, piso quadriculado, inclinação visível nas curvas. Na câmera do jogo a base da cabeça não aparece.
- `lateral_*`: câmera extra, fechada, ao lado do piloto (não existe no jogo). Em `lateral_curva_esquerda` (cabeça a cerca de 24° relativos) aparece, sob o queixo, uma fresta na gola em que a borda da base aberta fica à mostra. Em `lateral_pico_cabeca_25.0_graus` a grade do kart esconde a região. `sem_teto_lateral_pico_cabeca_32.7_graus.png` é da primeira execução, antes do teto.
- Na pista, o kart fica mais azulado que no menu por causa da luz e do céu da cena. O material não foi comparado com o Blender.

## 6. Regressão do Jake

Para não alterar arquivos do Jake, o verificador dele foi copiado temporariamente com destino na pasta de rascunho e depois apagado. `rodas`, `curvas` e `reta_com_vibracao` saíram **idênticos** a [`validacao_godot_jake.json`](../../P001_jake/validacao/validacao_godot_jake.json), e `conclusao` não mudou. `pilotos_cadastrados` passou de 1 para 2, como esperado. No percurso, a rolagem variou alguns décimos de grau (13,87° contra 14,21°) porque a pista sorteia a semente do ruído (`randi()`). O relatório do Jake não foi regravado; os hashes de scripts registrados nele descrevem a versão anterior.

## 7. Limitações e o que não foi feito

- O requisito de cabeça **sempre** oposta não é cumprido (seção 4). Corrigir exige mudar a mecânica comum aos dois pilotos, por exemplo calcular a meta pela rolagem total com o tremor e reduzir o atraso da mola. Isso depende de decisão do usuário.
- A suspensão é visual (sem curso individual por roda nem contato por raycast), como no Jake.
- As bolinhas das rodas atravessam o chão até 2,5 cm durante o giro.
- O teto de 25° na inclinação vem da medida em Y da Fase 6, não de uma medida em rolagem. De perto e de lado a borda aparece perto de 24°; na câmera do jogo, não.
- O jogo não foi jogado com teclado por uma pessoa: a entrada foi simulada com `Input.action_press`.
- Não houve commit.

## 8. Artefatos

| Arquivo | SHA-256 |
| --- | --- |
| `jogo/personagens/dimi/dimi.tres` | `f68edad8…3f400` |
| `jogo/scripts/visual_kart.gd` | `b87183e5…caf92b` (antes `ba48f815…84de4`) |
| `jogo/scripts/definicao_personagem.gd` | `a475788d…60e752` (antes `d5b35971…6506f3`) |
| `jogo/scripts/jogo.gd` | `6f7dcca3…b91c` (antes `e45e820d…89b2`) |
| `jogo/ferramentas/validar_mecanicas_dimi.gd` | `7c9a4059…af2` |
| `jogo/ferramentas/capturar_vistas_dimi.gd` | `da7dcd09…cede` |
| `validacao/validacao_mecanicas_fase8.json` | `d13eb50e…71cd4` |
| `jogo/personagens/dimi/dimi_kart.glb` (não alterado) | `2b25281b…606258b` |
| `blender/dimi.blend` (não alterado) | `e28bf878…cd649e1` |

Qualquer mudança em `kart.gd`, `visual_kart.gd`, `camera_perseguicao.gd`, na ficha ou no GLB exige repetir os dois comandos da seção 3.
