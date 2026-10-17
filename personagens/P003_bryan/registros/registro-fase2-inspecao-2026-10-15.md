# Registro da Fase 2 — inspeção e preservação da entrada — P003 Bryan

Data: 15/10/2026, 19:16–19:20 (-03:00).

## 1. Pedido e escopo

O usuário pediu o início da Fase 2 do Bryan. Escopo padrão de piloto jogável de kart: `Cabeca` (com pescoço), `Corpo_Kart` e quatro `Wheel_*`; acessórios (giroflex, antena, câmera, holofote, tablet, extintor, guincho, gaiola, caixas traseiras) ficam fixos no `Corpo_Kart`.

## 2. Ferramentas e forma de execução

- Blender 5.2.2 LTS, **somente pela sessão aberta via Blender MCP** (`execute_blender_code`). Nenhuma instância extra nem CLI do Blender.
- Estado inicial da sessão: `blender/bryan.blend` aberto, sem alterações não salvas, modo objeto, 1 objeto de malha. SHA-256 do arquivo em disco igual ao do checkpoint (`f116458b…c43201ef`).
- Scripts usados: [`scripts_fase2/`](scripts_fase2/). Análise do NPZ feita com `python3 -I` fora do Blender (somente leitura).
- Operações temporárias (câmera e render das vistas; carga da malha do backup na verificação) foram desfeitas com `wm.revert_mainfile`; a sessão terminou sem alterações não salvas.

## 3. Cópia de segurança

Antes de qualquer edição, o arquivo de trabalho foi copiado byte a byte:

| Arquivo | Tamanho | SHA-256 |
| --- | --- | --- |
| [`backups/bryan_antes_da_edicao_20261015_191749.blend`](../backups/bryan_antes_da_edicao_20261015_191749.blend) | 79.276.145 bytes | `f116458b74812705a7c8acca87bbc127763bb69f9a062dc539de44d4c43201ef` (igual ao `bryan.blend` de então) |

## 4. Levantamento do modelo

Detalhes completos em [`validacao/inspecao_malha_original.json`](../validacao/inspecao_malha_original.json).

| Item | Resultado |
| --- | --- |
| Objetos | 1 malha, `tripo_node_1db849c3-8e37-4423-b45a-4dcd0d8abf93`, sem pai, matriz mundial identidade, coleção `Scene Collection` |
| Contagens | 986.320 vértices, 2.839.751 arestas, 1.854.601 faces (todas triângulos), 5.563.803 cantos |
| Dimensões | X −0,3321…0,3321; Y −0,4898…0,4898; Z 0…0,7707 m (sistema métrico, escala 1) |
| UV | 1 camada `UVMap`, dentro de 0…1 |
| Materiais | 1 (`tripo_material_…`), índice 0 em todas as faces; texturas 4096² empacotadas: `bryan_basecolor.jpg`, `bryan_normal.png`, `bryan_rm.jpg` |
| Normais | Normais personalizadas (`custom_normal`); 1.840.200 faces suaves; atributos `sharp_face`/`sharp_edge` |
| Modificadores, grupos, shape keys, armature, ações | Nenhum |
| Ilhas conectadas | **1.170** (3 com mais de 10.000 vértices; 266 entre 1.001 e 10.000; 644 entre 101 e 1.000) |
| Vértices em posições coincidentes | 56.544 posições (costuras de UV do glTF; não foram soldados) |
| Arestas de borda / não-manifold (>2 faces) / soltas | 115.699 / 0 / 0 |

## 5. Orientação e escala

Vistas ortográficas texturizadas (Workbench) em [`vistas_fase2/`](vistas_fase2/):

- **Frente do kart: −Y** (`vista_neg_y.png` mostra o capô “POLÍCIA”, o guincho e o piloto de frente).
- **Esquerda do piloto: +X** (lado da antena e do extintor); Z para cima.
- Mesma convenção do Jake e do Dimi. Escala compatível: Bryan 0,66 × 0,98 × 0,77 m; Dimi 0,74 × 0,98 × 0,91 m; Jake 0,76 × 0,98 × 0,83 m.

## 6. Diagnóstico preliminar das partes (sem edição)

Detalhes em [`validacao/diagnostico_preliminar_partes.json`](../validacao/diagnostico_preliminar_partes.json); script [`pre_partes.py`](scripts_fase2/pre_partes.py). Limites medidos neste modelo, sem reaproveitar valores do Jake ou do Dimi.

- **Escopo padrão presente:** cabeça com quepe e óculos, corpo do piloto, kart e quatro rodas identificáveis nas vistas. Nenhuma divergência de escopo.
- **Rodas (estimativa pelo perfil YZ da face externa, |X| > 0,30):**

  | Roda | Centro Y, Z estimado (m) | Diâmetro Y / Z (m) |
  | --- | --- | --- |
  | `Wheel_Front_Left` (+X, −Y) | −0,2689; 0,1236 | 0,233 / 0,240 |
  | `Wheel_Front_Right` (−X, −Y) | −0,2688; 0,1233 | 0,233 / 0,241 |
  | `Wheel_Rear_Left` (+X, +Y) | 0,2938; 0,1232 | 0,236 / 0,240 |
  | `Wheel_Rear_Right` (−X, +Y) | 0,2936; 0,1229 | 0,236 / 0,240 |

  O modelo é quase simétrico em X. São centros preliminares; o critério definitivo do pivô fica para a Fase 4.
- **Risco para a Fase 3:** cada roda é formada por várias ilhas (8 a 20 inteiramente dentro do cilindro estimado) e há ilhas que **atravessam o limite da roda**. Exemplos: ilha 757 (9.436 v, 92% dentro da roda dianteira esquerda, mas se estende até X = 0,028) e ilha 113 (5.990 v, 71% dentro da traseira direita, até X = 0,008). Parte das ilhas parciais é para-lama/carroceria vizinha (o cilindro de teste começa em |X| = 0,19). Ainda não está comprovado que a separação por ilhas inteiras, sem corte, é suficiente — conferir visualmente essas ilhas antes de decidir.
- **Cabeça:** ilhas principais entre Z ≈ 0,47 e 0,73 e Y ≈ 0,01…0,21 (piloto sentado atrás do centro do kart). As ilhas 934, 945, 672, 633, 619, 676, 800, 801 e 328 (Y ≈ 0,35…0,49) também ficam acima de Z = 0,45, mas pertencem ao equipamento traseiro (antena, giroflex, câmera) e devem ser excluídas da seleção da cabeça.

## 7. Arrays originais e identificadores de rastreamento

[`backups/geometria_original.npz`](../backups/geometria_original.npz) (48.615.194 bytes; SHA-256 do arquivo `a7c558042c0902576b440f3c6a5bf16e25825d58eba79f5209e87d2c04c9c71f`) contém `co`, `edges`, `loops`, `uv`, `starts`, `totals`, `smooth`, `materials`, `corner_normals` e `components` (ilha de cada vértice).

SHA-256 dos bytes do array `co` (não do arquivo): `e707a208e8ed0565603308548fe5e39c19342df3fedc56d80679fd15d4ceb39e`.

Atributos inteiros adicionados a `bryan.blend` com o índice original de cada elemento: `rig_original_vertex` (ponto), `rig_original_edge` (aresta), `rig_original_face` (face), `rig_original_corner` (canto).

## 8. Tolerâncias definidas para as próximas validações

| Grandeza | Critério |
| --- | --- |
| Presença e unicidade | Cada `rig_original_*` aparece exatamente uma vez no conjunto das partes |
| Conectividade, UV, índice de material, suavização, `custom_normal`, `sharp_*` | Igualdade exata por identificador original |
| Posição mundial dos vértices | Desvio máximo ≤ 1e-6 m (arredondamento de float32 após mudança de origem); registrar o valor medido |
| Pivô em testes de rotação | Deslocamento ≤ 1e-6 m; corpo parado ao girar a cabeça/rodas |

## 9. Verificação após adicionar os atributos

[`validacao/verificacao_preservacao_fase2.json`](../validacao/verificacao_preservacao_fase2.json), executada depois de salvar e recarregar o arquivo do disco: `co`, arestas, cantos, UV, início/tamanho de faces, suavização e materiais **iguais** ao NPZ (desvio máximo de coordenadas 0,0); `custom_normal`, `sharp_face` e `sharp_edge` **iguais** ao backup; os quatro atributos de rastreamento conferem com a sequência 0…n−1; matriz mundial identidade. Material e imagens foram lidos antes de carregar o backup: 1 material e 3 imagens empacotadas.

Arquivo de trabalho resultante: `blender/bryan.blend`, 109.622.761 bytes, SHA-256 `5768c98f54ba1ae4124e52932ceb71cb30822910bd99db1090043f0cdcbb5478`. Ao fim, a sessão estava com esse arquivo aberto, recarregado do disco e sem alterações não salvas.

## 10. Limitações

- Nenhuma separação, rig ou mudança de origem foi feita.
- A aparência dos materiais não foi avaliada além das renderizações Workbench (`KHR_materials_volume` do GLB não conferido).
- O objeto ainda tem o nome gerado pelo Tripo; a padronização de nomes fica para a Fase 3.
- O salvamento gerou `blender/bryan.blend1` (versão anterior; backup automático local, ignorado pelo Git). O backup oficial é o de `backups/`.
