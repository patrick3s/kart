# P002 — Dimi

Ficha e histórico do segundo personagem do projeto. Tudo que pertence a ele fica nesta pasta; o método genérico está na [receita de personagem](../../documentacao/RECEITA_PERSONAGEM.md).

| Item | Valor |
| --- | --- |
| Identificador | P002 |
| Nome de exibição | Dimi |
| Nome de pasta | `dimi` (pasta `personagens/P002_dimi/`) |
| Criado em | 15/10/2026 |
| Objetivo | Piloto jogável (escopo padrão de todos os personagens) |
| Estado atual | **Entregue (Fases 0 a 9 concluídas)**: Dimi jogável ao lado do Jake; todas as regras medidas passam. Pendências na [entrega](#resumo-da-entrega). Sem commit |
| Veículo/acessórios | Kart nº 1 com 4 rodas; grades, mamadeira, molas e móbile com hélice ficam fixos no corpo |
| Partes independentes | `Cabeca` (com pescoço), `Corpo_Kart`, `Wheel_Front_Left/Right`, `Wheel_Rear_Left/Right`; rig `Root → Torso → Neck → Head` |
| Referência visual | [`referencia/Dimi.png`](referencia/Dimi.png) |
| Modelo 3D de entrada | [`referencia/Dimi.glb`](referencia/Dimi.glb) — malha única, 995.477 vértices |
| Arquivo de trabalho do Blender | [`blender/dimi.blend`](blender/dimi.blend) — `Cabeca`, `Corpo_Kart`, 4 `Wheel_*` e `Personagem_Rig`; pivô da cabeça `(0, −0.0105, 0.4453)` e rodas no eixo medido; ações da cabeça (SHA-256 `e28bf878…49e1`) |
| Orientação | Frente −Y, esquerda do piloto +X, Z para cima |
| Backup | [`backups/dimi_antes_da_edicao_20261015_160718.blend`](backups/dimi_antes_da_edicao_20261015_160718.blend), [`backups/dimi_antes_fase3_20261015_162824.blend`](backups/dimi_antes_fase3_20261015_162824.blend), [`backups/dimi_antes_fase4_20261015_163922.blend`](backups/dimi_antes_fase4_20261015_163922.blend), [`backups/dimi_antes_fase6_20261015_172956.blend`](backups/dimi_antes_fase6_20261015_172956.blend) e [`backups/geometria_original.npz`](backups/geometria_original.npz) |
| Exportação para o jogo | [`jogo/personagens/dimi/dimi_kart.glb`](../../jogo/personagens/dimi/dimi_kart.glb) — pose de repouso e as duas ações da cabeça, SHA-256 `2b25281b…606258b`; ficha [`dimi.tres`](../../jogo/personagens/dimi/dimi.tres) no catálogo, depois do Jake |

## Resumo da entrega

**Controles do modelo:**
- `Personagem_Rig`, com `Root_Bone → Torso_Bone → Neck_Bone → Head_Bone`.
- `Cabeca` segue `Head_Bone`, com pivô na base do pescoço `(0, −0.0105, 0.4453)`.
- `Corpo_Kart` segue `Torso_Bone`.
- Quatro `Wheel_*` com pivô no centro medido: giro em X local e esterço em Z local nas dianteiras.
- Ações `Cabeca_Direita_Ida_e_Volta` e `Cabeca_Esquerda_Ida_e_Volta`: 0° → ∓25° → 0° em 2 s, a 24 FPS.

**No jogo:**
- Ficha [`dimi.tres`](../../jogo/personagens/dimi/dimi.tres): escala 2,0, raio das rodas 0,1297 e teto da cabeça de 25°.
- Escolha no menu com ◀/▶. Na pista: W/↑ acelera; S/↓ freia e dá ré; A/D ou ←/→ esterçam; Esc volta ao menu.
- As rodas giram, invertem na ré e as dianteiras esterçam. A suspensão pende para fora da curva. A cabeça fica oposta ao corpo em todo quadro ([T001](../../jogo/tarefas/T001-cabeca-sempre-oposta.md)).

**Reproduzir as verificações** (pasta `jogo/`):

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --script res://ferramentas/inspecionar_importacao_dimi.gd
/Applications/Godot.app/Contents/MacOS/Godot --headless --path . --fixed-fps 60 --script res://ferramentas/validar_mecanicas_dimi.gd -- --saida=res://../personagens/P002_dimi/validacao/validacao_mecanicas_t001.json
/Applications/Godot.app/Contents/MacOS/Godot --path . --fixed-fps 60 --script res://ferramentas/capturar_vistas_dimi.gd -- --pasta=res://../personagens/P002_dimi/registros/vistas_t001/
```

Sem `--saida`/`--pasta`, os dois últimos comandos gravam por cima das evidências da Fase 8. As verificações do Blender (Fases 4 a 6) estão nos scripts de `registros/scripts_fase*/` e devem rodar na sessão aberta pelo MCP.

**Limitações:**
- A base da cabeça é aberta (giro limitado a 25°).
- As bolinhas das rodas passam até 2,5 cm abaixo do chão durante o giro.
- A suspensão é só visual.
- Ninguém jogou com teclado: a entrada foi simulada por script.
- O material na Godot não foi comparado com o do Blender.

Detalhes no [registro da Fase 9](registros/registro-fase9-entrega-2026-10-15.md).

## Documentos do personagem

- [Checkpoint](CHECKPOINT.md): estado atual e próximo passo para retomar o trabalho.
- [Checklist por fases](CHECKLIST.md): tarefas, dependências e critérios de conclusão.
- [Referências](referencia/LEIA-ME.md): onde colocar imagens, modelos e texturas, com o inventário dos arquivos.
- [Receita de personagem](../../documentacao/RECEITA_PERSONAGEM.md): método seguido.

## Histórico do personagem

| Etapa | O que foi feito | Resultado e referência |
| --- | --- | --- |
| P002.01 — Inicialização documental (15/10/2026) | Reserva do identificador, criação das pastas, ficha, checklist, checkpoint, guia de referências e entrada no índice da documentação; referências solicitadas | Somente documentação. Não houve modelagem, rig, exportação nem validação. [Checkpoint](CHECKPOINT.md) e [checklist](CHECKLIST.md) |
| P002.02 — Referências e projeto Blender (15/10/2026) | Inventário de `Dimi.glb` e `Dimi.png`; criação de `blender/dimi.blend` com Blender 5.2.2 LTS em segundo plano (`-b --factory-startup`, cena vazia + importador glTF padrão, sem transformações extras); conferência da abertura em outra instância isolada | Arquivo de 78,9 MB, SHA-256 `9befa956…0825bfd8`; 1 objeto de malha (995.477 v / 1.881.354 f), 1 material, 3 texturas 4K empacotadas, nenhum arquivo ausente. Valida o arquivo e o carregamento, **não** a preservação numérica da malha nem a aparência dos materiais. [Conferência](registros/conferencia-blend-inicial-2026-10-15.json) |
| P002.03 — Escopo e Fase 2 (15/10/2026) | Escopo padrão confirmado (piloto jogável: cabeça/pescoço, corpo/kart, 4 rodas). Backup byte a byte, levantamento da malha (1.040 ilhas, normais personalizadas), vistas de orientação, diagnóstico preliminar das partes, NPZ dos arrays originais e atributos `rig_original_*` | Geometria, UV, normais e materiais idênticos ao original após os atributos. Separação por ilhas parece viável, ainda não comprovada. [Registro](registros/registro-fase2-inspecao-2026-10-15.md) e [verificação](validacao/verificacao_preservacao_fase2.json) |
| P002.04 — Fase 3: separação das partes (15/10/2026) | Backup pré-Fase 3. Seleção por ilhas inteiras: rodas pelo eixo ajustado (pneu, aro, bolinhas, cubo) e cabeça por posição e cor da textura (boné, rosto, cabelo, orelhas, chupeta, pele do pescoço; gola e móbile no corpo). Separação em `Cabeca` (83 ilhas), `Corpo_Kart` (781) e `Wheel_*` (58/51/32/35); restauração das normais codificadas e remoção de texturas órfãs | Cada elemento original aparece exatamente uma vez; coordenadas e normais com desvio 0,0; UV e material iguais. Origens ainda não movidas; base da cabeça aberta (escondida pela gola). [Registro](registros/registro-fase3-separacao-2026-10-15.md) e [verificação](validacao/verificacao_separacao_fase3.json) |
| P002.05 — Fase 4: pivôs, esqueleto e pesos (15/10/2026) | Primeira fase na sessão aberta do Blender (MCP). Backup pré-Fase 4; pivô da cabeça em `(0, −0.010498, 0.4453125)` (toco do pescoço e plano em que a gola fecha); centros das rodas por círculo ajustado à banda de rodagem sem as bolinhas (raio ≈ 0,1297); `Personagem_Rig` com `Root → Torso → Neck → Head`; pesos 1,0 exclusivos (`Cabeca` → `Head_Bone`, `Corpo_Kart` → `Torso_Bone`) com o modificador Armature; rodas com parentesco de osso em `Torso_Bone` | `tudo_ok: true` no arquivo recarregado do disco; desvio mundial ≤ 6e-8 m; testes de cabeça, torso, raiz e rodas com pivô fixo, restaurados. Limitação: a borda da base aberta aparece de lado a −40°. Topologia, UV e materiais ficam para a Fase 5. [Registro](registros/registro-fase4-rig-2026-10-15.md), [medidas](validacao/medidas_pivos_fase4.json) e [verificação](validacao/verificacao_rig_fase4.json) |
| P002.06 — Fase 5: validação da preparação (15/10/2026) | Na sessão aberta do Blender (MCP), sobre o arquivo recarregado do disco: repetição de `verificar_rig.py` e novo `validar_preparacao.py`, comparando cada parte com o NPZ e com o backup pré-Fase 3; teste combinado de raiz, torso, cabeça e rodas; conferência de arquivos ausentes | `tudo_ok: true` nos dois relatórios. Cada elemento original uma vez; conectividade, UV, suavização, materiais, `custom_normal`/`sharp_*` e texturas idênticos; posições ≤ 5.96e-8 m; pivôs estáveis e partes isoladas. Arquivo não alterado (SHA-256 `229034cf…25a7d7`). Aparência renderizada e Godot não testadas; base aberta da cabeça continua pendente. [Registro](registros/registro-fase5-validacao-2026-10-15.md), [validação](validacao/validacao_preparacao_fase5.json) e [repetição do rig](validacao/verificacao_rig_fase5.json) |
| P002.07 — Fase 6, início: amplitude do giro da cabeça (15/10/2026) | Usuário escolheu limitar o giro em vez de tampar a base. Na sessão MCP: giros de 0 a ±40° em Y local de `Head_Bone`, 55 vistas (lados, câmera do jogo e em curva) e grade de raios contando interior visível da abertura; tudo desfeito com `revert_mainfile` | De lado e de frente a abertura aparece a partir de ~10°; na câmera do jogo fica escondida até ±25° (pequeno recorte em curva a ±40°). Recomendado 25°, não confirmado. `dimi.blend` não alterado (`229034cf…25a7d7`). [Registro](registros/registro-fase6-amplitude-2026-10-15.md), [medidas](validacao/amplitude_cabeca_fase6.json), [vistas](registros/vistas_fase6/) |
| P002.08 — Fase 6: ações da cabeça (15/10/2026) | Usuário confirmou 25° e 2 s a 24 FPS. Backup pré-Fase 6; `Cabeca_Direita_Ida_e_Volta` (0° → −25° → 0°) e `Cabeca_Esquerda_Ida_e_Volta` (0° → +25° → 0°) nos quadros 1/25/49, só no Y local de `Head_Bone`, `BEZIER`/`AUTO_CLAMPED`, prévia 1–49. Nomes do ponto de vista do piloto (no Jake, “direita” era +X) | `tudo_ok: true` no arquivo recarregado: pivô e partes fixas sem movimento nos 49 quadros, cabeça rígida, espelhamento exato; preparação e rig revalidados. SHA-256 `e28bf878…49e1`. Vídeo não renderizado; borda da base continua visível de lado. [Registro](registros/registro-fase6-acoes-cabeca-2026-10-15.md) e [validação](validacao/validacao_acoes_cabeca_fase6.json) |
| P002.09 — Fase 7: exportação e importação na Godot (15/10/2026) | Sessão MCP alterada só pela timeline (conferida e recarregada). GLB exportado como o Jake, com as duas ações da cabeça, para `jogo/personagens/dimi/`; importado pela CLI da Godot 4.7.2; texturas ajustadas para VRAM, `animation/fps=24` e otimizador desligado no `AnimationPlayer` (o padrão perdia o pico de 25°); verificador `inspecionar_importacao_dimi.gd` | `tudo_ok: true`: hierarquia e pivôs ≤ 3e-8 m do Blender, rodas ≤ 7e-8 m, triângulos e imagens idênticos, animações 0 → ∓25° → 0 exatas, `VisualKart.montar()` encontra ossos e rodas. `dimi.blend` não alterado. Sem ficha `.tres`, catálogo ou inspeção visual; raio das rodas pela caixa (RL 0,1429) fica para a Fase 8. [Registro](registros/registro-fase7-exportacao-godot-2026-10-15.md), [exportação](validacao/exportacao_glb_fase7.json) e [inspeção](validacao/importacao_godot_fase7.json) |
| P002.10 — Fase 8: personagem jogável e mecânicas (15/10/2026) | Ficha `dimi.tres` (raio das rodas 0,1297 e teto da cabeça 25°, campos opcionais novos na ficha) e entrada no catálogo depois do Jake; verificador `validar_mecanicas_dimi.gd` (escolha, movimento, frenagem, ré, câmera, rodas, suspensão e cabeça) e imagens renderizadas pela Godot com janela | Tudo passou, exceto a cabeça oposta em **todo** quadro: 18/15/16 quadros no mesmo lado na entrada, inversão e saída de curva, iguais aos do Jake. Sem o teto, a cabeça chegava a 32,74°. Jake sem regressão. `dimi.blend` e GLB não alterados. [Registro](registros/registro-fase8-jogavel-2026-10-15.md), [relatório](validacao/validacao_mecanicas_fase8.json) e [vistas](registros/vistas_fase8/) |
| P002.11 — T001: cabeça sempre oposta (15/10/2026) | Pedido do usuário: “corrija então a tarefa”. Em `visual_kart.gd` (comum aos pilotos), a meta da cabeça passou a usar a rolagem com o tremor, e uma faixa por quadro mantém a cabeça oposta ao corpo (0,2 a 1,0 vez a inclinação dele). A primeira tentativa, só com o limite mínimo, foi descartada por causa de um salto de 10,9° | 0 quadros no mesmo lado (antes 18/15/16 e 84 na reta com vibração), a 60 e 120 passos/s, com e sem ruído; cabeça estabilizada igual; maior variação 2,67°/quadro; teto de 25° mantido; demais regras passam; Jake sem falhas numa cópia do verificador. [Tarefa](../../jogo/tarefas/T001-cabeca-sempre-oposta.md), [relatório](validacao/validacao_mecanicas_t001.json) e [vistas](registros/vistas_t001/) |
| P002.12 — Fase 9: entrega e documentação (15/10/2026) | Hashes dos artefatos conferidos; verificadores da Godot repetidos (gravando na pasta de rascunho); 217 links conferidos; critérios das Fases 0 a 8 revisados; resumo da entrega; índice da documentação atualizado; cache `__pycache__` removido | Hashes iguais aos registrados; resultados idênticos aos relatórios da Fase 7 e da T001; nenhum link quebrado. Sem commit. [Registro](registros/registro-fase9-entrega-2026-10-15.md) |
