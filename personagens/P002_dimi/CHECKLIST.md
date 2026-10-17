# Checklist — P002 — Dimi

| Campo | Valor |
| --- | --- |
| Personagem | Dimi (`personagens/P002_dimi/`) |
| Data | 15/10/2026 |
| Receita | [RECEITA_PERSONAGEM.md](../../documentacao/RECEITA_PERSONAGEM.md) |
| Versão da receita consultada | Último commit que a altera: `2594727`; HEAD `8472837` na criação e `326a962` na Fase 7; com alterações locais não commitadas em `RECEITA_PERSONAGEM.md` e `PROMPT_NOVO_PERSONAGEM.md` |
| Fase atual | Todas as fases concluídas (Fase 9 em 15/10/2026) |
| Próximo passo | Nenhuma fase pendente; commit quando solicitado e pendências da [entrega](registros/registro-fase9-entrega-2026-10-15.md#5-pendências-que-continuam-abertas) |
| Pendências | Base da cabeça aberta: limitar o giro (escolha do usuário); de lado e de frente aparece a partir de ~10°, na câmera do jogo fica escondida até ±25° ([registro](registros/registro-fase6-amplitude-2026-10-15.md)); teto de 25° aplicado à inclinação da cabeça, que não foi medida na Fase 6 — [registro da Fase 8](registros/registro-fase8-jogavel-2026-10-15.md) |

Legenda: `[ ]` pendente; `[x]` concluída com evidência.

## Fase 0 — Identificação e organização

- **Objetivo:** reservar o identificador e criar a estrutura documental.
- **Dependências:** nome informado pelo usuário.
- **Entregáveis:** pastas, `LEIA-ME.md`, `CHECKLIST.md`, `CHECKPOINT.md`, `referencia/LEIA-ME.md`, entrada no índice.
- **Critério de conclusão:** arquivos criados e referências solicitadas.
- **Estado:** Concluída.

- [x] Confirmar o nome de exibição e reservar o identificador único. — "Dimi", P002.
- [x] Criar as pastas e a ficha `LEIA-ME.md`.
- [x] Criar este checklist e o guia de referências.
- [x] Criar `CHECKPOINT.md` com o estado inicial e o próximo passo.
- [x] Criar ou retomar o projeto exclusivo em `blender/dimi.blend`, preservando projetos e referências existentes. — criado em 15/10/2026 (item acrescentado pela receita após a inicialização), já com o GLB importado.
- [x] Conferir o arquivo `.blend` salvo e registrar se está vazio ou com modelo carregado. — modelo carregado; ver [conferência](registros/conferencia-blend-inicial-2026-10-15.json).
- [x] Registrar o personagem no índice da documentação.
- [x] Solicitar as referências e informar o caminho da pasta.

## Fase 1 — Referências e escopo

- **Objetivo:** reunir as entradas e definir o que será entregue.
- **Dependências:** arquivos enviados pelo usuário.
- **Entregáveis:** inventário em `referencia/LEIA-ME.md`; escopo e arquivo de entrada na ficha.
- **Critério de conclusão:** entrada identificada (ou plano para obtê-la), partes independentes e objetivo definidos.
- **Estado:** Concluída.

- [x] Receber, inventariar e conferir os arquivos de referência acessíveis. — `Dimi.glb` e `Dimi.png`, com hashes no [inventário](referencia/LEIA-ME.md).
- [x] Identificar o modelo 3D de entrada ou registrar que ele ainda não existe. — `referencia/Dimi.glb`.
- [x] Preparar e conferir uma cópia do modelo no `.blend` exclusivo quando o arquivo de entrada estiver disponível. — `blender/dimi.blend`, aberto e conferido em instância isolada.
- [x] Definir aparência, veículo/acessórios, partes independentes e objetivo de entrega. — Escopo padrão confirmado pelo usuário em 15/10/2026: piloto jogável; `Cabeca` (com pescoço), `Corpo_Kart` e 4 `Wheel_*`; rig `Root → Torso → Neck → Head`. Móbile, mamadeira, molas e grades ficam fixos no `Corpo_Kart`.
- [x] Se houver apenas imagens, planejar a obtenção ou criação da malha antes do rig; não considerar uma imagem como modelo pronto. — Não se aplica: há modelo 3D.
- [x] Registrar lacunas, dependências e o arquivo de entrada escolhido na ficha.

## Fase 2 — Inspeção e preservação da entrada

- **Objetivo:** conhecer e preservar o modelo antes de editá-lo.
- **Dependências:** Fase 1; Blender com MCP conectado.
- **Entregáveis:** backup em `backups/`; dados de referência para comparação.
- **Critério de conclusão:** backup salvo e atributos originais registrados.
- **Estado:** Concluída — [registro](registros/registro-fase2-inspecao-2026-10-15.md).

- [x] Inspecionar o modelo e conferir orientação, escala e partes existentes. — Blender 5.2.2 pela CLI em segundo plano (sessão MCP não usada); frente −Y, esquerda do piloto +X, Z para cima; escala compatível com o Jake; [vistas](registros/vistas_fase2/).
- [x] Confirmar que o arquivo de trabalho é o `.blend` exclusivo deste personagem e contém a entrada correta.
- [x] Levantar malhas, ilhas, pais, materiais, UVs, normais, modificadores, shape keys, grupos e animações. — [inspeção](validacao/inspecao_malha_original.json): 1 malha, 1.040 ilhas, normais personalizadas, sem modificadores/grupos/shape keys/ações.
- [x] Salvar uma cópia anterior à edição em `backups/`. — `dimi_antes_da_edicao_20261015_160718.blend`.
- [x] Registrar contagens, coordenadas, conectividade e atributos necessários à comparação. — `backups/geometria_original.npz`.
- [x] Definir identificadores de rastreamento e tolerâncias para a validação. — `rig_original_*` no `dimi.blend`; tolerâncias no registro; [verificação](validacao/verificacao_preservacao_fase2.json) sem diferenças.

## Fase 3 — Separação das partes

- **Objetivo:** separar cabeça, corpo, veículo e acessórios sem alterar a geometria.
- **Dependências:** Fase 2.
- **Entregáveis:** objetos separados com nomes padronizados.
- **Critério de conclusão:** partes conferidas isoladas e reunidas, sem fragmentos perdidos.
- **Estado:** Concluída — [registro](registros/registro-fase3-separacao-2026-10-15.md) e [verificação](validacao/verificacao_separacao_fase3.json) (`tudo_ok: true`).

- [x] Identificar cabeça, corpo, veículo e acessórios com base neste modelo. — critérios próprios por ilha em [`rotulos_partes.py`](registros/scripts_fase3/rotulos_partes.py), conferidos por vistas e pela cor da textura.
- [x] Separar a cabeça completa e seus detalhes por partes existentes, preservando a geometria. — `Cabeca`: 83 ilhas (boné, rosto, cabelo, orelhas, chupeta, pele do pescoço); gola e móbile ficam no corpo.
- [x] Definir e realizar a separação entre personagem e veículo quando exigida pela entrega. — Escopo padrão: corpo e kart ficam unidos em `Corpo_Kart` (781 ilhas, com móbile, mamadeira, molas e grades).
- [x] Identificar e separar as quatro rodas em objetos com malhas exclusivas, se houver kart. — pneu, aro, bolinhas e cubo; para-lamas e eixos ficam no corpo.
- [x] Padronizar nomes (`Cabeca`, `Corpo_Kart`, `Wheel_*`) e conferir frente, traseira, esquerda e direita do piloto. — lados conferidos (frente −Y, esquerda +X).
- [x] Conferir as partes isoladas e reunidas; registrar impedimentos e tentativas desfeitas. — cada elemento original exatamente uma vez, desvio 0,0; [vistas](registros/vistas_fase3/); normais recodificadas e texturas órfãs corrigidas (ver registro, seção 6).

Não reutilize limites de coordenadas ou índices de ilhas do Jake. Se preservar a topologia for incompatível com o corte necessário, registre o impedimento e resolva o escopo antes de alterar a geometria.

## Fase 4 — Pivôs, esqueleto e pesos

- **Objetivo:** criar controles rígidos com pivôs corretos.
- **Dependências:** Fase 3.
- **Entregáveis:** armature, pesos, parentesco e modificadores.
- **Critério de conclusão:** pivôs medidos e pesos exclusivos, sem vazamento.
- **Estado:** Concluída — [registro](registros/registro-fase4-rig-2026-10-15.md) e [verificação](validacao/verificacao_rig_fase4.json) (`tudo_ok: true`, no arquivo recarregado do disco).

- [x] Medir e posicionar o pivô da cabeça na base do pescoço deste personagem. — `(0, −0.010498, 0.4453125)`: centro do toco do pescoço em Y, plano em que a gola fecha em Z; [medidas](validacao/medidas_pivos_fase4.json).
- [x] Medir os centros das rodas e registrar o critério geométrico adotado, quando aplicável. — círculo ajustado ao contorno externo da banda de rodagem, sem os picos das bolinhas (raio ≈ 0,1297, eixo Z ≈ 0,128); a caixa delimitadora foi descartada (registro, seção 5).
- [x] Criar `Personagem_Rig` com a hierarquia padrão `Root_Bone → Torso_Bone → Neck_Bone → Head_Bone`. — Y local de `Head_Bone` = Z mundial.
- [x] Atribuir pesos rígidos exclusivos às partes que devem permanecer rígidas. — `Cabeca` → `Head_Bone` e `Corpo_Kart` → `Torso_Bone`, peso 1,0 em todos os vértices.
- [x] Definir o parentesco e os modificadores necessários, compensando as transformações. — malhas filhas do rig com o modificador `Rig_Rigido_Sem_Deformacao`; rodas com parentesco de osso em `Torso_Bone`, sem modificador.
- [x] Conferir ausência de vazamento de pesos, pivôs deslocados e influência duplicada. — desvio mundial ≤ 6e-8 m; testes temporários na cabeça (Y ±, Z, X), no torso, na raiz e nas rodas, com pivô fixo e partes fixas paradas, todos restaurados; [vistas](registros/vistas_fase4/). A borda da base aberta aparece de lado a −40° (limitação registrada).

## Fase 5 — Validação da preparação

- **Objetivo:** comprovar a preservação e o funcionamento dos controles.
- **Dependências:** Fase 4.
- **Entregáveis:** relatório em `validacao/`, registro em `registros/`, `.blend` salvo.
- **Critério de conclusão:** medições dentro das tolerâncias e arquivo em disco conferido.
- **Estado:** Concluída — [registro](registros/registro-fase5-validacao-2026-10-15.md), [validação](validacao/validacao_preparacao_fase5.json) e [repetição do rig](validacao/verificacao_rig_fase5.json) (ambos `tudo_ok: true`).

- [x] Comparar presença, contagens, conectividade, coordenadas, UVs, materiais e normais com a referência. — cada elemento original uma vez (995.477 v / 2.875.792 a / 1.881.354 f / 5.644.062 cantos); arestas, cantos, faces, UV, suavização e materiais idênticos ao NPZ; `custom_normal`/`sharp_*` e texturas empacotadas idênticos ao backup pré-Fase 3.
- [x] Medir a preservação no espaço apropriado e registrar arredondamentos numéricos. — espaço mundial, malha-base e avaliada: desvio ≤ 5.96e-8 m; normais decodificadas ≤ 9.3e-4 por componente (registro, seções 4 e 5).
- [x] Testar temporariamente os controles da cabeça, corpo e rodas, quando aplicável. — testes da Fase 4 repetidos e teste combinado novo (raiz + torso + cabeça + rodas), erro rígido ≤ 1.3e-7.
- [x] Confirmar isolamento entre partes e estabilidade dos pivôs; restaurar os testes. — pivôs sem deslocamento, partes fixas paradas, posição final idêntica à de repouso.
- [x] Salvar relatório em `validacao/` e registro detalhado em `registros/`.
- [x] Salvar e conferir o `.blend` gravado, distinguindo cena aberta de arquivo em disco. — o arquivo não foi alterado; sessão recarregada do disco (`is_dirty: false`) e SHA-256 `229034cf…25a7d7` igual ao da Fase 4.

## Fase 6 — Animações da cabeça

- **Objetivo:** criar as ações de olhar para a direita e para a esquerda.
- **Dependências:** Fase 5.
- **Entregáveis:** ações nomeadas, relatório de validação e registro.
- **Critério de conclusão:** keyframes conferidos, corpo preservado, pivô estável, arquivo salvo.
- **Estado:** Concluída — [amplitude](registros/registro-fase6-amplitude-2026-10-15.md), [ações](registros/registro-fase6-acoes-cabeca-2026-10-15.md) e [validação](validacao/validacao_acoes_cabeca_fase6.json) (`tudo_ok: true`, no arquivo recarregado do disco).

- [x] Definir eixo, sentidos, amplitude, duração e FPS para este personagem. — Y local de `Head_Bone` (positivo = rosto para a esquerda do piloto, +X); 25° confirmado pelo usuário (limite pela base aberta); 2 s a 24 FPS, quadros 1/25/49.
- [x] Criar a ação de olhar para a direita e retornar à posição original. — `Cabeca_Direita_Ida_e_Volta`: 0° → −25° → 0°.
- [x] Criar a ação para a esquerda preservando a ação anterior. — `Cabeca_Esquerda_Ida_e_Volta`: 0° → +25° → 0°; as duas com `use_fake_user`; espelhamento exato.
- [x] Conferir keyframes, alças, interpolação e quadros intermediários. — `BEZIER`/`AUTO_CLAMPED`/`CONSTANT`, alças dos extremos horizontais, 481 amostras dentro de 0…±25°, ida e volta monótonas.
- [x] Medir preservação do corpo, rigidez da cabeça e estabilidade do pivô. — pivô e partes fixas sem movimento nos 49 quadros; cabeça rígida ≤ 5.96e-8; preparação e rig revalidados no arquivo salvo.
- [x] Registrar ações, intervalos de prévia, FPS, testes e estado salvo. — prévia 1–49, intervalo 1–250, `Direita` ativa no quadro 1; SHA-256 `e28bf878…49e1`.

## Fase 7 — Exportação e importação na Godot

- **Objetivo:** levar o personagem para o projeto `jogo/`.
- **Dependências:** Fases 5 e 6; projeto Godot (já existe em `jogo/`).
- **Entregáveis:** exportação em `jogo/personagens/dimi/` e registro de importação.
- **Critério de conclusão:** recurso importado inspecionado pela CLI, estrutura e pivôs conferidos.
- **Estado:** Concluída — [registro](registros/registro-fase7-exportacao-godot-2026-10-15.md), [exportação](validacao/exportacao_glb_fase7.json) e [inspeção na Godot](validacao/importacao_godot_fase7.json) (`tudo_ok: true`).

- [x] Definir o formato de exportação e quais ações/poses devem ser exportadas. — GLB como o Jake, pose de repouso (quadro 1), com as duas ações da cabeça (começando em 0 s; `AnimationPlayer` sem autoplay).
- [x] Conferir materiais, texturas, escala, orientação, nomes, ossos e partes independentes. — no GLB: nomes e hierarquia iguais aos do Jake, triângulos iguais ao Blender, imagens embutidas idênticas byte a byte às empacotadas, Y para cima e frente +Z.
- [x] Exportar para `jogo/personagens/dimi/`. — `dimi_kart.glb`, SHA-256 `2b25281b…e606258b`, exportado da sessão MCP com `dimi.blend` recarregado do disco (`e28bf878…49e1`, não alterado).
- [x] Importar e inspecionar o recurso real na Godot pela CLI. — Godot 4.7.2 `--headless --import`; texturas ajustadas para VRAM como as do Jake; `animation/fps=24` e otimizador desligado no nó `AnimationPlayer` para manter as 49 chaves (o padrão perdia o pico de 25°).
- [x] Verificar novamente a estrutura e os pivôs após a importação. — [`inspecionar_importacao_dimi.gd`](../../jogo/ferramentas/inspecionar_importacao_dimi.gd): ossos ≤ 2,98e-8 m e rodas ≤ 6,7e-8 m do Blender; animações 0 → ∓25° → 0 exatas; `VisualKart.montar()` encontra ossos e rodas (ficha só em memória).
- [x] Registrar o artefato exportado e as diferenças em relação ao Blender. — vértices divididos nas costuras, interpolação linear a 24 FPS e raio das rodas pela caixa (registro, seção 6). Aparência na Godot não conferida visualmente.

## Fase 8 — Personagem jogável e mecânicas

- **Objetivo:** tornar Dimi selecionável e validar as mecânicas no jogo.
- **Dependências:** Fase 7.
- **Entregáveis:** ficha de piloto no catálogo, registro e relatório de testes.
- **Critério de conclusão:** mecânicas medidas no novo personagem, com falhas registradas.
- **Estado:** Concluída. A falha registrada (cabeça não oposta em todo quadro) foi corrigida depois pela [T001](../../jogo/tarefas/T001-cabeca-sempre-oposta.md) ([relatório](validacao/validacao_mecanicas_t001.json): `cabeca_sempre_oposta: true`) — [registro](registros/registro-fase8-jogavel-2026-10-15.md), [relatório](validacao/validacao_mecanicas_fase8.json) e [vistas](registros/vistas_fase8/).

- [x] Criar a ficha do novo piloto e integrá-lo ao catálogo sem substituir os existentes. — [`dimi.tres`](../../jogo/personagens/dimi/dimi.tres) (`escala 2.0`, `raio_rodas 0.1297`, `giro_maximo_cabeca 25`); catálogo `["Jake", "Dimi"]`. Campos novos e opcionais em `definicao_personagem.gd`/`visual_kart.gd`; com zero, o Jake segue igual (regressão: rodas, curvas e vibração idênticas ao relatório dele).
- [x] Testar a escolha entre o novo personagem e pelo menos um piloto já cadastrado (Jake). — Jake → ▶ Dimi → ▶ Jake → ◀ Dimi; “Jogar” carrega `dimi_kart.glb` na pista.
- [x] Testar movimento, frenagem, ré e direção no cenário quadriculado. — 24 m em 2 s, 22 m/s; de 22 m/s a 0 em 0,80 s; ré −8 m/s (12 m para trás); giro ±1,43 rad/s.
- [x] Testar a câmera atrás do personagem, acompanhamento e resposta dinâmica. — atrás (+4,47), FOV 68° → 82°, até 19,8° de atraso na curva, rolagem de imagem −2,1°; vistas renderizadas.
- [x] Verificar giro das quatro rodas, ré, parada e esterço dianteiro, se houver kart. — raio 0,1297 nas quatro, giro, ré, parada e ±28° corretos; bandas exatamente no chão; pivôs sem deriva.
- [x] Verificar suspensão e vibração nos dois sentidos de curva, quando aplicável. — ±6,88° estabilizado (até 14° a 22 m/s), sempre para fora da curva; vibração ativa.
- [x] Medir a inclinação global da cabeça, considerando o movimento herdado do corpo. — oposta estabilizada: ∓4,81° global contra ±6,88° do corpo; relativa máxima de 25,0° com o teto (32,74° sem ele).
- [x] Verificar compensação em entrada, inversão e saída de curva, parada e tremor. — 18 / 15 / 16 / 0 quadros no mesmo lado (60 passos/s, sem ruído); reta com vibração, 84 de 120.
- [x] Distinguir compensação estabilizada de oposição em todo quadro; se o requisito for “sempre”, tratar violações transitórias como falhas. — estabilizada: passa; “sempre”: **falhou** na Fase 8 (`cabeca_sempre_oposta: false`) e passou depois da T001 (0 quadros no mesmo lado).
- [x] Registrar testes no motor, inspeção visual e limitações separadamente. — registro, seções 4, 5 e 7.

A auditoria do Jake encontrou atraso de mola e tremor não compensado. Reutilizar o código dele não comprova que essas regras passaram neste personagem. **Confirmado no Dimi:** sem ruído, os mesmos 18 e 15 quadros do Jake.

## Fase 9 — Entrega e documentação

- **Objetivo:** fechar a entrega com documentação consistente.
- **Dependências:** fases anteriores aplicáveis.
- **Entregáveis:** ficha, checklist e checkpoint atualizados; links válidos.
- **Critério de conclusão:** critérios de cada fase conferidos e pendências registradas.
- **Estado:** Concluída — [registro](registros/registro-fase9-entrega-2026-10-15.md).

- [x] Atualizar ficha, histórico e checklist com os resultados efetivamente obtidos. — P002.12; índice `documentacao/README.md` corrigido (dizia “próxima: Fase 7”).
- [x] Vincular modelos, backups, exportações, relatórios e registros com caminhos relativos válidos. — 217 links conferidos por script, nenhum quebrado.
- [x] Conferir critérios de conclusão de cada fase e registrar pendências restantes. — registro, seções 4 e 5; hashes iguais e verificadores da Godot repetidos com resultado idêntico.
- [x] Resumir controles, limitações e instruções para reproduzir as verificações. — [resumo da entrega](LEIA-ME.md#resumo-da-entrega).
- [x] Registrar eventual commit ou publicação somente quando solicitado e realizado. — não solicitado; nenhum commit.

Preserve os resultados históricos e seus hashes. Um teste de uma versão anterior não valida automaticamente o artefato modificado.
