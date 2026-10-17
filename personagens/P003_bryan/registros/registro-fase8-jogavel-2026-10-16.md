# Registro — Fase 8 — personagem jogável e mecânicas — P003 Bryan

Data: 16/10/2026 (−03:00). Ferramenta: Godot 4.7.2.stable pela CLI (`--headless` para as medições; com janela, Metal/Forward+, para as imagens). Pedido do usuário: “inicie a fase 8 do bryan”. O Blender não foi usado e `bryan.blend` não mudou (SHA-256 `b25be23b…5fe43c11`).

## 1. Estado de entrada

- `bryan_kart.glb` com SHA-256 `b51c51a5…48bea9e4`, igual ao da Fase 7; `.import` sem mudança.
- Catálogo `scripts/jogo.gd` com Jake e Dimi. `visual_kart.gd` já com a correção da [T001](../../../jogo/tarefas/T001-cabeca-sempre-oposta.md) (`73be89b8…b361db`), **não alterado nesta fase**.
- Pendência herdada da Fase 7: sem `raio_rodas`, o raio sai da caixa da malha (0,1247–0,1270), 4–6% acima do medido na Fase 4.

## 2. Alterações no jogo

| Arquivo | Mudança | Efeito no Jake e no Dimi |
| --- | --- | --- |
| `jogo/personagens/bryan/bryan.tres` (novo) | Ficha `DefinicaoPersonagem`: nome “Bryan”, `escala = 2.0`, `raio_rodas = 0.1196`, `giro_maximo_cabeca = 25.0` | — |
| `jogo/scripts/jogo.gd` | Bryan acrescentado **depois** do Dimi no catálogo | Jake no índice 0, Dimi no 1 |
| `jogo/ferramentas/validar_mecanicas_bryan.gd` (novo) | Cópia do verificador do Dimi com a ficha do Bryan, o catálogo de três pilotos, a troca completa no menu e o apoio das rodas no chão | — |
| `jogo/ferramentas/capturar_vistas_bryan.gd` (novo) | Cópia do capturador do Dimi com o menu do Bryan e uma vista traseira fechada da nuca | — |

Nenhum script de mecânica foi alterado (`kart.gd`, `visual_kart.gd`, `camera_perseguicao.gd`, `definicao_personagem.gd`, `selecao_personagem.gd`).

**Por que 0,1196:** a ficha aceita um raio único. É a média dos quatro raios da banda medidos na Fase 4 (0,11926, 0,11948, 0,11982 e 0,11991; diferença máxima de 0,3 mm até a média). Com esse raio, a roda dianteira esquerda, cujo centro é o mais baixo, toca o chão (altura da banda 5e-12). A dianteira direita fica 0,49 mm acima e as traseiras, 0,98 mm, em unidades do modelo (cerca de 2 mm no jogo, escala 2,0). Essa diferença vem dos centros medidos, que diferem em Z até 1 mm. O modelo sobe 0,22 mm. Como aceito na Fase 5, o preenchimento do para-lama no topo das rodas faz o contato oscilar 12–19 mm durante o giro.

**Por que o teto de 25°:** é a amplitude decidida pelo usuário na Fase 6, registrada no checkpoint para `giro_maximo_cabeca`. Como no Dimi, a medida foi feita para o giro em **Y** (olhar para os lados), mas no jogo a cabeça **inclina** na rolagem e acompanha a arfagem. Aplicar o mesmo valor à inclinação é uma interpretação, não uma medida da nuca nessa direção (ver seção 5).

## 3. Verificador e comandos

Na pasta `jogo/`:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --fixed-fps 60 --script res://ferramentas/validar_mecanicas_bryan.gd
/Applications/Godot.app/Contents/MacOS/Godot --path . --fixed-fps 60 --script res://ferramentas/capturar_vistas_bryan.gd
```

O primeiro grava [`validacao_mecanicas_fase8.json`](../validacao/validacao_mecanicas_fase8.json) e o segundo, as imagens em [`vistas_fase8/`](vistas_fase8/). Nenhum dos dois altera scripts, cenas ou fichas. A entrada é simulada com `Input.action_press`, no motor de física a 60 passos/s. As curvas manuais usam a semente fixa 12345.

## 4. Resultados no motor

| Verificação | Resultado |
| --- | --- |
| Catálogo | `["Jake", "Dimi", "Bryan"]` |
| Escolha | O menu começa no Jake. ▶ mostra o Dimi, ▶ mostra o Bryan (vitrine com `bryan_kart.glb`), ▶ volta ao Jake e ◀ volta ao Bryan (índice 2). Botões de troca visíveis. “Jogar” carrega `bryan_kart.glb` na pista quadriculada |
| Estrutura | Ossos `Root_Bone`, `Torso_Bone`, `Neck_Bone`, `Head_Bone`; `Cabeca` e `Corpo_Kart` com skin; quatro `Wheel_*`; `AnimationPlayer` sem autoplay |
| Tamanho | Comprimento no jogo 1,959 m (Jake 1,962, Dimi 1,961) e altura 1,541 m (Jake 1,659, Dimi 1,828), todos com escala 2,0 |
| Movimento | 24,0 m em 2 s acelerando; velocidade máxima de 22 m/s |
| Direção | Giro de +1,43 rad/s à esquerda e −1,43 rad/s à direita a 22 m/s; esterço ±1 |
| Frenagem e ré | De 22 m/s a 0 em 0,80 s. O bico mergulha até 6,53° (limite de 6° mais o excesso da mola). Ré a −8,0 m/s, 12,06 m para trás. Parado 4 s depois: velocidade 0, rolagem e cabeça em 0 |
| Câmera | Atrás do kart (produto escalar +4,47). FOV de 68° → 80,5° acelerando, 82° no máximo e 73° em ré. Na curva, fica até 19,8° atrás do kart; rolagem da imagem −2,1° |
| Rodas | Raio 0,1196 nas quatro (caixa: 0,1247–0,1270); giro avante = `v / escala / raio · dt`; a ré cancela o giro; parado não gira; dianteiras ±28°, traseiras 0°; pivôs das rodas sem deriva (0,0) com o corpo inclinando |
| Apoio | Altura da banda sobre o chão: mínimo 5e-12 e máximo 0,98 mm (unidades do modelo); `rodas_apoio_no_chao: true` |
| Suspensão | Curva à esquerda: corpo +6,88° (pende para a direita); à direita: −6,88°. Nenhum quadro contra o sinal da curva. No percurso a 22 m/s, +14,35° / −14,20° |
| Cabeça estabilizada | Oposta ao corpo nos dois sentidos: −4,81° / +4,81° globais (sem ruído, 60 passos/s); no percurso, −9,32° / +9,54° |
| Cabeça em todo quadro | **0 quadros no mesmo lado do corpo** na entrada, inversão, saída e parada, a 60 passos/s sem e com ruído e a 120 passos/s com ruído; reta com vibração: 0 de 120 |
| Variação por quadro | Máximo de 2,27° (60 sem ruído), 2,67° (60 com ruído) e 1,52° (120 com ruído), iguais aos do Dimi na T001 |
| Teto da cabeça | Máximo relativo de 25,0° (no percurso real, no pico da mola ao inverter a curva) |
| Pivô da cabeça | Deriva máxima de 0,035 no espaço do esqueleto. O pivô acompanha a rolagem do corpo e o salto da vibração, como no Dimi; não é deslocamento relativo ao corpo |

`conclusao`: **todos os itens `true`**, inclusive `cabeca_sempre_oposta` e `cabeca_dentro_do_teto_25`.

As medidas no espaço do esqueleto (inclinação, quadros no mesmo lado) coincidem com as do Dimi. Isso é esperado, porque a mecânica é a mesma e não depende da geometria. Mudam o raio, o apoio das rodas e as dimensões.

## 5. Inspeção visual (Godot com janela)

Imagens em [`vistas_fase8/`](vistas_fase8/), todas do executável real, com a ficha final:

- `menu_jake.png`, `menu_dimi.png`, `menu_bryan.png`: o Bryan aparece texturizado no pedestal (uniforme, quepe, óculos, kart “POLÍCIA” com giroflex, antena e caixas), com nome, descrição e setas de troca.
- `pista_parado`, `pista_reta`, `pista_curva_esquerda`, `pista_pico_cabeca`, `pista_curva_direita`, `pista_re`: câmera atrás do kart, piso quadriculado, inclinação visível nas curvas. **Na câmera do jogo, as caixas traseiras e o giroflex escondem a nuca e quase toda a cabeça; só o quepe aparece.**
- `lateral_*`: câmera extra, fechada, ao lado do piloto (não existe no jogo). Em `lateral_curva_esquerda`, aparece uma **fresta fina entre o pescoço e a gola**, nas costas. Em `lateral_pico_cabeca_25.0_graus`, a gola cobre a região.
- `nuca_curva_esquerda`, `nuca_pico_cabeca`: câmera extra, fechada, atrás e acima do piloto. A barra traseira e o rádio cobrem a nuca; nenhuma borda aberta ficou visível nesses quadros.
- Na pista, o kart fica mais escuro e azulado que no menu, por causa da luz e do céu da cena. O material não foi comparado numericamente com o Blender.

## 6. Regressão do Jake e do Dimi

Os dois verificadores rodaram como cópias com destino na pasta de rascunho. Nenhum arquivo das pastas do Jake e do Dimi foi regravado.

- **Dimi** (`validar_mecanicas_dimi.gd -- --saida=<rascunho>`): `rodas`, `curvas`, `reta_com_vibracao` e `dimensoes` saíram **idênticos** a [`validacao_mecanicas_t001.json`](../../P002_dimi/validacao/validacao_mecanicas_t001.json). Só mudaram `catalogo_jake_e_dimi` e `selecao_troca_e_volta`, que passaram a `false`, porque o verificador do Dimi espera exatamente dois pilotos: com três, a volta completa para em Bryan. Todas as conclusões de mecânica continuam `true`. **O verificador do Dimi não foi alterado**; para voltar a passar nesses dois itens, ele precisa aceitar o catálogo atual.
- **Jake** (cópia de `validar_mecanicas_jake.gd` com destino no rascunho): a conclusão ficou igual à de [`T001/regressao_jake_depois.json`](../../../jogo/tarefas/T001/regressao_jake_depois.json). `pilotos_cadastrados` passou de 2 para 3. No percurso, a rolagem e a cabeça variaram alguns décimos de grau (14,21° → 14,01°), porque a pista sorteia a semente do ruído.

## 7. Limitações e o que não foi feito

- Raio único na ficha: as rodas traseiras ficam até 0,98 mm (modelo) acima do chão. Para zerar, seria preciso um raio por roda na `DefinicaoPersonagem`, que é uma mudança no código comum.
- O contato das rodas oscila 12–19 mm durante o giro, por causa do preenchimento do para-lama (aceito na Fase 5).
- O teto de 25° na inclinação vem da medida em Y da Fase 6. De perto e de lado, aparece uma fresta fina na gola durante a curva; na câmera do jogo, não.
- A suspensão é visual (sem curso por roda nem contato por raycast), como nos outros pilotos.
- O jogo não foi jogado com teclado por uma pessoa: a entrada foi simulada.
- O verificador do Dimi passou a reprovar o catálogo e a troca (seção 6). Não foi corrigido para não alterar ferramentas de outro personagem sem pedido.
- Não houve commit.

## 8. Artefatos

| Arquivo | SHA-256 |
| --- | --- |
| `jogo/personagens/bryan/bryan.tres` | `2b847e0e…4774c0` |
| `jogo/scripts/jogo.gd` | `f3f0fa52…f76ad0` (antes `6f7dcca3…b91c`) |
| `jogo/scripts/visual_kart.gd` (não alterado) | `73be89b8…b361db` |
| `jogo/ferramentas/validar_mecanicas_bryan.gd` | `360ea534…439a517c` |
| `jogo/ferramentas/capturar_vistas_bryan.gd` | `c73cb7ff…741c99e1` |
| `validacao/validacao_mecanicas_fase8.json` | `8a459289…d86d351ff` |
| `jogo/personagens/bryan/bryan_kart.glb` (não alterado) | `b51c51a5…48bea9e4` |
| `blender/bryan.blend` (não alterado) | `b25be23b…5fe43c11` |

Qualquer mudança em `kart.gd`, `visual_kart.gd`, `camera_perseguicao.gd`, `jogo.gd`, na ficha ou no GLB exige repetir os dois comandos da seção 3.
