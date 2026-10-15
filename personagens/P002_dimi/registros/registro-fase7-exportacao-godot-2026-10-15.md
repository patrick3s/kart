# Registro — Fase 7 — exportação e importação na Godot — P002 Dimi

Data: 15/10/2026 (−03:00). Ferramentas: Blender 5.2.2 LTS pela sessão aberta (MCP) e Godot 4.7.2.stable pela CLI (`--headless`). Pedido do usuário: “inicie a fase 7 do dimi”.

## 1. Estado de entrada

- `blender/dimi.blend` em disco com SHA-256 `e28bf87840fa0f2c5a42f486e7727d8aca15606e11ab7ebb1927cd647cd649e1`, igual ao do checkpoint.
- O Blender aberto mostrava esse arquivo com `is_dirty: true` e a timeline no quadro 48 (o arquivo foi salvo no quadro 1). Antes de descartar, `verificar_rig.py` e `validar_acoes.py` rodaram na cena aberta, sem salvar: as ações estavam idênticas (`tudo_ok: true`). O rig só falhou porque a cabeça estava levemente girada pela ação ativa no quadro 48 (desvio ≤ 3,9e-4 m, `pose_em_repouso: false`). Com isso, a única alteração pendente era a posição da timeline. A sessão foi recarregada do disco (`revert_mainfile`) e ficou no quadro 1, com `is_dirty: false`.

## 2. Decisões de formato

| Item | Decisão | Motivo |
| --- | --- | --- |
| Formato | GLB (glTF 2.0 binário), texturas embutidas | Mesmo formato e estrutura do Jake (`jake_kart.glb`) |
| Destino | `jogo/personagens/dimi/dimi_kart.glb` | Nome de pasta do personagem; nome do arquivo segue `jake_kart.glb` |
| Pose | Repouso, quadro 1, `export_rest_position_armature` | Mecânica do jogo parte da pose de repouso |
| Ações | As duas ações da cabeça vão como animações (`export_animation_mode=ACTIONS`, deslocadas para começar em 0 s) | O Jake saiu sem animações. Aqui elas ficam num `AnimationPlayer` sem autoplay e não interferem no `visual_kart.gd`, que controla os ossos por código. Se não forem desejadas, basta reexportar com `export_animations=False` |
| Atributos | Sem tangentes (a Godot gera), sem atributos personalizados (`rig_original_*` ficam só no Blender), sem cores de vértice | Iguais ao GLB do Jake |

Script: [`scripts_fase7/exportar_glb.py`](scripts_fase7/exportar_glb.py). Opções e hash: [`exportacao_glb_fase7.json`](../validacao/exportacao_glb_fase7.json). O `.blend` não foi salvo; a ação ativa e o quadro foram restaurados (`is_dirty: false` ao final).

## 3. Conteúdo do GLB (lido do arquivo)

- 76.802.648 bytes, SHA-256 `2b25281baee6a9bd1f123267bd2a3278ba426a2c2a177a725d4cb8e7e606258b`.
- Nós: `Personagem_Rig` → `Cabeca`, `Corpo_Kart` (com skin) e `Root_Bone → Torso_Bone → Neck_Bone → Head_Bone`; as quatro `Wheel_*` são filhas de `Torso_Bone`, sem skin. Mesma organização do Jake.
- Skin `Personagem_Rig` com as juntas `[Root, Torso, Neck, Head]`.
- Triângulos: 1.881.354 (5.644.062 índices), igual ao Blender, objeto por objeto.
- 1 material com base color, normal e metallic/roughness. As três imagens embutidas são **idênticas byte a byte** às empacotadas no `.blend` (`22e9e752…`, `c27e3e53…`, `2e73e607…`).
- Aviso do exportador: “More than one shader node tex image used for a texture”. A mesma imagem `Dimi_rm.jpg` alimenta metal e rugosidade pelo `Separate Color`; o amostrador é único, sem efeito no resultado.
- Animações: `Cabeca_Direita_Ida_e_Volta` e `Cabeca_Esquerda_Ida_e_Volta`, cada uma com 49 amostras lineares de 0 a 2 s na rotação de `Head_Bone` (−25,0° / +25,0° exatos em 1,0 s). Os demais canais são constantes, com 2 chaves `STEP`.

## 4. Importação na Godot

`Godot --headless --path jogo --import`. Ajustes na importação, todos em `dimi_kart.glb.import` e nos `.import` das texturas:

1. **Texturas.** No modo headless a Godot não faz a detecção de uso 3D e deixou as três texturas sem compressão (`compress/mode=0`, `detect_3d/compress_to=1`). Elas foram ajustadas para o estado final do Jake: VRAM (`compress/mode=2`, S3TC/BPTC), `detect_3d/compress_to=0` e, na normal, `compress/normal_map=1` com `roughness/mode=1`.
2. **FPS das animações.** O padrão `animation/fps=30` reamostra as amostras de 24 FPS e perde o pico (−24,8987°). Foi trocado para `animation/fps=24`.
3. **Otimizador.** Mesmo a 24 FPS, o otimizador de animação removia as chaves de 0,5 s, 1,0 s e 1,5 s, ficando com 46 chaves e pico de −24,8734°. A opção por animação (`_subresources.animations.<nome>.optimizer/enabled`) **não teve efeito**. O que funcionou foi a opção no nó: `_subresources.nodes."PATH:AnimationPlayer".optimizer/enabled=false`. Para isolar a causa, um teste com `GLTFDocument` puro gerou as 49 chaves exatas. As tentativas intermediárias (opções por animação e `remove_immutable_tracks=false`) foram desfeitas e o `.import` ficou com o bloco `_subresources` mínimo.

## 5. Inspeção do recurso importado

Verificador: [`jogo/ferramentas/inspecionar_importacao_dimi.gd`](../../../jogo/ferramentas/inspecionar_importacao_dimi.gd). Relatório: [`importacao_godot_fase7.json`](../validacao/importacao_godot_fase7.json) com `tudo_ok: true`.

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --script res://ferramentas/inspecionar_importacao_dimi.gd
```

| Verificação | Resultado |
| --- | --- |
| Árvore | `Personagem_Rig/Skeleton3D` com `Cabeca` e `Corpo_Kart` (skin) e `BoneAttachment3D` `Torso_Bone` com as quatro rodas; `AnimationPlayer` sem autoplay; um `PhysicalBoneSimulator3D` criado automaticamente pela Godot |
| Ossos | 4, hierarquia `Root → Torso → Neck → Head`; origens comparadas com o Blender convertido (x, z, −y): desvio máximo 2,98e-8 m; pose igual ao repouso |
| Pivô da cabeça | `(0, 0.4453125, 0.010498)` no espaço Godot = `(0, −0.010498, 0.4453125)` no Blender |
| Rodas | Origem de cada roda ≤ 6,7e-8 m da origem do Blender; sem skin; filhas do `BoneAttachment3D` de `Torso_Bone` |
| Malhas | Triângulos iguais ao Blender em cada objeto; 1 superfície e 1 `StandardMaterial3D` com albedo, normal, metallic e roughness em `res://personagens/dimi/` |
| Animações | 2 animações de 2,0 s, sem loop, cada uma com uma única trilha (rotação de `Head_Bone`) e 49 chaves; giro só em Y (X e Z = 0); 0 → ∓25,0° → 0; diferença para o GLB ≤ 1,3e-6° e igual à curva do Blender nos quadros 1, 7, 13…49 |
| Montagem com o código do jogo | `VisualKart.montar()` com uma ficha `DefinicaoPersonagem` **só em memória** encontrou `Torso_Bone` (1), `Head_Bone` (3) e as 4 rodas |

## 6. Diferenças em relação ao Blender

- **Vértices:** a Godot divide os vértices nas costuras de UV e de normais. `Cabeca` tem 93.157 vértices na Godot e 93.155 no Blender; `Corpo_Kart`, 673.053 e 672.481. As rodas têm a mesma contagem. Os triângulos são iguais.
- **Eixos:** Blender Z para cima e frente −Y; glTF/Godot Y para cima e frente +Z. O jogo gira o modelo em 180° (`visual_kart.gd`), como faz com o Jake. A rotação Y local de `Head_Bone` no Blender vira a rotação em Y na Godot, com o mesmo sinal (direita do piloto = negativo).
- **Interpolação:** no Blender a curva é Bézier; na Godot são 49 chaves lineares a 24 FPS. Os valores coincidem nas chaves, e entre elas a interpolação é linear.
- **Raio das rodas:** `visual_kart.gd` calcula o raio pela caixa da malha: FL 0,1372, FR 0,1310, RL 0,1429 e RR 0,1309, contra 0,1297 medido na Fase 4. As bolinhas inflam a RL em cerca de 10%. Isso altera a velocidade de giro e a altura em que o modelo é apoiado (`base`). É pendência da Fase 8; o código do jogo não foi alterado.
- **Material:** o `Principled BSDF` virou `StandardMaterial3D`. A aparência não foi conferida visualmente: o modo headless usa um renderizador simulado e nenhuma captura foi feita.

## 7. O que não foi feito

- Não foi criada ficha `.tres` nem houve entrada no catálogo `scripts/jogo.gd`, que pertencem à Fase 8. Cenas e scripts do jogo não foram alterados.
- Não houve inspeção visual na Godot, execução do jogo nem teste de mecânicas.
- Não houve commit.

## 8. Artefatos

| Arquivo | SHA-256 |
| --- | --- |
| `jogo/personagens/dimi/dimi_kart.glb` | `2b25281baee6a9bd1f123267bd2a3278ba426a2c2a177a725d4cb8e7e606258b` |
| `jogo/personagens/dimi/dimi_kart.glb.import` | `487777e7…19a711a0` |
| `jogo/personagens/dimi/dimi_kart_Dimi_basecolor.jpg` (extraída pela Godot) | `22e9e752…af995a4d` |
| `jogo/personagens/dimi/dimi_kart_Dimi_normal.png` (extraída pela Godot) | `c27e3e53…6935985a` |
| `jogo/personagens/dimi/dimi_kart_Dimi_rm.jpg` (extraída pela Godot) | `2e73e607…a0a10260` |
| `blender/dimi.blend` (origem, não alterado) | `e28bf878…cd649e1` |

Qualquer reexportação muda o hash do GLB e exige repetir o verificador. Mudanças no `.blend` invalidam também os relatórios `*_fase6.json`.
