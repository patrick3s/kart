# Prompt — iniciar um novo personagem

Para usar, peça ao agente: **“Execute o fluxo de `documentacao/PROMPT_NOVO_PERSONAGEM.md`.”** Também é possível copiar o conteúdo abaixo para uma nova conversa na pasta deste projeto.

Este prompt inicia a organização e o planejamento. As fases de produção ficam registradas no checklist; o estado de retomada fica em um `CHECKPOINT.md` próprio de cada personagem, para continuar o trabalho mesmo em outra conversa.

## Instruções para o agente

Atue como artista técnico de personagens 3D e responsável pela organização deste projeto. Inicie o fluxo de um **novo personagem**, seguindo a versão atual de [RECEITA_PERSONAGEM.md](RECEITA_PERSONAGEM.md), inclusive seus prompts de rig, animações, rodas e integração com a Godot. Responda sempre em português.

Leia a receita e as instruções locais aplicáveis antes de criar arquivos. Resolva os caminhos a partir da raiz deste repositório; não dependa dos caminhos absolutos do computador de quem escreveu este prompt. A receita define o método; a pasta de cada personagem guarda os dados e as evidências dele.

### 1. Perguntar o nome

Se o nome ainda não tiver sido informado, pergunte: **“Qual é o nome do novo personagem?”** Aguarde a resposta antes de criar uma pasta de personagem. Se o usuário já informou o nome no pedido, aproveite essa informação sem perguntar novamente.

Preserve o nome de exibição exatamente como informado. Para nomes de arquivos e pastas, gere um identificador seguro em minúsculas, sem acentos, usando `_` entre palavras e sem separadores de caminho. Registre a relação entre nome de exibição e nome de pasta na ficha.

### 2. Reservar o identificador e criar a estrutura

Inspecione as pastas reais de `personagens/` e escolha o próximo identificador sequencial disponível, no formato `P001`, `P002` etc., depois do maior número existente. Não fixe o próximo número com base no exemplo do Jake.

Confira também se já existe personagem com o mesmo nome de pasta. Se houver dúvida entre retomar um personagem e iniciar outro, esclareça essa escolha antes de criar uma duplicata. Ao retomar, preserve o identificador, os arquivos e as marcações existentes.

Crie a estrutura abaixo, substituindo `P00N` e `nome` pelos valores calculados:

```text
personagens/P00N_nome/
  LEIA-ME.md
  CHECKLIST.md
  CHECKPOINT.md
  referencia/
    LEIA-ME.md
  blender/
  backups/
  validacao/
  registros/
```

Em pastas que continuarem vazias, use `.gitkeep` se necessário para que possam ser versionadas. Não crie modelos, exportações ou relatórios fictícios como preenchimento.

Preencha `LEIA-ME.md` com identificador, nome, data local de criação, objetivo, estado inicial, links para a receita, checklist, checkpoint e referências, além de uma tabela de histórico. Dados ainda desconhecidos devem constar como **“A informar”**. Registre a inicialização documental como a primeira etapa, sem afirmar que houve modelagem, rig ou validação.

Crie `CHECKPOINT.md` usando o [modelo de checkpoint](MODELO_CHECKPOINT_PERSONAGEM.md) e preencha os dados deste personagem. Esse arquivo deve existir desde a inicialização, mesmo enquanto faltam referências.

Inclua um link para a ficha no índice `documentacao/README.md`, preservando as entradas existentes. Não altere arquivos de outros personagens.

### 3. Solicitar as referências

Depois de criar as pastas, informe o **caminho real completo** de `referencia/` e peça:

**“Adicione as referências do personagem nesta pasta, ou anexe os arquivos aqui para eu organizá-los nela. Envie as imagens disponíveis, o modelo 3D se já existir e suas texturas. Depois me avise para conferir os arquivos.”**

Aceite os arquivos disponíveis, sem exigir imagens de ângulos que o usuário não possui. Imagens de frente, lado, costas e detalhes são úteis quando existirem. Diferencie referência visual de modelo 3D que será efetivamente trabalhado.

Em `referencia/LEIA-ME.md`, explique onde colocar imagens, modelos e texturas e mantenha um inventário com nome do arquivo, tipo, função e origem informada. Se nenhum arquivo tiver chegado, escreva **“Aguardando referências”**, sem inventar entradas.

Quando receber anexos, copie somente os arquivos efetivamente acessíveis para a pasta do personagem, preservando os originais e os nomes quando possível. Resolva colisões sem sobrescrever arquivos. Se um anexo não tiver caminho acessível, explique essa limitação e solicite a colocação do arquivo na pasta; não finja que a cópia foi feita.

Pergunte se há kart/veículo e quais partes precisam ser independentes apenas se isso não estiver claro nas referências ou no pedido. Enquanto aguarda os arquivos ou essa informação, prepare o checklist abaixo. Não dependa das referências para criar o planejamento inicial.

### 4. Criar `CHECKLIST.md` por fases

Gere um checklist próprio para este personagem usando a receita atual como fonte. Use a base abaixo, acrescentando tarefas se a receita tiver evoluído. Substitua identificador, nome e caminhos pelos valores reais; não deixe campos de modelo sem preencher quando a informação já estiver disponível.

No início do arquivo, registre personagem, data, link para a receita, fase atual, próximo passo, pendências e a versão da receita consultada — commit e estado local, quando disponíveis. Se houver alterações locais na receita, registre esse fato; não atribua essas alterações somente ao último commit.

Use `[ ]` para tarefas pendentes e `[x]` somente para tarefas concluídas com evidência. Para cada fase, informe **objetivo, dependências, entregáveis, critério de conclusão e estado**. Estados: `Pendente`, `Em andamento`, `Aguardando referências`, `Bloqueada`, `Concluída` ou `Não se aplica`. Uma fase não aplicável exige justificativa, sem marcar suas tarefas como executadas.

#### Fase 0 — Identificação e organização

- [ ] Confirmar o nome de exibição e reservar o identificador único.
- [ ] Criar as pastas e a ficha `LEIA-ME.md`.
- [ ] Criar este checklist e o guia de referências.
- [ ] Criar `CHECKPOINT.md` com o estado inicial e o próximo passo.
- [ ] Registrar o personagem no índice da documentação.
- [ ] Solicitar as referências e informar o caminho da pasta.

Marque nesta fase apenas as ações de inicialização que você tiver acabado de executar. Solicitar referências não significa que elas foram recebidas.

#### Fase 1 — Referências e escopo

- [ ] Receber, inventariar e conferir os arquivos de referência acessíveis.
- [ ] Identificar o modelo 3D de entrada ou registrar que ele ainda não existe.
- [ ] Definir aparência, veículo/acessórios, partes independentes e objetivo de entrega.
- [ ] Se houver apenas imagens, planejar a obtenção ou criação da malha antes do rig; não considerar uma imagem como modelo pronto.
- [ ] Registrar lacunas, dependências e o arquivo de entrada escolhido na ficha.

#### Fase 2 — Inspeção e preservação da entrada

- [ ] Inspecionar o modelo no Blender MCP e conferir orientação, escala e partes existentes.
- [ ] Levantar malhas, ilhas, pais, materiais, UVs, normais, modificadores, shape keys, grupos e animações.
- [ ] Salvar uma cópia anterior à edição em `backups/`.
- [ ] Registrar contagens, coordenadas, conectividade e atributos necessários à comparação.
- [ ] Definir identificadores de rastreamento e tolerâncias para a validação.

#### Fase 3 — Separação das partes

- [ ] Identificar cabeça, corpo, veículo e acessórios com base neste modelo.
- [ ] Separar a cabeça completa e seus detalhes por partes existentes, preservando a geometria.
- [ ] Definir e realizar a separação entre personagem e veículo quando exigida pela entrega.
- [ ] Identificar e separar as quatro rodas em objetos com malhas exclusivas, se houver kart.
- [ ] Padronizar nomes e conferir frente, traseira, esquerda e direita do piloto.
- [ ] Conferir as partes isoladas e reunidas; registrar impedimentos e tentativas desfeitas.

Não reutilize limites de coordenadas ou índices de ilhas do Jake. Se preservar a topologia for incompatível com o corte necessário, registre o impedimento e resolva o escopo antes de alterar a geometria.

#### Fase 4 — Pivôs, esqueleto e pesos

- [ ] Medir e posicionar o pivô da cabeça na base do pescoço deste personagem.
- [ ] Medir os centros das rodas e registrar o critério geométrico adotado, quando aplicável.
- [ ] Criar ou adaptar a hierarquia de ossos e os nomes dos controles.
- [ ] Atribuir pesos rígidos exclusivos às partes que devem permanecer rígidas.
- [ ] Definir o parentesco e os modificadores necessários, compensando as transformações.
- [ ] Conferir ausência de vazamento de pesos, pivôs deslocados e influência duplicada.

#### Fase 5 — Validação da preparação

- [ ] Comparar presença, contagens, conectividade, coordenadas, UVs, materiais e normais com a referência.
- [ ] Medir a preservação no espaço apropriado e registrar arredondamentos numéricos.
- [ ] Testar temporariamente os controles da cabeça, corpo e rodas, quando aplicável.
- [ ] Confirmar isolamento entre partes e estabilidade dos pivôs; restaurar os testes.
- [ ] Salvar relatório em `validacao/` e registro detalhado em `registros/`.
- [ ] Salvar e conferir o `.blend` gravado, distinguindo cena aberta de arquivo em disco.

#### Fase 6 — Animações da cabeça

- [ ] Definir eixo, sentidos, amplitude, duração e FPS para este personagem.
- [ ] Criar a ação de olhar para a direita e retornar à posição original.
- [ ] Criar a ação para a esquerda preservando a ação anterior.
- [ ] Conferir keyframes, alças, interpolação e quadros intermediários.
- [ ] Medir preservação do corpo, rigidez da cabeça e estabilidade do pivô.
- [ ] Registrar ações, intervalos de prévia, FPS, testes e estado salvo.

#### Fase 7 — Exportação e importação na Godot

- [ ] Definir o formato de exportação e quais ações/poses devem ser exportadas.
- [ ] Conferir materiais, texturas, escala, orientação, nomes, ossos e partes independentes.
- [ ] Exportar para `jogo/personagens/nome/`, usando o nome de pasta deste personagem.
- [ ] Importar e inspecionar o recurso real na Godot pela CLI.
- [ ] Verificar novamente a estrutura e os pivôs após a importação.
- [ ] Registrar o artefato exportado e as diferenças em relação ao Blender.

Não crie uma pasta de exportação vazia durante a inicialização. Se o projeto Godot ainda não existir, registre sua criação como dependência desta fase.

#### Fase 8 — Personagem jogável e mecânicas

- [ ] Criar a ficha do novo piloto e integrá-lo ao catálogo sem substituir os existentes.
- [ ] Testar a escolha entre o novo personagem e pelo menos um piloto já cadastrado, quando disponível.
- [ ] Testar movimento, frenagem, ré e direção no cenário quadriculado.
- [ ] Testar a câmera atrás do personagem, acompanhamento e resposta dinâmica.
- [ ] Verificar giro das quatro rodas, ré, parada e esterço dianteiro, se houver kart.
- [ ] Verificar suspensão e vibração nos dois sentidos de curva, quando aplicável.
- [ ] Medir a inclinação global da cabeça, considerando o movimento herdado do corpo.
- [ ] Verificar compensação em entrada, inversão e saída de curva, parada e tremor.
- [ ] Distinguir compensação estabilizada de oposição em todo quadro; se o requisito for “sempre”, tratar violações transitórias como falhas.
- [ ] Registrar testes no motor, inspeção visual e limitações separadamente.

A auditoria do Jake encontrou atraso de mola e tremor não compensado. Reutilizar o código dele não comprova que essas regras passaram no novo personagem. Se o personagem não tiver veículo, adaptar esta fase ao movimento e às mecânicas previstas, justificando os itens não aplicáveis.

#### Fase 9 — Entrega e documentação

- [ ] Atualizar ficha, histórico e checklist com os resultados efetivamente obtidos.
- [ ] Vincular modelos, backups, exportações, relatórios e registros com caminhos relativos válidos.
- [ ] Conferir critérios de conclusão de cada fase e registrar pendências restantes.
- [ ] Resumir controles, limitações e instruções para reproduzir as verificações.
- [ ] Registrar eventual commit ou publicação somente quando solicitado e realizado.

Preserve os resultados históricos e seus hashes. Um teste de uma versão anterior não valida automaticamente o artefato modificado.

### 5. Manter o estado em `CHECKPOINT.md`

O checkpoint é o resumo atual para retomada; o checklist mantém as tarefas e suas marcações, e os registros guardam o histórico detalhado. Não use o checkpoint para substituir relatórios ou duplicar todas as tarefas.

Mantenha nele: identidade e pasta do personagem; data/hora local da atualização com fuso; objetivo e escopo informado pelo usuário; fase e tarefa atuais; último passo confirmado; arquivos de entrada e de trabalho; estado salvo ou não salvo das ferramentas; evidências de validação; decisões; pendências; pergunta ainda sem resposta, quando houver; e próximo passo concreto.

Na inicialização, registre como concluídas somente as ações documentais realizadas. Se os arquivos ainda não chegaram, o estado deve ser **“Aguardando referências”**, com o caminho de `referencia/`, a solicitação já feita e a conferência dos anexos como próximo passo. Não registre inspeção de malha, backup de modelo ou testes como executados.

Atualize o checkpoint depois de cada avanço relevante, conclusão de fase ou teste, ao encontrar um impedimento e antes de encerrar a resposta ou aguardar material do usuário. Preserve o último passo comprovado quando uma tentativa falhar e registre a falha separadamente. Faça a atualização junto ao checklist e à ficha para evitar estados contraditórios. Não reescreva o arquivo apenas porque o tempo passou.

Sempre que um artefato mudar, indique quais validações precisam ser refeitas. Registre caminhos relativos à pasta do personagem e links para evidências existentes; inclua revisão/hash do artefato quando medidos. Distinga arquivo salvo, cena aberta com alterações não salvas e recurso importado na Godot. Se a ferramenta não puder ser consultada, escreva **“Não verificado nesta atualização”**.

Grave o estado completo sem apagar a última versão válida antes de terminar a escrita; quando possível, escreva um arquivo temporário na mesma pasta e substitua o checkpoint somente após conferir seu conteúdo. Não armazene credenciais ou outros segredos. O checkpoint é um retrato do último estado observado, não uma confirmação de que uma ferramenta ou processo continua aberto.

### 6. Encerrar a inicialização e permitir retomada

Depois de criar os arquivos iniciais, apresente links para a ficha, o checklist e o checkpoint, o caminho das referências e a próxima ação concreta. Enquanto faltarem arquivos, mantenha o estado **“Aguardando referências”**. Quando chegarem, atualize o inventário e as tarefas correspondentes com o que foi realmente conferido.

O pedido de inicialização autoriza criar a estrutura, solicitar/organizar as referências e preparar o planejamento. Não execute todas as fases de produção por interpretar o checklist como autorização. Se o usuário já tiver solicitado uma fase de produção, avance dentro desse escopo, sem pedir de novo autorização para etapas rotineiras já incluídas nele.

Em uma retomada, leia primeiro `CHECKPOINT.md`, depois `CHECKLIST.md` e `LEIA-ME.md` do personagem. Confira a existência e a versão dos arquivos relevantes e consulte a ferramenta real antes de depender do estado de uma sessão anterior. Se houver divergência, registre o que mudou e ajuste o checkpoint antes de continuar; não repita automaticamente passos já comprovados nem confie em validações de uma versão antiga.

Se um personagem anterior ainda não tiver checkpoint, crie-o a partir da ficha, checklist, arquivos e evidências disponíveis, identificando o que não pôde ser verificado. Não reinicie o personagem nem invente resultados para preencher lacunas.

Continue da fase pendente pertinente ao pedido atual, preservando o trabalho existente. O escopo resumido no checkpoint é contexto histórico; não amplia a solicitação atual nem concede autorizações por si só. Atualize checklist, ficha, evidências e próximo passo ao concluir cada fase. Não marque uma fase como concluída apenas porque existe um script, um arquivo ou uma previsão de resultado.
