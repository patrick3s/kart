# Registro — Fase 9 — entrega e documentação — P003 Bryan

Data: 16/10/2026 (−03:00). Pedido do usuário: “inicie a fase 9 do bryan”. Nesta fase não houve mudança no modelo, no GLB, na ficha nem no código do jogo. Foram conferidos o estado e a documentação.

## 1. Conferência dos artefatos

| Artefato | SHA-256 atual | Igual ao registrado? |
| --- | --- | --- |
| `blender/bryan.blend` | `b25be23be7279cb8d1bae26a4c62b18bd197b06d023a4820975348395fe43c11` | Sim (Fase 6) |
| `blender/bryan.blend1` | `da58cc33…96c81b77` | Sim (pré-Fase 6, Fase 6) |
| Backups em `backups/` (6 `.blend` e `geometria_original.npz`) | `f116458b…`, `5768c98f…`, `0ffb2802…`, `da58cc33…` (×2), `b25be23b…`, `a7c55804…c9c71f` | Sim (Fases 2 a 7) |
| `jogo/personagens/bryan/bryan_kart.glb` | `b51c51a5d8a0bafbd1a2a87ee0e1eb2b43e4e3e82842db72d040573d48bea9e4` | Sim (Fase 7) |
| `jogo/personagens/bryan/bryan_kart.glb.import` | `60fcdbec…1db444` | Sim (Fase 7) |
| Texturas extraídas (`_basecolor.jpg`, `_normal.png`, `_rm.jpg`) | `3fe7ee02…`, `3831547e…`, `8d404a8e…` | Sim (Fase 7) |
| `jogo/personagens/bryan/bryan.tres` | `2b847e0e…4774c0` | Sim (Fase 8) |
| `jogo/scripts/` (`jogo.gd`, `kart.gd`, `visual_kart.gd`, `camera_perseguicao.gd`, `definicao_personagem.gd`, `selecao_personagem.gd`) e `project.godot` | iguais aos de `sha256` em [`validacao_mecanicas_fase8.json`](../validacao/validacao_mecanicas_fase8.json) | Sim (Fase 8) |
| Ferramentas `inspecionar_importacao_bryan.gd`, `validar_mecanicas_bryan.gd`, `capturar_vistas_bryan.gd` | `c3cbd010…`, `360ea534…`, `c73cb7ff…` | Sim (Fases 7 e 8) |

**Blender** (MCP, sessão aberta, só leitura): `bryan.blend` aberto, `is_dirty: false`, modo objeto, quadro 1; 7 objetos (`Cabeca`, `Corpo_Kart`, `Personagem_Rig`, quatro `Wheel_*`); ações `Cabeca_Direita_Ida_e_Volta` e `Cabeca_Esquerda_Ida_e_Volta`, ativa a `Direita`. Nada foi salvo.

## 2. Repetição das verificações (Godot 4.7.2, CLI)

- `inspecionar_importacao_bryan.gd` grava direto na evidência. A evidência foi copiada para o rascunho antes, o verificador rodou e o original foi restaurado. A saída nova foi **idêntica byte a byte** a [`importacao_godot_fase7.json`](../validacao/importacao_godot_fase7.json) (`d9152d1a…7d864024`; `tudo_ok: true`).
- `validar_mecanicas_bryan.gd -- --saida=<rascunho>`, duas vezes: as **14 conclusões** iguais às da Fase 8 e verdadeiras (`cabeca_relativa_max_graus` = 25,0; apoio das rodas de 0 a 0,98 mm). Também saíram iguais `curvas`, `rodas`, `reta_com_vibracao`, `selecao`, `estrutura`, `dimensoes` e `sha256`.
- Só a seção `percurso` mudou, e mudou também entre as duas execuções desta fase: na curva, o corpo ficou entre 13,9° e 14,35° e a cabeça global entre 9,4° e 10,0°, sempre com sinais opostos. É um instantâneo da pista, que sorteia a semente do ruído (o mesmo foi visto no Jake na Fase 8). As curvas manuais, de semente fixa 12345, não variaram.
- `capturar_vistas_bryan.gd` não foi repetido: as imagens dependem só dos artefatos acima, que não mudaram.

A primeira execução da Godot nesta fase gerou `jogo/ferramentas/capturar_vistas_bryan.gd.uid`, arquivo de identificador que a Godot cria para cada script. Os demais verificadores já tinham o seu.

## 3. Links

Um script de conferência (no rascunho, fora do repositório) leu todos os links relativos, com âncoras, em: `.md` da pasta do Bryan, `jogo/LEIA-ME.md`, `jogo/tarefas/*.md` e `documentacao/README.md`. Resultado antes das atualizações: **292 links, nenhum quebrado**. A entrada do Bryan no índice `documentacao/README.md` ainda dizia “próxima: Fase 8” e foi atualizada. A conferência foi repetida depois das atualizações desta fase (seção 8).

## 4. Critérios de conclusão por fase

| Fase | Critério | Situação | Evidência |
| --- | --- | --- | --- |
| 0 | Documentos criados; `.blend` salvo e recarregado na sessão aberta | Atendido | [Conferência](conferencia-blend-inicial-2026-10-15.json) |
| 1 | Inventário conferido, entrada escolhida, escopo confirmado | Atendido | [`referencia/LEIA-ME.md`](../referencia/LEIA-ME.md), [conferência](conferencia-blend-modelo-2026-10-15.json) |
| 2 | Backup salvo e conferido; contagens, atributos e tolerâncias registrados | Atendido (Blender MCP) | [Registro](registro-fase2-inspecao-2026-10-15.md), [verificação](../validacao/verificacao_preservacao_fase2.json) |
| 3 | Partes conferidas, faces e cantos exatamente uma vez | Atendido (`tudo_ok`); desvio aceito: 1.730 vértices duplicados na costura das rodas | [Verificação](../validacao/verificacao_separacao_fase3.json) |
| 4 | Pivôs medidos, pesos exclusivos, hierarquia padrão | Atendido (`tudo_ok`) | [Medidas](../validacao/medidas_pivos_fase4.json), [verificação](../validacao/verificacao_rig_fase4.json) |
| 5 | Tolerâncias e arquivo em disco conferidos; testes restaurados | Atendido (`tudo_ok`); revalidado na Fase 6 | [Comparação](../validacao/comparacao_preparacao_fase5.json), [rig](../validacao/verificacao_rig_fase5.json) |
| 6 | Keyframes, corpo e pivô; arquivo salvo e recarregado | Atendido (`tudo_ok`); hash ainda igual | [Ações](../validacao/validacao_acoes_cabeca_fase6.json), [comparação](../validacao/comparacao_preparacao_fase6.json) |
| 7 | Recurso importado inspecionado | Atendido (`tudo_ok`); repetido nesta fase, idêntico | [Inspeção](../validacao/importacao_godot_fase7.json) |
| 8 | Todas as regras medidas passam, cabeça oposta em todo quadro | Atendido; repetido nesta fase, conclusões iguais | [Mecânicas](../validacao/validacao_mecanicas_fase8.json) |

## 5. Pendências que continuam abertas

| Pendência | Impacto | Como resolver |
| --- | --- | --- |
| Nuca aberta | Fragmentos visíveis a 25° de perto e com a câmera atrasada 30°; escondida na câmera do jogo por trás | Tampar a nuca no Blender (refazer as Fases 5 a 8) ou manter o teto de 25° (decisão atual do usuário) |
| Topo das rodas | O preenchimento do para-lama faz o contato oscilar 12–19 mm ao girar | Aceito pelo usuário; só muda alterando o modelo |
| Raio único das rodas | Traseiras até 0,98 mm (modelo) acima do chão | Raio por roda na ficha, se o jogo passar a aceitar |
| Fresta entre pescoço e gola | Visível de perto e de lado na curva; invisível na câmera do jogo | Ajuste no modelo, se necessário |
| Verificador do Dimi | `validar_mecanicas_dimi.gd` reprova `catalogo_jake_e_dimi` e `selecao_troca_e_volta` com três pilotos; mecânicas do Dimi intactas | Ajustar o verificador ao catálogo atual, quando autorizado |
| Aparência na Godot | Imagens conferidas a olho; material não comparado com o Blender | Comparação lado a lado, se necessária |
| Teste com teclado | Entrada simulada por script; ninguém jogou | Jogar e avaliar |
| Suspensão | Visual, sem curso por roda | Fora do escopo atual |
| Versionamento | Nada do Bryan foi commitado (pasta, GLB, ficha, ferramentas, catálogo em `jogo.gd`) | Commit quando solicitado (`.blend` de 105 MB e backups exigem Git LFS ou exclusão; GLB de 74,6 MB abaixo do limite de 100 MB do GitHub) |

## 6. Limpeza

Nenhum `__pycache__`, `.tmp` ou `.pyc` na pasta do Bryan nem em `jogo/personagens/bryan/`. O `bryan.blend1` (pré-Fase 6) foi mantido; o conteúdo dele também está nos backups.

## 7. Commit

Não solicitado e não realizado.

## 8. Conferência final dos links

Repetida depois das atualizações desta fase (ficha, checklist, checkpoint, índice e este registro): **325 links, nenhum quebrado**. As evidências da Fase 7 (`d9152d1a…`) e da Fase 8 (`8a459289…`) continuam com o hash original.
