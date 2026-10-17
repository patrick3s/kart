# PI001 — Checkpoint

Atualizado em 16/10/2026, após a integração na Godot.

- **Estado:** pista integrada e jogável no menu existente, com Jake, Dimi e Bryan.
- **Modelo original:** [`blender/primeira_pista.blend`](blender/primeira_pista.blend), preservado com o mesmo SHA-256 da leitura inicial. Referência JPG também preservada. Exportação e inspeção executadas pelo Blender MCP.
- **Cena:** [`jogo/pistas/primeira_pista/primeira_pista.tscn`](../../jogo/pistas/primeira_pista/primeira_pista.tscn). No menu, selecionar “PI001 — Primeira pista” e “Jogar”. A arena antiga continua na opção “Arena de testes”.
- **Recursos:** `primeira_pista.glb`, `percurso.json`, `percurso.gd`, `primeira_pista.gd`, `superficie.gdshader` e respectivos metadados Godot em `jogo/pistas/primeira_pista/`.
- **Implementado:** colisões estáticas para asfalto, zebras e terreno; eixo real fechado com 1.000 pontos; largada pela tangente em duas colunas; IA com antecipação, frenagem e contorno dentro da pista; configuração antes de `_ready()`; inclusão no gerador de cenas.
- **Validado por código:** importação e scripts headless, controles, zebras/retorno do gramado, contato dos pneus, colisões entre karts, regressões dos três personagens e regeneração equivalente das quatro cenas.
- **IA:** 5 adversários × 3 escolhas de jogador concluíram pelo menos uma volta cada, a 60 Hz; 0 quadros fora do asfalto e 0 em contramão nos ensaios finais; primeiras voltas entre 84,10 e 91,82 s. As tentativas iniciais com falhas foram guardadas separadamente.
- **Conferido visualmente:** capturas do viewport real Metal / Forward+ com menu, largada, escala, materiais, HDRI, câmera, movimento e vistas laterais dos pneus dos três personagens. Os comandos foram exercitados por Input automatizado; sem pilotagem manual de volta completa.
- **Evidências:** [`validacao/integracao_20261016/RELATORIO.md`](validacao/integracao_20261016/RELATORIO.md), JSONs, telemetria por segundo, PNGs, logs, hashes e cópias de preservação. Ferramentas: `validar_pi001.gd`, `validar_contato_pi001.gd` e `capturar_pi001.gd` em `jogo/ferramentas/`.
- **Preservação:** alterações anteriores registradas em status/diff; arena e kart comparados ao estado inicial; rigs, modelos dos personagens e câmera compartilhada preservados. Relatórios históricos não foram regravados. A queda/reabertura do Blender e a recuperação do original por hash estão documentadas no relatório.
- **Limitações:** escala/sentido/largada provisórios; material equivalente, sem bake exato; suspensão visual e penetração dos pneus de cerca de 6–10 mm; validação não cobre colisões arbitrárias ou sessões longas.
- **Pendências de produto:** aprovação artística/medidas definitivas, cenário e regras de corrida (classificação, cronômetro e checkpoints). Nenhuma etapa técnica bloqueada para jogar a integração entregue.
- **Barreiras (16/10/2026):** 657 módulos nas duas bordas (Blender e Godot), com colisão contida em 96/96 batidas; IA inalterada. Ver LEIA-ME.
- **Barreiras na borda (17/10/2026):** as barreiras foram encostadas na zebra (`AFASTAMENTO` de 5,13 m, face a 4,8 m), com 319 + 338 módulos. Validação com 96/96 batidas contidas e 5/5 IAs completando a volta sem sair do asfalto. Ver [`validacao/barreiras_20261017/RELATORIO.md`](validacao/barreiras_20261017/RELATORIO.md).
- **Próxima etapa:** experimentar a PI001 e definir ajustes de ritmo, direção artística e regras da corrida mantendo este traçado e as evidências.
