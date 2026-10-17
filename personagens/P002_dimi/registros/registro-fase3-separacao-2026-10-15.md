# Registro da Fase 3 — separação das partes — P002 Dimi

Data: 15/10/2026, 16:18–16:32 (-03:00).

## 1. Pedido e escopo

O usuário pediu para iniciar a Fase 3 do Dimi. O escopo é o padrão de todos os personagens: `Cabeca` (com o pescoço), `Corpo_Kart` e as quatro rodas `Wheel_*`. Móbile, mamadeira, molas e grades ficam fixos no `Corpo_Kart`. Pivôs, origens e rig ficam para a Fase 4. Nesta fase as origens continuam em `(0, 0, 0)`, com a matriz identidade.

## 2. Ferramentas e forma de execução

- Blender 5.2.2 LTS (`/Applications/Blender.app`), sempre em segundo plano (`-b --factory-startup`), uma instância por etapa. A sessão interativa/Blender MCP **não** foi usada nem alterada.
- Scripts em [`scripts_fase3/`](scripts_fase3/). As seleções vêm só de `backups/geometria_original.npz` (array `components`, uma ilha por vértice). Não foram usados limites nem índices do Jake.
- Conferência do estado inicial: SHA-256 de `blender/dimi.blend` = `c537c908…8da756e`, igual ao checkpoint.

## 3. Cópia de segurança

| Arquivo | SHA-256 |
| --- | --- |
| [`backups/dimi_antes_fase3_20261015_162824.blend`](../backups/dimi_antes_fase3_20261015_162824.blend) | `c537c908a5d02339e0121124c69c5f297420e810d048a55531b91e81d8da756e` (cópia byte a byte do arquivo da Fase 2) |

## 4. Identificação das partes

Os critérios ficam em [`scripts_fase3/rotulos_partes.py`](scripts_fase3/rotulos_partes.py). Cada ilha inteira recebe um só rótulo; o script falha se uma ilha cair em duas partes.

### Rodas

- **Centro do eixo de cada roda:** círculo ajustado no plano YZ aos vértices da face externa (|X| > 0,33). Resultado (Y, Z): FL `(-0.2515, 0.1288)`, FR `(-0.2511, 0.1292)`, RL `(0.2246, 0.1311)`, RR `(0.2286, 0.1282)`. Raio do pneu ≈ 0,13 m.
- **Critério:** uma ilha pertence à roda se (a) todos os seus vértices estão a até 0,15 m do eixo e no lado de fora da face interna do pneu (|X| ≥ 0,268); ou (b) é uma peça coaxial do cubo (raio ≤ 0,10 m) que chega ao plano do aro (|X| máx ≥ 0,30) sem entrar no corpo (|X| mín ≥ 0,20).
- **Ficam no corpo:** para-lamas e caixas de roda (raio de até 0,20 m e |X| a partir de 0,17), além dos eixos e semieixos que saem da carroceria (|X| mín < 0,20).
- **Conferência visual:** vistas coloridas de fora, de dentro, de baixo e de cima de cada canto, durante o diagnóstico (arquivos temporários fora do repositório). As bolinhas rosadas no topo da roda traseira esquerda (ilhas 950, 961 e 1002) foram conferidas com textura: são bolinhas decorativas presas ao pneu, como as demais, e ficaram na roda.

### Cabeça

- **Critério-base:** ilhas com Z mín ≥ 0,44, Z máx ≤ 0,76, centro |X| ≤ 0,16, Y entre −0,17 e 0,23. Ficam de fora as ilhas que começam em Y ≥ 0,165, que são pingentes do móbile atrás do boné (por exemplo, 585, 499 e 498).
- **Ajuste pela cor da textura** (mediana da textura base nas UVs de cada ilha):
  - **Removidas** da cabeça por serem gola ou capuz (azul): 273, 346, 462, 503 e 700.
  - **Incluídas** por serem pele do pescoço abaixo de Z 0,44 (rosadas): 482, 531, 548 e 556.
  - As ilhas 302 e 641 são a parte de baixo da aba do boné (vermelha) e ficaram na cabeça.
- **Conteúdo resultante:** boné com aba, rosto, cabelo, orelhas, chupeta e pele do pescoço, em 83 ilhas.

## 5. Separação

[`scripts_fase3/separar_partes.py`](scripts_fase3/separar_partes.py) seleciona vértices, arestas e faces de ilhas inteiras e usa `mesh.separate(type='SELECTED')`, uma parte por vez. O objeto restante foi renomeado para `Corpo_Kart`; cada objeto e sua malha usam o nome padrão. As ilhas de cada parte ficaram em [`validacao/separacao_partes_fase3.json`](../validacao/separacao_partes_fase3.json).

| Parte | Ilhas | Vértices | Faces | Centro da caixa (m) |
| --- | ---: | ---: | ---: | --- |
| `Cabeca` | 83 | 93.155 | 176.764 | (−0.0003, 0.0269, 0.561) |
| `Corpo_Kart` | 781 | 672.481 | 1.266.983 | (0.0041, 0.0, 0.4954) |
| `Wheel_Front_Left` | 58 | 58.232 | 110.318 | (0.2977, −0.2562, 0.1288) |
| `Wheel_Front_Right` | 51 | 56.941 | 108.004 | (−0.3006, −0.25, 0.1288) |
| `Wheel_Rear_Left` | 32 | 60.989 | 116.908 | (0.3018, 0.2282, 0.1342) |
| `Wheel_Rear_Right` | 35 | 53.679 | 102.377 | (−0.3081, 0.2286, 0.1289) |
| **Total** | **1.040** | **995.477** | **1.881.354** | — |

Não houve corte, subdivisão, solda, tampa, remalhamento nem mudança de origem.

## 6. Incidentes e correções

1. **Normais personalizadas recodificadas:** a passagem pelo modo de edição recodificou o atributo `custom_normal` (INT16_2D). O desvio máximo da normal decodificada chegou a 0,00143 (cerca de 0,08°). O caso é o mesmo já registrado no Jake. [`restaurar_normais.py`](scripts_fase3/restaurar_normais.py) copiou os valores codificados do backup pré-Fase 3 pelo `rig_original_corner`; a geometria não mudou. Depois disso, as normais decodificadas ficaram iguais às do NPZ, com desvio 0,0.
2. **Texturas duplicadas:** a primeira execução da restauração anexou o backup e salvou três cópias órfãs das texturas (`*.001`). [`remover_imagens_orfas.py`](scripts_fase3/remover_imagens_orfas.py) removeu essas cópias, que não eram usadas pelo material. O script de restauração foi corrigido depois para apagar o que anexa. A versão salva no repositório é a corrigida.
3. **Comparação de material no verificador:** o verificador listava o material anexado do backup (`.001`) como se fosse do arquivo e marcava erro. Passou a registrar materiais e imagens antes de anexar o backup e a comparar os índices de material com o NPZ.
4. **Enquadramento da vista da cabeça:** a primeira renderização usou uma matriz desatualizada e enquadrou mal a cabeça. O script ganhou `view_layer.update()` e as vistas foram refeitas. O modelo não foi afetado.
5. O arquivo `dimi.blend1`, criado automaticamente pelo Blender ao salvar um estado intermediário (com as texturas órfãs), foi apagado. O backup oficial é o da seção 3.

## 7. Validação

[`validacao/verificacao_separacao_fase3.json`](../validacao/verificacao_separacao_fase3.json), gerada por [`verificar_partes.py`](scripts_fase3/verificar_partes.py) em uma instância isolada, com o arquivo salvo: **`tudo_ok: true`**.

- Cada vértice, aresta, face e canto original aparece **exatamente uma vez** no conjunto das seis partes.
- Cada parte contém exatamente as ilhas do seu rótulo.
- Posições mundiais iguais às do NPZ: desvio máximo **0,0**, com as origens ainda em `(0, 0, 0)`.
- Arestas, cantos, início e ordem das faces, UV, suavização e índice de material iguais ao NPZ. O único material e as três texturas 4K empacotadas estão no arquivo.
- `custom_normal` igual ao backup pré-Fase 3 e normais de canto decodificadas iguais às do NPZ (desvio 0,0). `sharp_face` e `sharp_edge` iguais ao backup. O Blender removeu os atributos que ficaram todos falsos em uma parte: `sharp_edge` em todas e `sharp_face` nas rodas. A comparação tratou a ausência como falso.
- Nomes padronizados. Lados das rodas conferidos pela convenção frente −Y e esquerda do piloto +X.
- Nenhum pai, modificador ou armature; cada parte com malha exclusiva.
- Conferência independente do arquivo em disco: [`validacao/conferencia_blend_fase3.json`](../validacao/conferencia_blend_fase3.json) (6 objetos, 995.477 v, 1.881.354 f, 1 material, 3 imagens empacotadas, nenhum arquivo ausente).

Vistas com textura em [`vistas_fase3/`](vistas_fase3/): partes reunidas, vista explodida (deslocamento só na renderização, sem salvar), a cabeça e o corpo isolados e cada roda vista de fora e de dentro.

Arquivo de trabalho resultante: `blender/dimi.blend`, 108.629.425 bytes, SHA-256 `edac92bf920fa7ed0b9e1779ccc8b9590297b987c0b250d94afe2d0c1a51170d`.

## 8. Limitações e pontos para a Fase 4

- **A base da cabeça é aberta.** A malha gerada não fecha o pescoço, e por baixo do boné aparecem faces internas. Na pose original, a gola do capuz esconde essa abertura. Ao girar a cabeça na Fase 4, conferir se a abertura aparece. Não foi criada nenhuma tampa.
- Alguns fragmentos finos de pele do pescoço ficam dentro da gola. Eles acompanham a cabeça.
- As origens continuam em `(0, 0, 0)`. Os pivôs da cabeça (base do pescoço, perto de Z ≈ 0,42–0,45) e das rodas serão medidos na Fase 4. Os centros de eixo ajustados acima e os centros das caixas da tabela servem de ponto de partida, e não de decisão final.
- O ajuste fino da cabeça e das rodas usou critérios geométricos e de cor com conferência visual. Peças muito pequenas e escondidas, como os fragmentos do pescoço e as bolinhas presas ao pneu, foram decididas por proximidade e cor.
