# Personagem — receita de criação e evolução

**Este é o registro central dos personagens do projeto. O personagem apresentado neste documento é o primeiro personagem trabalhado e documentado aqui.** Seu preparo no Blender iniciou a primeira versão desta receita.

Tudo que for desenvolvido para os personagens deve passar por este arquivo: criação ou preparação da malha, rig, pesos, animações, materiais, ajustes, testes e exportações. O resumo e a referência de cada nova etapa ficam aqui; o procedimento detalhado e suas evidências ficam nos documentos próprios. Assim, este arquivo funciona como ponto de partida para criar outros personagens e acompanhar a evolução dos existentes.

Criado em **15/10/2026**. Esta versão foi elaborada a partir dos documentos e artefatos existentes no projeto; não representa uma nova inspeção da cena aberta no Blender.

## 1. Primeiro personagem: P001 — Jake

Identificação de trabalho no projeto: **Jake**, conforme os nomes dos arquivos de referência existentes. O modelo representa o personagem sentado em um kart.

| Item | Arquivo ou identificação |
| --- | --- |
| Referência visual existente | [imagens/jake.png](../imagens/jake.png) |
| Modelo GLB existente no projeto | [modelos/jake.glb](../modelos/jake.glb) |
| Arquivo de trabalho do Blender | [kart_modular_rig.blend](../kart_modular_rig.blend) |
| Armature | `Personagem_Rig` |
| Malhas após P001.05 | `Cabeca`, `Corpo_Kart`, `Wheel_Front_Left`, `Wheel_Front_Right`, `Wheel_Rear_Left` e `Wheel_Rear_Right` |
| Primeira animação documentada | `Cabeca_Direita_Ida_e_Volta` |
| Nova animação ativa — 15/10/2026 | `Cabeca_Esquerda_Ida_e_Volta`, com a ação da direita preservada |

O trabalho registrado começou com uma malha já existente na cena. **Não foi documentada aqui a modelagem ou geração original do personagem do zero**, nem foi demonstrada a procedência dessa malha a partir do GLB listado. Esta receita cobre o preparo, o rig e a animação documentados a partir dela; a etapa de criação visual deve ser acrescentada quando for realizada.

### Histórico do primeiro personagem

| Etapa | O que foi feito | Resultado e referência |
| --- | --- | --- |
| P001.01 — Preparação e rig | Cópia da cena original, registro da geometria, separação da cabeça por ilhas existentes, origem na base do pescoço, armature e pesos rígidos exclusivos | [Registro completo do rig](registro-rig-personagem-2026-10-15.md) e [validação numérica](../rigging/validacao_rig.json) |
| P001.02 — Segundo passo: animação da cabeça | Pose a 40° seguida de animação de ida e volta; testes de preservação; orientações sobre FPS e exportação; documentação e envio ao GitHub com Git LFS | [Resumo e referências do segundo passo](#segundo-passo--p00102-animação-da-cabeça), [registro completo](registro-animacao-cabeca-2026-10-15.md) e [commit publicado](https://github.com/patrick3s/kart/commit/7105f36b3c60ee444dfda92cf1e4d0976df5667e) |
| P001.03 — Consolidação da receita | Criação deste arquivo central, reunindo o histórico e o método para os próximos personagens | Este documento e o [índice da documentação](README.md) |
| P001.04 — Cabeça para a esquerda | Cópia da ação da direita com inversão de sinal da rotação Y local: 0° → −40° → 0°, nos quadros 1/25/49; rig e geometria preservados | [Registro da animação para a esquerda](registro-animacao-cabeca-esquerda-2026-10-15.md) e [validação numérica](../rigging/validacao_animacao_cabeca_esquerda.json) |
| P001.05 — Rodas independentes | Separação das quatro rodas por ilhas existentes, malhas exclusivas, origens no centro dos limites geométricos e parentesco com `Torso_Bone` para preservar o acompanhamento do rig | [Registro da separação das rodas](registro-rodas-independentes-2026-10-15.md) e [validação numérica](../rigging/verificacao_rodas_independentes.json); modelo e evidências no commit local `e2a2848` |

As cinco entradas são de **15/10/2026**. A terceira etapa é documental e não modifica o modelo, os pesos ou a animação. A quarta acrescenta a ação da esquerda; a quinta separa as rodas, preservando o acompanhamento da animação existente.

### Resultado de referência do rig original — P001.01

| Parte | Vértices | Faces | Grupo e peso |
| --- | ---: | ---: | --- |
| `Cabeca` | 160.046 | 305.705 | `Head_Bone`, 100% |
| `Corpo_Kart` | 874.925 | 1.662.516 | `Torso_Bone`, 100% |
| Total | 1.034.971 | 1.968.221 | Duas partes rígidas |

Hierarquia: `Root_Bone` → `Torso_Bone` → `Neck_Bone` → `Head_Bone`.

A origem de `Cabeca` e o início de `Head_Bone` coincidem em **`(0, -0.0625, 0.4375)`**, na base do pescoço deste modelo. O modificador Armature das duas malhas é `Rig_Rigido_Sem_Deformacao`.

Nesse resultado inicial, o kart permaneceu unido ao corpo em `Corpo_Kart` e acompanhava o torso. A separação independente do veículo foi investigada, mas não ficou naquela etapa. Os detalhes, incluindo as tentativas desfeitas, estão no [registro do rig, seções 6 a 13](registro-rig-personagem-2026-10-15.md#6-diagnósticos-e-separações-intermediárias-de-corpo-e-kart). Em **P001.05**, as quatro rodas foram separadas em objetos próprios; o restante do kart continua em `Corpo_Kart`. Não foram criados controles novos para braços, pernas ou boca, nem animação de rodagem ou direção.

### Segundo passo — P001.02: animação da cabeça

**Data: 15/10/2026.** Esta etapa reúne o trabalho deste chat após a preparação e o rig de `P001.01`. O objetivo inicial foi virar a cabeça para a direita entre 30° e 45°, preservando o pescoço e o corpo. Depois, o usuário esclareceu que o movimento deveria incluir o retorno à posição original.

O Blender MCP foi usado para inspecionar a cena, os ossos e os pesos, selecionar `Head_Bone`, aplicar a pose e criar a animação. A cabeça já estava separada e com peso integral no osso; não foi necessário alterar a geometria, os pesos ou a origem. Neste esqueleto, o eixo vertical corresponde ao **Y local de `Head_Bone`**, aproximadamente alinhado ao Z mundial. Foi aplicada primeiro uma pose estática de **+40°**, depois substituída pelos keyframes abaixo.

| Quadro | Rotação Y local de `Head_Bone` |
| ---: | ---: |
| 1 | 0° |
| 25 | 40° |
| 49 | 0° |

A ação `Cabeca_Direita_Ida_e_Volta` usa interpolação Bézier com alças automáticas limitadas. A repetição na viewport usa a prévia de **1 a 49**, sem modificador de ciclos na curva.

A curva anima somente `pose.bones["Head_Bone"].rotation_euler`, índice `1`, com extrapolação constante. Após o quadro 49, a cabeça permanece na posição original fora do intervalo de prévia. A animação foi salva em [kart_modular_rig.blend](../kart_modular_rig.blend), e a reprodução em loop foi iniciada para apresentar o resultado.

**Preservação verificada:** nos quadros **1, 13, 25, 37 e 49**, os ângulos medidos foram aproximadamente **0°, 20°, 40°, 20° e 0°**. O deslocamento medido do pivô e a maior diferença por componente nos **874.925 vértices avaliados de `Corpo_Kart` foram `0.0`**. O pivô permaneceu em `(0, -0.0625, 0.4375)`, com localização e escala do osso preservadas. Na pose estática, as matrizes dos demais ossos também permaneceram iguais. Essas medições são dos estados amostrados, com tolerância de `1e-7`.

A animação foi criada em **24 FPS**. O último estado descrito no registro da animação mostrou **30 FPS**, mas o documento não confirma que essa alteração de FPS tenha sido salva no disco. O intervalo principal observado continuava de **1 a 250**, e a saída configurada era PNG. Não há vídeo final exportado e validado documentado.

**Orientações registradas:** a taxa de quadros pode ser alterada em Propriedades de saída → Formato → Taxa de quadros. Mantendo os keyframes em 1/25/49, o tempo entre início e retorno é de **2 segundos a 24 FPS**, **1,6 segundo a 30 FPS** e **0,8 segundo a 60 FPS**. Para manter dois segundos, os exemplos são **1/31/61 a 30 FPS** e **1/61/121 a 60 FPS**. A prévia de 2 a 3 quadros/s relatada pelo usuário representa o desempenho da viewport; o vídeo renderizado segue a taxa configurada na saída. Aumentar o FPS da cena não melhora, por si só, o desempenho da prévia. Essas orientações não constituem uma exportação realizada.

**Versionamento realizado ao final do chat:** a animação e sua documentação foram enviadas à branch `main` de [patrick3s/kart](https://github.com/patrick3s/kart), no commit [7105f36 — anima ida e volta da cabeça e documenta o processo](https://github.com/patrick3s/kart/commit/7105f36b3c60ee444dfda92cf1e4d0976df5667e). Como o arquivo principal tinha aproximadamente 114 MB, foi instalado o Git LFS e foram migrados os arquivos `.blend` dos dois commits ainda locais. A comparação por SHA-256 confirmou o conteúdo integral dos arquivos antes e depois da migração, e `git lfs fsck` passou. O envio incluiu três versões de arquivos Blender, aproximadamente 309 MB; a referência remota foi consultada e confirmou o commit. Backups automáticos como `.blend1` ficaram locais e passaram a ser ignorados pelo Git.

O registro detalhado da animação foi escrito **antes** desse commit e envio. Portanto, sua indicação de que ainda não havia publicação descreve o momento da documentação; a publicação posterior fica registrada aqui. Esta atualização do `PERSONAGEM.md` é posterior ao commit citado e não faz parte dele.

#### Referências do segundo passo

| Parte do trabalho deste chat | Referência detalhada |
| --- | --- |
| Inspeção de objetos, ossos e pesos | [Estado inicial consultado pelo Blender MCP](registro-animacao-cabeca-2026-10-15.md#2-inspeção-inicial-pelo-blender-mcp) |
| Sentido da rotação, eixo correto e seleção de `PoseBone` | [Rotação estática de 40° e compatibilidade da API](registro-animacao-cabeca-2026-10-15.md#3-rotação-estática-de-40) |
| Ação, keyframes, interpolação e loop de prévia | [Animação de ida e volta](registro-animacao-cabeca-2026-10-15.md#4-animação-de-ida-e-volta) |
| Corpo, pivô e quadros intermediários | [Verificações de preservação](registro-animacao-cabeca-2026-10-15.md#5-verificações-de-preservação) |
| FPS e duração do movimento | [Orientação sobre FPS](registro-animacao-cabeca-2026-10-15.md#6-orientação-sobre-fps) |
| Prévia lenta e comportamento esperado do vídeo | [Prévia lenta e exportação](registro-animacao-cabeca-2026-10-15.md#7-prévia-lenta-e-exportação) |
| Estado observado, arquivos e limites da entrega | [Consulta durante a documentação](registro-animacao-cabeca-2026-10-15.md#8-estado-consultado-durante-a-documentação) e [limites do registro](registro-animacao-cabeca-2026-10-15.md#9-arquivos-e-limites-do-registro) |
| Reprodução da animação no Blender | [Como visualizar o resultado](registro-animacao-cabeca-2026-10-15.md#10-como-visualizar-o-resultado) |
| Entrega versionada e arquivos grandes | [Commit publicado](https://github.com/patrick3s/kart/commit/7105f36b3c60ee444dfda92cf1e4d0976df5667e), [configuração do Git LFS](../.gitattributes) e [instruções para obter os arquivos](README.md#arquivos-do-blender-no-repositório) |

Não tratar a descrição desta etapa histórica como confirmação automática do estado atual do arquivo ou do Blender aberto. A receita geral para novos personagens continua abaixo; seu Passo 2 trata da preservação da entrada, enquanto `P001.02` identifica o segundo trabalho realizado no primeiro personagem.

### P001.04 — Animação da cabeça para a esquerda

**Executada pelo Blender MCP em 15/10/2026**, após inspeção da cena aberta. A ação `Cabeca_Esquerda_Ida_e_Volta` é uma cópia da ação da direita com o sinal dos valores e das alças Bézier invertido. Anima somente o índice 1 de `pose.bones["Head_Bone"].rotation_euler`: **1: 0°; 25: −40°; 49: 0°**. Mantém `BEZIER`, `AUTO_CLAMPED` e extrapolação constante. Nenhum limite novo foi aplicado ao rig; a amplitude de 40° foi mantida no sentido oposto, sem ultrapassagem nas amostras da curva.

A hierarquia `Root_Bone` → `Torso_Bone` → `Neck_Bone` → `Head_Bone`, o pivô `(0, -0.0625, 0.4375)`, os pesos exclusivos e os modificadores foram preservados. A ação da direita mantém suas curvas originais e foi marcada para retenção no arquivo, mesmo sem estar ativa.

**Validação:** pivô, matrizes dos demais ossos, localização e escala da cabeça permaneceram iguais nos 49 quadros inteiros. Nos quadros 1/13/25/37/49, todos os vértices avaliados do corpo permaneceram imóveis; a diferença máxima da cabeça em relação a uma transformação rígida foi `3.494387468272464e-8` unidade, e a variação máxima no comprimento das arestas foi `3.606600965273821e-8`. Os hashes da geometria-base, conectividade, UVs e índices de materiais permaneceram iguais. A comparação da curva esquerda com a negativa da direita teve erro zero em 481 amostras. A viewport foi inspecionada nas duas ações no quadro 25.

O arquivo principal foi salvo com **30 FPS**, ação esquerda ativa, **quadro 25** e prévia **1 a 49**. O tempo entre início e retorno é **1,6 segundo**. O intervalo principal continua em 1 a 250. Para assistir, reproduzir a timeline com a prévia ativa. Backup anterior à edição: [kart_antes_animacao_esquerda_20261015.blend](../rigging/kart_antes_animacao_esquerda_20261015.blend). Não houve exportação de vídeo, commit ou publicação nesta etapa.

Procedimento e limites: [registro detalhado](registro-animacao-cabeca-esquerda-2026-10-15.md). Medições: [relatório JSON](../rigging/validacao_animacao_cabeca_esquerda.json).

### P001.05 — Separação das quatro rodas

**Executada pelo Blender MCP em 15/10/2026.** As rodas foram identificadas entre as ilhas desconectadas de `Corpo_Kart` e separadas como conjuntos completos, preservando os elementos originais. Cada objeto tem uma malha exclusiva: `Wheel_Front_Left`, `Wheel_Front_Right`, `Wheel_Rear_Left` e `Wheel_Rear_Right`. A frente do modelo é **−Y**; esquerda e direita são as do piloto, com **+X à esquerda**.

As origens usam o **centro da caixa delimitadora da geometria de cada roda**, calculado por `ORIGIN_GEOMETRY` com `BOUNDS`. O giro usa **X local** e o esterço usa **Z local**. Cada roda foi ligada diretamente a `Torso_Bone`, com compensação das transformações; o modificador Armature herdado foi removido dessas quatro malhas para permitir rotação por objeto em torno de sua própria origem. O restante de `Corpo_Kart` mantém sua ligação anterior ao rig.

**Preservação verificada:** os **874.925 vértices, 2.536.689 arestas e 1.662.516 faces** do `Corpo_Kart` anterior estão presentes exatamente uma vez entre o corpo restante e as quatro rodas. Coordenadas reconstruídas no espaço de referência tiveram erro zero. Conectividade, UVs, dados de normais personalizadas, materiais e suavização foram preservados. O maior erro numérico de centralização da origem foi `1.666000468656264e-8` unidade.

Nos quadros **1, 8, 17, 29 e 49**, a diferença máxima das posições mundiais em relação ao acompanhamento anterior do rig foi `5.960464477539063e-8` unidade. Testes temporários de **90° em X** e **30° em Z** tiveram deslocamento zero do pivô; as rotações foram restauradas. O arquivo salvo foi aberto em uma segunda instância do Blender para conferir os quatro objetos, a exclusividade das malhas e as contagens totais.

O modelo, o backup anterior à separação e o relatório foram incluídos no **commit local `e2a2848`**. Este registro textual complementa essa entrega em um commit documental posterior, junto ao índice e aos registros referenciados da evolução do personagem. Não houve exportação ou validação na Godot nesta etapa.

Procedimento, contagens por objeto e limites: [registro detalhado das rodas](registro-rodas-independentes-2026-10-15.md). Evidências: [relatório JSON](../rigging/verificacao_rodas_independentes.json). Cópia anterior: [backup das rodas](../rigging/kart_antes_separar_rodas_20261015_134523.blend).

## 2. Receita para preparar outros personagens

Esta é a **versão 1 da receita**, derivada do primeiro personagem. Ela é um procedimento documentado, ainda sem um script único de execução automática. Os passos abaixo devem ser adaptados à anatomia, à orientação e à estrutura de cada novo modelo.

### Passo 1 — Identificar o personagem e reunir os materiais

1. Criar uma ficha neste arquivo com o próximo identificador, começando por `P002`.
2. Registrar nome, referências visuais, modelo de entrada, arquivo de trabalho e objetivo da primeira etapa.
3. Descrever o que já existe e o que será criado: malha pronta, importação, modelagem, rig ou animação.
4. Definir quais partes precisam de controles independentes. Se houver veículo ou acessórios, registrar se acompanharão o corpo ou terão controles próprios.

**Referência do primeiro caso:** [ficha P001](#1-primeiro-personagem-p001--jake) e [estado inicial do rig](registro-rig-personagem-2026-10-15.md#2-estado-inicial-observado).

### Passo 2 — Inspecionar e preservar a entrada

1. Consultar a cena real pelo Blender MCP: objetos, transformações, pais, materiais, UVs, modificadores, grupos de vértices, shape keys e animações existentes.
2. Conferir visualmente o personagem e sua orientação.
3. Salvar uma cópia anterior à edição e registrar o caminho.
4. Registrar contagens e coordenadas originais, conectividade, UVs e demais dados necessários à comparação.
5. Adicionar identificadores de rastreamento quando a separação ou a reorganização exigir correspondência entre os elementos originais e finais.

Para uma tarefa de preservação como a do P001, manter a forma e as proporções originais durante a preparação. A referência intacta serve para demonstrar o que foi preservado.

**Referência:** [cópia e registro da geometria](registro-rig-personagem-2026-10-15.md#4-cópia-de-segurança-e-registro-da-geometria), [backup do P001](../rigging/kart_antes_do_rig_20261015_120547.blend) e [arrays originais do P001](../rigging/geometria_original.npz).

### Passo 3 — Identificar e separar as partes existentes

1. Examinar as ilhas conectadas, as faces e os limites anatômicos, conferindo frente, lado e detalhes relevantes.
2. Aproveitar partes já desconectadas quando isso permitir a separação sem acrescentar ou remover geometria.
3. Separar a cabeça completa, incluindo os elementos que devem acompanhá-la, como olhos, boca e acessórios.
4. Conferir as partes isoladamente e juntas para detectar fragmentos ausentes, partes atribuídas ao conjunto errado e alterações de aparência.
5. Registrar o método efetivamente adotado e as tentativas descartadas. Se uma separação adicional não funcionar, documentar o limite em vez de considerá-la concluída.

No P001, a cabeça foi separada usando **86 ilhas existentes**, sem corte planar ou tampa nova. As tentativas iniciais de separar corpo e kart foram desfeitas. Posteriormente, em **P001.05**, as rodas foram isoladas por conjuntos de ilhas existentes; o corpo e o restante do kart continuam unidos. Para veículos, conferir também pneus, aros, cubos e suspensão antes de atribuir as ilhas a cada roda.

**Referência:** [identificação da cabeça](registro-rig-personagem-2026-10-15.md#5-inspeção-e-identificação-da-cabeça) e [diagnósticos intermediários](registro-rig-personagem-2026-10-15.md#6-diagnósticos-e-separações-intermediárias-de-corpo-e-kart).

### Passo 4 — Posicionar os pivôs e construir o esqueleto

1. Localizar a base do pescoço no novo modelo.
2. Ajustar a origem da cabeça com compensação da transformação para preservar sua posição mundial.
3. Colocar o início do osso da cabeça nesse mesmo pivô.
4. Criar a hierarquia necessária. Para um personagem com o mesmo comportamento rígido do P001, usar como referência raiz → torso → pescoço → cabeça.
5. Registrar nomes, posições de repouso, relações de parentesco e quais ossos deformam.

Os valores do pivô devem ser medidos no novo personagem. A mudança de origem altera a representação local dos vértices; medir a preservação no espaço mundial e informar qualquer arredondamento numérico.

**Referência:** [origem e pivô](registro-rig-personagem-2026-10-15.md#7-origem-e-pivô-da-cabeça) e [armature criada](registro-rig-personagem-2026-10-15.md#8-armature-criada).

### Passo 5 — Atribuir os pesos e ligar as malhas

1. Para uma parte que deva permanecer rígida, atribuir peso 1.0 a todos os seus vértices no osso responsável.
2. Conferir que nenhum vértice dessa parte recebeu influência de outro osso.
3. Ligar os objetos à armature preservando suas transformações mundiais.
4. Usar o modificador Armature com grupos de vértices e sem envelopes para repetir a configuração do P001.
5. Manter o modificador na pilha e registrar a configuração adotada.

Esse método produz partes rígidas. Um personagem que precise dobrar cotovelos, joelhos ou outras articulações exige uma etapa própria de rig e pesos, com novos testes e referências neste arquivo.

**Referência:** [pesos, parentesco e modificadores](registro-rig-personagem-2026-10-15.md#9-pesos-parentesco-e-modificadores) e [instruções resumidas do rig](../rigging/LEIA-ME_Rig.txt).

Para acessórios que precisam girar como objetos, a etapa **P001.05** oferece outra configuração: malha exclusiva, origem própria e parentesco direto com o osso responsável, com compensação da transformação. As rodas usam essa configuração sem modificador Armature. Medir novamente o acompanhamento do rig e a estabilidade dos pivôs ao aplicar o método em outro modelo; ver o [procedimento das rodas](registro-rodas-independentes-2026-10-15.md).

### Passo 6 — Validar antes de animar

1. Comparar elementos originais e finais, verificando presença, contagens, conectividade e UVs.
2. Comparar as coordenadas mundiais da malha-base e da malha avaliada em repouso.
3. Conferir exclusividade e valores dos pesos.
4. Aplicar uma rotação temporária de teste no osso da cabeça e medir se o corpo e o pivô permanecem estáveis.
5. Restaurar a pose de referência após o teste.
6. Salvar o relatório numérico e registrar o que foi verificado visualmente e o que não foi testado.

No primeiro rig, o teste foi de **25°**, sem movimento medido do corpo/kart. O relatório preservou as contagens e mostrou diferenças numéricas de até `2.9802322387695312e-8` unidade na avaliação em repouso. Esses são resultados do P001, não garantias para qualquer outro modelo.

**Referência:** [validação original em JSON](../rigging/validacao_rig.json) e [descrição dos testes](registro-rig-personagem-2026-10-15.md#10-validação-executada).

### Passo 7 — Criar uma primeira animação simples

1. Identificar o eixo local correto do osso no novo personagem.
2. Criar uma ação com nome claro e animar apenas o canal necessário.
3. Para repetir a ideia do P001, usar posição inicial → virada → retorno, ajustando o ângulo ao modelo e ao movimento desejado.
4. Definir o FPS e a duração desejada antes de posicionar os keyframes.
5. Conferir keyframes e quadros intermediários, medindo isolamento do corpo e estabilidade do pivô.
6. Configurar o intervalo de prévia e, separadamente, o intervalo de renderização quando houver exportação.

No P001, o canal correto foi Y local de `Head_Bone`, com **0° → 40° → 0°** nos quadros **1 → 25 → 49**. Esse eixo e esses números não devem ser copiados sem conferência.

Para manter a duração ao trocar o FPS, redistribuir os keyframes. Os exemplos já documentados para dois segundos entre início e retorno são 1/25/49 a 24 FPS, 1/31/61 a 30 FPS e 1/61/121 a 60 FPS.

**Referência:** [animação de ida e volta](registro-animacao-cabeca-2026-10-15.md#4-animação-de-ida-e-volta), [verificações](registro-animacao-cabeca-2026-10-15.md#5-verificações-de-preservação) e [FPS](registro-animacao-cabeca-2026-10-15.md#6-orientação-sobre-fps).

### Passo 8 — Salvar, documentar e preparar a próxima etapa

1. Salvar o arquivo de trabalho e preservar os arquivos de entrada e os registros anteriores.
2. Criar um documento detalhado para a etapa executada, com resultado, testes, arquivos e limitações.
3. Acrescentar a etapa à ficha do personagem neste arquivo e colocar o link no índice da documentação.
4. Quando uma alteração modificar o arquivo principal, manter o significado histórico dos relatórios e hashes anteriores. Um hash do rig anterior não identifica o arquivo depois de animado.
5. Quando houver renderização ou exportação, criar uma etapa específica, com formato, destino e validação do resultado. Até essa etapa ocorrer, registrar a exportação como não realizada.

**Referência:** [arquivos do rig](registro-rig-personagem-2026-10-15.md#14-arquivos-entregues-e-rastreabilidade), [limites do registro da animação](registro-animacao-cabeca-2026-10-15.md#9-arquivos-e-limites-do-registro) e [manifesto histórico do rig](manifesto-artefatos-rig.json).

## 3. O que reaproveitar e o que medir novamente

| Reaproveitar como método | Adaptar ou medir no novo personagem |
| --- | --- |
| Backup e registro anterior às alterações | Caminhos, identidade e origem do modelo |
| Inspeção das partes e validação da separação | Anatomia, ilhas, limites e partes independentes |
| Pivô da cabeça na base do pescoço | Coordenadas do pivô e tamanho dos ossos |
| Hierarquia e pesos exclusivos para partes rígidas | Quantidade de ossos e necessidade de deformação articulada |
| Teste de isolamento entre cabeça e corpo | Eixo local, sentido, amplitude e limites de rotação |
| Comparação numérica e visual | Escala, tolerâncias e resultados medidos |
| Registro por etapas com referências | Ações, FPS, duração e formato de entrega |

Em particular, **não reutilizar como regra geral** os índices de ilhas `294` e `589`, o limite de altura `0.49`, as contagens da malha, o pivô do P001 ou seu eixo de animação. Esses valores vieram da inspeção específica do primeiro modelo.

## 4. Como manter este arquivo a partir de agora

- Para cada novo personagem, acrescentar uma ficha com identificador sequencial (`P002`, `P003` etc.), nome e arquivos próprios. Não substituir os arquivos do P001 para registrar outro personagem.
- Para cada trabalho no personagem existente, acrescentar uma etapa ao histórico dele. Registrar também ajustes, correções e tentativas relevantes que não ficaram no resultado.
- Incluir em cada etapa: data, pedido, mudança realizada, estado do resultado, testes, limitações e links para o documento detalhado e os artefatos.
- Quando surgir uma técnica reutilizável, atualizar a receita e indicar de qual personagem e etapa ela veio. Um teste em um modelo deve continuar identificado como evidência daquele modelo.
- Preservar os relatos históricos. Se uma informação anterior mudar, acrescentar a evolução e sua referência, deixando claro qual estado foi observado em cada etapa.
- Manter as referências relativas à pasta `documentacao` para que a documentação continue navegável após clonar o projeto.

Modelo de ficha para copiar neste arquivo quando o próximo personagem for iniciado:

```markdown
## Personagem P00N — Nome

Primeiro registro: DD/MM/AAAA.
Objetivo e descrição:
Referências visuais:
Modelo de entrada:
Arquivo de trabalho:
Partes e controles independentes:
Estado documentado:

| Etapa | Data | Mudança realizada | Documento e artefatos | Validação e limites |
| --- | --- | --- | --- | --- |
| P00N.01 | DD/MM/AAAA | Descrever | Vincular arquivos | Informar evidências |

Aprendizados que entram na receita:
Próxima etapa ou entregas ainda não realizadas:
```

## 5. Mapa dos documentos de referência

| Documento | Para que consultar |
| --- | --- |
| [Índice da documentação](README.md) | Navegar pelos registros do projeto |
| [Registro do rig](registro-rig-personagem-2026-10-15.md) | Reconstituir as operações do primeiro preparo, inclusive tentativas e limites |
| [Validação original do rig](../rigging/validacao_rig.json) | Conferir os números medidos na etapa de rig |
| [Manifesto histórico](manifesto-artefatos-rig.json) | Identificar as versões dos artefatos na documentação original do rig |
| [Instruções resumidas do rig](../rigging/LEIA-ME_Rig.txt) | Consultar controles e configuração da etapa inicial |
| [Registro da animação](registro-animacao-cabeca-2026-10-15.md) | Repetir o movimento de ida e volta, entender FPS e distinguir prévia de exportação |
| [Animação para a esquerda](registro-animacao-cabeca-esquerda-2026-10-15.md) | Consultar o espelhamento da ação e as verificações de pivô, rig e malha |
| [Rodas independentes — P001.05](registro-rodas-independentes-2026-10-15.md) | Consultar separação por ilhas, nomenclatura, pivôs, parentesco e verificações das rodas |
| [Validação das rodas](../rigging/verificacao_rodas_independentes.json) | Conferir preservação dos elementos, centros, amostras da animação e testes de giro e esterço |

O registro inicial e suas instruções descrevem o rig antes dos keyframes. A evolução posterior está nos registros de animação e de separação das rodas. Esta atualização documental consulta as evidências salvas das etapas e não constitui uma nova inspeção da cena aberta nem modifica o Blender.
