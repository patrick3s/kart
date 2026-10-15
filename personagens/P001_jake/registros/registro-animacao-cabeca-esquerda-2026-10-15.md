# P001.04 — Cabeça para a esquerda

Executada em **15/10/2026**, pelo **Blender MCP**, no Blender 5.2.2 LTS. Referência central: [ficha do personagem](../LEIA-ME.md).

## Resultado salvo

Arquivo: [kart_modular_rig.blend](../blender/jake.blend). Nova ação ativa: **`Cabeca_Esquerda_Ida_e_Volta`**. A ação **`Cabeca_Direita_Ida_e_Volta`** foi preservada integralmente e marcada com `use_fake_user` para continuar salva quando não estiver ativa. A nova ação também tem retenção ativada.

| Quadro | Y local de `Head_Bone` | Estado |
| ---: | ---: | --- |
| 1 | 0° | Frente |
| 25 | −40° | Esquerda do personagem |
| 49 | 0° | Retorno |

Apenas `pose.bones["Head_Bone"].rotation_euler`, índice 1, é animado. Modo Euler `XYZ`, interpolação `BEZIER`, alças `AUTO_CLAMPED` e extrapolação `CONSTANT`. Não há modificador de ciclos nem trilhas NLA. A prévia repete 1–49; fora dela, a cabeça permanece neutra depois de 49.

**30 FPS**, base 1,0, preservados da cena inspecionada. Os 48 intervalos entre os keyframes inicial e final equivalem a **1,6 segundo**. O intervalo principal de renderização permanece 1–250. O arquivo foi salvo pausado no quadro 25 para apresentar a pose da esquerda.

## Procedimento

1. Leitura do `PERSONAGEM.md` e do registro anterior, seguida de inspeção real de objetos, ossos, transformações, ações, keyframes, FPS, prévia, modificadores e pesos pelo MCP.
2. Cópia da cena aberta antes da edição: [kart_antes_animacao_esquerda_20261015.blend](../backups/kart_antes_animacao_esquerda_20261015.blend). A cópia inclui os 30 FPS e o estado aberto anterior, sem trocar o caminho do arquivo principal.
3. Conferência visual da ação da direita no quadro 25. A documentação anterior estabelece +40° como direita; o novo movimento usa −40° no mesmo eixo. A direção frontal medida na pose esquerda foi aproximadamente `(-0.642788, -0.766044, 0)`, oposta em X à pose direita documentada.
4. Duplicação da ação existente, invertendo o sinal dos valores dos keyframes e das coordenadas verticais de suas alças Bézier. Os tempos, os tipos de alça e a suavização permanecem iguais. Nenhuma nova restrição de rotação foi acrescentada.
5. Ativação da ação esquerda, validação numérica, inspeção visual no quadro 25 e salvamento do arquivo principal. Nenhum objeto, osso, origem, peso ou vértice foi editado.

## Preservação do rig e da malha

Hierarquia mantida: `Root_Bone` → `Torso_Bone` → `Neck_Bone` → `Head_Bone`.

Pivô mundial mantido em **`(0, -0.0625, 0.4375)`**, na base do pescoço. `Cabeca` permanece com 160.046 vértices e 305.705 faces, todos com peso 1,0 exclusivo em `Head_Bone`. `Corpo_Kart` permanece com 874.925 vértices e 1.662.516 faces, todos com peso 1,0 exclusivo em `Torso_Bone`. Ambos continuam filhos de `Personagem_Rig`, com o modificador `Rig_Rigido_Sem_Deformacao`.

O relatório [validacao_animacao_cabeca_esquerda.json](../validacao/validacao_animacao_cabeca_esquerda.json) contém as medições completas.

| Verificação | Abrangência | Maior diferença |
| --- | --- | ---: |
| Deslocamento do pivô | Todos os 49 quadros inteiros | 0 |
| Matrizes dos outros ossos e dos objetos | Todos os 49 quadros inteiros | 0 |
| Localização e escala de `Head_Bone` | Todos os 49 quadros inteiros | 0 |
| Coordenadas avaliadas do corpo | Todos os vértices nos quadros 1/13/25/37/49 | 0 |
| Cabeça avaliada versus transformação rígida esperada | Todos os vértices nos mesmos cinco quadros | 3,494387468272464 × 10⁻⁸ unidade |
| Comprimento das arestas da cabeça | Todas as arestas nos mesmos cinco quadros | 3,606600965273821 × 10⁻⁸ unidade |
| Curva esquerda versus negativa da direita | 481 amostras entre 1 e 49 | 0 radiano |

Ângulos medidos nos cinco quadros: aproximadamente **0°, −20°, −40°, −20°, 0°**. A curva amostrada permanece entre −40° e 0°. O comportamento é rígido, sem esticamento além dos resíduos numéricos medidos, abaixo da tolerância de `2e-7` unidade. Os hashes SHA-256 antes/depois das coordenadas-base, arestas, conectividade de faces, UVs e índices de materiais coincidem. Os valores e alças da ação direita também coincidem integralmente antes/depois.

A inspeção visual cobriu a viewport das ações direita e esquerda no quadro 25. As amostras de geometria completa são os cinco quadros descritos; não se afirma uma renderização validada de cada quadro. Não foi exportado vídeo, feito commit ou enviado conteúdo remoto.

## Como visualizar

1. Abrir `kart_modular_rig.blend`: a ação esquerda já está ativa em `Personagem_Rig`, no quadro 25.
2. Reproduzir a timeline com a prévia 1–49 ativada, usando a barra de espaço sobre a viewport.
3. Para comparar, selecionar a ação `Cabeca_Direita_Ida_e_Volta` no Editor de ações; selecionar novamente `Cabeca_Esquerda_Ida_e_Volta` para retornar ao movimento novo.

O desempenho da viewport pode ser inferior a 30 FPS. Essa limitação de prévia não altera os keyframes nem determina a velocidade de um futuro vídeo renderizado.
