# Registro — Fase 7 — exportação e importação na Godot — P003 Bryan

Data: 16/10/2026, 09:20–09:25 (−03:00). Ferramentas: Blender 5.2.2 LTS pela sessão aberta (MCP) e Godot 4.7.2.stable pela CLI (`--headless`). Pedido do usuário: “inicie a fase 7 do bryan”. Procedimento: o mesmo do [Dimi](../../P002_dimi/registros/registro-fase7-exportacao-godot-2026-10-15.md); todas as medidas abaixo são do Bryan.

## 1. Estado de entrada

- `blender/bryan.blend` em disco com SHA-256 `b25be23be7279cb8d1bae26a4c62b18bd197b06d023a4820975348395fe43c11`, igual ao do checkpoint.
- Sessão do Blender: esse arquivo aberto, `is_dirty: false`, modo objeto, quadro 1, ação ativa `Cabeca_Direita_Ida_e_Volta`. Objetos, ações e as três imagens empacotadas conferem com o checkpoint. Não foi preciso recarregar.
- Backup pré-Fase 7: [`backups/bryan_antes_fase7_20261016_092206.blend`](../backups/bryan_antes_fase7_20261016_092206.blend), cópia byte a byte (mesmo hash `b25be23b…`).

## 2. Decisões de formato

| Item | Decisão | Motivo |
| --- | --- | --- |
| Formato | GLB (glTF 2.0 binário), texturas embutidas | Mesmo formato dos GLBs do Jake e do Dimi |
| Destino | `jogo/personagens/bryan/bryan_kart.glb` | Nome de pasta do personagem; arquivo segue `jake_kart.glb` e `dimi_kart.glb` |
| Pose | Repouso, quadro 1, `export_rest_position_armature` | A mecânica do jogo parte da pose de repouso |
| Ações | As duas ações da cabeça vão como animações (`export_animation_mode=ACTIONS`, começando em 0 s) | Como no Dimi: ficam num `AnimationPlayer` sem autoplay e não interferem no `visual_kart.gd`, que controla os ossos por código. Para tirá-las, reexportar com `export_animations=False` |
| Atributos | Sem tangentes (a Godot gera), sem atributos personalizados (`rig_original_*` ficam só no Blender), sem cores de vértice | Iguais aos GLBs anteriores |

Script: [`scripts_fase7/exportar_glb.py`](scripts_fase7/exportar_glb.py) (cópia do script do Dimi com o nome do arquivo trocado). Opções e hash: [`exportacao_glb_fase7.json`](../validacao/exportacao_glb_fase7.json). O `.blend` não foi salvo; o quadro e a ação ativa foram restaurados (`is_dirty: false` ao final).

## 3. Conteúdo do GLB (lido do arquivo)

Leitor: [`scripts_fase7/ler_glb.py`](scripts_fase7/ler_glb.py). Resumo: [`conteudo_glb_fase7.json`](../validacao/conteudo_glb_fase7.json).

- 78.265.000 bytes, SHA-256 `b51c51a5d8a0bafbd1a2a87ee0e1eb2b43e4e3e82842db72d040573d48bea9e4`.
- Nós: `Personagem_Rig` → `Cabeca`, `Corpo_Kart` (com skin) e `Root_Bone → Torso_Bone → Neck_Bone → Head_Bone`; as quatro `Wheel_*` são filhas de `Torso_Bone`, sem skin. Mesma organização do Jake e do Dimi.
- Skin `Personagem_Rig` com as juntas `[Root, Torso, Neck, Head]`.
- Triângulos iguais ao Blender, objeto por objeto: `Cabeca` 80.608, `Corpo_Kart` 1.439.415, FL 80.611, FR 81.386, RL 87.392, RR 85.189 — total 1.854.601, igual ao `referencia/bryan.glb`.
- 1 material (`tripo_material_1db849c3…`) com base color, normal e metallic/roughness. As três imagens embutidas são **idênticas byte a byte** às empacotadas no `.blend`: `bryan_basecolor` `3fe7ee02…`, `bryan_normal` `3831547e…`, `bryan_rm` `8d404a8e…`.
- Aviso do exportador: “More than one shader node tex image used for a texture”. É o mesmo caso do Dimi: `bryan_rm.jpg` alimenta metal e rugosidade; amostrador único, sem efeito no resultado.
- Animações `Cabeca_Direita_Ida_e_Volta` e `Cabeca_Esquerda_Ida_e_Volta`: em cada uma, a rotação de `Head_Bone` tem 49 amostras lineares de 0 a 2 s, com −25,000002° / +25,000002° em 1,0 s e componentes X/Z do quaternion ≤ 3e-8. Os demais canais são constantes, com 2 chaves `STEP`.

## 4. Importação na Godot

`Godot --headless --path jogo --import`. A primeira importação produziu exatamente as mesmas diferenças que o Dimi teve em relação ao estado final dele, e os mesmos ajustes foram aplicados:

1. **Texturas:** de `compress/mode=0` e `detect_3d/compress_to=1` (sem detecção de uso 3D no modo headless) para VRAM (`compress/mode=2`, S3TC/BPTC) e `detect_3d/compress_to=0`. Na normal, `compress/normal_map=1`, `roughness/mode=1` e `roughness/src_normal` apontando para a própria normal do Bryan.
2. **FPS das animações:** `animation/fps=30` → `24`, para não reamostrar as 49 amostras.
3. **Otimizador:** `_subresources.nodes."PATH:AnimationPlayer".optimizer/enabled=false`, a opção que funcionou no Dimi.

Depois da reimportação, os blocos `[params]` dos quatro `.import` são idênticos aos do Dimi, exceto pelo caminho de `roughness/src_normal`. Nenhum erro ou aviso na saída da importação.

## 5. Inspeção do recurso importado

Verificador: [`jogo/ferramentas/inspecionar_importacao_bryan.gd`](../../../jogo/ferramentas/inspecionar_importacao_bryan.gd), adaptado do verificador do Dimi trocando só as constantes (valores medidos no `bryan.blend`) e o nome. Relatório: [`importacao_godot_fase7.json`](../validacao/importacao_godot_fase7.json) com `tudo_ok: true`.

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --script res://ferramentas/inspecionar_importacao_bryan.gd
```

| Verificação | Resultado |
| --- | --- |
| Árvore | `Personagem_Rig/Skeleton3D` com `Cabeca` e `Corpo_Kart` (skin) e `BoneAttachment3D` `Torso_Bone` com as quatro rodas; `AnimationPlayer` sem autoplay; um `PhysicalBoneSimulator3D` criado automaticamente pela Godot |
| Ossos | 4, hierarquia `Root → Torso → Neck → Head`; origens comparadas com o Blender convertido (x, z, −y): desvio máximo 3,33e-8 m; pose igual ao repouso |
| Pivô da cabeça | `(−0.0075684, 0.4941407, −0.0712891)` no espaço Godot = `(−0.0075684, 0.0712891, 0.4941406)` no Blender, o pivô medido na Fase 4 |
| Rodas | Origem de cada roda ≤ 7,03e-8 m da origem do Blender; sem skin; filhas do `BoneAttachment3D` de `Torso_Bone` |
| Malhas | Triângulos iguais ao Blender em cada objeto; 1 superfície e 1 `StandardMaterial3D` com albedo, normal, metallic e roughness em `res://personagens/bryan/` |
| Animações | 2 animações de 2,0 s, sem loop, cada uma com uma única trilha (rotação de `Head_Bone`) e 49 chaves; giro só em Y (X e Z = 0); 0 → ∓25,0° → 0. Nos quadros 1, 7, 13…49 os valores coincidem com a curva Bézier do Blender (diferença ≤ 1e-5°) |
| Montagem com o código do jogo | `VisualKart.montar()` com uma ficha `DefinicaoPersonagem` **só em memória** encontrou `Torso_Bone` (1), `Head_Bone` (3) e as 4 rodas |

## 6. Diferenças em relação ao Blender

- **Vértices:** a Godot divide vértices nas costuras de UV e de normais. `Cabeca`: 41.982 nos dois. `Corpo_Kart`: 771.669 na Godot contra 771.146 no Blender. Rodas: FL 42.002/41.998, FR 42.709/42.702, RL 45.728/45.724, RR 44.501/44.498. Os triângulos são iguais.
- **Eixos:** Blender Z para cima e frente −Y; glTF/Godot Y para cima e frente +Z. O jogo gira o modelo em 180° (`visual_kart.gd`), como faz com o Jake e o Dimi. A rotação Y local de `Head_Bone` vira rotação em Y na Godot, com o mesmo sinal (direita do piloto = negativo).
- **Interpolação:** no Blender a curva é Bézier; na Godot são 49 chaves lineares a 24 FPS. Os valores coincidem nas chaves, e entre elas a interpolação é linear.
- **Raio das rodas:** `visual_kart.gd` calcula o raio pela caixa da malha: FL 0,1261, FR 0,1270, RL 0,1248 e RR 0,1247. Na Fase 4 foram medidos 0,1193, 0,1195, 0,1198 e 0,1199, na banda de rodagem. A caixa fica 4–6% maior por causa do preenchimento do para-lama no topo das rodas (limitação aceita na Fase 5). Isso altera a velocidade de giro e a altura de apoio (`base`). Na Fase 8, a ficha deve informar `raio_rodas`, como fez a do Dimi; o código do jogo não foi alterado.
- **Material:** o `Principled BSDF` virou `StandardMaterial3D`. A aparência não foi conferida visualmente: o modo headless usa um renderizador simulado, e nenhuma captura foi feita.

## 7. O que não foi feito

- Não foi criada ficha `.tres` nem houve entrada no catálogo `scripts/jogo.gd`; isso pertence à Fase 8. Cenas e scripts do jogo não foram alterados.
- Não houve inspeção visual na Godot, execução do jogo nem teste de mecânicas.
- Não houve commit.

## 8. Artefatos

| Arquivo | SHA-256 |
| --- | --- |
| `jogo/personagens/bryan/bryan_kart.glb` | `b51c51a5d8a0bafbd1a2a87ee0e1eb2b43e4e3e82842db72d040573d48bea9e4` |
| `jogo/personagens/bryan/bryan_kart.glb.import` | `60fcdbec…1db444` |
| `jogo/personagens/bryan/bryan_kart_bryan_basecolor.jpg` (extraída pela Godot) | `3fe7ee02…ec2a5e` |
| `jogo/personagens/bryan/bryan_kart_bryan_normal.png` (extraída pela Godot) | `3831547e…623396` |
| `jogo/personagens/bryan/bryan_kart_bryan_rm.jpg` (extraída pela Godot) | `8d404a8e…efb817a` |
| `jogo/ferramentas/inspecionar_importacao_bryan.gd` | `c3cbd010…7e37f0` |
| `blender/bryan.blend` (origem, não alterado) | `b25be23b…fe43c11` |

Qualquer reexportação muda o hash do GLB e exige repetir o verificador. Mudanças no `.blend` invalidam também os relatórios `*_fase6.json`.
