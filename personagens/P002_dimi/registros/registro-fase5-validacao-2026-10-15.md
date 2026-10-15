# Registro da Fase 5 — validação da preparação — P002 Dimi

Data: 15/10/2026, 17:06–17:09 (-03:00).

## 1. Pedido e escopo

O usuário pediu para iniciar a Fase 5 do Dimi. O objetivo é comprovar, no estado com rig, que a geometria original foi preservada (presença, contagens, conectividade, coordenadas, UVs, materiais, normais e texturas) e que os controles da cabeça, do corpo e das rodas funcionam com pivôs estáveis e partes isoladas. Esta fase **não altera** o arquivo de trabalho.

## 2. Ferramentas e estado inicial

- **Blender 5.2.2 LTS, sessão interativa já aberta, pelo Blender MCP** (`execute_blender_code`, `get_blendfile_summary_missing_files`). Não foi aberta outra instância nem usada a CLI.
- **Sessão ao começar:** `blender/dimi.blend` aberto, em modo Objeto, marcado como alterado. Pose em repouso, origens e rotações iguais às da Fase 4, sem ações nem câmeras; a única diferença observada foi a seleção da `Cabeca`. O arquivo foi recarregado do disco com `wm.revert_mainfile`, descartando apenas esse estado de seleção.
- **Arquivo em disco ao começar:** 109.893.282 bytes, SHA-256 `229034cfebf4fc8c63f0f3ae0cd3a0089021614a863bb5387059c0376c25a7d7`, igual ao do checkpoint.

## 3. Verificações executadas

Todas rodaram sobre o arquivo recém-recarregado do disco.

1. **Repetição da verificação do rig** — [`scripts_fase4/verificar_rig.py`](scripts_fase4/verificar_rig.py), sem alterações, com saída em [`validacao/verificacao_rig_fase5.json`](../validacao/verificacao_rig_fase5.json). O resultado da Fase 4 foi preservado em `verificacao_rig_fase4.json`.
2. **Validação completa da preparação** — novo script [`scripts_fase5/validar_preparacao.py`](scripts_fase5/validar_preparacao.py), com saída em [`validacao/validacao_preparacao_fase5.json`](../validacao/validacao_preparacao_fase5.json). Compara cada parte com `backups/geometria_original.npz`, pelos atributos `rig_original_*`, e os dados codificados com o backup pré-Fase 3 ([`backups/dimi_antes_fase3_20261015_162824.blend`](../backups/dimi_antes_fase3_20261015_162824.blend)), cuja malha única ainda tem as normais e as texturas originais. Esse backup foi anexado só na sessão e removido em seguida; o arquivo foi recarregado do disco ao final.
3. **Arquivos externos ausentes** — `get_blendfile_summary_missing_files`: nenhum.

Os dois relatórios terminaram com **`tudo_ok: true`**. A tolerância de posição é 1e-6 m.

## 4. Preservação da geometria

| Parte | Vértices | Arestas | Faces | Cantos | Posição mundial base × NPZ | Avaliada em repouso × NPZ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Cabeca` | 93.155 | 269.837 | 176.764 | 530.292 | 7.45e-9 | 5.96e-8 |
| `Corpo_Kart` | 672.481 | 1.938.683 | 1.266.983 | 3.800.949 | 0.0 | 5.96e-8 |
| `Wheel_Front_Left` | 58.232 | 168.492 | 110.318 | 330.954 | 2.98e-8 | 2.98e-8 |
| `Wheel_Front_Right` | 56.941 | 164.894 | 108.004 | 324.012 | 2.98e-8 | 2.98e-8 |
| `Wheel_Rear_Left` | 60.989 | 177.865 | 116.908 | 350.724 | 2.98e-8 | 2.98e-8 |
| `Wheel_Rear_Right` | 53.679 | 156.021 | 102.377 | 307.131 | 2.98e-8 | 2.98e-8 |
| **Total** | **995.477** | **2.875.792** | **1.881.354** | **5.644.062** | — | — |

- **Presença:** cada vértice, aresta, face e canto original aparece exatamente uma vez entre as seis partes. Os totais são iguais aos do modelo importado.
- **Conectividade:** arestas, vértices dos cantos, início, tamanho e ordem das faces iguais ao NPZ em todas as partes.
- **Malha avaliada (com o modificador Armature em repouso):** mesmas contagens, arestas e cantos da malha-base; UV igual ao NPZ.
- **UVs:** uma camada (`UVMap`), valores idênticos ao NPZ (comparação exata).
- **Suavização e materiais:** `use_smooth` e índices de material idênticos; todas as partes usam o único material, `tripo_material_e9d2c8b0-…`.
- **Dados de malha exclusivos** em cada parte; nenhuma shape key.

Os desvios de posição são arredondamento de ponto flutuante das coordenadas locais compensadas na Fase 4 (no máximo 5.96e-8 m), **não um deslocamento absolutamente zero**.

## 5. Normais

- **Dado codificado (`custom_normal`), `sharp_face` e `sharp_edge`:** idênticos aos do backup pré-Fase 3, ou seja, aos do modelo importado, em todas as partes. As malhas atuais não têm o atributo `sharp_edge`; no backup ele existe, mas todos os valores correspondentes são falsos, por isso a comparação coincide.
- **Normais de canto decodificadas × NPZ:** desvio máximo por componente de 3.97e-4 (`Cabeca`), 0.0 (`Corpo_Kart`) e até 2.30e-4 (rodas). Com o modificador ativo, no `Corpo_Kart` avaliado chega a 9.3e-4. O Blender recalcula o espaço das normais com as coordenadas locais; o dado codificado não mudou.
- O ângulo máximo calculado (≈ 0,025°–0,029° em todas as partes, inclusive no `Corpo_Kart`, cujo desvio é 0) é o limite de precisão do `arccos` em vetores de 32 bits, não uma diferença real. O critério usado é o desvio por componente.

## 6. Materiais e texturas

| Imagem | Resolução | Espaço de cor | Empacotada | SHA-256 dos dados | Igual ao backup |
| --- | --- | --- | --- | --- | --- |
| `Dimi_basecolor.jpg` | 4096×4096 | sRGB | sim | `22e9e752…995a4d` | sim |
| `Dimi_normal.png` | 4096×4096 | Non-Color | sim | `c27e3e53…935985a` | sim |
| `Dimi_rm.jpg` | 4096×4096 | Non-Color | sim | `2e73e607…146801` | sim |

O material tem as três imagens nos seus nós, e as sete ligações do grafo são iguais às do backup. Isso confirma os dados do material; **a aparência renderizada não foi comparada** nesta fase.

## 7. Controles, isolamento e pivôs

**Repetição dos testes da Fase 4** (`verificacao_rig_fase5.json`): mesmos valores da Fase 4. Pesos 1,0 exclusivos (um grupo por malha, nenhum vértice sem peso ou em dois grupos); cabeça Y +25°/−40°, Z +15°, X +15°, torso Y +10°, raiz Z +20° e cada roda (giro X 90°, esterço Z 30°), todos com pivô sem deslocamento e partes fixas paradas. Oscilação do contato no giro de 360° igual à da Fase 4 (característica da geometria).

**Teste combinado novo:** todos os controles ao mesmo tempo — raiz Z +20°, torso Y +10°, cabeça Y +25° com Z +10°, `Wheel_Front_Left` esterçada 30° e girada 90°, `Wheel_Rear_Right` girada −45°. Cada parte foi comparada com a composição rígida esperada (torso para o corpo e as rodas, mais o giro local da roda; cadeia completa para a cabeça).

| Medida | Resultado |
| --- | ---: |
| Erro em relação à composição esperada — `Cabeca` | 1.30e-7 |
| `Corpo_Kart` | 1.01e-7 |
| Rodas | ≤ 4.05e-8 |
| Pivô da cabeça × fim do `Neck_Bone` | 0.0 |
| Pivô da cabeça × pivô em repouso transformado pelo torso | 3.07e-8 |
| Centros das rodas × centros em repouso transformados pelo torso | 4.47e-8 |

Os testes foram desfeitos num bloco `finally`. A posição final é idêntica à de repouso (diferença 0,0). As rodas sem giro próprio (FR, RL) só acompanharam o torso, o que confirma o isolamento entre elas.

**Conferência visual:** não foram feitas vistas novas nesta fase. As vistas da Fase 4 ([`vistas_fase4/`](vistas_fase4/)) continuam válidas, porque o arquivo é o mesmo (hash idêntico). A limitação da base aberta da cabeça, visível de lado no giro de −40°, continua.

## 8. Arquivo resultante

- O `dimi.blend` **não foi alterado nem salvo** nesta fase. Depois das verificações, a sessão foi recarregada do disco (`is_dirty: false`, 7 objetos, 6 malhas, 3 imagens, 1 material, nenhuma biblioteca anexada).
- **Arquivo em disco ao terminar:** 109.893.282 bytes, SHA-256 `229034cfebf4fc8c63f0f3ae0cd3a0089021614a863bb5387059c0376c25a7d7`, igual ao da Fase 4. Por isso, os relatórios desta fase valem para esse arquivo.

| Artefato | SHA-256 |
| --- | --- |
| `validacao/validacao_preparacao_fase5.json` | `7a22e16b88e4034fc9436925703eee094a5a4dc7baa32080c57748cadbe5ddc5` |
| `validacao/verificacao_rig_fase5.json` | `02dc1cec6f9b0d6af33adea8ff2600182e90f0f9482cd2a886bec46678cba89d` |
| `registros/scripts_fase5/validar_preparacao.py` | `dd6c8ff0421aeb4fd0628ad9985c5bdf7fb2e15245ec709ffc8f1d680482521b` |

## 9. O que não foi testado e pendências

- Aparência renderizada dos materiais, exportação e comportamento na Godot (Fases 7 e 8).
- **Base aberta da cabeça:** continua aguardando decisão do usuário (aceitar, limitar o giro na Fase 6 ou criar uma tampa, o que altera a topologia e invalida estes relatórios).
- **Raio das rodas no jogo:** `visual_kart.gd` calcula o raio pela caixa da malha; na RL as bolinhas levam o valor a ≈ 0,143, contra 0,1297 medido.
- Qualquer mudança em malhas, origens, ossos, pesos ou materiais invalida o hash e os dois relatórios desta fase.
