# Checkpoint — P002 — Dimi

| Campo | Estado |
| --- | --- |
| Identificador | P002 |
| Nome de exibição | Dimi |
| Pasta no repositório | `personagens/P002_dimi/` |
| Atualizado em | 15/10/2026 18:13 (-03:00), Fase 9 |
| Estado | **Entregue**: Fases 0 a 9 concluídas e T001 aplicada; hashes conferidos e verificadores da Godot repetidos com resultado idêntico; sem commit |
| Fase atual | Nenhuma: todas as fases concluídas |
| Tarefa atual | Nenhuma em execução |
| Último passo confirmado | Fase 9: [registro de entrega](registros/registro-fase9-entrega-2026-10-15.md); 238 links sem problema |
| Próximo passo | Commit quando solicitado; pendências abertas no registro da Fase 9 (seção 5) |
| Receita consultada | `documentacao/RECEITA_PERSONAGEM.md` e `PROMPT_NOVO_PERSONAGEM.md` com alterações locais não commitadas (HEAD `326a962`) |

## Objetivo e escopo

Escopo padrão confirmado pelo usuário em 15/10/2026: **piloto jogável** com `Cabeca` (inclui o pescoço), `Corpo_Kart` e as quatro rodas `Wheel_Front_Left/Right` e `Wheel_Rear_Left/Right`; rig `Personagem_Rig` com `Root_Bone → Torso_Bone → Neck_Bone → Head_Bone`. Móbile, mamadeira, molas e grades ficam fixos no `Corpo_Kart`. Na Fase 6 o usuário confirmou 25° e 2 s a 24 FPS, depois de escolher limitar o giro em vez de tampar a base da cabeça. Pedidos seguintes: “inicie a fase 8 do dimi”, a correção da T001 e “inicie a fase 9 do dimi” (o último).

## Arquivos e evidências

| Item | Caminho relativo ao checkpoint | Estado ou evidência |
| --- | --- | --- |
| Ficha | [`LEIA-ME.md`](LEIA-ME.md) | Atualizada (P002.12), com o resumo da entrega |
| Checklist | [`CHECKLIST.md`](CHECKLIST.md) | Fases 0 a 9 concluídas |
| Modelo de entrada | [`referencia/Dimi.glb`](referencia/Dimi.glb) | Original preservado |
| Arquivo de trabalho | [`blender/dimi.blend`](blender/dimi.blend) | 109.893.929 bytes, SHA-256 `e28bf87840fa0f2c5a42f486e7727d8aca15606e11ab7ebb1927cd647cd649e1`; salvo na Fase 6 com as duas ações (`Direita` ativa, quadro 1) |
| Backup pré-Fase 6 | [`backups/dimi_antes_fase6_20261015_172956.blend`](backups/dimi_antes_fase6_20261015_172956.blend) | SHA-256 `229034cf…25a7d7` (arquivo das Fases 4 e 5) |
| Backup pré-Fase 4 | [`backups/dimi_antes_fase4_20261015_163922.blend`](backups/dimi_antes_fase4_20261015_163922.blend) | SHA-256 `edac92bf…1170d` (arquivo da Fase 3) |
| Backup pré-Fase 3 | [`backups/dimi_antes_fase3_20261015_162824.blend`](backups/dimi_antes_fase3_20261015_162824.blend) | SHA-256 `c537c908…8da756e` |
| Backup anterior à edição | [`backups/dimi_antes_da_edicao_20261015_160718.blend`](backups/dimi_antes_da_edicao_20261015_160718.blend) | SHA-256 `9befa956…0825bfd8` |
| Arrays originais | [`backups/geometria_original.npz`](backups/geometria_original.npz) | Referência das comparações |
| Registro da Fase 4 | [`registros/registro-fase4-rig-2026-10-15.md`](registros/registro-fase4-rig-2026-10-15.md) | Critérios, ossos, pesos, testes e limitações |
| Medidas dos pivôs | [`validacao/medidas_pivos_fase4.json`](validacao/medidas_pivos_fase4.json) | Pivô da cabeça e ajustes das rodas |
| Verificação | [`validacao/verificacao_rig_fase4.json`](validacao/verificacao_rig_fase4.json) | `tudo_ok: true`; desvio mundial ≤ 6e-8 m; testes restaurados |
| Vistas | [`registros/vistas_fase4/`](registros/vistas_fase4/) | Cabeça girada/inclinada, rodas esterçadas (válidas: mesmo arquivo) |
| Registro da Fase 5 | [`registros/registro-fase5-validacao-2026-10-15.md`](registros/registro-fase5-validacao-2026-10-15.md) | Verificações, números, testes e o que não foi testado |
| Validação da preparação | [`validacao/validacao_preparacao_fase5.json`](validacao/validacao_preparacao_fase5.json) | `tudo_ok: true`; SHA-256 `7a22e16b…e5ddc5` |
| Repetição do rig | [`validacao/verificacao_rig_fase5.json`](validacao/verificacao_rig_fase5.json) | `tudo_ok: true`; mesmos valores da Fase 4 |
| Amplitude da cabeça (Fase 6) | [`registros/registro-fase6-amplitude-2026-10-15.md`](registros/registro-fase6-amplitude-2026-10-15.md), [`validacao/amplitude_cabeca_fase6.json`](validacao/amplitude_cabeca_fase6.json), [`registros/vistas_fase6/`](registros/vistas_fase6/) | Amplitude escolhida: 25° |
| Ações da cabeça (Fase 6) | [`registros/registro-fase6-acoes-cabeca-2026-10-15.md`](registros/registro-fase6-acoes-cabeca-2026-10-15.md), [`validacao/validacao_acoes_cabeca_fase6.json`](validacao/validacao_acoes_cabeca_fase6.json), [`registros/vistas_fase6/acoes/`](registros/vistas_fase6/acoes/) | `tudo_ok: true`; preparação e rig revalidados em `validacao/*_fase6.json` |
| Exportação para o jogo | [`../../jogo/personagens/dimi/dimi_kart.glb`](../../jogo/personagens/dimi/dimi_kart.glb) | 76.802.648 bytes, SHA-256 `2b25281baee6a9bd1f123267bd2a3278ba426a2c2a177a725d4cb8e7e606258b`; texturas extraídas pela Godot na mesma pasta |
| Registro da Fase 7 | [`registros/registro-fase7-exportacao-godot-2026-10-15.md`](registros/registro-fase7-exportacao-godot-2026-10-15.md) | Decisões, ajustes de importação, inspeção e diferenças |
| Exportação e inspeção | [`validacao/exportacao_glb_fase7.json`](validacao/exportacao_glb_fase7.json), [`validacao/importacao_godot_fase7.json`](validacao/importacao_godot_fase7.json) | Opções e hash; `tudo_ok: true` na Godot |
| Ficha do piloto | [`../../jogo/personagens/dimi/dimi.tres`](../../jogo/personagens/dimi/dimi.tres) | SHA-256 `f68edad8…3f400`; `escala 2.0`, `raio_rodas 0.1297`, `giro_maximo_cabeca 25.0` |
| Registro da Fase 8 | [`registros/registro-fase8-jogavel-2026-10-15.md`](registros/registro-fase8-jogavel-2026-10-15.md) | Alterações no jogo, resultados, inspeção visual, regressão do Jake e limitações |
| Mecânicas após a T001 | [`validacao/validacao_mecanicas_t001.json`](validacao/validacao_mecanicas_t001.json), [`registros/vistas_t001/`](registros/vistas_t001/), [tarefa T001](../../jogo/tarefas/T001-cabeca-sempre-oposta.md) | Todos os itens de `conclusao` verdadeiros; `visual_kart.gd` com SHA-256 `73be89b8…b361db` |
| Mecânicas (Fase 8) | [`validacao/validacao_mecanicas_fase8.json`](validacao/validacao_mecanicas_fase8.json), [`registros/vistas_fase8/`](registros/vistas_fase8/) | Histórico: `cabeca_sempre_oposta: false` antes da T001; descreve `visual_kart.gd` `b87183e5…` |

## Estado das ferramentas e dos artefatos

- **Blender:** 5.2.2 LTS, sessão interativa pelo MCP. As Fases 4 a 7 rodaram nessa sessão, sem CLI e sem outra instância. No início da Fase 7 a sessão estava alterada só pela timeline (quadro 48; ações conferidas na cena antes de descartar) e foi recarregada. Ao final, `dimi.blend` estava aberto, no quadro 1, sem alterações pendentes (`is_dirty: false`). Na próxima sessão, conferir de novo o arquivo aberto e o estado de alteração.
- **Arquivo salvo versus cena aberta:** o hash acima é do arquivo em disco, salvo na Fase 6 e recarregado (`is_dirty: false`). Vistas e anexos de comparação foram descartados com `revert_mainfile`. O `dimi.blend1` criado ao salvar (igual ao backup) foi apagado.
- **Godot:** 4.7.2.stable pela CLI. Na Fase 8: `dimi.tres` criado; `jogo.gd` com `[Jake, Dimi]`; `definicao_personagem.gd` e `visual_kart.gd` com os campos opcionais `raio_rodas` e `giro_maximo_cabeca` (zero = comportamento anterior). Hashes antes/depois no registro da Fase 8; `visual_kart.gd` mudou de novo na T001 (faixa de oposição da cabeça). O `.import` do GLB não mudou.
- **Validações a refazer:** mudança em `kart.gd`, `visual_kart.gd`, `camera_perseguicao.gd`, `jogo.gd`, na ficha ou no GLB exige repetir `validar_mecanicas_dimi.gd` e `capturar_vistas_dimi.gd`. Qualquer mudança em origens, ossos, pesos, malhas, materiais ou ações invalida o hash do `.blend`, os relatórios `*_fase6.json` e a exportação (reexportar com `exportar_glb.py` e repetir `inspecionar_importacao_dimi.gd`). Mudanças no `.import` também exigem repetir o verificador. Os relatórios das Fases 4 e 5 descrevem o arquivo anterior (`229034cf…`).

## Decisões e restrições

- Frente −Y, esquerda do piloto +X, Z para cima.
- **Ações da cabeça:** Y local de `Head_Bone`, quadros 1/25/49 a 24 FPS (2 s). `Cabeca_Direita_Ida_e_Volta` = −25° (direita do piloto), `Cabeca_Esquerda_Ida_e_Volta` = +25°. Nomes do ponto de vista do piloto; no Jake, “direita” era +X. Teto de 25° vale também para a compensação da Fase 8.
- **Pivô da cabeça** (= início de `Head_Bone`): `(0, −0.010498046875, 0.4453125)`. Em Y, é o centro do toco do pescoço; em Z, o plano em que a gola fecha. Y local de `Head_Bone` = Z mundial.
- **Rodas:** centro do círculo ajustado ao contorno externo da banda de rodagem, sem os picos das bolinhas, com X no meio da banda. O centro da caixa delimitadora foi rejeitado por causa das bolinhas e da ovalização. Giro em X local, esterço em Z local.
- Ossos: `Root (0,0,0.1172)→(0,0,0.2344)`, `Torso →(0,y,0.4063)`, `Neck →pivô`, `Head →(0,y,0.7031)`. Deformam só `Torso_Bone` e `Head_Bone`.
- `Cabeca` → `Head_Bone` e `Corpo_Kart` → `Torso_Bone`, com peso 1,0 e o modificador `Rig_Rigido_Sem_Deformacao`. As rodas usam parentesco de osso em `Torso_Bone`, sem modificador, como no Jake.
- Pivôs arredondados para a grade de 1/4096 m. Tolerância de 1e-6 m para posições e pivôs (1e-5 m na Godot).
- **Exportação:** GLB com as duas ações (iniciando em 0 s), pose de repouso, sem tangentes nem atributos `rig_original_*`. Na Godot: frente +Z, Y para cima; Y de `Head_Bone` com o mesmo sinal do Blender.

## Pendências e impedimentos

- **Cabeça “sempre” oposta (jogo):** corrigida pela T001 (faixa de oposição por quadro). Fica pendente atualizar a documentação e o relatório do Jake, se autorizado, e avaliar ao vivo com teclado se o movimento parece natural.
- **Teto da cabeça:** 25° aplicado à inclinação (rolagem) no jogo; sem ele, 32,74°. O teto da Fase 6 foi medido para o giro em Y. Numa vista lateral fechada (que não existe no jogo), a borda da base aparece sob o queixo perto de 24°; na câmera do jogo, não.
- **Base aberta da cabeça:** giro limitado a 25° (decisão do usuário). Se alguma tela mostrar o piloto de lado com a cabeça girada, só a tampa resolve.
- **Rodas:** no giro de 360°, as bolinhas passam até 2,5 cm abaixo do chão (RL); a RR, sem bolinhas, oscila 3,5 mm. É uma característica da geometria. As bandas apoiam exatamente no chão com o raio de 0,1297.
- Pergunta sem resposta: nenhuma.

## Última tentativa e resultado

- **Ação (Fase 9):** hashes, `inspecionar_importacao_dimi.gd` e `validar_mecanicas_dimi.gd` repetidos com saída na pasta de rascunho (idênticos aos relatórios), conferência de 217 links, revisão dos critérios, resumo da entrega, índice corrigido, `__pycache__` removido. Blender não consultado (sessão: não verificada nesta atualização).

- **Ação (T001):** medição de base, correção em `visual_kart.gd`, nova medição no Dimi e cópia do verificador do Jake, captura de imagens. Resultado: `cabeca_sempre_oposta: true` nos dois pilotos; maior variação 2,67°/quadro.
- **Falha intermediária (T001):** só o limite mínimo gerava um salto de 10,9° quando o corpo cruzava o zero; resolvido com o limite máximo. A captura do pico não acontecia porque a cabeça passava a cruzar o centro em passos maiores que 1°; o script passou a detectar a troca de sinal.

- **Ação (Fase 8):** ficha e catálogo; campos opcionais na ficha; `validar_mecanicas_dimi.gd` (headless, 60 passos/s), `capturar_vistas_dimi.gd` (com janela) e regressão do Jake com uma cópia temporária do verificador dele, gravando na pasta de rascunho. Resultado: tudo passa, exceto `cabeca_sempre_oposta`; Jake idêntico nas medições determinísticas.
- **Falha intermediária (Fase 8):** a primeira execução, sem o teto, mediu 32,74° de cabeça relativa no percurso real. O teto de 25° foi aplicado na ficha e as duas medições foram repetidas; a imagem antiga ficou como `sem_teto_lateral_pico_cabeca_32.7_graus.png`.

- **Ação (Fase 7):** conferência da sessão alterada, recarga, `exportar_glb.py`, leitura do GLB (nós, skin, triângulos, imagens, amostras), `--import`, ajustes do `.import` e `inspecionar_importacao_dimi.gd`. Resultado: `tudo_ok: true`.
- **Falhas intermediárias (Fase 7):** pico importado como −24,8987° (30 FPS) e −24,8734° (otimizador). A opção do otimizador por animação e `remove_immutable_tracks=false` não resolveram e foram desfeitas. Resolvido com 24 FPS e o otimizador desligado no nó `AnimationPlayer`.
- **Ação (Fase 6, ações):** backup, `criar_acoes.py`, validação na cena, gravação, recarga, `validar_acoes.py` + `validar_preparacao.py` + `verificar_rig.py` no arquivo salvo, vistas nos quadros 13/25 e reversão. Resultado: `tudo_ok: true` em todos; `.blend1` apagado.
- **Ação (Fase 6, amplitude):** giros temporários de 0 a ±40°, vistas e grade de raios; a primeira medida, por vértices de borda, foi descartada (falso positivo em repouso). Resultado: interior visível ≈ 0 em repouso, crescente desde 10° de lado; zero na câmera do jogo até ±25°. Revertido sem salvar.
- **Ação (Fase 5):** recarga do arquivo, repetição de `verificar_rig.py`, `validar_preparacao.py` (NPZ + backup pré-Fase 3 + teste combinado), conferência de arquivos ausentes, recarga e hash.
- **Resultado observado (Fase 5):** `tudo_ok: true` nos dois relatórios; nenhum arquivo ausente; hash inalterado. Falhas intermediárias: nenhuma.

## Como retomar

1. Ler este checkpoint, `CHECKLIST.md` e `LEIA-ME.md`.
2. Conferir o SHA-256 de `blender/dimi.blend` (`e28bf878…49e1`).
3. No Blender aberto (MCP), conferir `bpy.data.filepath` e `is_dirty`.
4. Conferir o SHA-256 de `jogo/personagens/dimi/dimi_kart.glb` (`2b25281b…606258b`) e repetir `inspecionar_importacao_dimi.gd` se algo mudou.
5. Conferir os hashes do registro da Fase 9 e repetir os comandos do resumo da entrega (`LEIA-ME.md`) se algo mudou.
6. Tratar as pendências do registro da Fase 9 conforme o pedido.
7. Atualizar checkpoint, checklist e ficha.
