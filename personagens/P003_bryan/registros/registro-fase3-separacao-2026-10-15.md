# Registro da Fase 3 — separação das partes — P003 Bryan

Data: 15/10/2026, 19:23–19:45 (-03:00).

## 1. Pedido e escopo

O usuário pediu para seguir para a Fase 3 do Bryan. O escopo é o padrão de todos os personagens: `Cabeca` (com o pescoço), `Corpo_Kart` e as quatro rodas `Wheel_*`. Giroflex, antena, câmera, holofote, tablet, extintor, guincho, gaiola, caixas traseiras, rádio do ombro e gola ficam fixos no `Corpo_Kart`. Pivôs, origens e rig ficam para a Fase 4. Nesta fase as origens continuam em `(0, 0, 0)`, com a matriz identidade.

## 2. Ferramentas e forma de execução

- Blender 5.2.2 LTS, **somente pela sessão aberta via Blender MCP**. Nenhuma instância extra nem CLI do Blender.
- Estado inicial: sessão com `blender/bryan.blend`, sem alterações não salvas; SHA-256 igual ao do checkpoint (`5768c98f…0cdcbb5478`).
- Scripts em [`scripts_fase3/`](scripts_fase3/). As seleções vêm só de `backups/geometria_original.npz`. Não foram usados limites nem índices do Jake ou do Dimi.
- Os diagnósticos visuais (cores temporárias, câmeras) foram desfeitos com `wm.revert_mainfile`, sem salvar.

## 3. Cópia de segurança

| Arquivo | SHA-256 |
| --- | --- |
| [`backups/bryan_antes_fase3_20261015_192311.blend`](../backups/bryan_antes_fase3_20261015_192311.blend) | `5768c98f54ba1ae4124e52932ceb71cb30822910bd99db1090043f0cdcbb5478` (cópia byte a byte do arquivo da Fase 2) |

## 4. Impedimento encontrado e decisão do usuário

**O modelo não permite separar as rodas só por ilhas inteiras**, a estratégia usada no Jake e no Dimi:

- **Assoalho fundido ao pneu:** nas ilhas 757 (FL), 234 (FR) e 113 (RR), uma placa plana do assoalho (faces horizontais em Z ≈ 0,080, de |X| ≈ 0 a 0,20) está na mesma ilha que a banda de rodagem e a parede interna do pneu. Evidência: [`ilhas_fundidas_baixo.png`](vistas_fase3/diagnostico/ilhas_fundidas_baixo.png) e [`ilha757_assoalho_pneu_FL.png`](vistas_fase3/diagnostico/ilha757_assoalho_pneu_FL.png) (vermelho).
- **Pneu fundido ao vão do para-lama:** em todas as rodas, várias ilhas misturam o pneu (raio ≤ 0,123 m) com um preenchimento escuro, com cor de pneu, que sobe para dentro do para-lama (até r ≈ 0,149 m).

Com ilhas inteiras, uma fatia do assoalho giraria com a roda, ou um pedaço do pneu ficaria parado. A receita exige registrar o impedimento e resolver o escopo antes de cortar. Foram apresentadas três opções ao usuário: dividir pelas arestas existentes, manter só ilhas inteiras aceitando os artefatos, ou parar e revisar o modelo. **O usuário escolheu dividir pelas arestas existentes.**

**Diferença em relação à receita:** a divisão não cria faces, não subdivide, não move vértices e não solda nada. Ela **duplica os vértices e as arestas da costura** entre roda e corpo, então a topologia de vértices e arestas **não** é preservada exatamente. Faces e cantos continuam preservados exatamente.

## 5. Identificação das partes

Critérios em [`scripts_fase3/rotulos_faces.py`](scripts_fase3/rotulos_faces.py). Cada **face** recebe um rótulo; o script falha se uma face cair em duas partes.

### Rodas

- **Eixo de cada roda:** círculo ajustado no plano YZ à silhueta da face externa (|X| > 0,31). Resultado (Y, Z): FL `(−0,2694; 0,1229)`, FR `(−0,2693; 0,1227)`, RL `(0,2939; 0,1233)`, RR `(0,2938; 0,1233)`. Raio externo da banda ≈ 0,123 m (0,117 na face externa arredondada).
- **Critério por face:** a face pertence à roda se todos os seus vértices estão a até **0,1265 m** do eixo e em |X| ≥ **0,15**, e se a face **não** é da placa do assoalho (os três vértices em Z = 0,0805 ± 0,002, normal vertical e |X| máx ≤ 0,205).
- **Limpeza:** dentro de cada ilha dividida, componentes conexos com menos de **60 faces** voltam ao rótulo vizinho, para não deixar fragmentos soltos.
- **Resultado:** 42 ilhas divididas (14 em FL, 14 em FR, 7 em RL, 7 em RR); as demais ilhas de roda são inteiras. Conferência visual com textura em [`divisao_faces_FL.png`](vistas_fase3/diagnostico/divisao_faces_FL.png), [`_FR`](vistas_fase3/diagnostico/divisao_faces_FR.png), [`_RL`](vistas_fase3/diagnostico/divisao_faces_RL.png) e [`_RR`](vistas_fase3/diagnostico/divisao_faces_RR.png): a linha de corte acompanha o contorno do pneu, e assoalho e vão do para-lama ficam no corpo.

### Cabeça

Separada por **17 ilhas inteiras**, sem divisão. A escolha usou posição, a cor mediana da textura base nas UVs de cada ilha e conferência visual ([`cabeca_gola_radio.png`](vistas_fase3/diagnostico/cabeca_gola_radio.png)):

- **Na cabeça:** quepe (511, 510, 749, 474, 497, 611), insígnia (712), óculos (516, 522, 523), cabelo (559, 481, 536), orelhas (496, 758), rosto (529) e pele do pescoço (570).
- **No corpo:** gola da camisa (500, 501, 545, 556, 711, 766, 817) e rádio do ombro esquerdo (790, 806, 829, 835, 852).

## 6. Separação

[`scripts_fase3/separar_partes.py`](scripts_fase3/separar_partes.py) seleciona as faces de cada rótulo (vértices e arestas selecionados somente quando pertencem a uma face selecionada, para não levar arestas soltas) e usa `mesh.separate(type='SELECTED')`, uma parte por vez. O objeto restante foi renomeado para `Corpo_Kart`; cada objeto e sua malha usam o nome padrão. Faces e ilhas de cada parte: [`validacao/separacao_partes_fase3.json`](../validacao/separacao_partes_fase3.json).

| Parte | Ilhas inteiras | Ilhas divididas | Vértices | Faces | Centro da caixa (m) |
| --- | ---: | ---: | ---: | ---: | --- |
| `Cabeca` | 17 | 0 | 41.982 | 80.608 | (0.0014, 0.0992, 0.6139) |
| `Corpo_Kart` | 1.052 | 42 | 771.146 | 1.439.415 | (0.0006, 0.0000, 0.4132) |
| `Wheel_Front_Left` | 10 | 14 | 41.998 | 80.611 | (0.2405, -0.2697, 0.1246) |
| `Wheel_Front_Right` | 10 | 14 | 42.702 | 81.386 | (-0.2399, -0.2698, 0.1247) |
| `Wheel_Rear_Left` | 23 | 7 | 45.724 | 87.392 | (0.2407, 0.2913, 0.1252) |
| `Wheel_Rear_Right` | 16 | 7 | 44.498 | 85.189 | (-0.2411, 0.2911, 0.1249) |
| **Total** | — | — | **988.050** | **1.854.601** | — |

Total de vértices = 986.320 originais + 1.730 duplicados na costura; arestas = 2.839.751 + 1.689. Nenhuma face nova, corte, subdivisão, solda, tampa, remalhamento ou mudança de origem.

## 7. Incidentes e correções

1. **Normais personalizadas recodificadas** pela passagem no modo de edição (já visto no Jake e no Dimi). [`restaurar_normais.py`](scripts_fase3/restaurar_normais.py) copiou os códigos `custom_normal` do backup pré-Fase 3 pelo `rig_original_corner`.
2. **Cantos da costura:** nos vértices duplicados, o código original é relativo ao leque de normais do vértice inteiro e decodificava outra direção (desvio de até 0,91). Para esses cantos, e só para eles, o código foi refeito a partir do vetor original do NPZ com `normals_split_custom_set`. Os demais cantos mantêm o código original. Um primeiro teste recodificou todos os cantos da roda traseira esquerda (61.852 códigos alterados, erro de 5,8e-4); foi desfeito e substituído pelo método só na costura.
3. **Arestas marcadas como sharp:** o modo de edição e depois o `normals_split_custom_set` marcaram como `sharp_edge` 3 arestas de faces quase degeneradas (≈ 4e-7 m²) da ilha 257 do corpo, o que desviava 12 cantos em até 1,81. `sharp_edge` e `sharp_face` foram restaurados do backup **depois** da recodificação.
4. A malha do backup, anexada em uma das conferências, ficou na sessão com o nome `meshes[0]` e foi removida antes de salvar. O arquivo salvo tem 6 malhas, 1 material e 3 imagens.
5. `blender/bryan.blend1` (gerado ao salvar) é a versão da Fase 2, igual ao backup pré-Fase 3; backup automático local, ignorado pelo Git.

## 8. Validação

[`validacao/verificacao_separacao_fase3.json`](../validacao/verificacao_separacao_fase3.json), gerada por [`verificar_partes.py`](scripts_fase3/verificar_partes.py) com o arquivo salvo e recarregado do disco: **`tudo_ok: true`**.

- Cada **face** e cada **canto** original aparece **exatamente uma vez** no conjunto das seis partes, e cada face está na parte do seu rótulo.
- Cada **vértice** e **aresta** original aparece uma vez por parte cujas faces o usam: 1.730 vértices e 1.689 arestas aparecem duas vezes (costura); todos os demais, uma vez. Nenhum vértice sem aresta nem aresta sem face.
- Posições mundiais iguais às do NPZ: desvio máximo **0,0**, com as origens ainda em `(0, 0, 0)`.
- Arestas (por vértices originais), cantos, arestas dos cantos, início e ordem das faces, UV, suavização e índice de material iguais ao NPZ. O único material e as três texturas 4K empacotadas estão no arquivo.
- **Normais de canto decodificadas:** iguais ao NPZ (desvio **0,0**) em todos os cantos fora da costura. Na costura, desvio máximo de **4,5e-4** (≈ 0,026°), dentro da tolerância nova de 1e-3 definida para esses cantos. `sharp_face` e `sharp_edge` iguais ao backup. A `Cabeca` não tem `sharp_*` porque eram todos falsos; a ausência foi tratada como falso.
- Nomes padronizados; lados das rodas conferidos pela convenção frente −Y e esquerda do piloto +X.
- Nenhum pai, modificador ou armature; cada parte com malha exclusiva.
- Conferência do arquivo em disco: [`validacao/conferencia_blend_fase3.json`](../validacao/conferencia_blend_fase3.json) (6 objetos, 988.050 v, 1.854.601 f, 1 material, 3 imagens empacotadas, nenhum arquivo ausente).

Vistas com textura em [`vistas_fase3/`](vistas_fase3/): partes reunidas; vistas explodidas iso, de trás e de baixo (deslocamento só na renderização, sem salvar); cabeça e corpo isolados; cada roda por fora e por dentro.

Arquivo de trabalho resultante: `blender/bryan.blend`, 108.940.246 bytes, SHA-256 `0ffb28027b6cbbbce958ac1aae6188dbc4d6b1821d6693ce8a02c7dad0954d17`.

## 9. Limitações e pontos para a Fase 4

- **Costura aberta:** a divisão deixa bordas abertas onde o pneu encostava no assoalho e no vão do para-lama. Na pose parada, elas ficam no mesmo lugar e não aparecem. Ao girar a roda, conferir se aparece alguma fresta.
- **Parede interna do pneu:** abaixo do nível do assoalho, a parede interna de cada roda tem uma faixa plana com textura borrada (geometria original, antes escondida pela placa). Ao girar, essa faixa sobe e passa por trás do corpo. Avaliar na Fase 5 se fica visível.
- **Borda superior serrilhada:** no topo das rodas, o limite de raio de 0,1265 m deixa uma borda irregular onde o preenchimento do para-lama foi cortado. Fica dentro do para-lama.
- **A base da cabeça é aberta**, sem tampa, como no Dimi. A gola fica no corpo e esconde a abertura na pose original. Conferir ao girar a cabeça.
- As origens continuam em `(0, 0, 0)`. O pivô da cabeça (base do pescoço, perto de Z ≈ 0,49–0,50) e os das rodas serão medidos na Fase 4. Os eixos ajustados acima são ponto de partida, e não decisão final.
- **Validações do Blender que dependem da costura** (na Fase 5) devem usar as tolerâncias desta fase: igualdade exata fora da costura e desvio ≤ 1e-3 nas normais dos cantos da costura.
