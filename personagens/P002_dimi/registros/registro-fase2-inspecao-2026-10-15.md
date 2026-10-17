# Registro da Fase 2 — inspeção e preservação da entrada — P002 Dimi

Data: 15/10/2026, 16:07–16:15 (-03:00).

## 1. Pedido e escopo

O usuário confirmou que todo personagem é um **piloto jogável** com a estrutura padrão do Jake: cabeça (com pescoço), corpo/kart e quatro rodas independentes. Esse escopo passou a constar em [`PROMPT_NOVO_PERSONAGEM.md`](../../../documentacao/PROMPT_NOVO_PERSONAGEM.md). Em seguida, pediu a execução da Fase 2.

Acessórios do Dimi que não estão no escopo padrão (móbile com hélice, mamadeira, molas, grades) ficam no `Corpo_Kart` como partes fixas.

## 2. Ferramentas e forma de execução

- Blender 5.2.2 LTS (`/Applications/Blender.app`), sempre em segundo plano (`-b --factory-startup`), uma instância por etapa. A sessão interativa/Blender MCP **não** foi usada nem alterada.
- Scripts usados: [`scripts_fase2/`](scripts_fase2/).

## 3. Cópia de segurança

Antes de qualquer edição, o arquivo de trabalho foi copiado byte a byte:

| Arquivo | SHA-256 |
| --- | --- |
| [`backups/dimi_antes_da_edicao_20261015_160718.blend`](../backups/dimi_antes_da_edicao_20261015_160718.blend) | `9befa956304543499b25f9cb134c45a0f33603c8db0cdbff35be042b0825bfd8` (igual ao `dimi.blend` de então) |

## 4. Levantamento do modelo

Detalhes completos em [`validacao/inspecao_malha_original.json`](../validacao/inspecao_malha_original.json).

| Item | Resultado |
| --- | --- |
| Objetos | 1 malha, `tripo_node_e9d2c8b0-6721-4488-b079-0d0338a98d93`, sem pai, matriz mundial identidade |
| Contagens | 995.477 vértices, 2.875.792 arestas, 1.881.354 faces (todas triângulos), 5.644.062 cantos |
| Dimensões | X −0,3716…0,3716; Y −0,4902…0,4902; Z 0…0,9138 m (sistema métrico, escala 1) |
| UV | 1 camada `UVMap`, dentro de 0…1 |
| Materiais | 1 (`tripo_material_…`), índice 0 em todas as faces; texturas 4096² empacotadas: basecolor, normal, roughness/metal |
| Normais | Normais personalizadas (`custom_normal`); 1.871.081 faces suaves; atributos `sharp_face`/`sharp_edge` |
| Modificadores, grupos, shape keys, armature, ações | Nenhum |
| Ilhas conectadas | **1.040** (5 com mais de 10.000 vértices; 303 entre 1.001 e 10.000) |
| Vértices em posições coincidentes | 52.614 posições (costuras de UV do glTF; não foram soldados) |
| Arestas de borda / não-manifold (>2 faces) / soltas | 107.522 / 0 / 0 |

## 5. Orientação e escala

Vistas ortográficas texturizadas em [`vistas_fase2/`](vistas_fase2/):

- **Frente do kart: −Y** (vista `vista_neg_y.png` mostra o capô com o número 1).
- **Esquerda do piloto: +X** (lado da mamadeira); Z para cima.
- Mesma convenção do Jake. Escala compatível: Dimi 0,74 × 0,98 × 0,91 m; Jake 0,76 × 0,98 × 0,83 m (Z 0,06…0,89).

## 6. Diagnóstico preliminar das partes (sem edição)

Detalhes em [`validacao/diagnostico_preliminar_partes.json`](../validacao/diagnostico_preliminar_partes.json).

- **Rodas:** há ilhas próprias nos quatro cantos (|X| > 0,255, Z < 0,30). O critério bruto ainda inclui peças vizinhas (faixa em Y de ~0,43 m para rodas de ~0,28 m de altura). A seleção definitiva e a conferência visual ficam para a Fase 3.
- **Cabeça:** formada por várias ilhas entre Z ≈ 0,43 e 0,75 (rosto, boné, cabelo, chupeta); o móbile ocupa Z ≈ 0,80–0,91 e precisa ser excluído da seleção.
- **Conclusão:** a separação por ilhas inteiras, sem corte, parece viável, como no Jake. Ainda não foi comprovada.

## 7. Arrays originais e identificadores de rastreamento

[`backups/geometria_original.npz`](../backups/geometria_original.npz) (SHA-256 do arquivo `da7b48ea…1be95e6`) contém `co`, `edges`, `loops`, `uv`, `starts`, `totals`, `smooth`, `materials`, `corner_normals` e `components` (ilha de cada vértice).

SHA-256 dos bytes do array `co` (não do arquivo): `f177cb1e00e186ce4bff67028af4f8178f9e897a5d0688833804fec1edc90c27`.

Atributos inteiros adicionados a `dimi.blend` com o índice original de cada elemento: `rig_original_vertex` (ponto), `rig_original_edge` (aresta), `rig_original_face` (face), `rig_original_corner` (canto).

## 8. Tolerâncias definidas para as próximas validações

| Grandeza | Critério |
| --- | --- |
| Presença e unicidade | Cada `rig_original_*` aparece exatamente uma vez no conjunto das partes |
| Conectividade, UV, índice de material, suavização, `custom_normal`, `sharp_*` | Igualdade exata por identificador original |
| Posição mundial dos vértices | Desvio máximo ≤ 1e-6 m (arredondamento de float32 após mudança de origem); registrar o valor medido |
| Pivô em testes de rotação | Deslocamento ≤ 1e-6 m; corpo parado ao girar a cabeça/rodas |

## 9. Verificação após adicionar os atributos

[`validacao/verificacao_preservacao_fase2.json`](../validacao/verificacao_preservacao_fase2.json): `co`, arestas, cantos, UV, início/tamanho de faces, suavização e materiais **iguais** ao NPZ (desvio máximo de coordenadas 0,0); `custom_normal`, `sharp_face` e `sharp_edge` **iguais** ao backup; os quatro atributos de rastreamento conferem com a sequência 0…n−1. Os nomes `.001` de material e imagens no relatório vêm da biblioteca do backup carregada só durante a verificação; o arquivo salvo tem 1 material e 3 imagens (conferido em outra instância).

Arquivo de trabalho resultante: `blender/dimi.blend`, 109.683.656 bytes, SHA-256 `c537c908a5d02339e0121124c69c5f297420e810d048a55531b91e81d8da756e`.

## 10. Limitações

- Nenhuma separação, rig ou mudança de origem foi feita.
- A aparência dos materiais não foi avaliada além das renderizações Workbench.
- O objeto ainda tem o nome gerado pelo Tripo; a padronização de nomes fica para a Fase 3.
