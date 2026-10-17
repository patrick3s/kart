# Checkpoint — P003 — Bryan

| Campo | Estado |
| --- | --- |
| Identificador | P003 |
| Nome de exibição | Bryan |
| Pasta no repositório | `personagens/P003_bryan/` |
| Atualizado em | 16/10/2026 09:43 (-03:00) |
| Estado | **Entregue**: jogável no catálogo; todas as fases concluídas |
| Fase atual | Fase 9 — Entrega e documentação (concluída); nenhuma fase pendente |
| Tarefa atual | Nenhuma em andamento |
| Último passo confirmado | Fase 9: hashes de todos os artefatos iguais aos registrados; sessão do Blender conferida (só leitura); inspeção da Godot repetida, idêntica byte a byte; mecânicas repetidas com as 14 conclusões iguais e verdadeiras; links sem quebra; ficha, checklist, índice e [registro da entrega](registros/registro-fase9-entrega-2026-10-16.md) gravados |
| Próximo passo | Nenhuma fase pendente. Quando pedido: commit (o `.blend` e os backups passam de 100 MB) ou tratar as [pendências da entrega](registros/registro-fase9-entrega-2026-10-16.md#5-pendências-que-continuam-abertas), como ajustar o verificador do Dimi ao catálogo de três pilotos |
| Receita consultada | `documentacao/RECEITA_PERSONAGEM.md` no commit `5340930` (último que a alterou); HEAD `5d1dd29`, sem alterações locais na receita |
| Projeto Blender exclusivo | [`blender/bryan.blend`](blender/bryan.blend) |
| Estado do projeto Blender | **Rig validado com 2 ações da cabeça; exportado (não alterado nas Fases 7 a 9)** (6 partes + `Personagem_Rig`; origens nos pivôs medidos; ação ativa `Direita` no quadro 1, pose neutra) |

## Objetivo e escopo

Piloto jogável de kart, com o escopo padrão de todos os personagens:

- `Cabeca` (com pescoço), controlada por `Head_Bone`;
- `Neck_Bone` como osso intermediário;
- `Corpo_Kart`, controlado por `Torso_Bone`;
- quatro `Wheel_*` com malha exclusiva e pivô no centro;
- `Personagem_Rig` com a hierarquia `Root_Bone → Torso_Bone → Neck_Bone → Head_Bone`.

Os acessórios ficam fixos no `Corpo_Kart`: giroflex, antena, câmera, holofote, tablet, extintor, guincho, gaiola, caixas traseiras, rádio do ombro e gola.

Pedidos do usuário:

- 15/10/2026: Fases 2, 3 e 4, uma de cada vez;
- 16/10/2026: Fase 5, depois Fase 6, Fase 7, Fase 8 e Fase 9 (“inicie a fase 9 do bryan”).

Commit ou publicação dependem de novo pedido.

## Arquivos e evidências

| Item | Caminho relativo ao checkpoint | Estado ou evidência |
| --- | --- | --- |
| Ficha | [`LEIA-ME.md`](LEIA-ME.md) | Atualizada com P003.10 e [resumo da entrega](LEIA-ME.md#resumo-da-entrega) |
| Checklist | [`CHECKLIST.md`](CHECKLIST.md) | Fases 0 a 9 concluídas |
| Inventário das referências | [`referencia/LEIA-ME.md`](referencia/LEIA-ME.md) | 2 arquivos conferidos |
| Modelo de entrada | [`referencia/bryan.glb`](referencia/bryan.glb) | SHA-256 `14fcb6a4…d6cfcf2`; 986.320 v, 1.854.601 triângulos |
| Arquivo de trabalho | [`blender/bryan.blend`](blender/bryan.blend) | 110.262.030 bytes, SHA-256 `b25be23be7279cb8d1bae26a4c62b18bd197b06d023a4820975348395fe43c11` |
| Backups | [`backups/`](backups/) | Antes da edição `f116458b…`, pré-Fase 3 `5768c98f…`, pré-Fase 4 `0ffb2802…`, pré-Fase 5 `da58cc33…`, [pré-Fase 6](backups/bryan_antes_fase6_20261016_091341.blend) `da58cc33…`, [pré-Fase 7](backups/bryan_antes_fase7_20261016_092206.blend) `b25be23b…` (igual ao arquivo de trabalho) |
| Geometria original | [`backups/geometria_original.npz`](backups/geometria_original.npz) | SHA-256 `a7c55804…c9c71f` |
| Registro da Fase 6 | [`registros/registro-fase6-acoes-cabeca-2026-10-16.md`](registros/registro-fase6-acoes-cabeca-2026-10-16.md) | Decisão de 25°, eixos medidos, ações, validações, vistas, estado salvo |
| Validação das ações | [`validacao/validacao_acoes_cabeca_fase6.json`](validacao/validacao_acoes_cabeca_fase6.json) | `tudo_ok: true` (arquivo recarregado) |
| Comparação da Fase 6 | [`validacao/comparacao_preparacao_fase6.json`](validacao/comparacao_preparacao_fase6.json) | `tudo_ok: true`; igual ao backup pré-Fase 6 |
| Verificação do rig (Fase 6) | [`validacao/verificacao_rig_fase6.json`](validacao/verificacao_rig_fase6.json) | `tudo_ok: true` (script da Fase 4) |
| Vistas da Fase 6 | [`registros/vistas_fase6/`](registros/vistas_fase6/) | 16 vistas (quadros 13 e 25) e 4 folhas de contato |
| Registros anteriores | [Fase 2](registros/registro-fase2-inspecao-2026-10-15.md), [Fase 3](registros/registro-fase3-separacao-2026-10-15.md), [Fase 4](registros/registro-fase4-rig-2026-10-15.md), [Fase 5](registros/registro-fase5-validacao-2026-10-16.md) | Inspeção, separação, rig, validação e nuca |
| Registro da Fase 7 | [`registros/registro-fase7-exportacao-godot-2026-10-16.md`](registros/registro-fase7-exportacao-godot-2026-10-16.md) | Decisões de formato, conteúdo do GLB, ajustes de importação, inspeção e diferenças |
| Exportação para o jogo | [`../../jogo/personagens/bryan/bryan_kart.glb`](../../jogo/personagens/bryan/bryan_kart.glb) | 78.265.000 bytes, SHA-256 `b51c51a5d8a0bafbd1a2a87ee0e1eb2b43e4e3e82842db72d040573d48bea9e4`; [exportação](validacao/exportacao_glb_fase7.json), [conteúdo](validacao/conteudo_glb_fase7.json) |
| Inspeção na Godot | [`validacao/importacao_godot_fase7.json`](validacao/importacao_godot_fase7.json) | `tudo_ok: true`, gerado por [`inspecionar_importacao_bryan.gd`](../../jogo/ferramentas/inspecionar_importacao_bryan.gd) |
| Registro da Fase 8 | [`registros/registro-fase8-jogavel-2026-10-16.md`](registros/registro-fase8-jogavel-2026-10-16.md) | Ficha, catálogo, resultados no motor, inspeção visual, regressão, limitações e hashes |
| Registro da Fase 9 | [`registros/registro-fase9-entrega-2026-10-16.md`](registros/registro-fase9-entrega-2026-10-16.md) | Hashes, repetição das verificações, links, critérios por fase e pendências |
| Ficha do jogo | [`../../jogo/personagens/bryan/bryan.tres`](../../jogo/personagens/bryan/bryan.tres) | SHA-256 `2b847e0e…4774c0`; `raio_rodas = 0.1196`, `giro_maximo_cabeca = 25.0` |
| Mecânicas | [`validacao/validacao_mecanicas_fase8.json`](validacao/validacao_mecanicas_fase8.json) | Todas as conclusões `true`; SHA-256 `8a459289…d86d351ff`; gerado por [`validar_mecanicas_bryan.gd`](../../jogo/ferramentas/validar_mecanicas_bryan.gd) |
| Vistas da Fase 8 | [`registros/vistas_fase8/`](registros/vistas_fase8/) | 14 imagens do executável (menu, pista, lateral e nuca), por [`capturar_vistas_bryan.gd`](../../jogo/ferramentas/capturar_vistas_bryan.gd) |

## Estado das ferramentas e dos artefatos

- **Blender:** Blender MCP na sessão aberta, Blender 5.2.2 LTS. Nenhuma instância extra nem CLI.
- **Arquivo salvo versus cena aberta:** às 09:16 de 16/10, a sessão estava com `blender/bryan.blend` aberto e recarregado do disco:
  - `is_dirty: false`;
  - sem câmera de conferência;
  - ação ativa `Cabeca_Direita_Ida_e_Volta`, no quadro 1.
- **`bryan.blend1`:** agora é idêntico ao backup pré-Fase 6 (`da58cc33…`). A cópia byte a byte da Fase 4 (`561475c1…`) foi sobrescrita no salvamento desta fase. O conteúdo dela, idêntico ao dos backups pré-Fase 5 e pré-Fase 6, continua preservado.
- **Conteúdo:**
  - `Cabeca` com 41.982 v e origem no pivô `(−0.0075684, 0.0712891, 0.4941406)`;
  - `Corpo_Kart` com 771.146 v e origem em (0, 0, 0);
  - 4 `Wheel_*` com origem no centro medido;
  - `Personagem_Rig` com matriz identidade;
  - 24 FPS, intervalo 1–250, prévia 1–49.
- **Ações:** um canal em cada, `pose.bones["Head_Bone"].rotation_euler[1]`, com keyframes nos quadros 1/25/49:
  - `Cabeca_Direita_Ida_e_Volta`: 0° → −25° → 0°;
  - `Cabeca_Esquerda_Ida_e_Volta`: 0° → +25° → 0°.

  Curvas Bézier, alças `AUTO_CLAMPED`, extrapolação `CONSTANT`; `use_fake_user`; sem NLA nem drivers.
- **Orientação:** frente −Y, esquerda do piloto +X, Z para cima. Eixos locais de `Head_Bone`, reconferidos na Fase 6:
  - Y = giro horizontal (+Z mundial; positivo → rosto para +X, a esquerda do piloto);
  - Z = rolagem;
  - X = arfagem (+ inclina para trás).
- **Godot:** 4.7.2, pela CLI (`--headless` nas medições; com janela nas imagens). `bryan_kart.glb` importado (`.import` sem mudança na Fase 8). Ficha `bryan.tres` no catálogo `scripts/jogo.gd` (`f3f0fa52…f76ad0`), depois do Jake e do Dimi. `visual_kart.gd` não alterado (`73be89b8…b361db`, versão da T001). Jogo executado pelos verificadores, com entrada simulada; não jogado por uma pessoa.
- **Blender após a Fase 7:** `bryan.blend` aberto, `is_dirty: false`, quadro 1, ação ativa `Direita`; nada salvo nesta fase (hash inalterado).
- **Blender na Fase 8:** não usado nem consultado. Hash do arquivo em disco reconferido: `b25be23b…5fe43c11`.
- **Blender na Fase 9 (09:42 de 16/10, MCP, só leitura):** `bryan.blend` aberto, `is_dirty: false`, modo objeto, quadro 1, 7 objetos, 2 ações, ativa `Cabeca_Direita_Ida_e_Volta`. Nada salvo; hash em disco igual.
- **Validações a refazer:** qualquer alteração em `bryan.blend` invalida o hash e os três relatórios da Fase 6; qualquer reexportação muda o hash do GLB e exige repetir `inspecionar_importacao_bryan.gd`; qualquer mudança em `kart.gd`, `visual_kart.gd`, `camera_perseguicao.gd`, `jogo.gd`, na ficha ou no GLB exige repetir `validar_mecanicas_bryan.gd` e `capturar_vistas_bryan.gd`.

## Decisões e restrições

- **Amplitude da cabeça (usuário, 16/10):** **25°**, nas ações e no `giro_maximo_cabeca` da ficha (aplicado à inclinação no jogo; interpretação igual à do Dimi).
  - Aceitos fragmentos da nuca visíveis de perto e com a câmera do jogo atrasada 30°.
  - Na câmera do jogo por trás, o pescoço fica escondido.
- **Nomes das ações:** seguem o ponto de vista do piloto, como no Dimi (`Direita` = negativo).
- **Topo das rodas (usuário, 16/10):** aceito como está. A oscilação do contato é de 12–19 mm ao girar; essas faces ficam nas rodas.
- **Nuca (usuário, 16/10):** limitar a amplitude em vez de criar tampa.
- **Rodas divididas por faces (usuário, Fase 3):** 1.730 vértices e 1.689 arestas de costura duplicados; nenhuma face nova.
- **Pivôs:** os da Fase 4 continuam valendo; os critérios estão no registro da Fase 4.
- **Raio das rodas no jogo (Fase 8):** 0,1196, média dos quatro raios da Fase 4, porque a ficha aceita um valor único. Dianteira esquerda no chão; traseiras 0,98 mm (modelo) acima.
- **Tolerâncias:**
  - posições ≤ 1e-6 m (mundial, float64);
  - normais decodificadas ≤ 1e-3;
  - `sharp_*` idênticos;
  - rigidez e arestas da cabeça nas ações ≤ 2e-7.

  O arredondamento de float32 das coordenadas locais (≤ 3e-8 m) é esperado nas partes com origem deslocada.
- Não reaproveitar medidas, índices de ilhas ou resultados do Jake ou do Dimi como se fossem deste modelo. Na Fase 6, os scripts do Dimi foram reutilizados, mas os eixos e o sentido foram medidos no Bryan.
- Trabalhar somente no Blender já aberto, via MCP.

## Pendências e impedimentos

- **Material aguardado:** nenhum.
- **Perguntas sem resposta:** nenhuma.
- **Limitações da Fase 8:**
  - raio único: traseiras até 0,98 mm (modelo) acima do chão;
  - fresta fina entre pescoço e gola visível de perto e de lado na curva; invisível na câmera do jogo;
  - o verificador do Dimi (`validar_mecanicas_dimi.gd`) reprova `catalogo_jake_e_dimi` e `selecao_troca_e_volta` com três pilotos; as mecânicas dele continuam iguais. Não corrigido sem pedido.

## Última tentativa e resultado

- **Ação (Fase 9):**
  - conferência dos hashes do `.blend`, `.blend1`, backups, GLB, `.import`, texturas, ficha, scripts do jogo e ferramentas;
  - consulta somente de leitura à sessão do Blender;
  - `inspecionar_importacao_bryan.gd` repetido (evidência copiada e restaurada) e `validar_mecanicas_bryan.gd` repetido duas vezes com saída no rascunho;
  - conferência dos links; documentação.
- **Resultado observado:**
  - todos os hashes iguais aos registrados;
  - inspeção da importação idêntica byte a byte (`tudo_ok: true`);
  - mecânicas: 14 conclusões iguais e verdadeiras; só o instantâneo `percurso` variou (semente do ruído sorteada pela pista);
  - links sem quebra.
- **Incidentes:** nenhum. A Godot gerou `jogo/ferramentas/capturar_vistas_bryan.gd.uid`, identificador padrão do script.

## Como retomar

1. Ler este checkpoint, `CHECKLIST.md` e `LEIA-ME.md`.
2. Conferir o SHA-256 de `blender/bryan.blend` contra o registrado acima.
3. Consultar a sessão do Blender pelo MCP (`filepath`, `is_dirty`, objetos, ações) antes de agir.
4. Para revalidar, usar os comandos do [resumo da entrega](LEIA-ME.md#resumo-da-entrega), com saída no rascunho.
5. Atualizar checkpoint, checklist e ficha com estado, evidências e próximo passo consistentes.
