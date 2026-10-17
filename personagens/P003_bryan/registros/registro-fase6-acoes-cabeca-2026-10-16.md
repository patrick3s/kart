# Registro da Fase 6 — ações da cabeça — P003 Bryan

Data: 16/10/2026, 09:05–09:20 (-03:00).

## 1. Pedido e decisão da amplitude

O usuário pediu o início da Fase 6. A pendência da Fase 5 (limite de amplitude da nuca) foi respondida antes de criar as ações: **25°**, a opção recomendada. Esse valor vale para as duas ações e para o `giro_maximo_cabeca` da Fase 8.

A escolha considerou as medições da [seção 6 do registro da Fase 5](registro-fase5-validacao-2026-10-16.md#6-nuca-medição-da-amplitude-decisão-limitar):

- a câmera do jogo, por trás, esconde o pescoço até ±40°;
- com a câmera atrasada 30° numa curva, aparecem fragmentos pequenos a partir de cerca de 10°;
- de perto, de trás e do alto, a borda aparece a partir de cerca de ±10°.

**Limitação aceita:** esses fragmentos continuam aparecendo a 25° nas vistas de perto e com a câmera atrasada (ver seção 5).

Duração e FPS seguem o Jake e o Dimi: 2 s de ida e volta a 24 FPS, que já era o FPS da cena.

| Item | Valor |
| --- | --- |
| Osso e canal | `pose.bones["Head_Bone"].rotation_euler[1]`: Y local, que é o +Z mundial. Euler `XYZ`, sem restrições nem travas. |
| Sentido | Medido no Bryan: com +25°, a frente vai de (0, −1, 0) para (+0,4226, −0,9063, 0), ou seja, para +X, que é a **esquerda do piloto**. Os nomes seguem o ponto de vista do piloto, como no Dimi. |
| `Cabeca_Direita_Ida_e_Volta` | 0° → **−25°** → 0° nos quadros 1 → 25 → 49 |
| `Cabeca_Esquerda_Ida_e_Volta` | 0° → **+25°** → 0° nos quadros 1 → 25 → 49 |
| Curva | `BEZIER`, alças `AUTO_CLAMPED`, extrapolação `CONSTANT`; sem modificador de ciclos e sem NLA |
| Cena | 24 FPS (base 1,0) e intervalo principal 1–250, preservados; prévia 1–49 ativada |
| Estado salvo | Ação ativa `Cabeca_Direita_Ida_e_Volta`, no quadro 1 (pose neutra). As duas ações têm `use_fake_user`. |

## 2. Procedimento

Tudo foi feito na sessão aberta do Blender 5.2.2 LTS, pelo MCP, sem CLI e sem outra instância.

1. **Retomada:** o SHA-256 em disco era `da58cc33…96c81b77`, o mesmo do checkpoint. A sessão estava com `bryan.blend`, `is_dirty: false`, 24 FPS, sem ações, drivers ou NLA.
2. **Backup byte a byte:** [`backups/bryan_antes_fase6_20261016_091341.blend`](../backups/bryan_antes_fase6_20261016_091341.blend), SHA-256 `da58cc33…96c81b77`.
3. **Eixos medidos no Bryan:** os eixos de `Head_Bone` no mundo são X = (1, 0, 0), Y = (0, 0, 1) e Z = (0, −1, 0). O pivô está em `(−0.0075684, 0.0712891, 0.4941406)`, igual à Fase 4. O teste temporário de +25° foi desfeito.
4. **Criação:** [`scripts_fase6/criar_acoes.py`](scripts_fase6/criar_acoes.py), copiado do P002 sem mudar a lógica. Criou as duas ações (um canal e três keyframes cada). Nenhum objeto, osso, origem, peso ou vértice foi editado.
5. **Validação das ações na cena aberta:** [`validar_acoes.py`](scripts_fase6/validar_acoes.py), também do P002, deu `tudo_ok: true`.
6. **Salvamento e recarga:** `wm.save_mainfile` e depois `wm.revert_mainfile`, com `is_dirty: false`, duas ações e a `Direita` ativa no quadro 1.
7. **Validações no arquivo recarregado:** as três deram `tudo_ok: true`:
   - [`validar_acoes.py`](scripts_fase6/validar_acoes.py);
   - [`comparar_preparacao.py`](scripts_fase6/comparar_preparacao.py) da Fase 6;
   - [`verificar_rig.py`](scripts_fase4/verificar_rig.py) da Fase 4, sem alterações.
8. **Vistas:** [`render_acoes.py`](scripts_fase6/render_acoes.py) renderizou os quadros 13 e 25 das duas ações. Depois, câmera e render foram desfeitos com `revert_mainfile`, sem salvar.

**Mudanças em `comparar_preparacao.py` em relação à Fase 5:**

- passa a exigir exatamente as duas ações, em vez de nenhuma;
- compara com o backup pré-Fase 6 (o arquivo validado na Fase 5) em vez de `bryan.blend1`, que o salvamento desta fase sobrescreveu.

O restante do script é igual.

## 3. Validação das ações

O resultado completo está em [`validacao/validacao_acoes_cabeca_fase6.json`](../validacao/validacao_acoes_cabeca_fase6.json): **`tudo_ok: true`**, no arquivo recarregado do disco.

| Verificação | Abrangência | Direita | Esquerda |
| --- | --- | ---: | ---: |
| Keyframes, interpolação, alças e extrapolação | 3 keyframes | conforme | conforme |
| Alças dos extremos horizontais (sem ultrapassar) | 3 keyframes | sim | sim |
| Curva amostrada: mínimo/máximo | 481 amostras entre 1 e 49 | −25,0000001° / 0° | 0° / 25,0000001° |
| Ida e volta monótonas | mesmas amostras | sim | sim |
| Valor fora do intervalo (quadros 0 e 60) | — | 0° | 0° |
| Deslocamento do pivô | todos os 49 quadros | 7,45e-9 m | 7,45e-9 m |
| Outros ossos, localização/escala e eixos X/Z da cabeça | todos os 49 quadros | 0,0 | 0,0 |
| Matrizes de todos os objetos | todos os 49 quadros | 0,0 | 0,0 |
| Cabeça avaliada × rotação rígida esperada em torno do pivô | todos os vértices, quadros 1/13/25/37/49 | 5,96e-8 | 5,96e-8 |
| Comprimento das arestas da cabeça | mesmos quadros | ≤ 2,65e-8 | ≤ 2,95e-8 |
| `Corpo_Kart` e rodas × NPZ original | mesmos quadros | 2,98e-8 | 2,98e-8 |
| Direção do rosto no quadro 25 | — | (−0,4226, −0,9063, 0) | (+0,4226, −0,9063, 0) |

- **Ângulos medidos nos quadros 1/13/25/37/49:** 0°, ∓12,5°, ∓25°, ∓12,5°, 0°.
- **Espelhamento:** a curva da esquerda é exatamente a negativa da direita (diferença máxima de 0° nas 481 amostras).
- **Desvios residuais:** são arredondamentos de float32 da origem deslocada, já medidos em repouso nas Fases 4 e 5 (≤ 3e-8 m na posição). O pivô (7,45e-9 m) também está abaixo da tolerância de 1e-6 m. As partes fixas não se moveram (matrizes com 0,0).
- **Ângulo de 25°:** a API devolve 25,00000012650595°, por causa da representação em ponto flutuante.

## 4. Preservação no arquivo salvo

As verificações abaixo foram feitas no arquivo recarregado, com as ações e a `Direita` ativa no quadro 1 (pose de repouso).

- **[`validacao/comparacao_preparacao_fase6.json`](../validacao/comparacao_preparacao_fase6.json): `tudo_ok: true`.**
  - Cada face e cada canto originais aparecem exatamente uma vez, e a divisão da Fase 3 está intacta.
  - UV, materiais, `sharp_*` e as três texturas empacotadas são iguais.
  - Posições ≤ 2,98e-8 m e normais ≤ 4,5e-4.
  - A comparação exata com o backup pré-Fase 6 deu `tudo_igual: true` em malhas, atributos, pesos, pais, matrizes, ossos, pose e imagens.
  - Os testes combinados (corpo + cabeça; esterço de 28° + giro) foram restaurados.
- **[`validacao/verificacao_rig_fase6.json`](../validacao/verificacao_rig_fase6.json): `tudo_ok: true`.** Inclui pesos, pivôs e testes temporários de `Head_Bone` (Y +25/−40, Z 15, X 15), `Torso_Bone`, `Root_Bone` e das quatro rodas, todos restaurados.

**O arquivo `.blend` mudou** (novas ações), por isso as validações foram refeitas sobre ele, e não herdadas da Fase 5.

## 5. Conferência visual

As imagens estão em [`vistas_fase6/acoes/`](vistas_fase6/acoes/) (16 vistas) e as folhas de contato em [`vistas_fase6/folhas/`](vistas_fase6/folhas/).

- **De frente** ([folha](vistas_fase6/folhas/acoes_frente.png)): a `Direita` vira o rosto para a direita do piloto, que é a esquerda da imagem; a `Esquerda`, para o lado oposto. A cabeça não se deforma e a gola esconde a base do pescoço.
- **Câmera do jogo, kart inteiro** ([folha](vistas_fase6/folhas/acoes_jogo_kart.png)): o pescoço fica escondido atrás da barra de luzes nos quadros 13 e 25 das duas ações.
- **Câmera do jogo atrasada 30°, ampliada** ([folha](vistas_fase6/folhas/acoes_jogo_lat30.png)): na `Esquerda` a 25°, aparece um fragmento laranja pequeno ao lado do pescoço. Na `Direita`, nada aparece.
- **De trás e do alto, ampliada** ([folha](vistas_fase6/folhas/acoes_tras_alto.png)): na `Esquerda` a 25°, aparece um fragmento laranja na gola; na `Direita`, uma fresta escura discreta.

Esses fragmentos são a limitação aceita com o limite de 25° e coincidem com o previsto na Fase 5.

**Não verificado:** não foi renderizado vídeo nem cada quadro. A reprodução na viewport pode ficar abaixo de 24 FPS, o que não altera os keyframes.

## 6. Arquivos resultantes

| Artefato | Bytes | SHA-256 |
| --- | ---: | --- |
| `blender/bryan.blend` | 110.262.030 | `b25be23be7279cb8d1bae26a4c62b18bd197b06d023a4820975348395fe43c11` |
| `backups/bryan_antes_fase6_20261016_091341.blend` | 110.263.103 | `da58cc33afdb36ecd21c49d044abe12bc63280c9c4a32e923bdda33696c81b77` |
| `validacao/validacao_acoes_cabeca_fase6.json` | — | `66c7e381d137547e8953e859b0dee089eec616a137412cdde5961cec186016c9` |
| `validacao/comparacao_preparacao_fase6.json` | — | `02de901ca872aeb87b84e39db8eb8b740a3321f003e28cb7b0f457522cf4535c` |
| `validacao/verificacao_rig_fase6.json` | — | `afcf7d638ffa7888180b16377fdf634f617c6387bdc2e4ef7fbc392faa93f07c` |

### Arquivo `bryan.blend1`

Ao salvar, o Blender substituiu `bryan.blend1` pela versão anterior. Agora ele é idêntico ao backup pré-Fase 6, conferido com `cmp`.

Com isso, a cópia byte a byte da Fase 4 (`561475c1…77460666`) deixou de existir no disco. Ela só estava no `.blend1`. Pela comparação exata da Fase 5, o conteúdo dela é idêntico ao do backup pré-Fase 5 e ao do pré-Fase 6. Nenhum dado de modelo foi perdido, mas aquele hash não pode mais ser reconferido.

## 7. Estado salvo e validações a refazer

- **Fim da fase:** a sessão está com `blender/bryan.blend` recarregado do disco, `is_dirty: false` e sem câmera de conferência. A ação ativa é a `Direita`, no quadro 1.
- **Validações a refazer:** qualquer nova alteração em `bryan.blend` invalida o hash acima e os três relatórios desta fase.
- **Fase 7:** precisa definir se as duas ações vão no GLB. O jogo não usa as ações pelo nome; `definicao_personagem.gd` só referencia `Head_Bone`.
- **Fase 8:** o limite de 25° deve ir para `giro_maximo_cabeca` na ficha do Bryan.
