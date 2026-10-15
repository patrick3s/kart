# P001 — Jake

Ficha e histórico do primeiro personagem do projeto. Tudo que pertence a ele fica nesta pasta; a receita genérica para outros personagens está em [documentacao/RECEITA_PERSONAGEM.md](../../documentacao/RECEITA_PERSONAGEM.md). O que é exportado para o jogo fica em [jogo/personagens/jake/](../../jogo/personagens/jake/).

> **Reorganização de 15/10/2026:** os arquivos deste personagem foram reunidos aqui. Antes estavam em `kart_modular_rig.blend` (raiz, agora `blender/jake.blend`), `modelos/`, `imagens/`, `rigging/` e `documentacao/`. Os registros e os JSONs de validação citam os caminhos antigos como parte do histórico; os links foram atualizados.


Identificação de trabalho no projeto: **Jake**, conforme os nomes dos arquivos de referência existentes. O modelo representa o personagem sentado em um kart.

| Item | Arquivo ou identificação |
| --- | --- |
| Referência visual existente | [referencia/jake.png](referencia/jake.png) |
| Modelo GLB existente no projeto | [referencia/jake.glb](referencia/jake.glb) |
| Arquivo de trabalho do Blender | [blender/jake.blend](blender/jake.blend) |
| Armature | `Personagem_Rig` |
| Malhas após P001.05 | `Cabeca`, `Corpo_Kart`, `Wheel_Front_Left`, `Wheel_Front_Right`, `Wheel_Rear_Left` e `Wheel_Rear_Right` |
| Primeira animação documentada | `Cabeca_Direita_Ida_e_Volta` |
| Nova animação ativa — 15/10/2026 | `Cabeca_Esquerda_Ida_e_Volta`, com a ação da direita preservada |

O trabalho registrado começou com uma malha já existente na cena. **Não foi documentada aqui a modelagem ou geração original do personagem do zero**, nem foi demonstrada a procedência dessa malha a partir do GLB listado. Esta receita cobre o preparo, o rig e a animação documentados a partir dela; a etapa de criação visual deve ser acrescentada quando for realizada.

## Histórico do primeiro personagem

| Etapa | O que foi feito | Resultado e referência |
| --- | --- | --- |
| P001.01 — Preparação e rig | Cópia da cena original, registro da geometria, separação da cabeça por ilhas existentes, origem na base do pescoço, armature e pesos rígidos exclusivos | [Registro completo do rig](registros/registro-rig-personagem-2026-10-15.md) e [validação numérica](validacao/validacao_rig.json) |
| P001.02 — Segundo passo: animação da cabeça | Pose a 40° seguida de animação de ida e volta; testes de preservação; orientações sobre FPS e exportação; documentação e envio ao GitHub com Git LFS | [Resumo e referências do segundo passo](#segundo-passo--p00102-animação-da-cabeça), [registro completo](registros/registro-animacao-cabeca-2026-10-15.md) e [commit publicado](https://github.com/patrick3s/kart/commit/7105f36b3c60ee444dfda92cf1e4d0976df5667e) |
| P001.03 — Consolidação da receita | Criação deste arquivo central, reunindo o histórico e o método para os próximos personagens | Este documento e o [índice da documentação](../../documentacao/README.md) |
| P001.04 — Cabeça para a esquerda | Cópia da ação da direita com inversão de sinal da rotação Y local: 0° → −40° → 0°, nos quadros 1/25/49; rig e geometria preservados | [Registro da animação para a esquerda](registros/registro-animacao-cabeca-esquerda-2026-10-15.md) e [validação numérica](validacao/validacao_animacao_cabeca_esquerda.json) |
| P001.05 — Rodas independentes | Separação das quatro rodas por ilhas existentes, malhas exclusivas, origens no centro dos limites geométricos e parentesco com `Torso_Bone` para preservar o acompanhamento do rig | [Registro da separação das rodas](registros/registro-rodas-independentes-2026-10-15.md) e [validação numérica](validacao/verificacao_rodas_independentes.json); modelo e evidências no commit local `e2a2848` |
| P001.06 — Pasta própria do personagem | Arquivos do Jake reunidos em `personagens/P001_jake/` (`.blend` renomeado de `kart_modular_rig.blend` para `blender/jake.blend`); receita genérica separada em `documentacao/RECEITA_PERSONAGEM.md`; links atualizados. Geometria, rig e animações não foram alterados | Esta ficha e a [receita](../../documentacao/RECEITA_PERSONAGEM.md) |

As seis entradas são de **15/10/2026**. A terceira etapa é documental e não modifica o modelo, os pesos ou a animação. A quarta acrescenta a ação da esquerda; a quinta separa as rodas, preservando o acompanhamento da animação existente.

## Resultado de referência do rig original — P001.01

| Parte | Vértices | Faces | Grupo e peso |
| --- | ---: | ---: | --- |
| `Cabeca` | 160.046 | 305.705 | `Head_Bone`, 100% |
| `Corpo_Kart` | 874.925 | 1.662.516 | `Torso_Bone`, 100% |
| Total | 1.034.971 | 1.968.221 | Duas partes rígidas |

Hierarquia: `Root_Bone` → `Torso_Bone` → `Neck_Bone` → `Head_Bone`.

A origem de `Cabeca` e o início de `Head_Bone` coincidem em **`(0, -0.0625, 0.4375)`**, na base do pescoço deste modelo. O modificador Armature das duas malhas é `Rig_Rigido_Sem_Deformacao`.

Nesse resultado inicial, o kart permaneceu unido ao corpo em `Corpo_Kart` e acompanhava o torso. A separação independente do veículo foi investigada, mas não ficou naquela etapa. Os detalhes, incluindo as tentativas desfeitas, estão no [registro do rig, seções 6 a 13](registros/registro-rig-personagem-2026-10-15.md#6-diagnósticos-e-separações-intermediárias-de-corpo-e-kart). Em **P001.05**, as quatro rodas foram separadas em objetos próprios; o restante do kart continua em `Corpo_Kart`. Não foram criados controles novos para braços, pernas ou boca, nem animação de rodagem ou direção.

## Segundo passo — P001.02: animação da cabeça

**Data: 15/10/2026.** Esta etapa reúne o trabalho deste chat após a preparação e o rig de `P001.01`. O objetivo inicial foi virar a cabeça para a direita entre 30° e 45°, preservando o pescoço e o corpo. Depois, o usuário esclareceu que o movimento deveria incluir o retorno à posição original.

O Blender MCP foi usado para inspecionar a cena, os ossos e os pesos, selecionar `Head_Bone`, aplicar a pose e criar a animação. A cabeça já estava separada e com peso integral no osso; não foi necessário alterar a geometria, os pesos ou a origem. Neste esqueleto, o eixo vertical corresponde ao **Y local de `Head_Bone`**, aproximadamente alinhado ao Z mundial. Foi aplicada primeiro uma pose estática de **+40°**, depois substituída pelos keyframes abaixo.

| Quadro | Rotação Y local de `Head_Bone` |
| ---: | ---: |
| 1 | 0° |
| 25 | 40° |
| 49 | 0° |

A ação `Cabeca_Direita_Ida_e_Volta` usa interpolação Bézier com alças automáticas limitadas. A repetição na viewport usa a prévia de **1 a 49**, sem modificador de ciclos na curva.

A curva anima somente `pose.bones["Head_Bone"].rotation_euler`, índice `1`, com extrapolação constante. Após o quadro 49, a cabeça permanece na posição original fora do intervalo de prévia. A animação foi salva em [blender/jake.blend](blender/jake.blend), e a reprodução em loop foi iniciada para apresentar o resultado.

**Preservação verificada:** nos quadros **1, 13, 25, 37 e 49**, os ângulos medidos foram aproximadamente **0°, 20°, 40°, 20° e 0°**. O deslocamento medido do pivô e a maior diferença por componente nos **874.925 vértices avaliados de `Corpo_Kart` foram `0.0`**. O pivô permaneceu em `(0, -0.0625, 0.4375)`, com localização e escala do osso preservadas. Na pose estática, as matrizes dos demais ossos também permaneceram iguais. Essas medições são dos estados amostrados, com tolerância de `1e-7`.

A animação foi criada em **24 FPS**. O último estado descrito no registro da animação mostrou **30 FPS**, mas o documento não confirma que essa alteração de FPS tenha sido salva no disco. O intervalo principal observado continuava de **1 a 250**, e a saída configurada era PNG. Não há vídeo final exportado e validado documentado.

**Orientações registradas:** a taxa de quadros pode ser alterada em Propriedades de saída → Formato → Taxa de quadros. Mantendo os keyframes em 1/25/49, o tempo entre início e retorno é de **2 segundos a 24 FPS**, **1,6 segundo a 30 FPS** e **0,8 segundo a 60 FPS**. Para manter dois segundos, os exemplos são **1/31/61 a 30 FPS** e **1/61/121 a 60 FPS**. A prévia de 2 a 3 quadros/s relatada pelo usuário representa o desempenho da viewport; o vídeo renderizado segue a taxa configurada na saída. Aumentar o FPS da cena não melhora, por si só, o desempenho da prévia. Essas orientações não constituem uma exportação realizada.

**Versionamento realizado ao final do chat:** a animação e sua documentação foram enviadas à branch `main` de [patrick3s/kart](https://github.com/patrick3s/kart), no commit [7105f36 — anima ida e volta da cabeça e documenta o processo](https://github.com/patrick3s/kart/commit/7105f36b3c60ee444dfda92cf1e4d0976df5667e). Como o arquivo principal tinha aproximadamente 114 MB, foi instalado o Git LFS e foram migrados os arquivos `.blend` dos dois commits ainda locais. A comparação por SHA-256 confirmou o conteúdo integral dos arquivos antes e depois da migração, e `git lfs fsck` passou. O envio incluiu três versões de arquivos Blender, aproximadamente 309 MB; a referência remota foi consultada e confirmou o commit. Backups automáticos como `.blend1` ficaram locais e passaram a ser ignorados pelo Git.

O registro detalhado da animação foi escrito **antes** desse commit e envio. Portanto, sua indicação de que ainda não havia publicação descreve o momento da documentação; a publicação posterior fica registrada aqui. Esta atualização do `PERSONAGEM.md` é posterior ao commit citado e não faz parte dele.

### Referências do segundo passo

| Parte do trabalho deste chat | Referência detalhada |
| --- | --- |
| Inspeção de objetos, ossos e pesos | [Estado inicial consultado pelo Blender MCP](registros/registro-animacao-cabeca-2026-10-15.md#2-inspeção-inicial-pelo-blender-mcp) |
| Sentido da rotação, eixo correto e seleção de `PoseBone` | [Rotação estática de 40° e compatibilidade da API](registros/registro-animacao-cabeca-2026-10-15.md#3-rotação-estática-de-40) |
| Ação, keyframes, interpolação e loop de prévia | [Animação de ida e volta](registros/registro-animacao-cabeca-2026-10-15.md#4-animação-de-ida-e-volta) |
| Corpo, pivô e quadros intermediários | [Verificações de preservação](registros/registro-animacao-cabeca-2026-10-15.md#5-verificações-de-preservação) |
| FPS e duração do movimento | [Orientação sobre FPS](registros/registro-animacao-cabeca-2026-10-15.md#6-orientação-sobre-fps) |
| Prévia lenta e comportamento esperado do vídeo | [Prévia lenta e exportação](registros/registro-animacao-cabeca-2026-10-15.md#7-prévia-lenta-e-exportação) |
| Estado observado, arquivos e limites da entrega | [Consulta durante a documentação](registros/registro-animacao-cabeca-2026-10-15.md#8-estado-consultado-durante-a-documentação) e [limites do registro](registros/registro-animacao-cabeca-2026-10-15.md#9-arquivos-e-limites-do-registro) |
| Reprodução da animação no Blender | [Como visualizar o resultado](registros/registro-animacao-cabeca-2026-10-15.md#10-como-visualizar-o-resultado) |
| Entrega versionada e arquivos grandes | [Commit publicado](https://github.com/patrick3s/kart/commit/7105f36b3c60ee444dfda92cf1e4d0976df5667e), [configuração do Git LFS](../../.gitattributes) e [instruções para obter os arquivos](../../documentacao/README.md#arquivos-do-blender-no-repositório) |

Não tratar a descrição desta etapa histórica como confirmação automática do estado atual do arquivo ou do Blender aberto. A receita geral para novos personagens continua abaixo; seu Passo 2 trata da preservação da entrada, enquanto `P001.02` identifica o segundo trabalho realizado no primeiro personagem.

## P001.04 — Animação da cabeça para a esquerda

**Executada pelo Blender MCP em 15/10/2026**, após inspeção da cena aberta. A ação `Cabeca_Esquerda_Ida_e_Volta` é uma cópia da ação da direita com o sinal dos valores e das alças Bézier invertido. Anima somente o índice 1 de `pose.bones["Head_Bone"].rotation_euler`: **1: 0°; 25: −40°; 49: 0°**. Mantém `BEZIER`, `AUTO_CLAMPED` e extrapolação constante. Nenhum limite novo foi aplicado ao rig; a amplitude de 40° foi mantida no sentido oposto, sem ultrapassagem nas amostras da curva.

A hierarquia `Root_Bone` → `Torso_Bone` → `Neck_Bone` → `Head_Bone`, o pivô `(0, -0.0625, 0.4375)`, os pesos exclusivos e os modificadores foram preservados. A ação da direita mantém suas curvas originais e foi marcada para retenção no arquivo, mesmo sem estar ativa.

**Validação:** pivô, matrizes dos demais ossos, localização e escala da cabeça permaneceram iguais nos 49 quadros inteiros. Nos quadros 1/13/25/37/49, todos os vértices avaliados do corpo permaneceram imóveis; a diferença máxima da cabeça em relação a uma transformação rígida foi `3.494387468272464e-8` unidade, e a variação máxima no comprimento das arestas foi `3.606600965273821e-8`. Os hashes da geometria-base, conectividade, UVs e índices de materiais permaneceram iguais. A comparação da curva esquerda com a negativa da direita teve erro zero em 481 amostras. A viewport foi inspecionada nas duas ações no quadro 25.

O arquivo principal foi salvo com **30 FPS**, ação esquerda ativa, **quadro 25** e prévia **1 a 49**. O tempo entre início e retorno é **1,6 segundo**. O intervalo principal continua em 1 a 250. Para assistir, reproduzir a timeline com a prévia ativa. Backup anterior à edição: [kart_antes_animacao_esquerda_20261015.blend](backups/kart_antes_animacao_esquerda_20261015.blend). Não houve exportação de vídeo, commit ou publicação nesta etapa.

Procedimento e limites: [registro detalhado](registros/registro-animacao-cabeca-esquerda-2026-10-15.md). Medições: [relatório JSON](validacao/validacao_animacao_cabeca_esquerda.json).

## P001.05 — Separação das quatro rodas

**Executada pelo Blender MCP em 15/10/2026.** As rodas foram identificadas entre as ilhas desconectadas de `Corpo_Kart` e separadas como conjuntos completos, preservando os elementos originais. Cada objeto tem uma malha exclusiva: `Wheel_Front_Left`, `Wheel_Front_Right`, `Wheel_Rear_Left` e `Wheel_Rear_Right`. A frente do modelo é **−Y**; esquerda e direita são as do piloto, com **+X à esquerda**.

As origens usam o **centro da caixa delimitadora da geometria de cada roda**, calculado por `ORIGIN_GEOMETRY` com `BOUNDS`. O giro usa **X local** e o esterço usa **Z local**. Cada roda foi ligada diretamente a `Torso_Bone`, com compensação das transformações; o modificador Armature herdado foi removido dessas quatro malhas para permitir rotação por objeto em torno de sua própria origem. O restante de `Corpo_Kart` mantém sua ligação anterior ao rig.

**Preservação verificada:** os **874.925 vértices, 2.536.689 arestas e 1.662.516 faces** do `Corpo_Kart` anterior estão presentes exatamente uma vez entre o corpo restante e as quatro rodas. Coordenadas reconstruídas no espaço de referência tiveram erro zero. Conectividade, UVs, dados de normais personalizadas, materiais e suavização foram preservados. O maior erro numérico de centralização da origem foi `1.666000468656264e-8` unidade.

Nos quadros **1, 8, 17, 29 e 49**, a diferença máxima das posições mundiais em relação ao acompanhamento anterior do rig foi `5.960464477539063e-8` unidade. Testes temporários de **90° em X** e **30° em Z** tiveram deslocamento zero do pivô; as rotações foram restauradas. O arquivo salvo foi aberto em uma segunda instância do Blender para conferir os quatro objetos, a exclusividade das malhas e as contagens totais.

O modelo, o backup anterior à separação e o relatório foram incluídos no **commit local `e2a2848`**. Este registro textual complementa essa entrega em um commit documental posterior, junto ao índice e aos registros referenciados da evolução do personagem. Não houve exportação ou validação na Godot nesta etapa.

Procedimento, contagens por objeto e limites: [registro detalhado das rodas](registros/registro-rodas-independentes-2026-10-15.md). Evidências: [relatório JSON](validacao/verificacao_rodas_independentes.json). Cópia anterior: [backup das rodas](backups/kart_antes_separar_rodas_20261015_134523.blend).
