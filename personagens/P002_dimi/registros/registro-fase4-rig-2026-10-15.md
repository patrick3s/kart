# Registro da Fase 4 — pivôs, esqueleto e pesos — P002 Dimi

Data: 15/10/2026, 16:36–17:05 (-03:00).

## 1. Pedido e escopo

O usuário pediu para iniciar a Fase 4 do Dimi. O escopo é o padrão de todos os personagens. A cabeça gira pela base do pescoço, as quatro rodas têm pivô no centro e o rig `Personagem_Rig` segue a hierarquia `Root_Bone → Torso_Bone → Neck_Bone → Head_Bone`. As partes rígidas recebem pesos exclusivos. A geometria não pode ser alterada.

## 2. Ferramentas e estado inicial

- **Blender 5.2.2 LTS, sessão interativa já aberta, pelo Blender MCP** (`execute_blender_code`). Não foi aberta outra instância nem usada a CLI. É a primeira fase do Dimi executada na sessão aberta.
- **Sessão ao começar:** `blender/dimi.blend` aberto, em modo Objeto, marcado como alterado. A única diferença eram cliques de seleção (`VIEW3D_OT_select`): malhas, contagens e transformações estavam iguais às da Fase 3. O arquivo foi recarregado do disco com `wm.revert_mainfile`, descartando apenas essa seleção.
- **Arquivo em disco ao começar:** SHA-256 `edac92bf…1170d`, igual ao do checkpoint.
- **Scripts:** ficam em [`scripts_fase4/`](scripts_fase4/) e foram executados por `exec` no MCP. As seleções e medidas são próprias deste modelo; não foram reutilizados valores do Jake.

## 3. Cópia de segurança

| Arquivo | SHA-256 |
| --- | --- |
| [`backups/dimi_antes_fase4_20261015_163922.blend`](../backups/dimi_antes_fase4_20261015_163922.blend) | `edac92bf920fa7ed0b9e1779ccc8b9590297b987c0b250d94afe2d0c1a51170d` (cópia byte a byte do arquivo da Fase 3) |

## 4. Pivô da cabeça

A medição foi feita por [`medir_pivos.py`](scripts_fase4/medir_pivos.py); os resultados estão em [`validacao/medidas_pivos_fase4.json`](../validacao/medidas_pivos_fase4.json).

- **Base aberta:** a malha da cabeça não fecha embaixo. Há um toco de pele do pescoço com 557 vértices entre Z 0,415 e 0,455, X de −0,034 a 0,030 e Y de −0,018 a −0,002. O queixo, no plano X = 0, desce até Z 0,457.
- **Gola do corpo:** em X, o furo em volta do pescoço mede 0 em Z 0,44, cerca de 2 cm em 0,45, 6,8 cm em 0,46 e 12 cm em 0,47. Ou seja, a gola fecha em volta do pescoço entre Z 0,44 e 0,45.
- **Corte de conferência:** seções nos planos X = 0 e Y = −0,01, com a cabeça e o corpo (imagem temporária fora do repositório). O pescoço entra na gola logo abaixo do queixo.
- **Critério adotado:**
  - X = 0, pela simetria.
  - Y = média entre o centro da caixa (−0,0099) e a média dos vértices (−0,0113) do toco.
  - Z = plano em que a gola fecha em volta do pescoço (0,4453).
  - Os valores foram arredondados para a grade de 1/4096 m, para reduzir o arredondamento ao compensar as coordenadas locais.

**Pivô da cabeça e início de `Head_Bone`: `(0, −0.010498046875, 0.4453125)`** no espaço mundial.

## 5. Centros das rodas

O critério do Jake, centro da caixa (`BOUNDS`), não serve neste modelo. Os pneus são levemente ovais, e as bolinhas decorativas passam da banda de rodagem: na `Wheel_Rear_Left`, as ilhas de 324 e 1.184 vértices sobem até Z 0,268. Com isso, o centro da caixa ficaria até 6 mm acima do eixo e até 1,8 cm para dentro em X, por causa do cubo.

**Critério adotado:**

1. No plano YZ, ajuste de um círculo por mínimos quadrados ao **contorno externo da banda de rodagem**.
2. Por setor de 5°, entram só os pontos a até 1 mm do raio máximo do setor.
3. Ficam de fora os setores cujo raio máximo passa 3 mm da mediana, que são os picos das bolinhas.
4. O cálculo é iterado até estabilizar o centro.
5. X é o meio da faixa X da banda.
6. Os valores foram arredondados para a grade de 1/4096 m.

| Roda | Centro medido (X, Y, Z) | Raio | Desvio padrão / máx. do ajuste | Setores usados | Pivô adotado |
| --- | --- | ---: | --- | ---: | --- |
| `Wheel_Front_Left` | (0.31599, −0.25003, 0.12801) | 0.1298 | 0.00085 / 0.00268 | 65/72 | (0.31591797, −0.25, 0.12792969) |
| `Wheel_Front_Right` | (−0.31647, −0.25015, 0.12799) | 0.1298 | 0.00083 / 0.00280 | 68/72 | (−0.31640625, −0.25024414, 0.12792969) |
| `Wheel_Rear_Left` | (0.31990, 0.22864, 0.12800) | 0.1296 | 0.00085 / 0.00250 | 48/72 | (0.31982422, 0.22851563, 0.12792969) |
| `Wheel_Rear_Right` | (−0.32011, 0.22847, 0.12784) | 0.1297 | 0.00089 / 0.00279 | 72/72 | (−0.32006836, 0.22851563, 0.12792969) |

As quatro rodas têm raio próximo de 0,1297 m e eixo em Z ≈ 0,128. O pneu é levemente achatado no contato: o chão fica a cerca de 1,8 mm dentro do círculo ajustado. A diferença entre o centro da caixa e o ajuste também está no JSON (`diferenca_caixa_menos_ajuste`).

## 6. Origens

[`montar_rig.py`](scripts_fase4/montar_rig.py) desloca a malha por −p (`mesh.transform`) e o objeto por +p, o mesmo efeito de `origin_set` com compensação, sem modo de edição. `Corpo_Kart` mantém a origem em `(0, 0, 0)`. O `custom_normal` codificado não mudou: ele foi comparado com um instantâneo tirado antes, em arquivo temporário fora do repositório.

## 7. Armature criada

- Objeto `Personagem_Rig`, dados `Personagem_Rig_Armature`, matriz identidade, octaedros visíveis à frente da malha.
- Na posição de repouso, o espaço do rig coincide com o mundial.

| Osso | Início | Fim | Pai | Conectado | Deforma |
| --- | --- | --- | --- | --- | --- |
| `Root_Bone` | `(0, 0, 0.1171875)` | `(0, 0, 0.234375)` | — | — | Não |
| `Torso_Bone` | `(0, 0, 0.234375)` | `(0, −0.010498, 0.40625)` | `Root_Bone` | Sim | Sim |
| `Neck_Bone` | `(0, −0.010498, 0.40625)` | `(0, −0.010498, 0.4453125)` | `Torso_Bone` | Sim | Não |
| `Head_Bone` | `(0, −0.010498, 0.4453125)` | `(0, −0.010498, 0.703125)` | `Neck_Bone` | Sim | Sim |

Referências de altura:

- `Root_Bone` começa na plataforma do chassi (Z ≈ 0,116).
- `Torso_Bone` começa no assento.
- `Head_Bone` termina perto do topo do boné (Z ≈ 0,707).
- A rolagem dos ossos é 0. O **Y local de `Head_Bone` coincide com o Z mundial** (eixo de giro horizontal da cabeça). O Z local corresponde à inclinação lateral e o X local à arfagem.

## 8. Pesos, parentesco e modificadores

| Objeto | Grupo de vértices | Pesos | Ligação |
| --- | --- | --- | --- |
| `Cabeca` | só `Head_Bone` | 1.0 em todos os 93.155 vértices | filho de `Personagem_Rig` + modificador `Rig_Rigido_Sem_Deformacao` |
| `Corpo_Kart` | só `Torso_Bone` | 1.0 em todos os 672.481 vértices | filho de `Personagem_Rig` + modificador `Rig_Rigido_Sem_Deformacao` |
| `Wheel_*` (4) | nenhum | — | parentesco de osso com `Torso_Bone`, com matriz inversa compensada; sem modificador |

O modificador Armature usa grupos de vértices, com envelopes e preservação de volume desativados. É a mesma configuração do Jake: as rodas acompanham o torso, mas giram e esterçam como objetos em torno da própria origem.

## 9. Validação

[`verificar_rig.py`](scripts_fase4/verificar_rig.py) foi executado duas vezes: na cena montada e, depois de salvar, **no arquivo recarregado do disco** (`wm.revert_mainfile`). Resultado: [`validacao/verificacao_rig_fase4.json`](../validacao/verificacao_rig_fase4.json), **`tudo_ok: true`**, com tolerância de 1e-6 m.

| Medida | `Cabeca` | `Corpo_Kart` | Rodas |
| --- | ---: | ---: | ---: |
| Posição mundial da malha-base × NPZ original | 7.45e-9 | 0.0 | 2.98e-8 |
| Posição mundial avaliada em repouso (com rig) × NPZ | 5.96e-8 | 5.96e-8 | 2.98e-8 |
| Origem × pivô adotado | 0.0 | 0.0 | 2.98e-8 |
| `custom_normal` codificado igual ao anterior | sim | sim | sim |
| Normais de canto decodificadas × NPZ | 3.97e-4 | 0.0 | até 2.30e-4 |

Esses desvios são arredondamento de ponto flutuante. **Não são um deslocamento absolutamente zero.** As normais decodificadas variam um pouco porque o espaço das normais é recalculado com as coordenadas locais compensadas. O desvio de até 4e-4 corresponde a cerca de 0,02°, e o dado codificado é idêntico, como previsto na receita.

**Pesos.** Cada malha tem um só grupo, com o nome do osso. Todos os vértices têm peso 1,0, nenhum ficou sem peso e nenhum está em dois grupos. As rodas não têm grupos nem modificador.

**Testes temporários.** Todos foram restaurados num bloco `finally`; a posição final é idêntica à de repouso (diferença 0,0).

| Teste | Deslocamento do pivô | Erro rígido das partes móveis | Movimento das partes fixas |
| --- | ---: | ---: | ---: |
| `Head_Bone` Y +25° | 0.0 | 2.6e-8 | 0.0 |
| `Head_Bone` Y −40° | 0.0 | 2.5e-8 | 0.0 |
| `Head_Bone` Z +15° (inclinação) | 0.0 | 8.6e-8 | 0.0 |
| `Head_Bone` X +15° (arfagem) | 0.0 | 1.0e-7 | 0.0 |
| `Torso_Bone` Y +10° (tudo acompanha) | 0.0 | 1.04e-7 | — |
| `Root_Bone` Z +20° (tudo acompanha) | 0.0 | 1.72e-7 | — |
| Cada roda: giro X 90° e esterço Z 30° | 0.0 | — | 0.0 nas outras partes |

**Oscilação do contato no giro de 360°** (em passos de 15°), medida pelo Z mínimo da roda:

| Roda | Oscilação |
| --- | ---: |
| FL | 15,4 mm |
| FR | 12,9 mm |
| RL | 25,4 mm |
| RR | 3,5 mm |

A RR, sem bolinhas salientes, mostra só a ovalização da malha. Nas outras, as bolinhas passam abaixo do chão quando giram. Isso vem da geometria; o pivô não está deslocado.

## 10. Conferência visual

As vistas ficam em [`vistas_fase4/`](vistas_fase4/) e foram feitas por [`render_vistas.py`](scripts_fase4/render_vistas.py) na sessão aberta. As poses e a câmera foram desfeitas com `wm.revert_mainfile`, sem salvar. São elas:

- repouso;
- cabeça girada a ±40° em Y, inclinada a ±15° em Z e com arfagem de +15° em X, cada uma de frente, de trás pelo alto e de lado;
- rodas dianteiras esterçadas 30° e traseira esquerda girada 90°.

- A cabeça gira em torno do pescoço sem se soltar da gola. De frente e por trás, a base aberta continua escondida.
- **Limitação observada:** no giro de **−40°, vista de lado** ([`cabeca_giro_y_-40_lado.png`](vistas_fase4/cabeca_giro_y_-40_lado.png)), aparece um recorte irregular de pele sob a mandíbula, junto à gola. É a borda da base aberta. Na arfagem de +15°, vista de lado, aparece uma pequena fresta escura no mesmo ponto. Nenhuma tampa nem geometria foi criada.

## 11. Incidentes

1. A sessão estava marcada como alterada por cliques de seleção. O arquivo foi recarregado do disco antes da fase (seção 2).
2. Sem `matplotlib` nem `scipy`, o corte do pescoço foi desenhado em PNG com Python puro, e a separação das ilhas das rodas foi calculada com NumPy.
3. O primeiro ajuste de círculo usava todos os pontos externos e foi descartado: na RL, as bolinhas puxavam o raio para 0,135. O ajuste pela moda da distância também foi descartado, porque na RL pegou uma superfície interna (raio 0,125, eixo 8 mm acima do chão). Ficou o critério da seção 5.
4. Ao salvar, o Blender criou `dimi.blend1`, idêntico ao backup pré-Fase 4 (`edac92bf…`). O arquivo foi apagado.

## 12. Arquivo resultante e pontos para as próximas fases

`blender/dimi.blend` tem **109.893.282 bytes** e SHA-256 `229034cfebf4fc8c63f0f3ae0cd3a0089021614a863bb5387059c0376c25a7d7`. Foi salvo pela sessão MCP e conferido depois de recarregar. São 7 objetos: as 6 partes e `Personagem_Rig`.

- **Fase 5:** repetir a comparação completa de topologia, UV e materiais contra o NPZ. A verificação desta fase cobriu posições, normais, pesos e pivôs, mas não repetiu arestas, cantos, UV e materiais. Como as malhas só foram transladadas, não se espera mudança nesses dados, mas isso ainda precisa ser comprovado.
- **Fase 7/8 (Godot):** `visual_kart.gd` calcula o raio da roda pela caixa da malha, `max(size.y, size.z)/2`. Na RL, as bolinhas fazem esse valor chegar a cerca de 0,143, contra 0,1297 medido. Isso elevaria o kart em cerca de 1,5 cm e mudaria a velocidade de giro dessa roda. Avaliar se o raio deve vir da ficha do personagem.
- **Base aberta da cabeça:** decidir com o usuário se a borda visível a −40° é aceitável, se a amplitude do giro deve ser limitada ou se será criada uma tampa, o que alteraria a topologia.
