# Registro — Fase 9 — entrega e documentação — P002 Dimi

Data: 15/10/2026 (−03:00). Pedido do usuário: “inicie a fase 9 do dimi”. Nesta fase não houve mudança no modelo, no GLB nem no código do jogo. Foram conferidos o estado e a documentação.

## 1. Conferência dos artefatos

| Artefato | SHA-256 atual | Igual ao registrado? |
| --- | --- | --- |
| `blender/dimi.blend` | `e28bf87840fa0f2c5a42f486e7727d8aca15606e11ab7ebb1927cd647cd649e1` | Sim (Fase 6) |
| `jogo/personagens/dimi/dimi_kart.glb` | `2b25281baee6a9bd1f123267bd2a3278ba426a2c2a177a725d4cb8e7e606258b` | Sim (Fase 7) |
| `jogo/personagens/dimi/dimi_kart.glb.import` | `487777e7…19a711a0` | Sim (Fase 7) |
| `jogo/personagens/dimi/dimi.tres` | `f68edad8…3f400` | Sim (Fase 8) |
| `jogo/scripts/visual_kart.gd` | `73be89b8…b361db` | Sim (T001) |
| `jogo/scripts/definicao_personagem.gd` / `jogo.gd` | `a475788d…60e752` / `6f7dcca3…b91c` | Sim (Fase 8) |

O Blender não foi consultado nesta fase. O arquivo em disco foi conferido só pelo hash; a sessão aberta: **não verificada nesta atualização**.

## 2. Repetição das verificações (Godot 4.7.2, CLI)

As duas verificações rodaram de novo, gravando na pasta de rascunho para não substituir as evidências:

- `inspecionar_importacao_dimi.gd`: `tudo_ok: true`, com **todas as chaves iguais** a [`importacao_godot_fase7.json`](../validacao/importacao_godot_fase7.json).
- `validar_mecanicas_dimi.gd`: `conclusao`, `curvas`, `rodas` e `sha256` **iguais** a [`validacao_mecanicas_t001.json`](../validacao/validacao_mecanicas_t001.json). Todas as regras são verdadeiras.

## 3. Links

Um script de conferência (fora do repositório) leu todos os links relativos, com âncoras, em: `.md` da pasta do Dimi, `jogo/LEIA-ME.md`, `jogo/tarefas/*.md` e `documentacao/README.md`. Resultado: **217 links, nenhum quebrado**. A entrada do Dimi no índice `documentacao/README.md` ainda dizia “próxima: Fase 7” e foi atualizada. Depois das atualizações desta fase, a conferência foi repetida: **238 links, nenhum quebrado**.

## 4. Critérios de conclusão por fase

| Fase | Critério | Situação | Evidência |
| --- | --- | --- | --- |
| 0 | Arquivos criados e referências solicitadas | Atendido | Ficha, checklist, checkpoint, índice |
| 1 | Entrada identificada e escopo definido | Atendido | [`referencia/LEIA-ME.md`](../referencia/LEIA-ME.md) |
| 2 | Backup salvo e atributos originais registrados | Atendido; foi feita pelo Blender em segundo plano (CLI), antes da regra atual de usar só a sessão aberta pelo MCP | [Registro](registro-fase2-inspecao-2026-10-15.md) |
| 3 | Partes conferidas, sem fragmentos perdidos | Atendido (`tudo_ok`) | [Verificação](../validacao/verificacao_separacao_fase3.json) |
| 4 | Pivôs medidos, pesos exclusivos | Atendido (`tudo_ok`) | [Verificação](../validacao/verificacao_rig_fase4.json) |
| 5 | Tolerâncias e arquivo em disco conferidos | Atendido (`tudo_ok`); revalidado na Fase 6 | [Validação](../validacao/validacao_preparacao_fase5.json) |
| 6 | Keyframes, corpo e pivô; arquivo salvo | Atendido (`tudo_ok`) | [Validação](../validacao/validacao_acoes_cabeca_fase6.json) |
| 7 | Recurso importado inspecionado | Atendido (`tudo_ok`); repetido nesta fase | [Inspeção](../validacao/importacao_godot_fase7.json) |
| 8 | Mecânicas medidas, falhas registradas | Atendido; a falha da cabeça foi corrigida pela T001 | [Fase 8](../validacao/validacao_mecanicas_fase8.json), [T001](../validacao/validacao_mecanicas_t001.json) |

## 5. Pendências que continuam abertas

| Pendência | Impacto | Como resolver |
| --- | --- | --- |
| Base aberta da cabeça | Escondida na câmera do jogo; aparece de lado ou de perto a partir de ~10° no giro em Y e perto de 24° na inclinação | Tampar a base no Blender (refazer as Fases 5 a 8), ou manter o teto de 25° |
| Bolinhas das rodas | Passam até 2,5 cm abaixo do chão durante o giro | Característica da geometria; só muda alterando o modelo |
| Aparência na Godot | Imagens renderizadas conferidas a olho; material não comparado com o Blender | Comparação lado a lado, se necessária |
| Teste com teclado | A entrada foi simulada por script; ninguém jogou | Jogar e avaliar a cabeça, que agora acompanha o tremor na reta |
| Suspensão | Visual, sem curso por roda | Fora do escopo atual |
| Documentação do Jake após a T001 | `validacao_godot_jake.json` e a ficha do Jake descrevem a mecânica antiga | Autorizar a atualização da pasta do Jake |
| Versionamento | Nada do Dimi foi commitado; receita e prompt têm alterações locais | Commit quando solicitado (`.blend` via Git LFS; GLBs de 64 a 77 MB, abaixo do limite de 100 MB do GitHub) |

## 6. Limpeza

Foi removido `registros/scripts_fase3/__pycache__/` (cache Python gerado ao rodar `rotulos_partes.py`; não é evidência). Nenhum `.blend1` ou arquivo temporário restante.

## 7. Commit

Não solicitado e não realizado.
