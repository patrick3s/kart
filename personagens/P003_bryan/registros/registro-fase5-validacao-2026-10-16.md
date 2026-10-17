# Registro — P003 Bryan — Fase 5: validação da preparação

| Campo | Valor |
| --- | --- |
| Data | 16/10/2026, 08:50–09:05 (-03:00) |
| Pedido | “inicie a fase 5 do bryan” |
| Ferramenta | Blender 5.2.2 LTS pela sessão aberta (Blender MCP); nenhuma instância extra nem CLI |
| Arquivo validado | [`blender/bryan.blend`](../blender/bryan.blend), 110.263.103 bytes, SHA-256 `da58cc33afdb36ecd21c49d044abe12bc63280c9c4a32e923bdda33696c81b77` |
| Backup pré-Fase 5 | [`backups/bryan_antes_fase5_20261016_085401.blend`](../backups/bryan_antes_fase5_20261016_085401.blend), mesmo SHA-256 |
| Resultado | **Concluída.** `tudo_ok: true` nas duas verificações numéricas. A nuca ainda depende de uma decisão sobre o limite (seção 6) |
| Geometria alterada | Não. O `.blend` não foi salvo de novo nesta fase |

## 1. Decisões do usuário no início da fase

Elas respondem às duas perguntas deixadas na Fase 4:

- **Topo das rodas:** aceitar como está. O preenchimento do para-lama continua nas rodas, e a oscilação do contato fica registrada como limitação visual.
- **Nuca:** limitar a amplitude, em vez de criar uma tampa. O valor do limite depende das medições da seção 6.

## 2. Divergência de hash encontrada na retomada

O checkpoint da Fase 4 registrava o SHA-256 `561475c1…77460666`, mas o `bryan.blend` em disco tinha `da58cc33…96c81b77`, gravado em 15/10/2026 às 21:20:25, depois do fechamento da Fase 4 (19:59). O `bryan.blend1` mantém exatamente o hash da Fase 4.

Para investigar, os dados das 6 partes e do rig foram carregados de `bryan.blend1` e comparados com o arquivo atual por igualdade exata ([`comparar_preparacao.py`](scripts_fase5/comparar_preparacao.py), seção 3). Foram comparados:

- coordenadas, arestas, cantos, UV, suavização, material por face, `sharp_*` e `custom_normal`;
- `rig_original_*`, normais de canto e lista de atributos;
- matriz base, inversa do pai, pai e pesos;
- ossos, matriz do rig, pose, ações e o hash das texturas empacotadas.

**Resultado: tudo igual.** O salvamento das 21:20 não mudou conteúdo comparável. A diferença de hash vem de metadados ou do estado da interface do arquivo. A origem desse salvamento não foi identificada.

Houve um incidente de método nessa comparação. Na primeira execução, a `matrix_world` dos objetos anexados apareceu diferente, mas isso era um artefato: um objeto anexado fora da cena não é avaliado, e por isso a matriz volta como identidade (translação 0). A comparação passou a usar a matriz base, a inversa do pai, o pai e os ossos, que determinam a matriz mundial.

## 3. Comparação completa com o original

Os scripts usados foram [`comparar_preparacao.py`](scripts_fase5/comparar_preparacao.py), que gera o relatório [`comparacao_preparacao_fase5.json`](../validacao/comparacao_preparacao_fase5.json), e o [`verificar_rig.py`](scripts_fase4/verificar_rig.py) da Fase 4 sem alterações, que gera o relatório [`verificacao_rig_fase5.json`](../validacao/verificacao_rig_fase5.json). Os dois foram executados no arquivo recém-recarregado do disco.

As referências foram três:

- [`backups/geometria_original.npz`](../backups/geometria_original.npz), lido pelos ids `rig_original_*`;
- a divisão por faces da Fase 3, recalculada por [`rotulos_faces.py`](scripts_fase3/rotulos_faces.py);
- os `sharp_*` da malha única do backup pré-Fase 3.

| Parte | Vértices | Arestas | Faces | Cantos | Posição mundial, desvio máx. (m) | Normais fora / na costura |
| --- | --- | --- | --- | --- | --- | --- |
| `Corpo_Kart` | 771.146 | 2.209.470 | 1.439.415 | 4.318.245 | 0,0 | 0,0 / 4,5e-4 |
| `Cabeca` | 41.982 | 122.573 | 80.608 | 241.824 | 3,7e-9 | 2,9e-4 / — |
| `Wheel_Front_Left` | 41.998 | 122.585 | 80.611 | 241.833 | 3,0e-8 | 2,4e-4 / 1,2e-4 |
| `Wheel_Front_Right` | 42.702 | 124.062 | 81.386 | 244.158 | 2,6e-8 | 4,3e-4 / 2,4e-4 |
| `Wheel_Rear_Left` | 45.724 | 133.086 | 87.392 | 262.176 | 2,6e-8 | 1,3e-4 / 2,3e-4 |
| `Wheel_Rear_Right` | 44.498 | 129.664 | 85.189 | 255.567 | 1,1e-8 | 1,7e-4 / 1,1e-4 |

Itens conferidos e aprovados:

- Cada face e cada canto originais aparecem exatamente uma vez (1.854.601 faces e 5.563.803 cantos).
- A multiplicidade de vértices e arestas é a esperada: 1.730 vértices e 1.689 arestas duplicados só na costura roda/corpo, num total de 988.050 v e 2.841.440 arestas nas partes.
- As faces de cada parte coincidem com a divisão da Fase 3.
- Os ids são únicos em cada parte, e não há vértices sem aresta nem arestas sem face.
- Arestas, cantos (vértice e aresta), início e ordem das faces, UV (1 camada), suavização, material por face e `sharp_edge`/`sharp_face` são iguais ao original.
- Há 1 material (`tripo_material_…`), ligado às 3 texturas 4K empacotadas (`bryan_basecolor.jpg`, `bryan_normal.png`, `bryan_rm.jpg`).
- Cena: 24 FPS, unidade métrica, escala 1,0, sem ações.
- Os pesos são exclusivos e iguais a 1,0, e não há vértices sem peso nem com mais de um grupo.
- Os pivôs têm desvio 0 em relação às medidas da Fase 4.
- A malha avaliada em repouso tem desvio ≤ 6e-8 m.

### Arredondamentos numéricos (espaço apropriado)

- **Espaço de comparação:** mundial, em float64, contra o NPZ em float32, com tolerância de 1e-6 m.
- **Origem do arredondamento:** na Fase 4, a origem da `Cabeca` e das rodas passou para o pivô, numa grade de 1/4096 m. As coordenadas locais são float32 relativas a essa origem. Ao recompor `local + origem` e arredondar para float32, o último bit muda em parte dos vértices: 5.701 na `Cabeca`, todos nas rodas dianteiras e na traseira esquerda e 23.548 na traseira direita. O desvio máximo é 3,0e-8 m, cerca de 30 mil vezes abaixo da tolerância. O `Corpo_Kart` manteve a origem em (0, 0, 0) e continua bit a bit igual.
- **Normais:** as normais decodificadas diferem até 4,5e-4 (tolerância 1e-3), o mesmo valor já medido nas Fases 3 e 4. Isso vem da reconstrução das normais personalizadas depois da separação; não houve mudança nesta fase.

## 4. Testes temporários dos controles

Os testes vieram de [`verificacao_rig_fase5.json`](../validacao/verificacao_rig_fase5.json), que repete os da Fase 4, e da seção 4 de [`comparar_preparacao.py`](scripts_fase5/comparar_preparacao.py), com testes combinados.

| Teste | Deslocamento do pivô | Erro rígido das partes móveis | Movimento das partes fixas |
| --- | --- | --- | --- |
| `Head_Bone` Y +25° / −40° (giro) | 7e-9 | 2,3e-8 | 0,0 |
| `Head_Bone` Z +15° (rolagem) | 7e-9 | 7,6e-8 | 0,0 |
| `Head_Bone` X +15° (arfagem) | 7e-9 | 1,0e-7 | 0,0 |
| `Torso_Bone` Y +10° | 0,0 | 9,7e-8 | — |
| `Root_Bone` Z +20° | 0,0 | 1,05e-7 | — |
| Cada roda: giro X 90° e esterço Z 30° | 0,0 | — | 0,0 (outras partes) |
| **Combinado:** corpo Y 10° + cabeça Z 15° e Y −10° | pivô segue o corpo: 1,4e-9 | cabeça 1,1e-7; corpo e rodas 9,7e-8 | — |
| **Combinado:** corpo X 6° + rodas dianteiras com esterço de 28° (máximo do jogo) e giro de 120° | 3,3e-8 / 4,5e-8 | 1,7e-8 / 9,6e-9 | cabeça além do corpo: 1,6e-7 |

Os testes foram restaurados (diferença 0,0 em todas as partes) e, depois, a cena foi recarregada com `wm.revert_mainfile`.

A oscilação do contato das rodas ao girar 360° é de 12,3, 12,6, 19,5 e 15,4 mm (FL, FR, RL e RR). Ela foi aceita pelo usuário, conforme a seção 1.

## 5. Isolamento e conferência visual das rodas

- Nenhum teste moveu uma parte que deveria ficar fixa (0,0 m).
- A geometria e o rig são idênticos aos da Fase 4 (seção 2), então as vistas de [`vistas_fase4/`](vistas_fase4/) continuam válidas para este arquivo. Na roda girada a 0°, 90° e 180°, a faixa azul interna acompanha a rotação junto com a textura e não apareceu fresta na costura. O topo serrilhado passa para baixo ao girar 180°, o que foi aceito.

## 6. Nuca: medição da amplitude (decisão “limitar”)

### 6.1 Métrica numérica (inconclusiva)

O script [`nuca_amplitude.py`](scripts_fase5/nuca_amplitude.py) gerou o relatório [`nuca_amplitude_fase5.json`](../validacao/nuca_amplitude_fase5.json). Ele lança raios por BVH a partir de 36 pontos de vista (12 azimutes × 3 elevações, a 2,5 m) até os 98 vértices de borda da `Cabeca` situados até 4 cm acima do pivô.

No repouso, os 98 já aparecem de algum ponto de vista, porque a borda encosta no corpo. Com 5° de rotação em qualquer eixo, 36 a 62 desses vértices já contam como "novos expostos". A métrica não separa um deslocamento submilimétrico de uma fresta visível, então **não foi usada para definir o limite**. O relatório foi mantido como evidência.

### 6.2 Vistas renderizadas

O script [`render_nuca.py`](scripts_fase5/render_nuca.py) gerou 124 vistas em [`vistas_fase5/nuca/`](vistas_fase5/nuca/), com folhas de contato em [`vistas_fase5/folhas/`](vistas_fase5/folhas/). As vistas foram:

- **jogo:** posição da `camera_perseguicao.gd` (3,4 m atrás e 1,4 m acima, dividido pela escala 2,0 do catálogo), ampliada sobre o pescoço;
- **jogo_lat30:** a mesma câmera, girada 30° pelo atraso nas curvas;
- **tras_alto:** a direção da Fase 4;
- **lado.**

| Movimento | De trás e do alto, de perto | Câmera do jogo, atrás | Câmera do jogo com atraso de 30° |
| --- | --- | --- | --- |
| Giro Y (±10° a ±40°) | Fresta escura ou fragmento laranja na gola a partir de **±10°**, crescendo até ±40° ([folha](vistas_fase5/folhas/giro_10_15_tras_alto.png), [±20/25](vistas_fase5/folhas/giro_20_25_tras_alto.png)) | Pescoço escondido pela barra de luzes traseira até ±40° ([folha](vistas_fase5/folhas/giro_jogo.png)) | Fragmentos laranja do lado voltado à câmera a partir de cerca de **+10°**; nítidos a +25° e +40° ([folha](vistas_fase5/folhas/jogo_lat30_giro.png)) |
| Rolagem Z (±5° a ±25°) | Fresta fina já a **±5°**; pele do pescoço fora da gola a ±15° ([folha](vistas_fase5/folhas/rolagem_5_10_tras_alto.png), [±15/25](vistas_fase5/folhas/rolagem_15_25_tras_alto.png)) | Escondido até ±25° ([folha](vistas_fase5/folhas/rol_jogo.png)) | Fragmento serrilhado ao lado da cabeça a partir de cerca de **+8°** ([folha](vistas_fase5/folhas/jogo_lat30_pequenos.png)) |
| Arfagem X para trás (+) | Fresta clara atrás da orelha já a **+3°**; maior a +6°, +10° e +15° ([folha](vistas_fase5/folhas/arfagem_3_6_lado.png)) | — | Visível a +10° e +15° ([folha](vistas_fase5/folhas/jogo_lat30_rolagem_arfagem.png)) |
| Arfagem X para a frente (−) | Sem defeito a −6° e −10° ([folha](vistas_fase5/folhas/arf_lado.png)) | — | Sem defeito a −6° |

As vistas da câmera do jogo foram ampliadas cerca de 1,6× em relação a uma tela de 1080p. Os fragmentos vistos com atraso de 30° ocupariam poucos pixels no jogo, mas existem.

**Conclusão:** a borda aberta aparece com rotações bem menores do que as indicadas na Fase 4 (±40° e +15°). Só um limite de cerca de 5° em todos os eixos (e cerca de 0° de arfagem para trás) evitaria tudo nas vistas de perto. Esse limite anula a compensação de cabeça do jogo (no Dimi, o limite é 25°) e o giro das animações da Fase 6. Pela câmera de trás, nada aparece até ±40° de giro e ±25° de rolagem.

**Pendente com o usuário:** escolher o valor do limite com base nesses dados, ou reconsiderar a tampa. A decisão afeta as Fases 6 e 8, não esta. Nenhum limite foi gravado no `.blend`; o limite do jogo fica em `giro_maximo_cabeca`, na ficha da Fase 8.

## 7. Estado salvo

- Nenhuma alteração foi feita no `.blend` nesta fase. Todos os testes e vistas foram desfeitos com `wm.revert_mainfile`, e o arquivo não foi salvo de novo para preservar o hash validado.
- Ao final, a sessão estava com `blender/bryan.blend` aberto, `is_dirty: false` e 7 objetos, sem a câmera de conferência.
- No disco, o SHA-256 `da58cc33…96c81b77` foi conferido antes e depois da fase, igual ao do backup pré-Fase 5.
- Observação: chamar `is_dirty` na mesma execução logo após `wm.revert_mainfile` retornou `true`. Numa chamada seguinte, retornou `false`.

## 8. Arquivos desta fase

- **Scripts:** [`comparar_preparacao.py`](scripts_fase5/comparar_preparacao.py), [`nuca_amplitude.py`](scripts_fase5/nuca_amplitude.py), [`render_nuca.py`](scripts_fase5/render_nuca.py) e [`folha_contato.py`](scripts_fase5/folha_contato.py), executado no Python do sistema com Pillow, fora do Blender.
- **Relatórios:** [`comparacao_preparacao_fase5.json`](../validacao/comparacao_preparacao_fase5.json), [`verificacao_rig_fase5.json`](../validacao/verificacao_rig_fase5.json) e [`nuca_amplitude_fase5.json`](../validacao/nuca_amplitude_fase5.json).
- **Vistas:** [`vistas_fase5/nuca/`](vistas_fase5/nuca/) (124) e [`vistas_fase5/folhas/`](vistas_fase5/folhas/) (13).
- **Backup:** [`backups/bryan_antes_fase5_20261016_085401.blend`](../backups/bryan_antes_fase5_20261016_085401.blend).

## 9. O que não foi testado

- Importação na Godot (Fase 7) e comportamento no jogo (Fase 8).
- A aparência dos materiais em EEVEE ou Cycles: só houve Workbench com textura.
- Colisão das rodas esterçadas com o para-lama além da vista iso da Fase 4.
