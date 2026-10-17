# PI001 — Integração jogável na Godot

Data: 16/10/2026. Godot 4.7.2; física a 60 Hz. Capturas com Metal / Forward+ no Apple M1 Pro.

## Resultado

PI001 disponível no menu como pista padrão, com Jake, Dimi e Bryan. Arena histórica disponível no seletor. Cinco adversários seguem o eixo real, no mesmo sentido da largada. As três escolhas de jogador foram executadas: 15 voltas individuais concluídas no total, sem saída do asfalto nem contramão nos ensaios finais.

## Exportação e preservação

- Blender MCP usado para inspecionar a cena e executar `registros/exportar_godot.py`. Exportação em cena temporária a partir do arquivo salvo, com sete malhas: asfalto, duas zebras, duas linhas laterais, quadriculado e gramado.
- Câmeras, luzes de apresentação, referência e curva de edição ficaram fora do GLB. A curva foi exportada separadamente para `percurso.json`, com 1.000 pontos, erro máximo de 0 m contra `tracado_extraido.json`.
- Conversão Blender `(x,y,z)` → Godot `(x,z,-y)`, em metros e escala 1:1. Topo do asfalto em Y=0,10; zebra em Y=0,145; gramado em Y=−0,10.
- Asfalto e grama usam equivalentes procedurais em `superficie.gdshader`: ruído por posição mundial, variação de cor e rugosidade. Não se trata de um bake idêntico do relevo do Blender. Zebras e tintas mantêm materiais PBR do glTF.
- A instância do Blender ficou indisponível durante a preparação e foi reaberta. Detectou-se uma mudança no arquivo salvo durante essa interrupção; a versão encontrada foi guardada em `fonte_apos_reabertura_blender.blend`, e o original foi recuperado da cópia `.blend1` cujo hash coincidia com a leitura inicial. A exportação final usa esse original. Os hashes finais do `.blend` e JPG são idênticos aos anteriores à tarefa: ver `originais_sha256.json`, `exportacao_blender.json` e `regeneracao_e_preservacao.json`.
- Git status e diff anteriores estão em `git_status_antes.txt` e `alteracoes_antes.patch`. Cena da arena e cena do kart foram comparadas ao conteúdo anterior, preservando suas mudanças existentes. Relatórios históricos dos personagens não foram sobrescritos.

## Implementação

- `jogo/pistas/primeira_pista/primeira_pista.tscn` contém o modelo, quatro corpos estáticos de colisão por triângulos (asfalto, zebras e terreno), percurso, jogador, câmera, HUD e o ambiente HDRI existente.
- `percurso.gd` cria uma Curve3D fechada pela repetição do primeiro ponto e define grid de duas colunas com 2,5 m entre centros e 7 m entre filas, alinhado à tangente da reta. Distância mínima inicial entre centros: 2.50 m.
- `kart_ia.gd` conserva o modo circular quando `percurso` é nulo. Na PI001, usa projeção no eixo, alvo à frente, antecipação da curvatura em até 40 m, limite de velocidade, espaçamento ao longo da curva e mudança de faixa diante de um kart parado. Não persegue presas fora da via. Percurso, faixa, definição, velocidade e transform são configurados antes de `add_child()`.
- Limite das IAs de 18 m/s nas retas e redução conforme a curva. Jogador mantém os 22 m/s existentes. As colisões entre karts continuam usando os impulsos e efeitos anteriores.
- `Kart.altura_degrau` é zero por padrão. A PI001 habilita 0,28 m para transpor zebras e retornar do gramado, cujo desnível até o asfalto é de 20 cm. A verificação ignora karts e só eleva se o movimento estiver livre na altura testada. A geometria/escala do modelo não foi alterada.
- `construir_cenas.gd` gera também a PI001 e o seletor. Uma segunda regeneração reproduziu as quatro cenas, desconsiderando apenas os `unique_id` que o editor atribui novamente.

## Medições por código

Importação headless e geração concluíram sem erros nos logs finais. `validar_pi001.gd` executa Input e física reais; os karts não são teletransportados durante a medição das voltas. O jogador fica parado no grid, exigindo contorno pela IA.

| Adversário | Piloto (jogador Jake) | Primeira volta | Desvio máximo do eixo | Quadros fora (centro > 4 m) | Quadros contramão |
| --- | --- | --- | --- | --- | --- |
| Adversario1 | Dimi | 84.10 s | 1.296 m | 0 | 0 |
| Adversario2 | Bryan | 90.25 s | 1.297 m | 0 | 0 |
| Adversario3 | Dimi | 86.05 s | 1.297 m | 0 | 0 |
| Adversario4 | Bryan | 91.82 s | 1.297 m | 0 | 0 |
| Adversario5 | Dimi | 87.82 s | 1.297 m | 0 | 0 |

As escolhas Dimi e Bryan repetiram a aprovação (`validacao_pi001_piloto1.json`, `validacao_pi001_piloto2.json`), incluindo Jake como IA. A telemetria por segundo contém posição, progresso, velocidade, desvio e faixa. Desvio máximo de aproximadamente 1,297 m nos ensaios finais; a meia largura do asfalto é 4 m. Não foi feito cálculo contínuo de toda a carroceria contra o perímetro da pista.

Controles: aceleração a 22 m/s, deslocamento de 24,02 m em 2 s, frenagem até cerca de −0,4 m/s após 0,8 s, ré até −8 m/s, giro em ré e travessia da zebra até o gramado. O retorno ao asfalto foi confirmado. Ver `validacao_pi001*.json`.

`validar_contato_pi001.gd` mediu todos os vértices das quatro rodas e comparou com raycast ao piso em repouso: penetração entre cerca de 6 e 10 mm, dentro da tolerância usada de 2 cm, sem flutuação. Também executou colisões Jake→Dimi, Dimi→Bryan e Bryan→Jake, com um alvo imobilizado no ensaio; houve sinal de batida e impulso de cerca de 9,3 m/s em cada alvo. Ver `contato_e_colisoes.json`.

As regressões de Jake, Dimi e Bryan passaram nas verificações booleanas de rodas, suspensão, cabeça, câmera, seleção e movimento existentes. O teste antigo do Dimi pressupunha somente dois pilotos: foi atualizado para testar presença e ciclo do catálogo atual; a primeira saída com as expectativas antigas está preservada. O teste de Jake ganhou `--saida=` e estado calculado a partir das medições, em vez do antigo texto fixo “parcial”. Nenhum rig, GLB ou script de animação foi alterado.

## Conferência visual

O jogo foi aberto com renderização real. As imagens foram capturadas pelo viewport da Godot e inspecionadas visualmente:

- `menu_pi001.png`: escolha de Jake e PI001 no menu existente.
- `largada_pi001.png`: faixa quadriculada, largura, sentido da largada, câmera, adversário ao lado, asfalto, zebras e céu HDRI.
- `aceleracao_pi001.png`, `curva_pi001.png`, `re_pi001.png`: deslocamento, HUD, afastamento/FOV e rolagem da câmera, poses dos personagens.
- `contato_jake.png`, `contato_dimi.png`, `contato_bryan.png` e `pneus_lateral_*.png`: cada personagem isolado no próprio visual, rodas apoiadas e escala relativa ao piso.
- `vista_geral_pi001.png`: modelo completo comparado ao JPG e ao traçado. Somente nessa captura de inspeção a neblina foi suspensa temporariamente; a cena salva mantém a neblina existente.

A aceleração/frenagem e as voltas foram testadas por Input automatizado e física; não foram pilotadas manualmente pelo teclado. As capturas são amostras renderizadas, não uma revisão visual de todos os quadros de uma volta.

## Limitações e pendências

- A escala, o sentido e a largada continuam provisórios conforme o modelo original. Aprovação artística e medidas definitivas não fazem parte da integração técnica concluída.
- Não foi acrescentado regulamento de corrida, cronômetro, classificação ou sistema de checkpoints/antiatalho; o progresso da IA está nos relatórios.
- A suspensão continua visual, sem apoio físico independente por roda. O pequeno afundamento dos pneus foi medido e explicitado acima.
- O material procedural da Godot é equivalente visual, sem reprodução exata dos nós/bump do Blender. O cenário permanece a base plana original.
- O ensaio final cobre uma volta de cada adversário por escolha de personagem, a 60 Hz, com jogador parado no grid; não garante ausência de saídas em colisões arbitrárias, sessões longas ou outras frequências de física.
- As tentativas iniciais, inclusive colisões/saídas e travamentos corrigidos, foram preservadas em `tentativa*_*.json`/`.log`; a conclusão usa somente os resultados finais.

## Reproduzir (a partir da raiz do repositório)

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --editor --import --quit
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --script res://ferramentas/construir_cenas.gd
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --fixed-fps 60 --script res://ferramentas/validar_pi001.gd
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --fixed-fps 60 --script res://ferramentas/validar_pi001.gd -- --personagem=1
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --fixed-fps 60 --script res://ferramentas/validar_pi001.gd -- --personagem=2
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --fixed-fps 60 --script res://ferramentas/validar_contato_pi001.gd
/Applications/Godot.app/Contents/MacOS/Godot --path jogo --fixed-fps 60 --script res://ferramentas/capturar_pi001.gd
/Applications/Godot.app/Contents/MacOS/Godot --path jogo
```

Para regressões, usar `--script res://ferramentas/validar_mecanicas_NOME.gd -- --saida=res://../pistas/PI001_primeira_pista/validacao/integracao_20261016/regressao_NOME.json`, substituindo NOME por jake, dimi ou bryan. Os comandos das ferramentas regravam apenas os arquivos com os nomes de saída indicados: para uma nova auditoria histórica, escolher outra pasta de destino antes de executá-los.
