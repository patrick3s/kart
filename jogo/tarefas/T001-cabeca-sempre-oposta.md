# T001 — Cabeça sempre oposta à inclinação da suspensão

| Campo | Valor |
| --- | --- |
| Criada em | 15/10/2026 |
| Estado | **Concluída** em 15/10/2026: opção A (faixa de oposição por quadro), pedida pelo usuário (“corrija então a tarefa”) |
| Afeta | Mecânica comum a todos os pilotos: P001 Jake e P002 Dimi |
| Origem | Auditoria do Jake (P001.07) e Fase 8 do Dimi (P002.10) |
| Arquivo principal | [`scripts/visual_kart.gd`](../scripts/visual_kart.gd) |

## Requisito

Do [quinto prompt da receita](../../documentacao/RECEITA_PERSONAGEM.md#quinto-prompt--jogo-na-godot-rodas-suspensão-e-equilíbrio-da-cabeça):

> A cabeça deve **sempre** girar para o lado inverso da inclinação da suspensão (se o carro joga para um lado, a cabeça pende para o outro tentando equilibrar).

## Problema

A cabeça só fica oposta ao corpo **depois que a curva se estabiliza**. Durante as transições e com o tremor, há quadros em que a inclinação global da cabeça fica do mesmo lado da inclinação do corpo.

Medição com o código atual (60 passos/s, sem ruído; os números são iguais nos dois pilotos):

| Trecho | Quadros no mesmo lado | Último quadro com falha |
| --- | --- | --- |
| Entrada da curva | 18 | 18 (0,30 s) |
| Inversão da curva | 15 | 22 |
| Saída para a reta | 16 | 50 |
| Parada | 0 | — |
| Reta com vibração (com ruído) | 84 de 120 | — |

Evidências: [relatório do Dimi](../../personagens/P002_dimi/validacao/validacao_mecanicas_fase8.json) (`cabeca_sempre_oposta: false`), [relatório do Jake](../../personagens/P001_jake/validacao/validacao_godot_jake.json), [registro da Fase 8 do Dimi](../../personagens/P002_dimi/registros/registro-fase8-jogavel-2026-10-15.md#4-resultados-no-motor-relatório-final-com-o-teto) e [auditoria do Jake](../../personagens/P001_jake/registros/registro-validacao-godot-2026-10-15.md).

## Causa

Em `VisualKart.atualizar()`:

1. **Atraso de mola:** a cabeça persegue `alvo_cabeca = -compensacao_cabeca * rolagem` com uma mola própria (`rigidez_cabeca`, `amortecimento_cabeca`). Quando o corpo muda de lado, a cabeça ainda está voltando e fica do mesmo lado por alguns quadros.
2. **Tremor fora da meta:** o corpo recebe `rolagem + tremor`, mas a meta da cabeça usa só `rolagem`. Na reta, o tremor inclina o corpo e a cabeça não reage, o que conta como “mesmo lado”.

A inclinação global da cabeça é a soma da inclinação do corpo (herdada pela hierarquia `Torso → Neck → Head`) com o giro relativo `_cabeca`.

## Decisão necessária

| Opção | Efeito | Observação |
| --- | --- | --- |
| **A — Restringir por quadro (recomendada)** | Mantém a mola para a sensação de movimento, mas depois de integrá-la limita `_cabeca` para que a inclinação global fique sempre do lado oposto ao corpo (`rolagem + tremor`) | Cumpre o “sempre” e preserva o movimento suave na maior parte do tempo |
| B — Sem mola | `_cabeca = -k * (rolagem + tremor)` direto, com `k > 1` | Cumpre o “sempre” de forma trivial; a cabeça perde a inércia própria e pode parecer rígida |
| C — Aceitar o atraso | Não muda o código; o requisito passa a ser “oposta em regime estabilizado” | Atualizar a receita e os relatórios para não tratar a transição como falha |

## Proposta de implementação (opção A)

1. Calcular a rolagem total do corpo uma vez: `rolagem_total = rolagem + tremor`.
2. Usar `rolagem_total` na meta da cabeça.
3. Depois de integrar a mola, garantir a oposição global com uma margem mínima:
   - global = `rolagem_total + _cabeca`;
   - se `|rolagem_total|` passar da zona neutra (0,05°) e `global * rolagem_total > 0`, ajustar `_cabeca` para que global = `-sign(rolagem_total) * margem` e zerar a componente de `_vel_cabeca` que empurra contra a restrição.
4. Aplicar o teto `giro_maximo_cabeca` **depois** da restrição e conferir que os dois não entram em conflito. Com o teto de 25° do Dimi e corpo de até 14,8° (14° + 0,8° de tremor), sobra espaço para a oposição.
5. Opcional: expor a margem como `@export` no grupo “Cabeça”.

Antes de escolher, confirmar que a inclinação medida no verificador (`_inclinacao`, no espaço do esqueleto) é a mesma grandeza que a restrição controla. A rolagem do corpo é aplicada em torno de `Vector3.BACK` no espaço do esqueleto e a cabeça herda a do pai.

## Critérios de aceite

- [x] `cabeca_sempre_oposta: true` no verificador do Dimi, a 60 e a 120 passos/s, com e sem ruído, incluindo a reta com vibração.
- [x] O mesmo resultado no verificador do Jake (cópia com destino fora da pasta do Jake; ver “Resultado”).
- [x] Continuam verdadeiros: suspensão para o lado certo, cabeça oposta estabilizada, rodas, câmera, movimento, escolha de piloto.
- [x] Cabeça do Dimi dentro do teto de 25° (`cabeca_dentro_do_teto_25`).
- [x] Sem saltos visíveis: variação máxima de `_cabeca` medida (até 2,67°/quadro, contra 1,47° antes) e [imagens](../../personagens/P002_dimi/registros/vistas_t001/) conferidas.
- [ ] Hashes novos de `visual_kart.gd` registrados nos dois personagens. — registrados no Dimi e aqui; a documentação do Jake não foi alterada (sem autorização para mexer na pasta dele).

## Verificação

Na pasta `jogo/`:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --fixed-fps 60 --script res://ferramentas/validar_mecanicas_dimi.gd
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --fixed-fps 60 --script res://ferramentas/validar_mecanicas_jake.gd
/Applications/Godot.app/Contents/MacOS/Godot --path . --fixed-fps 60 --script res://ferramentas/capturar_vistas_dimi.gd
```

O verificador do Jake **regrava** `personagens/P001_jake/validacao/validacao_godot_jake.json`. Como isso altera arquivos do Jake, a execução precisa de autorização explícita. Sem ela, rodar uma cópia com destino na pasta de rascunho, como foi feito na Fase 8 do Dimi.

## Documentos a atualizar ao concluir

- `jogo/LEIA-ME.md` (seção “Mecânica” e resultados das validações).
- Dimi: registro novo, `CHECKLIST.md` (Fase 8), `CHECKPOINT.md` e `LEIA-ME.md`.
- Jake: novo registro de validação e `LEIA-ME.md`, se autorizado.
- `documentacao/RECEITA_PERSONAGEM.md`, seção “Aplicação, validação e limites do quinto prompt”.
- Este arquivo: estado, opção escolhida e resultado.

## Fora do escopo

- Suspensão física por roda (raycast ou curso individual).
- Tampar a base aberta da cabeça do Dimi.
- Bolinhas das rodas atravessando o chão.

## Resultado — 15/10/2026

### Implementação (`visual_kart.gd`)

1. `rolagem_total = rolagem + tremor` passa a ser usado no corpo **e** na meta da cabeça (`-compensacao_cabeca * rolagem_total`).
2. A mola continua igual. Depois dela, `_cabeca` é limitada a uma **faixa de oposição**: a inclinação global da cabeça (`rolagem_total + _cabeca`) fica sempre do lado oposto ao corpo, entre `oposicao_minima_cabeca` (0,2) e `oposicao_maxima_cabeca` (1,0) vezes a inclinação dele. A velocidade da mola que empurra contra a faixa é zerada.
3. O teto `giro_maximo_cabeca` da ficha é aplicado depois. Com 25° no Dimi, só haveria conflito com o corpo acima de 20,8°; o máximo da suspensão é 14° mais 0,8° de tremor.

**Primeira tentativa, descartada:** só o limite mínimo, com fator 0,2. A regra passou, mas a cabeça saltava até **10,9°** num quadro quando o corpo cruzava o zero (ia de um lado ao outro de uma vez). O limite máximo faz a cabeça cruzar o centro junto com o corpo. A meta estabilizada (`-0,7 ×` o corpo) está dentro da faixa, então o regime de curva quase não mudou.

### Medições

| Caso | Antes (quadros no mesmo lado) | Depois | Cabeça estabilizada antes → depois | Maior variação por quadro antes → depois |
| --- | --- | --- | --- | --- |
| 60 passos/s, sem ruído: entrada / inversão / saída / parada | 18 / 15 / 16 / 0 | 0 / 0 / 0 / 0 | −4,812° / +4,812° → −4,813° / +4,812° | 1,47° → 2,27° |
| 60 passos/s, com ruído | 18 / 15 / 78 / 0 | 0 / 0 / 0 / 0 | −5,010° / +4,610° → −5,028° / +4,631° | 1,47° → 2,67° |
| 120 passos/s, com ruído | 40 / 31 / 148 / 0 | 0 / 0 / 0 / 0 | −5,010° / +4,610° → −5,022° / +4,638° | 0,73° → 1,52° |
| Reta com vibração (120 quadros) | 84 | 0 | — | — |

- **Dimi:** todos os itens de `conclusao` são `true`, inclusive `cabeca_sempre_oposta` e `cabeca_dentro_do_teto_25`. Percurso real a 22 m/s: corpo +14,14° / −14,10°, cabeça −9,75° / +9,77°. Relatório: [`validacao_mecanicas_t001.json`](../../personagens/P002_dimi/validacao/validacao_mecanicas_t001.json); antes da correção: [`T001/dimi_antes.json`](T001/dimi_antes.json).
- **Jake:** 0 quadros no mesmo lado em todos os casos; rodas e inclinação do corpo idênticas ao relatório anterior; `cabeca_sempre_oposta: true`. O verificador dele rodou como cópia temporária com destino fora da pasta do Jake: [`T001/regressao_jake_depois.json`](T001/regressao_jake_depois.json). O arquivo `personagens/P001_jake/validacao/validacao_godot_jake.json` **não** foi regravado e continua descrevendo a versão anterior. O campo `status: "parcial"` dessa cópia é fixo no código do verificador e não foi recalculado.
- **Imagens:** [`vistas_t001/`](../../personagens/P002_dimi/registros/vistas_t001/). Na câmera do jogo, nenhuma diferença visível.

### Hashes

| Arquivo | SHA-256 |
| --- | --- |
| `jogo/scripts/visual_kart.gd` | `73be89b8…b361db` (Fase 8 do Dimi: `b87183e5…caf92b`) |
| `jogo/ferramentas/validar_mecanicas_dimi.gd` | `c8e8dba7…e19185` (parâmetro `--saida=` e variação por quadro) |
| `jogo/ferramentas/capturar_vistas_dimi.gd` | `d8b4297f…1ee285b` (parâmetro `--pasta=` e detecção do pico pela troca de sinal) |
| `personagens/P002_dimi/validacao/validacao_mecanicas_t001.json` | `d44b0a55…2b55` |

### Pendente

- Atualizar a documentação e o relatório do Jake (P001), se autorizado.
- Avaliar ao vivo, com teclado, se a cabeça parece natural. Com a faixa, ela acompanha o tremor da carroceria na reta.
