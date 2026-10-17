# Checklist — {{ID}} — {{NOME}}

Modelo a preencher ao iniciar a pista pelo [prompt](../../documentacao/PROMPT_NOVA_PISTA.md), seguindo a [receita](../../documentacao/RECEITA_PISTA.md). Remova esta instrução de modelo da cópia preenchida.

- **Pasta:** `pistas/{{PASTA}}/`.
- **Criado/atualizado em:** {{DATA_HORA_COM_FUSO}}.
- **Receita consultada:** {{REVISAO_E_ALTERACOES_LOCAIS}}.
- **Fase atual:** {{FASE}}.
- **Próximo passo:** {{ACAO_CONCRETA}}.
- **Pendências:** {{PENDENCIAS_OU_NENHUMA}}.

Estados de fase: `Pendente`, `Em andamento`, `Aguardando referências`, `Bloqueada`, `Concluída` ou `Não se aplica`. Use `[x]` somente para tarefas executadas e comprovadas. Itens não aplicáveis continuam sem marca de execução e recebem justificativa. Preencha nomes/caminhos antes de usar e acrescente tarefas específicas do traçado.

## Fase 0 — Identificação e organização

**Objetivo:** organizar a pista e criar seu projeto exclusivo. **Dependências:** nome definido e acesso ao repositório; Blender MCP para o projeto. **Entregáveis:** ficha, inventário, checklist, checkpoint e `.blend` real conferido. **Critério:** identidade sem colisões e estado dos arquivos registrado. **Estado:** Pendente.

- [ ] Conferir `git status` e preservar alterações anteriores.
- [ ] Definir nome de exibição, nome seguro e próximo identificador PI disponível.
- [ ] Criar estrutura, ficha, inventário, este checklist e checkpoint.
- [ ] Consultar a sessão Blender MCP e preservar trabalho pendente antes de trocar de projeto.
- [ ] Criar ou retomar `blender/{{SLUG}}.blend`; conferir salvamento e recarga do disco.
- [ ] Distinguir projeto vazio, modelo carregado e criação bloqueada.
- [ ] Registrar a pista no índice e solicitar apenas as referências ausentes.

**Evidência/impedimentos:** A informar.

## Fase 1 — Referências e escopo

**Objetivo:** definir entradas e hipóteses de produção. **Dependências:** organização inicial e referências acessíveis. **Entregáveis:** inventário, entrada escolhida e escopo. **Critério:** originais preservados e lacunas explícitas. **Estado:** Pendente.

- [ ] Receber, inventariar e conferir imagens, desenhos, modelos e texturas disponíveis.
- [ ] Identificar a origem informada e preservar os arquivos recebidos.
- [ ] Preparar a cópia do modelo de entrada quando existir; distinguir imagem de malha 3D.
- [ ] Registrar tema, terreno, largura, escala, sentido e largada; identificar dados provisórios.
- [ ] Definir o escopo atual e separar regras de corrida de integração técnica.

**Evidência/impedimentos:** A informar.

## Fase 2 — Eixo, escala e largada

**Objetivo:** estabelecer o percurso real. **Dependências:** desenho/modelo definido. **Entregáveis:** eixo ordenado, convenções e relatório geométrico. **Critério:** continuidade, fechamento, largura e largada coerentes. **Estado:** Pendente.

- [ ] Extrair o eixo da referência/modelo e registrar o método.
- [ ] Conferir sentido, unidades, fechamento, extensão e limites.
- [ ] Medir largura útil, raios de curva, alturas e bordas; verificar cruzamentos indevidos.
- [ ] Justificar adaptações necessárias, preservando a escala/traçado existentes quando possível.
- [ ] Definir largada e orientação pela tangente; prever espaço para o grid.
- [ ] Salvar pontos e metadados, sem confundir arquivo criado com percurso validado.

**Evidência/impedimentos:** A informar.

## Fase 3 — Modelo e materiais no Blender

**Objetivo:** produzir/preparar a geometria jogável. **Dependências:** eixo/medidas definidos e Blender MCP conectado. **Entregáveis:** `.blend` salvo, relatório e vistas. **Critério:** geometria e aparência conferidas contra a referência. **Estado:** Pendente.

- [ ] Fazer e conferir backup antes da edição e levantar geometria/materiais de entrada.
- [ ] Preparar asfalto, zebras, sinalização e terreno conforme o escopo.
- [ ] Separar os objetos exportáveis de eixo, imagem, câmeras e luzes de apresentação.
- [ ] Verificar normais, degenerações, emendas e aberturas inesperadas.
- [ ] Conferir texturas/dependências e definir bake ou materiais equivalentes para a Godot.
- [ ] Salvar/recarregar o projeto e inspecionar renders superior e de perspectiva.

**Evidência/impedimentos:** A informar.

## Fase 4 — Exportação e importação

**Objetivo:** transportar a pista para a Godot. **Dependências:** fonte Blender definida e preservada. **Entregáveis:** recursos em `jogo/pistas/{{SLUG}}/`, eixo e manifesto. **Critério:** recurso importado mantém escala, orientação, alinhamento e materiais previstos. **Estado:** Pendente.

- [ ] Preparar e exportar pelo Blender MCP em cópia/cena temporária, sem sobrescrever a origem.
- [ ] Delimitar cena ativa e seleção; conferir nós exportados e excluir apresentação/referência.
- [ ] Exportar geometria, materiais, texturas necessárias e eixo real.
- [ ] Conferir transformação comum entre malha, eixo e largada, evitando dupla conversão.
- [ ] Executar importação headless e inspecionar recursos/materiais reais.
- [ ] Comparar pontos, dimensões e fechamento após importar; guardar hashes e logs.
- [ ] Restaurar o estado temporário da sessão e confirmar a preservação da fonte.

**Evidência/impedimentos:** A informar.

## Fase 5 — Cena jogável e menu

**Objetivo:** permitir entrar e dirigir na pista. **Dependências:** recursos importados. **Entregáveis:** `jogo/pistas/{{SLUG}}/{{SLUG}}.tscn`, acesso no menu e geração persistente. **Critério:** grid sem sobreposição, ambiente reutilizado e integrações anteriores acessíveis. **Estado:** Pendente.

- [ ] Criar colisões estáticas adequadas para asfalto, zebras e terreno.
- [ ] Reutilizar kart, câmera, HUD, controles, ambiente HDRI e personagens atuais.
- [ ] Posicionar o grid pela tangente e conferir volumes, altura e espaçamento.
- [ ] Medir desníveis e ajustar a transposição somente se necessário.
- [ ] Adicionar a pista ao menu preservando arena e demais pistas.
- [ ] Incluir a cena e seu acesso no gerador; regenerar e comparar as integrações.

**Evidência/impedimentos:** A informar.

## Fase 6 — Percurso e IA

**Objetivo:** fazer os adversários correrem pelo traçado. **Dependências:** cena e percurso utilizáveis. **Entregáveis:** IA configurada e telemetria inicial. **Critério:** eixo real usado, sentido comum e arena legada preservada. **Estado:** Pendente.

- [ ] Criar/verificar `Path3D/Curve3D` fechado ou recurso equivalente do eixo real.
- [ ] Configurar percurso, sentido, personagem, faixa, velocidade e transform antes de `add_child()`/`_ready()`.
- [ ] Antecipar curvas e frear pela geometria e distância disponíveis.
- [ ] Manter perseguição, espaçamento e contorno dentro da largura útil.
- [ ] Testar partida e contorno de jogador parado sem bloqueio indefinido.
- [ ] Medir progresso através do fechamento da volta e conferir ambiguidades de projeção.
- [ ] Confirmar funcionamento da IA circular anterior na arena.

**Evidência/impedimentos:** A informar.

## Fase 7 — Física, controles e personagens

**Objetivo:** conferir dirigibilidade e preservar os pilotos. **Dependências:** cena/IA funcionando. **Entregáveis:** ensaios e regressões em pasta própria. **Critério:** regras obrigatórias passam ou falhas ficam explicitadas como parcial. **Estado:** Pendente.

- [ ] Testar aceleração, frenagem, ré e direção para ambos os lados na física real.
- [ ] Testar subida/descida das zebras, saída ao terreno e retorno ao asfalto.
- [ ] Medir contato dos pneus, método e tolerância; verificar penetração/flutuação.
- [ ] Testar colisões entre karts, sinais, impulso e efeitos pertinentes.
- [ ] Exercitar todos os pilotos cadastrados, incluindo seleção e uso na pista.
- [ ] Executar regressões de rodas, suspensão, cabeça e câmera sem regravar relatórios históricos.
- [ ] Revalidar mecânicas/arena afetadas por alterações compartilhadas.

**Evidência/impedimentos:** A informar.

## Fase 8 — Voltas completas e conferência visual

**Objetivo:** comprovar a corrida e a aparência no motor. **Dependências:** física e IA estabilizadas. **Entregáveis:** telemetria, logs, imagens e inspeção registrada. **Critério:** cada adversário completa pelo menos uma volta, e imagens reais são conferidas. **Estado:** Pendente.

- [ ] Abrir o jogo com renderização real e inspecionar menu, largada, materiais e escala.
- [ ] Conferir câmera e pneus dos personagens em capturas identificadas.
- [ ] Executar cada IA por uma volta completa sem teletransporte durante a medição.
- [ ] Registrar participantes, tempo, progresso, desvio, contramão, saídas, colisões e recuperações.
- [ ] Definir o critério de saída e registrar suas limitações geométricas.
- [ ] Repetir cenários pertinentes com os pilotos cadastrados e jogador parado no grid.
- [ ] Separar Input automatizado, pilotagem manual, teste headless e conferência visual.
- [ ] Corrigir falhas obrigatórias e repetir os ensaios afetados, preservando tentativas anteriores.

**Evidência/impedimentos:** A informar.

## Fase 9 — Entrega e documentação

**Objetivo:** entregar a pista reproduzível e pronta para retomada. **Dependências:** fases autorizadas executadas. **Entregáveis:** ficha/checklist/checkpoint atualizados e relatório final. **Critério:** conclusão compatível com evidências, limitações e escopo. **Estado:** Pendente.

- [ ] Consolidar arquivos, versões, comandos e resultados realmente observados.
- [ ] Registrar acesso no menu, cena, controles, testes e imagens inspecionadas.
- [ ] Conferir preservação de referências, fontes, personagens, pistas e relatórios anteriores.
- [ ] Registrar hipóteses provisórias, falhas remanescentes e validações a refazer.
- [ ] Atualizar ficha, este checklist, checkpoint e índice com links existentes.
- [ ] Informar próximo passo e eventual etapa bloqueada; registrar commit/publicação somente se solicitado e realizado.

**Evidência/impedimentos:** A informar.
