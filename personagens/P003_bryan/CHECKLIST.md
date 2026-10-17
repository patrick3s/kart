# Checklist — P003 — Bryan

| Campo | Valor |
| --- | --- |
| Personagem | P003 — Bryan (`personagens/P003_bryan/`) |
| Data de criação | 15/10/2026 |
| Receita | [RECEITA_PERSONAGEM.md](../../documentacao/RECEITA_PERSONAGEM.md) |
| Versão da receita consultada | Commit `5340930` (último que alterou a receita); HEAD `5d1dd29`; sem alterações locais |
| Fase atual | Todas as fases concluídas (Fase 9 em 16/10/2026) |
| Próximo passo | Nenhuma fase pendente; commit quando solicitado e pendências da [entrega](registros/registro-fase9-entrega-2026-10-16.md#5-pendências-que-continuam-abertas) |
| Pendências | Topo das rodas: **aceito** pelo usuário (16/10). Nuca: amplitude limitada a **25°** (usuário, 16/10), aceitando fragmentos pequenos de perto e com a câmera atrasada 30°; aplicado em `giro_maximo_cabeca` na Fase 8. Raio único nas rodas: traseiras até 0,98 mm (modelo) acima do chão. Verificador do Dimi reprova catálogo e troca com três pilotos (mecânicas dele intactas) |

Legenda: `[ ]` pendente, `[x]` concluída com evidência. Estados: `Pendente`, `Em andamento`, `Aguardando referências`, `Bloqueada`, `Concluída`, `Não se aplica`.

## Fase 0 — Identificação e organização

- **Objetivo:** reservar o identificador, organizar a pasta e criar o projeto Blender exclusivo.
- **Dependências:** nome informado pelo usuário; Blender MCP conectado para o `.blend`.
- **Entregáveis:** pastas, `LEIA-ME.md`, `CHECKLIST.md`, `CHECKPOINT.md`, `referencia/LEIA-ME.md`, `blender/bryan.blend`, entrada no índice.
- **Critério de conclusão:** todos os documentos existem e o `.blend` foi salvo e recarregado na sessão aberta.
- **Estado:** Concluída.

- [x] Confirmar o nome de exibição e reservar o identificador único. (“Bryan” → `P003_bryan`; maior existente era P002)
- [x] Criar as pastas e a ficha `LEIA-ME.md`.
- [x] Criar este checklist e o guia de referências.
- [x] Criar `CHECKPOINT.md` com o estado inicial e o próximo passo.
- [x] Criar ou retomar o projeto exclusivo em `blender/bryan.blend`, preservando projetos e referências existentes. (Cena vazia salva pelo Blender MCP; a sessão só tinha a cena padrão sem caminho)
- [x] Conferir o arquivo `.blend` salvo e registrar se está vazio ou com modelo carregado. (Recarregado do disco: vazio, 84.706 bytes; [conferência](registros/conferencia-blend-inicial-2026-10-15.json))
- [x] Registrar o personagem no índice da documentação.
- [x] Solicitar as referências e informar o caminho da pasta.

## Fase 1 — Referências e escopo

- **Objetivo:** receber e inventariar as referências e definir o modelo de entrada.
- **Dependências:** arquivos do usuário; `.blend` já criado na Fase 0.
- **Entregáveis:** inventário em `referencia/LEIA-ME.md`; modelo de entrada registrado na ficha; cópia no `.blend`.
- **Critério de conclusão:** inventário conferido, modelo de entrada escolhido (ou ausência registrada) e escopo padrão confirmado ou divergências registradas.
- **Estado:** Concluída.

- [x] Receber, inventariar e conferir os arquivos de referência acessíveis. (`bryan.glb` e `bryan.png`; [inventário](referencia/LEIA-ME.md))
- [x] Identificar o modelo 3D de entrada ou registrar que ele ainda não existe. (`referencia/bryan.glb`)
- [x] Preparar e conferir uma cópia do modelo no `.blend` exclusivo quando o arquivo de entrada estiver disponível. ([conferência](registros/conferencia-blend-modelo-2026-10-15.json): contagens iguais ao GLB, texturas empacotadas)
- [x] Registrar aparência e acessórios e confirmar que o modelo tem as partes do escopo padrão (cabeça/pescoço, corpo, kart e quatro rodas); registrar divergências. (Vistas da Fase 2: escopo presente, sem divergência; [registro](registros/registro-fase2-inspecao-2026-10-15.md))
- [ ] ~~Se houver apenas imagens, planejar a obtenção ou criação da malha antes do rig~~ — não se aplica: existe modelo 3D.
- [x] Registrar lacunas, dependências e o arquivo de entrada escolhido na ficha.

## Fase 2 — Inspeção e preservação da entrada

- **Objetivo:** conhecer o modelo e guardar o estado original para comparação.
- **Dependências:** Fase 1 concluída; modelo carregado em `blender/bryan.blend`.
- **Entregáveis:** backup em `backups/`, dados originais de geometria, relatório de inspeção em `validacao/`, registro em `registros/`.
- **Critério de conclusão:** backup salvo e conferido; contagens, atributos e tolerâncias registrados.
- **Estado:** Concluída.

- [x] Inspecionar o modelo no Blender MCP e conferir orientação, escala e partes existentes. (Frente −Y, esquerda do piloto +X, Z para cima; 0,66 × 0,98 × 0,77 m; [vistas](registros/vistas_fase2/))
- [x] Confirmar que o arquivo de trabalho é o `.blend` exclusivo deste personagem e contém a entrada correta. (Sessão com `blender/bryan.blend`, hash igual ao checkpoint, 1 malha do GLB)
- [x] Levantar malhas, ilhas, pais, materiais, UVs, normais, modificadores, shape keys, grupos e animações. (1.170 ilhas, 1 material, 1 UV, normais personalizadas, sem modificadores/grupos/shape keys/ações; [inspeção](validacao/inspecao_malha_original.json))
- [x] Salvar uma cópia anterior à edição em `backups/`. ([`bryan_antes_da_edicao_20261015_191749.blend`](backups/bryan_antes_da_edicao_20261015_191749.blend), SHA-256 igual ao original)
- [x] Registrar contagens, coordenadas, conectividade e atributos necessários à comparação. ([`geometria_original.npz`](backups/geometria_original.npz); [verificação](validacao/verificacao_preservacao_fase2.json) com tudo igual)
- [x] Definir identificadores de rastreamento e tolerâncias para a validação. (`rig_original_vertex/edge/face/corner`; tolerâncias no [registro](registros/registro-fase2-inspecao-2026-10-15.md#8-tolerâncias-definidas-para-as-próximas-validações))

## Fase 3 — Separação das partes

- **Objetivo:** obter `Cabeca`, `Corpo_Kart` e quatro `Wheel_*` independentes sem alterar a geometria.
- **Dependências:** Fase 2 concluída.
- **Entregáveis:** objetos separados e nomeados; registro da separação; relatório de conferência.
- **Critério de conclusão:** todos os elementos originais presentes exatamente uma vez entre as partes; nomes e lados conferidos.
- **Estado:** Concluída — com desvio da receita autorizado pelo usuário: 42 ilhas em que o pneu estava fundido ao assoalho/vão do para-lama foram divididas pelas arestas existentes (1.730 vértices de costura duplicados; nenhuma face nova).

- [x] Identificar cabeça, corpo, veículo e acessórios com base neste modelo. (Cabeça: 17 ilhas por posição, cor e vistas; gola e rádio no corpo; [registro](registros/registro-fase3-separacao-2026-10-15.md#5-identificação-das-partes))
- [x] Separar a cabeça completa e seus detalhes por partes existentes, preservando a geometria. (17 ilhas inteiras, sem corte nem tampa; base do pescoço aberta)
- [x] Definir e realizar a separação entre personagem e veículo quando exigida pela entrega. (Escopo padrão: piloto e kart juntos em `Corpo_Kart`; só cabeça e rodas são independentes)
- [x] Identificar e separar as quatro rodas em objetos com malhas exclusivas, se houver kart. (Divisão por faces nas arestas existentes, decidida pelo usuário; [diagnóstico](registros/vistas_fase3/diagnostico/))
- [x] Padronizar nomes conforme o escopo padrão (`Cabeca`, `Corpo_Kart`, `Wheel_*`) e conferir frente, traseira, esquerda e direita do piloto. (Nomes padrão; lados conferidos com frente −Y, esquerda +X)
- [x] Conferir as partes isoladas e reunidas; registrar impedimentos e tentativas desfeitas. ([verificação](validacao/verificacao_separacao_fase3.json) `tudo_ok: true`; [vistas](registros/vistas_fase3/); incidentes no registro)

Não reutilize limites de coordenadas ou índices de ilhas do Jake ou do Dimi. Se preservar a topologia for incompatível com o corte necessário, registre o impedimento e resolva o escopo antes de alterar a geometria.

## Fase 4 — Pivôs, esqueleto e pesos

- **Objetivo:** criar `Personagem_Rig` com pivôs medidos e pesos rígidos exclusivos.
- **Dependências:** Fase 3 concluída.
- **Entregáveis:** armature, pivôs da cabeça e das rodas, medidas em `validacao/`, registro da etapa.
- **Critério de conclusão:** hierarquia correta, pivôs no lugar medido, pesos exclusivos sem vazamento.
- **Estado:** Concluída — com limitações visuais registradas (topo das rodas e nuca), sem alteração de geometria.

- [x] Medir e posicionar o pivô da cabeça na base do pescoço deste personagem. (`(−0.0075684, 0.0712891, 0.4941406)`: centro do toco do pescoço, Z na base onde o corpo fecha; [medidas](validacao/medidas_pivos_fase4.json))
- [x] Medir os centros das rodas e registrar o critério geométrico adotado, quando aplicável. (Círculo no contorno externo da banda, só setores limpos da metade de baixo; R ≈ 0,1193–0,1199, resíduo ≈ 0,35 mm; [registro](registros/registro-fase4-rig-2026-10-15.md#5-centros-das-rodas))
- [x] Criar `Personagem_Rig` com a hierarquia padrão `Root_Bone → Torso_Bone → Neck_Bone → Head_Bone`. (Y local de `Head_Bone` = Z mundial)
- [x] Atribuir pesos rígidos exclusivos às partes que devem permanecer rígidas. (`Cabeca` → `Head_Bone`, `Corpo_Kart` → `Torso_Bone`, peso 1,0 em todos os vértices)
- [x] Definir o parentesco e os modificadores necessários, compensando as transformações. (Armature com grupos, sem envelopes; rodas com parentesco de osso em `Torso_Bone`)
- [x] Conferir ausência de vazamento de pesos, pivôs deslocados e influência duplicada. ([verificação](validacao/verificacao_rig_fase4.json) `tudo_ok: true` no arquivo recarregado; [vistas](registros/vistas_fase4/))

## Fase 5 — Validação da preparação

- **Objetivo:** comprovar a preservação da geometria e o isolamento dos controles.
- **Dependências:** Fase 4 concluída.
- **Entregáveis:** relatório em `validacao/`, registro em `registros/`, `.blend` salvo e conferido.
- **Critério de conclusão:** comparações dentro das tolerâncias definidas na Fase 2; testes restaurados.
- **Estado:** Concluída, com a amplitude da nuca pendente de decisão (afeta as Fases 6 e 8; [registro](registros/registro-fase5-validacao-2026-10-16.md#6-nuca-medição-da-amplitude-decisão-limitar)).

- [x] Comparar presença, contagens, conectividade, coordenadas, UVs, materiais e normais com a referência. ([comparação](validacao/comparacao_preparacao_fase5.json) `tudo_ok: true`: faces e cantos uma vez, divisão da Fase 3 intacta, UV, materiais e `sharp_*` iguais, normais ≤ 4,5e-4)
- [x] Medir a preservação no espaço apropriado e registrar arredondamentos numéricos. (Mundial em float64: ≤ 3,0e-8 m; arredondamento de float32 pela origem deslocada registrado; `Corpo_Kart` bit a bit igual)
- [x] Testar temporariamente os controles da cabeça, corpo e rodas, quando aplicável. ([verificação](validacao/verificacao_rig_fase5.json) e testes combinados de corpo + cabeça e esterço de 28° + giro)
- [x] Confirmar isolamento entre partes e estabilidade dos pivôs; restaurar os testes. (Partes fixas 0,0; pivôs ≤ 4,5e-8; restaurado 0,0; cena recarregada)
- [x] Salvar relatório em `validacao/` e registro detalhado em `registros/`. ([registro](registros/registro-fase5-validacao-2026-10-16.md))
- [x] Salvar e conferir o `.blend` gravado, distinguindo cena aberta de arquivo em disco. (Sem alterações nesta fase, então não foi salvo de novo; disco com SHA-256 `da58cc33…96c81b77`, igual ao [backup pré-Fase 5](backups/bryan_antes_fase5_20261016_085401.blend) e ao conteúdo da Fase 4; sessão limpa)

## Fase 6 — Animações da cabeça

- **Objetivo:** criar as ações de olhar para a direita e para a esquerda, com ida e volta.
- **Dependências:** Fase 5 concluída.
- **Entregáveis:** ações `Cabeca_Direita_Ida_e_Volta` e `Cabeca_Esquerda_Ida_e_Volta`; relatório e registro.
- **Critério de conclusão:** keyframes conferidos, corpo preservado e pivô estável em todos os quadros.
- **Estado:** Concluída ([registro](registros/registro-fase6-acoes-cabeca-2026-10-16.md)); limitação aceita: fragmentos da nuca visíveis de perto e com a câmera atrasada a 25°.

- [x] Definir eixo, sentidos, amplitude, duração e FPS para este personagem. (Y local de `Head_Bone` = +Z mundial, medido; +25° → rosto para +X = esquerda do piloto; **25°** escolhido pelo usuário; 2 s a 24 FPS, quadros 1/25/49)
- [x] Criar a ação de olhar para a direita e retornar à posição original. (`Cabeca_Direita_Ida_e_Volta`: 0° → −25° → 0°)
- [x] Criar a ação para a esquerda preservando a ação anterior. (`Cabeca_Esquerda_Ida_e_Volta`: 0° → +25° → 0°; as duas com `use_fake_user`; espelhamento exato)
- [x] Conferir keyframes, alças, interpolação e quadros intermediários. (Bézier, `AUTO_CLAMPED`, `CONSTANT`; 481 amostras monótonas, sem ultrapassar; [validação](validacao/validacao_acoes_cabeca_fase6.json) `tudo_ok: true`)
- [x] Medir preservação do corpo, rigidez da cabeça e estabilidade do pivô. (Pivô ≤ 7,5e-9 m nos 49 quadros; cabeça rígida ≤ 6e-8; partes fixas imóveis; [comparação](validacao/comparacao_preparacao_fase6.json) e [rig](validacao/verificacao_rig_fase6.json) `tudo_ok: true` no arquivo recarregado)
- [x] Registrar ações, intervalos de prévia, FPS, testes e estado salvo. ([registro](registros/registro-fase6-acoes-cabeca-2026-10-16.md); prévia 1–49; `bryan.blend` SHA-256 `b25be23b…5fe43c11`; [vistas](registros/vistas_fase6/))

## Fase 7 — Exportação e importação na Godot

- **Objetivo:** levar o personagem ao projeto Godot sem perder estrutura e pivôs.
- **Dependências:** Fase 6 concluída; projeto Godot em `jogo/` (já existe).
- **Entregáveis:** GLB em `jogo/personagens/bryan/`; relatório de exportação e de importação.
- **Critério de conclusão:** recurso importado pela CLI com nomes, ossos, pivôs e partes conferidos.
- **Estado:** Concluída — [registro](registros/registro-fase7-exportacao-godot-2026-10-16.md), [exportação](validacao/exportacao_glb_fase7.json), [conteúdo do GLB](validacao/conteudo_glb_fase7.json) e [inspeção na Godot](validacao/importacao_godot_fase7.json) (`tudo_ok: true`).

- [x] Definir o formato de exportação e quais ações/poses devem ser exportadas. — GLB como o Jake e o Dimi, pose de repouso (quadro 1), com as duas ações da cabeça (começando em 0 s; `AnimationPlayer` sem autoplay).
- [x] Conferir materiais, texturas, escala, orientação, nomes, ossos e partes independentes. — no GLB: nomes e hierarquia iguais aos do Jake e do Dimi; triângulos iguais ao Blender por objeto (total 1.854.601); três imagens embutidas idênticas byte a byte às empacotadas; Y para cima e frente +Z.
- [x] Exportar para `jogo/personagens/bryan/`. — `bryan_kart.glb`, SHA-256 `b51c51a5…48bea9e4`, exportado da sessão MCP; `bryan.blend` não alterado (`b25be23b…`); backup pré-Fase 7 byte a byte.
- [x] Importar e inspecionar o recurso real na Godot pela CLI. — Godot 4.7.2 `--headless --import`; mesmos ajustes do Dimi: texturas em VRAM, `animation/fps=24` e otimizador desligado no `AnimationPlayer` (49 chaves mantidas).
- [x] Verificar novamente a estrutura e os pivôs após a importação. — [`inspecionar_importacao_bryan.gd`](../../jogo/ferramentas/inspecionar_importacao_bryan.gd): ossos ≤ 3,33e-8 m e rodas ≤ 7,03e-8 m do Blender; animações 0 → ∓25° → 0 exatas; `VisualKart.montar()` encontra ossos e rodas (ficha só em memória).
- [x] Registrar o artefato exportado e as diferenças em relação ao Blender. — vértices divididos nas costuras, interpolação linear a 24 FPS e raio das rodas pela caixa 4–6% maior que o medido (registro, seção 6). Aparência na Godot não conferida visualmente.

Não criar a pasta de exportação antes desta fase.

## Fase 8 — Personagem jogável e mecânicas

- **Objetivo:** Bryan jogável no catálogo, com rodas, suspensão e cabeça oposta funcionando.
- **Dependências:** Fase 7 concluída; mecânica da [T001](../../jogo/tarefas/T001-cabeca-sempre-oposta.md).
- **Entregáveis:** ficha `.tres` no catálogo; relatório de mecânicas em `validacao/`; capturas em `registros/`.
- **Critério de conclusão:** todas as regras medidas passam, inclusive oposição da cabeça em todo quadro.
- **Estado:** Concluída — [registro](registros/registro-fase8-jogavel-2026-10-16.md), [relatório](validacao/validacao_mecanicas_fase8.json) (todas as conclusões `true`), [vistas](registros/vistas_fase8/).

- [x] Criar a ficha do novo piloto e integrá-lo ao catálogo sem substituir os existentes (Jake e Dimi). (`jogo/personagens/bryan/bryan.tres`: `raio_rodas = 0.1196`, média da Fase 4; `giro_maximo_cabeca = 25.0`; catálogo `["Jake", "Dimi", "Bryan"]`)
- [x] Testar a escolha entre o novo personagem e pelo menos um piloto já cadastrado. (Jake → Dimi → Bryan → Jake e ◀ Bryan; vitrine e pista com `bryan_kart.glb`)
- [x] Testar movimento, frenagem, ré e direção no cenário quadriculado. (24 m em 2 s, 22 m/s; parada em 0,80 s; ré −8 m/s; giro ±1,43 rad/s)
- [x] Testar a câmera atrás do personagem, acompanhamento e resposta dinâmica. (Atrás do kart; FOV 68° → 82°, 73° em ré; atraso até 19,8° na curva)
- [x] Verificar giro das quatro rodas, ré, parada e esterço dianteiro. (Giro = v/escala/raio; ré cancela; parado não gira; ±28° nas dianteiras; apoio 0 a 0,98 mm do chão)
- [x] Verificar suspensão e vibração nos dois sentidos de curva. (+6,88° / −6,88° estabilizado; nenhum quadro contra o sinal da curva)
- [x] Medir a inclinação global da cabeça, considerando o movimento herdado do corpo. (Global no espaço do esqueleto: −4,81° / +4,81°; percurso −9,32° / +9,54°)
- [x] Verificar compensação em entrada, inversão e saída de curva, parada e tremor. (0 quadros no mesmo lado em todos os trechos)
- [x] Distinguir compensação estabilizada de oposição em todo quadro; o requisito é “sempre”, então violações transitórias são falhas (verificar com rolagem total e faixa de oposição da T001, a 60 e 120 passos/s, com e sem ruído). (0 quadros nos três casos e 0/120 na reta com vibração; teto de 25,0° respeitado)
- [x] Registrar testes no motor, inspeção visual e limitações separadamente. ([registro](registros/registro-fase8-jogavel-2026-10-16.md), seções 4, 5 e 7; regressão do Jake e do Dimi na seção 6)

Reutilizar o código do Jake ou do Dimi não comprova que essas regras passam no Bryan; por isso o verificador rodou com a ficha e o GLB do Bryan.

## Fase 9 — Entrega e documentação

- **Objetivo:** fechar a documentação com resultados reais.
- **Dependências:** Fases 0 a 8.
- **Entregáveis:** ficha, checklist e checkpoint atualizados; registro da entrega.
- **Critério de conclusão:** critérios de cada fase conferidos e pendências registradas.
- **Estado:** Concluída — [registro](registros/registro-fase9-entrega-2026-10-16.md).

- [x] Atualizar ficha, histórico e checklist com os resultados efetivamente obtidos. — P003.10; índice `documentacao/README.md` corrigido (dizia “próxima: Fase 8”).
- [x] Vincular modelos, backups, exportações, relatórios e registros com caminhos relativos válidos. — links conferidos por script antes e depois das atualizações, nenhum quebrado ([registro](registros/registro-fase9-entrega-2026-10-16.md), seções 3 e 8).
- [x] Conferir critérios de conclusão de cada fase e registrar pendências restantes. — registro, seções 4 e 5; hashes iguais, inspeção da Godot idêntica byte a byte e conclusões de mecânica iguais.
- [x] Resumir controles, limitações e instruções para reproduzir as verificações. — [resumo da entrega](LEIA-ME.md#resumo-da-entrega).
- [x] Registrar eventual commit ou publicação somente quando solicitado e realizado. — não solicitado; nenhum commit.

Preserve os resultados históricos e seus hashes. Um teste de uma versão anterior não valida automaticamente o artefato modificado.
