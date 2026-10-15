# Registro do rig e da separação do personagem

Data do trabalho: **15/10/2026**.

Projeto: `/Users/patricksoares/Documents/jogos/kart`.

Este documento descreve o que foi efetivamente executado nesta conversa, incluindo operações intermediárias que não permaneceram no resultado. As evidências são os retornos das ferramentas Blender MCP, as inspeções visuais e os arquivos relacionados abaixo. Não é um registro de um novo teste do Blender realizado durante a escrita da documentação.

## 1. Pedido recebido

Estruturar o esqueleto do personagem existente, separar cabeça e corpo, atribuir pesos exclusivos e posicionar a origem da cabeça na base do pescoço, preservando a forma, as proporções e a geometria originais.

## 2. Estado inicial observado

- Blender conectado pelo MCP, versão reportada: `5.2.2 LTS`.
- Cena: `Scene`; coleção: `Collection`; espaço de trabalho: `Layout`.
- Um único objeto de malha visível, reunindo personagem e kart:
  - Objeto: `tripo_node_be6224ef-9098-43f1-9b06-3e74ae9f6386`.
  - Dados da malha: `meshes[0]`.
  - Transformação mundial: identidade; localização e rotação zeradas, escala unitária.
  - Sem pai, modificadores, grupos de vértices ou shape keys.
  - Um material: `tripo_material_be6224ef-9098-43f1-9b06-3e74ae9f6386`.
  - Uma camada UV: `UVMap`.
- `Camera` e `Light` também estavam na cena.
- Existiam dados sem objetos usuários, incluindo `Body_Mesh` e `Head_Mesh`, com 362 vértices cada, e a armature `Kart_Character_Rig_Data`. Esses dados não foram usados como geometria ou esqueleto do resultado.
- A cena indicava o caminho `kart_modular_rig.blend` e alterações pendentes. A existência do arquivo nesse caminho não foi presumida; o salvamento final foi feito explicitamente.

| Elemento da malha original | Quantidade |
| --- | ---: |
| Vértices | 1.034.971 |
| Arestas | 3.002.354 |
| Faces | 1.968.221 |
| Cantos de faces, ou loops | 5.904.663 |
| Ilhas conectadas pelas arestas existentes | 838 |

Limites mundiais originais, em unidades da cena:

| Eixo | Mínimo | Máximo |
| --- | ---: | ---: |
| X | -0.38116455078125 | 0.38116455078125 |
| Y | -0.490386962890625 | 0.490386962890625 |
| Z | 0 | 0.827239990234375 |

As três imagens de textura de 4096 × 4096 estavam empacotadas no Blender: `go-kart+3d+model_basecolor.jpg`, `go-kart+3d+model_normal.png` e `go-kart+3d+model_rm.jpg`.

## 3. Ferramentas e forma de execução

Foram usadas as ferramentas do **Blender MCP** para consultar a cena e os objetos, enquadrar a malha, capturar imagens da viewport e executar operações no Blender.

As operações de separação, origem, armature, pesos, validação e salvamento foram enviadas por `execute_blender_code`, usando a API `bpy` e NumPy dentro do Blender. Foram usados operadores do Blender para separar e reunir objetos, mudar a origem, criar a armature e salvar arquivos. A API de dados foi usada para leituras precisas, atributos de rastreamento, posições dos ossos, grupos e modificadores.

Também foram feitas leituras locais para conferir os arquivos e o estado do Git. Nenhum commit, publicação ou exportação para outro formato foi realizado. Não foi salvo um script `.py` autônomo contendo toda a sessão; este documento não deve ser confundido com um script de reprodução integral.

## 4. Cópia de segurança e registro da geometria

Antes da primeira separação, foi salva uma cópia da cena com `save_as_mainfile(..., copy=True)`:

`rigging/kart_antes_do_rig_20261015_120547.blend`

Essa cópia foi feita antes de adicionar os atributos de rastreamento e antes de separar a cabeça.

As coordenadas e os índices originais foram mantidos temporariamente em `bpy.app.driver_namespace['rig_preservation_state']`. Esse estado é auxiliar da sessão, não um mecanismo de persistência do arquivo `.blend`.

Foi criado o arquivo `rigging/geometria_original.npz`, contendo:

- `co`: coordenadas locais originais dos vértices, em `float32`.
- `edges`: índices originais dos pares de vértices das arestas.
- `loops`: vértice original de cada canto de face.
- `uv`: coordenadas UV de cada canto.
- `starts` e `totals`: início e tamanho de cada face na sequência de cantos.
- `smooth`: sinalizadores originais de suavização das faces.
- `materials`: índices originais de material das faces.
- `components`: identificação da ilha conectada de cada vértice.

Hash SHA-256 observado para os bytes do array original de coordenadas, **não para o arquivo NPZ**:

`39c07c36302dc3b37e6fb8deafff1219541431846984d50c245af8098b9efacb`

Foram adicionados atributos inteiros à malha para rastrear os elementos depois das separações e reuniões:

| Atributo | Domínio | Valor inicial |
| --- | --- | --- |
| `rig_original_vertex` | Ponto | Índice original do vértice |
| `rig_original_edge` | Aresta | Índice original da aresta |
| `rig_original_face` | Face | Índice original da face |
| `rig_original_corner` | Canto | Índice original do canto |

Esses atributos permaneceram nas duas malhas finais.

## 5. Inspeção e identificação da cabeça

A malha foi enquadrada na viewport. Foi ativada a visualização de materiais e usada a vista lateral direita para distinguir cabeça, pescoço, roupa e kart.

As 838 ilhas foram calculadas por conectividade das arestas. Foram examinados seus limites, centros e quantidades de vértices. Também foram amostradas cores da textura base pelas UVs para ajudar a distinguir pele, roupa e peças do kart. Essa leitura não alterou a textura nem as UVs.

A seleção da cabeça usou ilhas inteiras, com esta regra sobre a numeração interna calculada naquela sessão:

```python
head_comp = maxs[:, 2] > 0.49
head_comp[[294, 589]] = False
head_vertices = head_comp[component_labels]
```

As ilhas `294` e `589` foram excluídas por pertencerem à roupa. Esses números são identificadores do diagnóstico original, não nomes de objetos nem índices de vértices. O array `components` do NPZ preserva a correspondência usada na seleção.

Foi confirmado que nenhuma aresta existente ligava um vértice selecionado a outro não selecionado. A seleção abrangia **86 ilhas**. Assim, a cabeça pôde ser separada sem inserir um plano de corte, subdividir faces ou duplicar vértices de fronteira.

Com `mesh.separate(type='SELECTED')`, foi criado o objeto `Cabeca`, com dados `Cabeca_Geometria_Original`. O restante recebeu inicialmente o nome `Corpo_e_Kart`.

| Resultado dessa separação | Vértices | Faces |
| --- | ---: | ---: |
| `Cabeca` | 160.046 | 305.705 |
| Restante da malha | 874.925 | 1.662.516 |
| Total | 1.034.971 | 1.968.221 |

A cabeça foi visualizada isoladamente para conferir rosto, boca, boné e região do pescoço. **Não foi realizado um corte planar nem criado um fechamento novo na base do pescoço.** O limite resultante aproveita a geometria existente, incluindo as partes do pescoço que ficam por dentro da roupa.

## 6. Diagnósticos e separações intermediárias de corpo e kart

Houve uma investigação adicional para tentar separar também o personagem do veículo. Ela não permaneceu como separação final:

1. Foi calculada uma conectividade virtual por posições exatamente coincidentes. Nenhum vértice foi soldado. Foram encontradas 984.027 posições únicas e três grandes conjuntos virtuais, com 30.821, 35.181 e 968.969 vértices. O maior ainda reunia regiões do personagem e do veículo, portanto não resolvia a separação semântica.
2. Uma seleção heurística de ilhas por posição e cor gerou temporariamente `Corpo`, com 193.666 vértices, e `Kart`, com 681.259 vértices. A cabeça continuou separada.
3. Após inspeção visual isolada, esses dois objetos foram reunidos e uma segunda seleção foi testada, gerando `Corpo`, com 221.188 vértices, e `Kart`, com 653.737 vértices.
4. As imagens isoladas mostraram limites incompletos em regiões de roupa, calça, sapatos e contato com o veículo. Essa divisão não foi adotada como resultado.
5. `Corpo` e `Kart` foram reunidos novamente com `object.join()`, formando o objeto final **`Corpo_Kart`**, com os mesmos 874.925 vértices do restante da malha após separar a cabeça.

As seleções intermediárias não deslocaram vértices e não ficaram como objetos separados no arquivo final. A validação final conferiu todos os identificadores originais após essas operações.

## 7. Origem e pivô da cabeça

Foram examinadas faixas de vértices próximas às alturas Z de 0.42, 0.44, 0.46 e 0.48 para localizar a base do pescoço. Foram comparados numericamente candidatos de pivô e o arredondamento gerado pela compensação das coordenadas locais.

O pivô escolhido foi:

```text
X =  0
Y = -0.0625
Z =  0.4375
```

São coordenadas mundiais, em unidades da cena. O cursor 3D foi movido temporariamente para essa posição, e foi executado `object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')` somente na cabeça. A posição anterior do cursor foi restaurada.

**A mudança de origem altera a representação das coordenadas locais da cabeça**, compensando a transformação do objeto para manter sua posição e forma mundiais. Portanto, não houve identidade bit a bit de todas as coordenadas locais depois dessa operação. Houve arredondamento de ponto flutuante, quantificado na seção de validação. Não foi aplicada uma edição artística, escala, remalha ou deformação do rosto.

## 8. Armature criada

Foi criada uma armature nova, sem reutilizar a armature sem usuários encontrada na inspeção inicial:

- Objeto: `Personagem_Rig`.
- Dados: `Personagem_Rig_Armature`.
- Transformação do objeto na criação: identidade.
- Exibição dos ossos: octaedros, visíveis à frente da malha.

As posições de repouso abaixo estão no espaço local da armature, coincidente com o mundial nessa configuração:

| Osso | Início | Fim | Pai | Deforma |
| --- | --- | --- | --- | --- |
| `Root_Bone` | `(0, 0, 0.08)` | `(0, 0, 0.23)` | — | Não |
| `Torso_Bone` | `(0, 0, 0.23)` | `(0, -0.045, 0.40)` | `Root_Bone` | Sim |
| `Neck_Bone` | `(0, -0.045, 0.40)` | `(0, -0.0625, 0.4375)` | `Torso_Bone` | Não |
| `Head_Bone` | `(0, -0.0625, 0.4375)` | `(0, -0.0625, 0.70)` | `Neck_Bone` | Sim |

A origem da cabeça coincide com o início de `Head_Bone`.

## 9. Pesos, parentesco e modificadores

Os pesos foram atribuídos explicitamente, sem pesos automáticos:

| Objeto | Único grupo de vértices | Peso de todos os vértices |
| --- | --- | ---: |
| `Cabeca` | `Head_Bone` | 1.0 |
| `Corpo_Kart` | `Torso_Bone` | 1.0 |

Ambos foram ligados como filhos de `Personagem_Rig`, preservando suas transformações mundiais. Cada objeto recebeu um modificador Armature chamado `Rig_Rigido_Sem_Deformacao`, com:

- Armature de destino: `Personagem_Rig`.
- Influência por grupos de vértices ativada.
- Influência por envelopes desativada.
- Preservação de volume desativada.
- Modificador mantido na pilha, sem aplicação destrutiva à malha.

Como cada malha recebe peso integral de um único osso, o comportamento é rígido dentro de cada conjunto. Não há mistura de pesos entre cabeça e torso. Os ossos intermediários propagam a hierarquia de transformações.

## 10. Validação executada

O relatório foi salvo em `rigging/validacao_rig.json`. A verificação usou os atributos `rig_original_*` e os arrays originais registrados antes da separação.

Foram confirmados:

- Cada vértice, aresta, face e canto original aparece exatamente uma vez no conjunto das duas malhas finais.
- Conectividade das arestas preservada, comparando os pares de índices originais sem depender da orientação da aresta.
- Associação de vértices aos cantos das faces preservada.
- Tamanhos das faces e correspondência dos seus cantos preservados.
- UVs exatamente iguais às originais para cada canto.
- Sinalizadores de suavização e índices de material das faces preservados.
- Um único grupo de vértices por objeto, com todos os pesos exatamente iguais a 1.0.
- Nenhuma violação encontrada nessas verificações.

Diferenças máximas registradas, por componente de coordenada:

| Medição | `Cabeca` | `Corpo_Kart` |
| --- | ---: | ---: |
| Coordenadas mundiais da malha-base versus registro original | `7.450580596923828e-9` | `0.0` |
| Coordenadas mundiais avaliadas em repouso, com armature | `2.9802322387695312e-8` | `2.9802322387695312e-8` |

Os valores são em unidades da cena. As diferenças foram tratadas como arredondamento de ponto flutuante; a verificação exigiu desvio avaliado menor que `1e-7`. **Isso não constitui uma prova de deslocamento numérico absolutamente zero.**

### Teste de rotação da cabeça

Foi aplicada temporariamente uma rotação de **25° no eixo Y local de `Head_Bone`**, em modo de rotação XYZ. A matriz original de pose do osso foi guardada antes do teste e restaurada em um bloco `finally`.

| Resultado medido | Valor |
| --- | ---: |
| Movimento máximo do corpo/kart | `0.0` |
| Erro máximo da cabeça em relação à transformação rígida esperada | `3.374527435262564e-8` |
| Movimento máximo da cabeça, por componente de coordenada | `0.08840443938970566` |
| Pose restaurada ao final | Sim |

Não foram criados keyframes. Esse teste verificou isolamento da cabeça e resposta rígida; não foi realizado um teste equivalente de rotação individual do torso ou do pescoço.

## 11. Intercorrências durante a execução

- Uma consulta de leitura das faixas do pescoço falhou por erro de sintaxe em uma expressão Python. A expressão foi corrigida e a consulta foi executada novamente. A chamada que falhou não alterou a cena.
- Ao preparar a seleção final dos ossos, o acesso a `Bone.select` falhou porque essa propriedade não estava disponível na versão conectada. Nesse ponto, o texto de instruções já havia sido criado, mas o salvamento final daquela chamada ainda não tinha ocorrido.
- A seleção foi corrigida com o operador de seleção de pose, a definição do osso ativo e `PoseBone.select`, cuja disponibilidade foi verificada no objeto. O arquivo final foi salvo com sucesso na chamada seguinte.

## 12. Estado final salvo

Arquivo principal: `kart_modular_rig.blend`.

| Objeto de malha | Dados da malha | Vértices | Faces |
| --- | --- | ---: | ---: |
| `Cabeca` | `Cabeca_Geometria_Original` | 160.046 | 305.705 |
| `Corpo_Kart` | `Corpo_Kart_Geometria_Original` | 874.925 | 1.662.516 |
| Total | — | 1.034.971 | 1.968.221 |

O arquivo foi salvo com a pose restaurada, a armature ativa em Modo de Pose e `Head_Bone` ativo e selecionado. A viewport final mostrou o modelo com materiais e os ossos à frente da malha.

Foi adicionado ao Blender o texto `LEIA-ME_Rig`. O mesmo conteúdo foi salvo externamente em `rigging/LEIA-ME_Rig.txt`. Os objetos receberam propriedades personalizadas com a descrição da preservação, o osso de controle e, na cabeça, a posição do pivô. A armature recebeu instruções de uso em uma propriedade personalizada.

## 13. Limitações e alcance real do resultado

1. **O kart não foi separado definitivamente do corpo.** `Torso_Bone` controla integralmente `Corpo_Kart`, incluindo o veículo. Não existe controle independente do torso em relação ao kart neste resultado.
2. O rig final tem duas partes rígidas. Não foram criadas articulações independentes para braços, pernas, mãos, boca, rodas ou direção, nem sistemas de IK ou controles de expressão.
3. O limite do pescoço usa as ilhas existentes. Não foi criada uma seção plana, tampa ou superfície interna nova.
4. As coordenadas locais da cabeça foram compensadas ao ajustar a origem; a preservação mundial está sujeita às diferenças numéricas medidas acima.
5. Não houve exportação para GLB/FBX nem validação de importação em motor de jogo, animação extensa ou render final. As inspeções visuais foram capturas da viewport.
6. A validação cobre coordenadas, elementos, conectividade, UVs, pesos, índices de material e flags de suavização. Não foi registrada uma comparação numérica específica das normais nem dos pixels das texturas antes e depois.

## 14. Arquivos entregues e rastreabilidade

| Caminho relativo ao projeto | Conteúdo |
| --- | --- |
| `kart_modular_rig.blend` | Cena final com duas malhas e armature |
| `rigging/kart_antes_do_rig_20261015_120547.blend` | Cópia da cena anterior à separação e aos atributos de rastreamento |
| `rigging/geometria_original.npz` | Arrays originais para comparação |
| `rigging/validacao_rig.json` | Resultados das verificações e do teste de pose |
| `rigging/LEIA-ME_Rig.txt` | Instruções resumidas de uso e preservação |
| `documentacao/README.md` | Índice desta documentação |
| `documentacao/registro-rig-personagem-2026-10-15.md` | Este registro detalhado |
| `documentacao/manifesto-artefatos-rig.json` | Tamanhos e hashes dos cinco artefatos do rig, calculados durante a documentação |

As capturas de viewport e os códigos de diagnóstico foram enviados na conversa, sem arquivos individuais de captura ou de script salvos no projeto. A geração desta documentação conferiu os arquivos existentes no disco e não modificou os artefatos do rig.
