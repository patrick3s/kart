# Registro da Fase 4 — pivôs, esqueleto e pesos — P003 Bryan

Data: 15/10/2026, 19:48–19:57 (-03:00).

## 1. Pedido e escopo

O usuário pediu para iniciar a Fase 4 do Bryan. Esta fase segue o escopo padrão:

- a cabeça gira pela base do pescoço;
- as quatro rodas têm pivô no centro;
- o `Personagem_Rig` tem a hierarquia `Root_Bone → Torso_Bone → Neck_Bone → Head_Bone`;
- as partes rígidas recebem pesos exclusivos;
- a geometria não é alterada; só as origens mudam, com compensação.

## 2. Ferramentas e estado inicial

- **Blender:** versão 5.2.2 LTS, usada só pela sessão já aberta, pelo Blender MCP (`execute_blender_code`). Nenhuma instância extra nem CLI.
- **Sessão ao começar:** `blender/bryan.blend` aberto, em modo Objeto e marcado como alterado. As únicas operações registradas eram três `VIEW3D_OT_select`. Objetos, contagens e origens estavam iguais aos da Fase 3. O arquivo foi recarregado do disco com `wm.revert_mainfile`, o que descartou só essa seleção.
- **Arquivo em disco ao começar:** SHA-256 `0ffb2802…0954d17`, igual ao do checkpoint.
- **Scripts:** ficam em [`scripts_fase4/`](scripts_fase4/) e foram executados por `exec` no MCP. O método é o do P002 (Dimi). As medidas, os limites e as alturas foram tirados deste modelo; nenhum valor do Jake ou do Dimi foi reaproveitado.

## 3. Cópia de segurança

| Arquivo | SHA-256 |
| --- | --- |
| [`backups/bryan_antes_fase4_20261015_195106.blend`](../backups/bryan_antes_fase4_20261015_195106.blend) | `0ffb28027b6cbbbce958ac1aae6188dbc4d6b1821d6693ce8a02c7dad0954d17` (cópia byte a byte do arquivo da Fase 3) |

## 4. Pivô da cabeça

As medidas foram feitas por [`medir_pivos.py`](scripts_fase4/medir_pivos.py) e gravadas em [`validacao/medidas_pivos_fase4.json`](../validacao/medidas_pivos_fase4.json).

- **Pele do pescoço:** é a ilha da cabeça que desce mais (3.013 vértices). Abaixo do queixo, entre Z 0,4941 e 0,525, ela forma um toco estreito de 362 vértices: X de −0,031 a 0,016 e Y de 0,063 a 0,080. Acima de Z ≈ 0,53, a ilha se alarga na mandíbula.
- **Corpo sob o pescoço:** em X, no plano Y do toco, o furo do corpo em volta do pescoço é praticamente 0 entre Z 0,485 e 0,495. Ou seja, a superfície da camisa fecha logo abaixo do pescoço. Acima de 0,50, o furo se abre na gola: cerca de ±1 cm em 0,50 e ±2,8 cm em 0,53. Na coluna logo abaixo do pivô, o corpo tem vértices entre Z 0,486 e 0,499.
- **Critério adotado:**
  - X e Y: média entre o centro da caixa e a média dos vértices do toco (X −0,00743/−0,00783; Y 0,07147/0,07112). X não é 0: o pescoço deste modelo está deslocado cerca de 7 mm para a direita do piloto, e o pivô acompanha o pescoço real.
  - Z: a base do toco, que é o menor Z da cabeça (0,494140625, já na grade). Fica onde a superfície do corpo fecha sob o pescoço.
  - Valores arredondados para a grade de 1/4096 m.

**Pivô da cabeça e início de `Head_Bone`: `(−0.007568359375, 0.0712890625, 0.494140625)`** no espaço mundial.

## 5. Centros das rodas

### Por que o critério de partida não serviu

O eixo da Fase 3 era o ponto de partida. Ele foi ajustado à silhueta da face externa, com o raio de corte de 0,1265 m. **Ele não serve como pivô:**

- **O topo das rodas guarda o preenchimento do para-lama** cortado na divisão da Fase 3. Por setor de 5°, o raio máximo na metade de cima chega a 0,126–0,139 m nas traseiras e cerca de 5 mm acima da banda nas dianteiras.
- **Nas dianteiras, o ajuste em todos os setores** (R 0,1238, eixo Z 0,125) acompanhava esse contorno cortado, não o pneu.
- **O critério do Dimi** (setores a até 3 mm da mediana de todos os setores) deixava entrar setores contaminados: os de 40–55° na RL e os de 35° e 80° na RR.
- **O cubo e o aro** foram medidos como alternativa, porque são concêntricos por construção. O desvio padrão do ajuste ficou entre 1,5 e 4,3 mm, contra 0,35 mm da banda, por causa dos parafusos e marcações. Foram descartados.

### Critério adotado

1. No plano YZ, ajuste de um círculo por mínimos quadrados ao **contorno externo da banda de rodagem**. Em cada setor de 5°, entram os pontos a até 1 mm do raio máximo do setor.
2. Entram só os setores cujo raio máximo fica **a até 2 mm da mediana da metade de baixo** (180–355°). A metade de baixo não tem preenchimento do para-lama.
3. O cálculo é iterado 12 vezes a partir do eixo da Fase 3.
4. X é o meio da banda, entre os percentis 1 e 99 de |X| da metade de baixo (cerca de 0,202 a 0,318). Esse valor coincide com o meio da roda entre a face interna (|X| ≈ 0,192) e a tampa do cubo (|X| ≈ 0,330).
5. Os valores foram arredondados para a grade de 1/4096 m.

| Roda | Centro medido (X, Y, Z) | Raio | Desvio padrão / máx. | Setores | Pivô adotado |
| --- | --- | ---: | --- | ---: | --- |
| `Wheel_Front_Left` | (0.26023, −0.26930, 0.11937) | 0.11926 | 0.00034 / — | 31/72 | (0.26025391, −0.26928711, 0.11938477) |
| `Wheel_Front_Right` | (−0.25999, −0.26953, 0.11988) | 0.11948 | 0.00034 / — | 26/72 | (−0.26000977, −0.26953125, 0.11987305) |
| `Wheel_Rear_Left` | (0.25977, 0.29443, 0.12036) | 0.11982 | 0.00038 / — | 36/72 | (0.25976563, 0.29443359, 0.12036133) |
| `Wheel_Rear_Right` | (−0.25952, 0.29443, 0.12036) | 0.11991 | 0.00039 / — | 36/72 | (−0.25952148, 0.29443359, 0.12036133) |

Os valores completos (resíduo máximo, setores descartados, raio por setor, diferença em relação ao centro da caixa) estão no JSON.

- O raio das quatro rodas fica entre 0,1193 e 0,1199 m.
- O círculo ajustado é tangente ao chão: a folga entre a base do círculo e o menor Z da roda vai de 0,1 a 0,3 mm.
- As traseiras ficaram com Y e Z idênticos.
- O centro da caixa (`BOUNDS`) também não serviria: ele fica cerca de 5 mm acima e cerca de 2 cm para dentro em X, por causa do preenchimento do para-lama e da costura até |X| = 0,15.

## 6. Origens

[`montar_rig.py`](scripts_fase4/montar_rig.py) desloca a malha por −p (`mesh.transform`) e o objeto por +p. O efeito é o mesmo de `origin_set` com compensação, sem passar pelo modo de edição. `Corpo_Kart` mantém a origem em `(0, 0, 0)`.

Antes da montagem foi guardado um instantâneo temporário, fora do repositório, com coordenadas, `custom_normal`, `sharp_edge` e `sharp_face`. Depois da montagem, os códigos de normal e os `sharp_*` estavam idênticos ao instantâneo. Não se repetiu o incidente da Fase 3.

## 7. Armature criada

- Objeto `Personagem_Rig`, dados `Personagem_Rig_Armature`, matriz identidade, octaedros visíveis à frente da malha.
- Na posição de repouso, o espaço do rig coincide com o mundial.

| Osso | Início | Fim | Pai | Conectado | Deforma |
| --- | --- | --- | --- | --- | --- |
| `Root_Bone` | `(0, 0, 0.0805664)` | `(0, 0, 0.25)` | — | — | Não |
| `Torso_Bone` | `(0, 0, 0.25)` | `(−0.0075684, 0.0712891, 0.4375)` | `Root_Bone` | Sim | Sim |
| `Neck_Bone` | `(−0.0075684, 0.0712891, 0.4375)` | `(−0.0075684, 0.0712891, 0.4941406)` | `Torso_Bone` | Sim | Não |
| `Head_Bone` | `(−0.0075684, 0.0712891, 0.4941406)` | `(−0.0075684, 0.0712891, 0.734375)` | `Neck_Bone` | Sim | Sim |

Referências de altura, medidas neste modelo:

- `Root_Bone` começa na placa do assoalho (Z ≈ 0,0805).
- `Torso_Bone` começa na altura do assento (0,25).
- `Neck_Bone` começa dentro do tronco, abaixo da superfície que fecha sob o pescoço (≈ 0,486).
- `Head_Bone` termina no topo do quepe (Z máx. da cabeça 0,7336).

A rolagem dos ossos é 0. O **Y local de `Head_Bone` coincide com o Z mundial** (`[0, 0, 0.99999988]`), que é o eixo de giro horizontal da cabeça. O Z local corresponde à inclinação lateral e o X local à arfagem.

## 8. Pesos, parentesco e modificadores

| Objeto | Grupo de vértices | Pesos | Ligação |
| --- | --- | --- | --- |
| `Cabeca` | só `Head_Bone` | 1.0 em todos os 41.982 vértices | filho de `Personagem_Rig` + modificador `Rig_Rigido_Sem_Deformacao` |
| `Corpo_Kart` | só `Torso_Bone` | 1.0 em todos os 771.146 vértices | filho de `Personagem_Rig` + modificador `Rig_Rigido_Sem_Deformacao` |
| `Wheel_*` (4) | nenhum | — | parentesco de osso com `Torso_Bone`, com matriz inversa compensada; sem modificador |

O modificador Armature usa grupos de vértices, com envelopes e preservação de volume desativados. É a mesma configuração do Jake e do Dimi.

## 9. Validação

[`verificar_rig.py`](scripts_fase4/verificar_rig.py) foi adaptado do P002 com três acréscimos:

- normais separadas dentro e fora da costura da Fase 3 (1.730 vértices originais);
- comparação de `sharp_edge` e `sharp_face` com o instantâneo;
- tolerância de 1e-3 para as normais decodificadas.

O script rodou duas vezes: na cena montada e, depois de salvar, **no arquivo recarregado do disco** (`wm.revert_mainfile`). Resultado: [`validacao/verificacao_rig_fase4.json`](../validacao/verificacao_rig_fase4.json), **`tudo_ok: true`**, com tolerância de 1e-6 m.

| Medida | `Cabeca` | `Corpo_Kart` | Rodas |
| --- | ---: | ---: | ---: |
| Posição mundial da malha-base × NPZ original | 3.7e-9 | 0.0 | até 3.0e-8 |
| Posição mundial avaliada em repouso (com rig) × NPZ | 6.0e-8 | 1.5e-8 | até 3.0e-8 |
| Origem × pivô adotado | 0.0 | 0.0 | até 3.0e-8 |
| `custom_normal`, `sharp_edge`, `sharp_face` iguais ao pré-Fase 4 | sim | sim | sim |
| Normais decodificadas × NPZ, fora da costura | 2.9e-4 | 0.0 | até 4.3e-4 |
| Normais decodificadas × NPZ, na costura | — | 4.5e-4 | até 2.4e-4 |

Esses desvios são arredondamento de ponto flutuante, **não um deslocamento absolutamente zero**. As normais decodificadas variam um pouco porque o espaço das normais é recalculado com as coordenadas locais compensadas. O dado codificado é idêntico. O desvio máximo, 4,5e-4, corresponde a cerca de 0,026°.

**Ajuste do critério de matriz.** O teste do P002 exigia que a rotação e a escala mundiais das rodas fossem identidade com erro ≤ 1e-9. No Bryan as quatro rodas falharam com 2,98e-8: a base local é exatamente identidade (rotação 0, escala 1), e o ruído vem do produto de matrizes em float32. Como o `Torso_Bone` inclina em X e Y, a matriz inversa do parentesco não é uma rotação pura em um eixo. O limite passou para 1e-6, a mesma tolerância das posições, e o valor medido fica no JSON (`rotacao_escala_desvio_identidade`).

**Pesos.** Cada malha tem um só grupo, com o nome do osso. Todos os vértices têm peso 1,0, nenhum ficou sem peso e nenhum está em dois grupos. As rodas não têm grupos nem modificador.

**Testes temporários.** Todos foram restaurados num bloco `finally`; a posição final é idêntica à de repouso (diferença 0,0).

| Teste | Deslocamento do pivô | Erro rígido das partes móveis | Movimento das partes fixas |
| --- | ---: | ---: | ---: |
| `Head_Bone` Y +25° | 0.0 | 0.0 | 0.0 |
| `Head_Bone` Y −40° | 0.0 | 0.0 | 0.0 |
| `Head_Bone` Z +15° (inclinação) | 0.0 | 1e-7 | 0.0 |
| `Head_Bone` X +15° (arfagem) | 0.0 | 1e-7 | 0.0 |
| `Torso_Bone` Y +10° (tudo acompanha) | 0.0 | 1e-7 | — |
| `Root_Bone` Z +20° (tudo acompanha) | 0.0 | 1e-7 | — |
| Cada roda: giro X 90° e esterço Z 30° | 0.0 | — | 0.0 nas outras partes |

**Oscilação do contato no giro de 360°** (em passos de 15°), medida pelo Z mínimo da roda:

| Roda | Z mínimo no giro | Oscilação |
| --- | --- | ---: |
| FL | −12,3 mm a 0,0 | 12,3 mm |
| FR | −12,4 mm a 0,2 mm | 12,6 mm |
| RL | −19,1 mm a 0,4 mm | 19,5 mm |
| RR | −15,0 mm a 0,4 mm | 15,4 mm |

Na pose original, o contato fica em Z ≈ 0. Quando a roda gira, o **preenchimento do para-lama que ficou no topo** da roda (Fase 3, raio de até 0,139 m) desce e atravessa o chão. Isso vem da geometria da divisão; o pivô não está deslocado, porque o círculo da metade limpa tem resíduo de 0,35 mm.

## 10. Conferência visual

As vistas ficam em [`vistas_fase4/`](vistas_fase4/) e foram feitas por [`render_vistas.py`](scripts_fase4/render_vistas.py) na sessão aberta. Poses e câmera foram desfeitas com `wm.revert_mainfile`, sem salvar. São elas:

- repouso;
- cabeça girada a ±40° em Y, inclinada a ±15° em Z e com arfagem de +15° em X, cada uma de frente, de trás pelo alto e de lado;
- rodas dianteiras esterçadas 30° e traseira esquerda girada 90°;
- lado esquerdo com as rodas giradas 0°, 90° e 180°, de longe e de perto.

Resultados:

- **A cabeça gira em torno do pescoço sem se soltar da gola.** De frente, os giros e inclinações ficam limpos ([`cabeca_giro_y_+40_frente.png`](vistas_fase4/cabeca_giro_y_+40_frente.png)).
- **Limitação — nuca:** de trás pelo alto, a ±40° ([`cabeca_giro_y_-40_tras_alto.png`](vistas_fase4/cabeca_giro_y_-40_tras_alto.png), [`_+40_`](vistas_fase4/cabeca_giro_y_+40_tras_alto.png)), aparecem recortes irregulares laranja e escuros atrás do pescoço, dentro da gola. Na arfagem de +15°, vista de lado ([`cabeca_arfagem_x_+15_lado.png`](vistas_fase4/cabeca_arfagem_x_+15_lado.png)), abre uma fresta clara entre a nuca e a gola, com um fragmento serrilhado. É a base aberta da cabeça. Nenhuma tampa nem geometria foi criada.
- **Rodas:** o cubo e o aro giram centrados. Com 180° de giro ([`rodas_esq_giro_180_lado.png`](vistas_fase4/rodas_esq_giro_180_lado.png), [`Wheel_Front_Left_giro_180_lado.png`](vistas_fase4/Wheel_Front_Left_giro_180_lado.png)), a borda serrilhada do topo passa para baixo e aparece abaixo da banda. O esterço de 30° não mostrou colisão visível com o para-lama na vista iso.

## 11. Incidentes

1. A sessão estava marcada como alterada por cliques de seleção. O arquivo foi recarregado do disco antes da fase (seção 2).
2. Na primeira execução de `medir_pivos.py`, um erro de desempacotamento (`ValueError`) foi corrigido sem alterar a cena.
3. O primeiro critério das rodas, a 3 mm da mediana da metade de baixo, aceitou dois setores contaminados na RR, que ficou com Z 1,2 mm acima da RL. A tolerância passou para 2 mm. Os critérios descartados estão na seção 5.
4. A primeira verificação deu `tudo_ok: false` só no critério de matriz identidade das rodas (seção 9). O critério foi corrigido e a verificação repetida.
5. `bpy.data.is_dirty` ficou falso depois da montagem pela API de dados. Antes de salvar, foi conferido que o rig e o parentesco estavam na cena. Depois de salvar e recarregar, os 7 objetos estavam presentes.
6. Ao salvar, o Blender regravou `blender/bryan.blend1` com a versão da Fase 3 (`0ffb2802…`, igual ao backup pré-Fase 4). É um backup automático local, ignorado pelo Git (`*.blend[0-9]*`).

## 12. Arquivo resultante e pontos para as próximas fases

`blender/bryan.blend` tem **110.264.434 bytes** e SHA-256 `561475c1ad20be56cc92635b88ea5ff4e68cb0ec5b4be4f4a173c87177460666`. Foi salvo pela sessão MCP e conferido depois de recarregar do disco. São 7 objetos: as 6 partes e `Personagem_Rig`.

- **Fase 5:** repetir a comparação completa de topologia, UV e materiais contra o NPZ. Esta fase cobriu posições, normais, `sharp_*`, pesos e pivôs, mas não repetiu arestas, cantos, UV e materiais. Como as malhas só foram transladadas, não se espera mudança nesses dados, mas isso ainda precisa ser comprovado.
- **Decisão pendente — topo das rodas:** o preenchimento do para-lama que ficou nas rodas faz o contato oscilar de 12 a 19 mm e aparece embaixo quando a roda gira. As opções são:
  - aceitar;
  - mover essas faces para o `Corpo_Kart`, o que altera a divisão da Fase 3, mas não cria geometria;
  - removê-las, o que altera a geometria.

  Precisa de decisão do usuário antes das Fases 7/8.
- **Decisão pendente — nuca:** decidir se a borda visível de trás e na arfagem é aceitável, se a amplitude do giro deve ser limitada, ou se será criada uma tampa, o que alteraria a topologia.
- **Fase 7/8 (Godot):** se `visual_kart.gd` ainda calcular o raio da roda pela caixa da malha, o preenchimento do para-lama aumentaria o raio, de cerca de 0,120 m para até cerca de 0,139 m. Usar o raio medido (≈ 0,1195 m) na ficha do personagem.
