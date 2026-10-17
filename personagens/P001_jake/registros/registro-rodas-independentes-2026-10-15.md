# P001.05 — Separação das quatro rodas do kart

Data: **15/10/2026**. Personagem: **P001 — Jake**. Registro central: [ficha do personagem](../LEIA-ME.md#p00105--separação-das-quatro-rodas).

## Pedido e resultado

Separar as quatro rodas do carro em objetos independentes, preservando sua geometria e topologia, centralizar as origens e padronizar os nomes para futuro controle na Godot.

O trabalho foi realizado na cena aberta com o **Blender MCP** e salvo em [kart_modular_rig.blend](../blender/jake.blend). Cada roda possui seu próprio objeto e datablock de malha, com um único usuário. A frente do modelo é **−Y**; os lados são os do piloto, com **+X à esquerda**.

| Objeto | Vértices | Faces |
| --- | ---: | ---: |
| `Wheel_Front_Left` | 52.726 | 102.418 |
| `Wheel_Front_Right` | 54.282 | 104.530 |
| `Wheel_Rear_Left` | 67.616 | 131.736 |
| `Wheel_Rear_Right` | 67.642 | 131.660 |
| `Corpo_Kart` restante | 632.659 | 1.192.172 |
| Total da malha anterior de `Corpo_Kart` | 874.925 | 1.662.516 |

`Cabeca` permaneceu separada e fora dessa partição. O modelo passou a ter seis objetos de malha.

## Procedimento executado

1. Inspecionar a cena, o objeto `Corpo_Kart`, o modificador Armature, as transformações, os grupos, os atributos de rastreamento e as ilhas conectadas.
2. Salvar uma cópia do estado aberto antes da edição: [kart_antes_separar_rodas_20261015_134523.blend](../backups/kart_antes_separar_rodas_20261015_134523.blend).
3. Identificar as rodas entre as **752 ilhas** de `Corpo_Kart`, usando limites espaciais e projeções da geometria para conferir pneus, aros e conexões com os eixos. Esses limites são específicos deste modelo.
4. Selecionar conjuntos completos de ilhas e usar separação de malha por seleção para criar cada objeto. Não houve subdivisão, remalhamento, corte de faces, tampa, redimensionamento ou deformação das rodas.
5. Nomear os objetos conforme a tabela e suas malhas com o sufixo `_Mesh`.
6. Aplicar `ORIGIN_GEOMETRY` com centro `BOUNDS`, compensando a representação local para manter a geometria na posição original.
7. Substituir, nas rodas, o modificador Armature herdado por parentesco direto com `Torso_Bone` de `Personagem_Rig`. Compensar as transformações para conservar o acompanhamento anterior do rig. O corpo restante manteve sua configuração anterior.
8. Comparar os elementos com uma cópia de referência pelos identificadores `rig_original_vertex`, `rig_original_edge`, `rig_original_face` e `rig_original_corner`.
9. Restaurar os dados codificados de normais personalizadas após a passagem pela separação em modo de edição e confirmar sua igualdade com a referência.
10. Testar temporariamente giro e esterço, restaurar as rotações, salvar o arquivo e conferir a versão em disco.

## Pivôs e controle

O centro adotado é o **centro da caixa delimitadora de toda a geometria atribuída a cada roda**. Não corresponde a uma média ponderada pela densidade de vértices nem a um novo ajuste manual de eixo mecânico. Os conjuntos preservam as ilhas completas, incluindo pequenas conexões já pertencentes a elas.

As coordenadas abaixo estão no espaço de referência anterior ao deslocamento do rig. As coordenadas mundiais observadas também estão no [relatório JSON](../validacao/verificacao_rodas_independentes.json).

| Objeto | X | Y | Z |
| --- | ---: | ---: | ---: |
| `Wheel_Front_Left` | 0.2334213555 | −0.2603454292 | 0.1025467068 |
| `Wheel_Front_Right` | −0.2538298965 | −0.2603531182 | 0.1022796631 |
| `Wheel_Rear_Left` | 0.3068847656 | 0.1983032674 | 0.1189727709 |
| `Wheel_Rear_Right` | −0.3051986694 | 0.1984176189 | 0.1192931905 |

O giro usa **X local** e o esterço usa **Z local**. As quatro rodas são objetos e malhas independentes, embora continuem vinculadas ao osso do torso para acompanhar a animação existente. Não foram criados ossos novos, ações de rodagem ou controladores de direção.

## Verificações e evidências

O relatório [verificacao_rodas_independentes.json](../validacao/verificacao_rodas_independentes.json) registra:

- Presença de cada elemento original exatamente uma vez na partição: **874.925 vértices, 2.536.689 arestas, 1.662.516 faces e 4.987.548 cantos**. Não houve perda ou duplicação de elementos.
- Erro **zero** ao reconstruir as coordenadas originais a partir das malhas recentradas; conectividade de arestas, vértices por canto, tamanhos de polígonos e pertencimento de cantos às faces preservados.
- Igualdade dos UVs, dos dados codificados de normais personalizadas, dos índices de materiais e da suavização. A igualdade dos dados codificados não afirma ausência absoluta de arredondamento na decodificação das normais após mudar a origem.
- Erro máximo de centralização da origem de `1.666000468656264e-8` unidade, compatível com a precisão numérica da malha.
- Nos quadros **1, 8, 17, 29 e 49**, diferença máxima por componente das posições mundiais de `5.960464477539063e-8` unidade em relação ao acompanhamento anterior do rig; diferença máxima da posição mundial prevista do pivô de `3.332000986233652e-8` unidade.
- Testes temporários de **90° em X** e **30° em Z**, em cada roda, com deslocamento medido do pivô igual a **zero**. As transformações originais foram restauradas.

A cena resultante foi conferida visualmente pelo Blender MCP. A tentativa de conferir o arquivo salvo pela ferramenta de execução em segundo plano do MCP falhou porque ela não encontrou o executável `blender`. A conferência em disco foi então concluída com uma segunda instância do Blender 5.2.2 instalada no computador: os quatro objetos existiam, as malhas eram exclusivas e as somas de vértices, arestas e faces correspondiam ao original. Essa conferência abriu o arquivo sem modificá-lo.

## Versionamento e limites

O **commit local `e2a2848`**, `feat: separa rodas do kart com pivôs independentes`, inclui o modelo, o backup desta etapa e o relatório numérico. Não foi realizado envio remoto nesta etapa. Este documento e a atualização do registro central complementam essa entrega em um commit documental posterior, junto ao índice e aos registros referenciados da evolução do personagem.

As verificações demonstram a separação e o comportamento dos pivôs no Blender. A exportação, a convenção de eixos após importação, o controle por script e a validação visual de rodagem ou esterço na Godot permanecem como próximas etapas. Os relatórios das etapas anteriores continuam sendo evidências históricas das respectivas versões do modelo.
