# Registro da Fase 6 — ações da cabeça — P002 Dimi

Data: 15/10/2026, 17:27–17:32 (-03:00). A primeira parte da fase, a escolha da amplitude, está em [`registro-fase6-amplitude-2026-10-15.md`](registro-fase6-amplitude-2026-10-15.md).

## 1. Pedido e definições

O usuário confirmou os parâmetros: **amplitude de 25°** e **2 s de ida e volta a 24 FPS** (quadros 1/25/49), como no primeiro rig do Jake.

| Item | Valor |
| --- | --- |
| Osso e canal | `pose.bones["Head_Bone"].rotation_euler[1]`: Y local, que é o Z mundial. Euler `XYZ`, já configurado no rig. |
| Sentido | Positivo vira o rosto para +X, que é a **esquerda do piloto** (frente −Y). Os nomes seguem o ponto de vista do piloto. |
| `Cabeca_Direita_Ida_e_Volta` | 0° → **−25°** → 0° nos quadros 1 → 25 → 49 |
| `Cabeca_Esquerda_Ida_e_Volta` | 0° → **+25°** → 0° nos quadros 1 → 25 → 49 |
| Curva | `BEZIER`, alças `AUTO_CLAMPED`, extrapolação `CONSTANT`; sem modificador de ciclos e sem NLA |
| Cena | 24 FPS (base 1,0) e intervalo principal 1–250, preservados; prévia 1–49 ativada |
| Estado salvo | Ação ativa `Cabeca_Direita_Ida_e_Volta`, no quadro 1 (pose neutra). As duas ações têm `use_fake_user`. |

**Diferença em relação ao Jake.** Lá, +40° foi chamado de "direita em relação à vista frontal", ou seja, a direita de quem olha o piloto de frente, que é +X e corresponde à esquerda do piloto. No Dimi, os nomes seguem o ponto de vista do piloto, por isso a `Direita` tem sinal negativo. O jogo não usa as ações pelo nome; `definicao_personagem.gd` só referencia `Head_Bone`.

## 2. Procedimento

Tudo foi feito na sessão aberta do Blender 5.2.2 LTS, pelo MCP.

1. Inspeção: 24 FPS, nenhuma ação, nenhuma trilha NLA e nenhum driver; `Head_Bone` em `XYZ`, sem restrições nem travas; sessão igual ao disco (`is_dirty: false`).
2. Backup byte a byte: [`backups/dimi_antes_fase6_20261015_172956.blend`](../backups/dimi_antes_fase6_20261015_172956.blend), SHA-256 `229034cf…25a7d7` (o arquivo das Fases 4 e 5).
3. [`scripts_fase6/criar_acoes.py`](scripts_fase6/criar_acoes.py): criou as duas ações (um canal e três keyframes cada), configurou as curvas e a prévia e deixou a `Direita` ativa no quadro 1. Nenhum objeto, osso, origem, peso ou vértice foi editado.
4. [`scripts_fase6/validar_acoes.py`](scripts_fase6/validar_acoes.py) foi executado na cena aberta e depois **no arquivo salvo e recarregado** (`wm.revert_mainfile`); os dois resultados deram `tudo_ok: true`.
5. Ao salvar, o Blender criou `dimi.blend1`, que era idêntico ao backup (`cmp`); o arquivo foi apagado.
6. No arquivo recarregado, foram repetidos [`validar_preparacao.py`](scripts_fase5/validar_preparacao.py) e [`verificar_rig.py`](scripts_fase4/verificar_rig.py), os dois com `tudo_ok: true`.
7. Foram renderizadas vistas nos quadros 13 e 25, de frente e pela câmera do jogo. Câmera e render foram desfeitos com `revert_mainfile`, sem salvar.

## 3. Validação das ações

Resultado completo em [`validacao/validacao_acoes_cabeca_fase6.json`](../validacao/validacao_acoes_cabeca_fase6.json). **`tudo_ok: true`**.

| Verificação | Abrangência | Direita | Esquerda |
| --- | --- | ---: | ---: |
| Keyframes, interpolação, alças e extrapolação | 3 keyframes | conforme | conforme |
| Alças dos extremos horizontais (sem ultrapassar) | 3 keyframes | sim | sim |
| Curva amostrada: mínimo/máximo | 481 amostras entre 1 e 49 | −25,0000001° / 0° | 0° / 25,0000001° |
| Ida e volta monótonas | mesmas amostras | sim | sim |
| Valor fora do intervalo (quadros 0 e 60) | — | 0° | 0° |
| Deslocamento do pivô | todos os 49 quadros | 0,0 | 0,0 |
| Outros ossos, localização/escala e eixos X/Z da cabeça | todos os 49 quadros | 0,0 | 0,0 |
| Matrizes de todos os objetos | todos os 49 quadros | 0,0 | 0,0 |
| Cabeça avaliada × rotação rígida esperada em torno do pivô | todos os vértices, quadros 1/13/25/37/49 | 5,96e-8 | 5,96e-8 |
| Comprimento das arestas da cabeça | mesmos quadros | ≤ 3,62e-8 | ≤ 3,77e-8 |
| `Corpo_Kart` e rodas × NPZ original | mesmos quadros | 5,96e-8 | 5,96e-8 |
| Direção do rosto no quadro 25 | — | (−0,4226, −0,9063, 0) | (+0,4226, −0,9063, 0) |

- **Ângulos medidos nos quadros 1/13/25/37/49:** 0°, ∓12,5°, ∓25°, ∓12,5°, 0°.
- **Espelhamento:** a curva da esquerda é exatamente a negativa da direita (diferença máxima de 0° nas 481 amostras).
- **Deslocamentos:** os desvios de 5,96e-8 m são o mesmo arredondamento das coordenadas compensadas medido em repouso nas Fases 4 e 5. Não houve movimento das partes fixas.
- **Ângulo de 25°:** a API devolve 25,00000012650595°, por causa da representação em ponto flutuante.

## 4. Preservação no arquivo salvo

No arquivo recarregado, com as ações e a ação `Direita` ativa no quadro 1:

- [`validacao/validacao_preparacao_fase6.json`](../validacao/validacao_preparacao_fase6.json): `tudo_ok: true`. Inclui cada elemento original exatamente uma vez, conectividade, UV, materiais, normais codificadas, texturas e o teste combinado.
- [`validacao/verificacao_rig_fase6.json`](../validacao/verificacao_rig_fase6.json): `tudo_ok: true`. Inclui pesos, pivôs e testes temporários.

Os dois JSON saíram byte a byte iguais aos da Fase 5 (mesmos SHA-256), porque a pose no quadro 1 é a de repouso e nenhum dado medido mudou. **O arquivo `.blend` mudou** (novas ações), por isso as validações foram refeitas sobre ele, e não herdadas da Fase 5.

## 5. Conferência visual

As imagens ficam em [`vistas_fase6/acoes/`](vistas_fase6/acoes/), nos quadros 13 e 25 de cada ação, de frente e pela câmera do jogo.

- **De frente, quadro 25:** em `direita_q25_frente.png` o rosto vira para a direita do piloto, que é a esquerda da imagem; em `esquerda_q25_frente.png`, para o lado oposto. A gola esconde a base do pescoço nessa vista.
- **Câmera do jogo:** o pescoço continua coberto pelo boné e pelo móbile.
- **De lado:** pela medição anterior, a borda da base aberta continua aparecendo nessa vista a 25° (mancha clara sob a mandíbula). É a limitação aceita junto com o limite de amplitude.
- **Não verificado:** não foi renderizado vídeo nem cada quadro. A reprodução na viewport pode ficar abaixo de 24 FPS, o que não altera os keyframes.

## 6. Arquivo resultante

| Artefato | Bytes | SHA-256 |
| --- | ---: | --- |
| `blender/dimi.blend` | 109.893.929 | `e28bf87840fa0f2c5a42f486e7727d8aca15606e11ab7ebb1927cd647cd649e1` |
| `validacao/validacao_acoes_cabeca_fase6.json` | — | `e4fe40f1420057c6868dc3661bff510f3001be4e702c97c77ca0183b876e8b74` |
| `validacao/validacao_preparacao_fase6.json` | — | `7a22e16b…e5ddc5` (igual ao da Fase 5) |
| `validacao/verificacao_rig_fase6.json` | — | `02dc1cec…cba89d` (igual ao da Fase 5) |
| `registros/scripts_fase6/criar_acoes.py` | — | `e14740fb…3c3295` |
| `registros/scripts_fase6/validar_acoes.py` | — | `42b7f05f…272d01` |

Sessão ao terminar: `dimi.blend` aberto, recarregado do disco, `is_dirty: false`, ação `Direita` ativa no quadro 1.

## 7. Como visualizar

1. Abrir `blender/dimi.blend`: a ação `Cabeca_Direita_Ida_e_Volta` já está ativa em `Personagem_Rig`.
2. Reproduzir a timeline (barra de espaço na viewport); a prévia repete os quadros 1–49.
3. Para ver a outra ação, escolher `Cabeca_Esquerda_Ida_e_Volta` no Editor de ações.

## 8. Pontos para as próximas fases

- **Fase 7 (exportação):** decidir se as duas ações vão para o GLB (por exemplo, com "Actions" como animações separadas) e conferir na Godot os nomes, o sinal e a duração de 2 s.
- **Fase 8:** respeitar o teto de 25° também na compensação da cabeça em curva. O raio das rodas deve vir da ficha (0,1297), não da caixa da malha.
- Qualquer mudança em malhas, origens, ossos, pesos, materiais ou nas ações invalida o hash acima e os relatórios desta fase.
