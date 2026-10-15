# Jogo — projeto Godot 4.7

Abrir/rodar (pela pasta `jogo/`):

```bash
/Applications/Godot.app/Contents/MacOS/Godot --path .            # roda o jogo
/Applications/Godot.app/Contents/MacOS/Godot -e --path .         # abre no editor
```

Controles: **W/↑** acelera · **S/↓** freia e dá ré · **A/D ou ←/→** esterça · **Esc** volta à escolha de piloto.

## Estrutura

| Caminho | Função |
| --- | --- |
| `personagens/jake/jake_kart.glb` | Exportado de `../personagens/P001_jake/blender/jake.blend` (sem animações, pose de repouso) |
| `personagens/jake/jake.tres` | Ficha do piloto (`DefinicaoPersonagem`) |
| `personagens/dimi/dimi_kart.glb` | Exportado de `../personagens/P002_dimi/blender/dimi.blend` (pose de repouso + ações `Cabeca_Direita/Esquerda_Ida_e_Volta`) |
| `personagens/dimi/dimi.tres` | Ficha do Dimi: raio das rodas 0,1297 (medido na banda, sem as bolinhas) e teto da cabeça de 25° |
| `scripts/jogo.gd` | Autoload `Jogo`: catálogo de pilotos e escolha atual |
| `scripts/kart.gd` | Direção arcade (`CharacterBody3D`) |
| `scripts/visual_kart.gd` | Rodas (giro + esterço), suspensão por mola, vibração e compensação da cabeça |
| `scripts/camera_perseguicao.gd` | Câmera atrás do kart, dinâmica |
| `ferramentas/construir_cenas.gd` | Gera `cenas/*.tscn` pela linha de comando |
| `ferramentas/validar_mecanicas_dimi.gd` | Fase 8 do Dimi: escolha entre pilotos, movimento, frenagem, ré, câmera, rodas, suspensão e cabeça |
| `ferramentas/capturar_vistas_dimi.gd` | Imagens renderizadas do menu e da pista com o Dimi (precisa de janela) |
| `ferramentas/inspecionar_importacao_dimi.gd` | Confere o GLB importado do Dimi contra o Blender (ossos, pivôs, rodas, malhas, animações) |

Regenerar as cenas:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --script res://ferramentas/construir_cenas.gd
```

## Mecânica

- Rodas saem do `Torso_Bone` em tempo de execução e ficam no chão; giram por `velocidade / raio` e as dianteiras esterçam. O raio vem de `raio_rodas` na ficha ou, se for zero, da caixa da malha.
- Suspensão: `Torso_Bone` rola conforme a aceleração lateral (`giro × velocidade`). Curva para a esquerda → carroceria pende para a direita; acelerar levanta o bico, frear o abaixa. Vibração por ruído cresce com a velocidade.
- Cabeça: `Head_Bone` busca `-1,7 ×` a rolagem total (com o tremor) em relação ao corpo, com mola própria. Em todo quadro, a inclinação global da cabeça fica do lado oposto ao corpo, entre 0,2 e 1,0 vez a inclinação dele (`oposicao_minima_cabeca`/`oposicao_maxima_cabeca`). Depois vem o limite `giro_maximo_cabeca`, quando a ficha informa. Ver [T001](tarefas/T001-cabeca-sempre-oposta.md).

## Validação das regras — 15/10/2026

Auditoria pela CLI, com o GLB e os scripts reais:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --fixed-fps 60 --script res://ferramentas/validar_mecanicas_jake.gd
```

O comando grava [validacao_godot_jake.json](../personagens/P001_jake/validacao/validacao_godot_jake.json). A auditoria concluiu com **atendimento parcial**: rodas, suspensão estabilizada, movimento e câmera passaram nas medições; a cabeça não cumpre literalmente a regra de permanecer sempre oposta. Sem ruído, a 60 passos/s, foram 18 quadros no mesmo lado ao entrar na curva e 15 ao inverter. Há somente um piloto, e `Corpo_Kart` reúne torso e veículo. Não houve alteração da mecânica nem inspeção de imagens renderizadas nesta auditoria.

Consultar o [registro completo](../personagens/P001_jake/registros/registro-validacao-godot-2026-10-15.md) e o [prompt original na receita](../documentacao/RECEITA_PERSONAGEM.md#quinto-prompt--jogo-na-godot-rodas-suspensão-e-equilíbrio-da-cabeça). Código zero do comando indica que o relatório foi produzido; os resultados das regras estão no campo `conclusao`.

## Inspeção da importação do Dimi

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --import
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --script res://ferramentas/inspecionar_importacao_dimi.gd
```

Grava [importacao_godot_fase7.json](../personagens/P002_dimi/validacao/importacao_godot_fase7.json). No modo headless a Godot não detecta o uso 3D das texturas; o `.import` delas já foi ajustado para VRAM. O `dimi_kart.glb.import` usa `animation/fps=24` e o otimizador desligado em `PATH:AnimationPlayer`, para manter as 49 chaves das ações. Ver o [registro](../personagens/P002_dimi/registros/registro-fase7-exportacao-godot-2026-10-15.md).

## Validação das mecânicas do Dimi — 15/10/2026

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --fixed-fps 60 --script res://ferramentas/validar_mecanicas_dimi.gd
/Applications/Godot.app/Contents/MacOS/Godot --path . --fixed-fps 60 --script res://ferramentas/capturar_vistas_dimi.gd
```

Gravam [validacao_mecanicas_fase8.json](../personagens/P002_dimi/validacao/validacao_mecanicas_fase8.json) e as imagens em [vistas_fase8/](../personagens/P002_dimi/registros/vistas_fase8/). Com dois pilotos, a troca no menu passou a ser testada. Passaram escolha, movimento, frenagem, ré, câmera, rodas e suspensão, além da cabeça oposta em regime estabilizado. A cabeça oposta em **todo** quadro falha como no Jake: 18 quadros na entrada da curva e 15 na inversão. Corrigido depois pela tarefa [T001](tarefas/T001-cabeca-sempre-oposta.md): 0 quadros no mesmo lado nos dois pilotos. A auditoria do Jake acima descreve os scripts antes dos campos `raio_rodas`/`giro_maximo_cabeca`; com esses campos em zero, os resultados dele foram reproduzidos sem diferença. Ver o [registro](../personagens/P002_dimi/registros/registro-fase8-jogavel-2026-10-15.md).

## Novo personagem

Exportar o GLB com a mesma estrutura (osso de corpo, osso de cabeça, quatro malhas de roda com origem no centro, frente em −Y no Blender), criar outra ficha `.tres` e acrescentá-la em `scripts/jogo.gd`. Os nomes de ossos e rodas podem ser trocados na ficha.
