# Prompt — iniciar e produzir uma nova pista

Para iniciar, peça ao agente: **“Execute o fluxo de `documentacao/PROMPT_NOVA_PISTA.md` para a pista NOME.”** Se o nome não for informado, o agente deve solicitá-lo. Também é possível usar este arquivo em uma nova conversa na raiz do repositório.

O fluxo segue a organização do [novo personagem](PROMPT_NOVO_PERSONAGEM.md): projeto Blender exclusivo, referências preservadas, checklist por fases e checkpoint para retomada. A produção segue a [receita de pistas](RECEITA_PISTA.md), baseada na integração real da PI001.

## Instruções para o agente

Atue como artista técnico de pistas 3D e responsável pela integração na Godot deste repositório. Responda sempre em português. Leia as instruções locais, `documentacao/RECEITA_PISTA.md`, `pistas/LEIA-ME.md` e o estado atual do jogo antes de editar. Confira `git status` e preserve todas as alterações existentes.

Resolva os caminhos a partir da raiz real do repositório. Não use caminhos absolutos de outra máquina nem fixe o próximo identificador com base no exemplo PI001. A receita define o método; a pasta de cada pista guarda suas escolhas e evidências.

### 1. Identificar o nome e a intenção

Se o nome não estiver disponível, pergunte **“Qual é o nome da nova pista?”** e aguarde antes de criar a pasta específica. Aproveite nomes e referências já informados, sem pedir novamente.

Preserve o nome de exibição. Gere um nome seguro em minúsculas, sem acentos, com `_` entre palavras e sem separadores de caminho. Inspecione as pastas reais de `pistas/` e escolha `PI001`, `PI002` etc., depois do maior número ocupado. Ignore `_modelo/` e a entrada de referências ao calcular a sequência.

Confira nomes já usados também em `jogo/pistas/`. Se o pedido for de retomada, preserve pasta e identificador. Se houver dúvida real entre retomar e duplicar uma pista, esclareça antes de criar outra.

O pedido de **iniciar** autoriza a organização, criação/conferência do projeto exclusivo, recebimento e preparação de cópias das referências e planejamento. Se o usuário pedir **produção completa ou integração até ficar jogável**, avance por todas as fases necessárias já autorizadas, atualizando o checkpoint; não encerre na inicialização nem peça autorização novamente para passos rotineiros desse escopo.

### 2. Criar ficha, checklist e checkpoint

Crie a estrutura abaixo com os valores reais:

```text
pistas/PI00N_nome/
  LEIA-ME.md
  CHECKLIST.md
  CHECKPOINT.md
  referencia/
    LEIA-ME.md
  blender/
    nome.blend
  texturas/
  backups/
  validacao/
  registros/
```

Use `pistas/_modelo/LEIA-ME.md` e `pistas/_modelo/referencia/LEIA-ME.md` como base. O `.blend` é criado na próxima seção, não por um arquivo fictício. Pastas vazias podem ter `.gitkeep`. Crie subpastas de evidência somente quando houver um trabalho ou ensaio real a registrar; `jogo/pistas/nome/` fica para a exportação.

Preencha a ficha com identificador, nome, data local, objetivo, tema/cenário, origem das referências, medidas, largura, sentido, largada, terreno, caminho do `.blend`, estado e histórico. Informações desconhecidas ficam como **“A informar”**; hipóteses ficam identificadas como provisórias.

Crie `CHECKLIST.md` a partir de `pistas/_modelo/CHECKLIST.md`, adaptando-o à pista e à receita atual. Registre revisão da receita, inclusive alterações locais, quando disponíveis. Cada fase deve ter objetivo, dependências, entregáveis, critério e estado. Marque `[x]` somente com evidência; uma tarefa não aplicável exige justificativa, sem fingir execução.

Crie `CHECKPOINT.md` usando `documentacao/MODELO_CHECKPOINT_PISTA.md`. Preencha o estado observado, a última ação confirmada e o próximo passo. Registre a pista no índice `documentacao/README.md`, preservando todas as entradas anteriores. Não altere documentos de outras pistas para preencher a inicialização.

### 3. Criar e conferir o Blender exclusivo

Crie um `.blend` real em `pistas/PI00N_nome/blender/nome.blend` pelo **Blender MCP, na instância já aberta**. Não abra outra instância nem execute Blender pela CLI. Se o destino já existir, inspecione-o e retome; não o substitua por um projeto vazio.

Antes de operar, consulte arquivo aberto, `bpy.data.is_dirty`, modo, cena e objetos. Preserve qualquer trabalho pendente de outro projeto numa cópia segura e confira o salvamento antes de mudar de arquivo na mesma sessão. Se o destino de preservação não puder ser definido com segurança, peça apenas a informação necessária.

Para projeto novo sem modelo, crie uma cena vazia depois da preservação, sem cubo/câmera/luz de exemplo, e salve imediatamente. Para `.blend` recebido, preserve o original em `referencia/` e prepare uma cópia no destino exclusivo. Para outro formato 3D, importe uma cópia. Não altere escala ou geometria durante a organização inicial. Com mais de uma entrada possível e sem escolha definida, aguarde essa definição antes de misturar modelos.

Confira existência, tamanho e carregamento do arquivo salvo, recarregando-o do disco na mesma sessão após preservar eventuais mudanças. Registre caminho e conteúdo: **“Projeto criado, aguardando modelo”**, **“Modelo carregado”** ou **“Criação bloqueada”**. Isso não comprova geometria ou materiais validados.

Se o MCP não estiver conectado, continue a documentação possível, registre o bloqueio e solicite a conexão da instância aberta com o add-on ativo. Não crie um `.blend` falso nem marque a fase como concluída.

### 4. Receber e inventariar referências

Informe o caminho real completo de `referencia/` e solicite os materiais ainda ausentes: desenho do traçado, imagens, tema/cenário, modelo 3D e texturas, quando existirem. Aceite o que estiver disponível; não exija vistas inexistentes. Peça ao usuário que coloque os arquivos na pasta ou os anexe para organização quando acessíveis.

Copie apenas arquivos efetivamente disponíveis, preservando originais e resolvendo colisões de nomes sem sobrescrever. Em `referencia/LEIA-ME.md`, registre arquivo, tipo, função e origem informada. Se um anexo não estiver acessível, explique a limitação; não declare uma cópia que não ocorreu.

Diferencie desenho, eixo, modelo e materiais. Uma imagem não é uma pista 3D pronta. Aproveite medidas já dadas; para lacunas, registre premissas reversíveis ou pergunte o indispensável. Se houver modelo pronto, preserve seu traçado e escala provisória, salvo necessidade demonstrada.

### 5. Executar as fases de produção autorizadas

Siga o checklist próprio da pista e a receita atual. As fases são:

| Fase | Resultado esperado |
| --- | --- |
| 0 — Identificação e organização | Ficha, inventário, planejamento e projeto Blender exclusivo conferido |
| 1 — Referências e escopo | Entrada definida; hipóteses, medidas e limites documentados |
| 2 — Eixo, escala e largada | Percurso ordenado/fechado, largura e tangente conferidos |
| 3 — Modelo e materiais | Pista modelada ou entrada preparada, com validação geométrica e visual |
| 4 — Exportação e importação | Recursos reais na Godot, eixo alinhado e materiais conferidos |
| 5 — Cena jogável | Colisões, grid, câmera, HUD, personagens e acesso no menu |
| 6 — Percurso e IA | Adversários seguindo o eixo real, freando nas curvas e no mesmo sentido |
| 7 — Controles e personagens | Física, zebras, terreno, pneus, colisões e regressões executados |
| 8 — Voltas e conferência visual | Cada IA completa volta medida; capturas reais inspecionadas |
| 9 — Entrega e retomada | Documentos consistentes, evidências preservadas e pendências explícitas |

Durante as fases:

- Inspecione/prepare/exporte pelo Blender MCP; use cópia ou cena temporária e preserve o `.blend` de origem. Delimite cena ativa e seleção e restaure o estado temporário após a exportação.
- Inclua asfalto, zebras, sinalização e terreno conforme a referência. Exclua câmeras/luzes de apresentação e imagem de referência do GLB. Converta materiais procedurais por bake ou equivalência documentada e confira o resultado importado/renderizado.
- Exporte para `jogo/pistas/nome/` e crie `nome.tscn`. Confira unidades, orientação e transformação comum de malha, eixo e largada. Use o percurso real em `Path3D/Curve3D` fechado ou equivalente.
- Reutilize kart, câmera de perseguição, HUD, controles e HDRI existentes. Preserve os pilotos cadastrados, a arena de testes e todas as pistas anteriores no menu. Não copie caminhos fixos ou índices do seletor da PI001 como se servissem à nova pista.
- Posicione o grid pela tangente, sem sobreposição. Meça os desníveis e teste ida/retorno do terreno; ajuste a transposição de degraus somente quando necessário e sem atravessar karts/barreiras.
- Na pista nova, não use o circuito circular de `kart_ia.gd`. Configure percurso, sentido, definição, faixa, velocidade e transform **antes de adicionar cada adversário à árvore**, pois `_ready()` depende deles. Preserve a IA legada na arena.
- Faça a IA antecipar curvas, reduzir velocidade e contornar obstáculos dentro da largura útil. Perseguição não pode fazê-la abandonar o percurso. Teste também jogador parado na largada.
- Atualize `jogo/ferramentas/construir_cenas.gd` ou o gerador vigente; regenerar não pode remover nenhuma integração.
- Execute importação/scripts headless e regressões pertinentes. Examine resultados e logs, além do código de saída. Use pastas novas para evidências; adapte os destinos fixos das ferramentas da PI001 antes de reutilizá-las.
- Abra o jogo no renderizador real e confira menu, grid, escala, materiais, câmera e contato dos pneus. Teste aceleração, frenagem, ré, curvas e zebras. Distinga o que foi automatizado do que foi pilotado manualmente.
- Execute **cada adversário por pelo menos uma volta completa**, registrando progresso, tempo, desvio, contramão, saídas, colisões e recuperações. Defina o critério de saída e não conte teletransporte como progresso de uma volta limpa.
- Exercite todos os personagens cadastrados. Preserve rodas, suspensão, cabeça, câmera e colisões. Registre tolerâncias, limitações e quais validações foram invalidadas por mudanças posteriores.

Não copie como padrões a largura, a escala, o número de pontos, a velocidade, as faixas ou a altura de degrau da PI001. Meça a pista atual. O regulamento de corrida (classificação, cronômetro e regras de checkpoints) só é implementado quando fizer parte do pedido.

### 6. Manter o estado para outra conversa

Após cada avanço relevante, teste ou impedimento, atualize ficha, checklist e checkpoint de forma consistente. Faça isso também antes de aguardar material do usuário ou encerrar a resposta. Preserve a última etapa comprovada quando uma tentativa falhar.

O checkpoint deve registrar identidade, data/hora com fuso, objetivo autorizado, fase/tarefa, última ação confirmada, entradas, projeto exclusivo, exportação, estado salvo/não salvo, revisão/hashes quando medidos, evidências, decisões, perguntas pendentes e próximo passo concreto. Só crie links para destinos existentes; saídas futuras ficam como “Ainda não criado”.

Distinga **documentação criada**, **projeto salvo**, **cena aberta**, **modelo validado**, **recurso importado**, **jogo executado** e **aparência conferida**. Não use um relatório de outra versão como comprovação. Se a ferramenta não tiver sido consultada, registre “Não verificado nesta atualização”.

Para retomar, leia primeiro `CHECKPOINT.md`, depois `CHECKLIST.md` e `LEIA-ME.md`. Confira arquivos, versões e ferramenta real quando necessário. Continue a fase pendente compatível com o pedido atual, sem repetir etapas comprovadas nem confiar em uma sessão supostamente ainda aberta.

Se uma pista antiga não tiver checklist/checkpoint, derive-os de arquivos e evidências reais, explicitando o que não foi verificado. Não reinicie a pista nem invente resultados para completar campos.

### 7. Entregar conforme o escopo

Na inicialização, apresente links para ficha, checklist, checkpoint e `.blend` efetivamente criado; informe caminho das referências, conteúdo do projeto e próximo passo. Se houver dependência ausente, informe o bloqueio concreto.

Na produção completa, entregue o acesso no menu, cena jogável, controles, arquivos criados/alterados, testes realmente executados, evidências numéricas e visuais, limitações e pendências. Se alguma etapa obrigatória falhar, trate o resultado como parcial; a existência dos arquivos não basta para declarar a pista jogável validada.

## Pedidos prontos para usar

**Inicializar:**

> Execute o fluxo de `documentacao/PROMPT_NOVA_PISTA.md` para a pista “NOME”. Crie a estrutura, o projeto Blender exclusivo, a ficha, o checklist e o checkpoint. Organize as referências disponíveis e prepare o planejamento das fases.

**Produzir até ficar jogável:**

> Execute a produção completa da pista “NOME” seguindo `documentacao/PROMPT_NOVA_PISTA.md` e `documentacao/RECEITA_PISTA.md`. Use as referências já fornecidas e avance até a integração jogável na Godot, com eixo real para a IA, preservação das pistas/personagens, validações e evidências. Registre premissas provisórias e informe qualquer impedimento concreto.

**Retomar:**

> Retome a pista em `pistas/PASTA_DA_PISTA/`: leia `CHECKPOINT.md`, `CHECKLIST.md` e `LEIA-ME.md`, confira os arquivos reais e continue a próxima etapa pendente até o resultado jogável, dentro das restrições registradas e deste pedido. Preserve os originais e os relatórios históricos.
