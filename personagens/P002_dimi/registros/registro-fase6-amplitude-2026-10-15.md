# Registro da Fase 6 (início) — escolha da amplitude do giro da cabeça — P002 Dimi

Data: 15/10/2026, 17:12–17:23 (-03:00).

## 1. Pedido e escopo

Depois da Fase 5, o usuário aceitou a recomendação de **limitar a amplitude do giro** em vez de criar uma tampa na base aberta da cabeça. Pediu para iniciar a Fase 6 pelas vistas de comparação. Esta etapa só mede e renderiza; **nenhuma ação foi criada** e o `dimi.blend` não foi alterado.

## 2. Ferramentas e estado

- Blender 5.2.2 LTS, sessão já aberta, pelo MCP. Não foi usada a CLI nem outra instância.
- Arquivo em disco antes e depois: SHA-256 `229034cf…25a7d7`, o mesmo das Fases 4 e 5. Poses, câmera e configurações de render foram desfeitas com `wm.revert_mainfile` (`is_dirty: false` ao final).
- Script: [`scripts_fase6/vistas_amplitude.py`](scripts_fase6/vistas_amplitude.py). Giro em Y local de `Head_Bone`, que é o Z mundial. O ângulo positivo vira o rosto para a esquerda do piloto (+X).

## 3. Método

**Vistas.** Câmera ortográfica de 0,45 m, centrada 6 cm acima do pivô da cabeça. Foram usadas seis direções:

- `lado_esq` (+X) e `lado_dir` (−X);
- `frente` (−Y);
- `jogo`: atrás e acima, na mesma razão de `camera_perseguicao.gd` (distância 3,4, altura 1,4);
- `jogo_curva_esq` e `jogo_curva_dir`: a câmera do jogo deslocada 1,5 para cada lado, como no atraso da câmera numa curva.

**Medida objetiva.** Para cada ângulo e direção, uma grade de 160×160 raios paralelos cobre uma janela de 0,22 m sobre o pescoço; cada raio corresponde a cerca de 1,9 mm². A medida conta os raios cujo **primeiro impacto** é uma face interna, voltada para longe da câmera, da `Cabeca` ou do `Corpo_Kart` (interior da gola). Ou seja, é a área em que se enxerga por dentro da abertura.

**Tentativa descartada.** A primeira medida contava vértices da borda aberta visíveis. Em repouso ela já dava 82 de frente, porque a borda fica na emenda do pescoço com a gola, rente à superfície externa. Além disso, a malha tem 9.381 vértices de borda espalhados por toda a cabeça. Foi substituída pela medida acima.

**Conferência da medida.** Em repouso, o interior visível é de 0 a 2 raios, de modo que a medida separa bem os casos. Nos ângulos testados, os impactos internos da cabeça ficam entre Z 0,416 e 0,488 m, no toco do pescoço e embaixo da mandíbula. Portanto são a abertura, e não normais invertidas em outra parte, como orelhas ou boné.

## 4. Resultados — raios com interior visível (cabeça + gola)

| Ângulo | lado_esq | lado_dir | frente | jogo | jogo_curva_esq | jogo_curva_dir |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| +10 | 80 | 120 | 15 | 0 | 4 | 0 |
| −10 | 217 | 16 | 18 | 0 | 0 | 14 |
| +15 | 87 | 184 | 26 | 0 | 35 | 0 |
| −15 | 309 | 20 | 24 | 0 | 0 | 62 |
| +20 | 77 | 247 | 38 | 0 | 41 | 0 |
| −20 | 376 | 23 | 56 | 0 | 0 | 70 |
| +25 | 60 | 305 | 74 | 0 | 42 | 0 |
| −25 | 444 | 28 | 89 | 0 | 0 | 61 |
| +30 | 34 | 362 | 104 | 0 | 31 | 0 |
| −30 | 511 | 25 | 126 | 14 | 0 | 92 |
| +35 | 9 | 411 | 146 | 0 | 39 | 0 |
| −35 | 563 | 21 | 170 | 36 | 0 | 117 |
| +40 | 7 | 458 | 185 | 1 | 113 | 0 |
| −40 | 588 | 20 | 219 | 37 | 0 | 110 |

Os dados completos, separados por cabeça e corpo e incluindo os raios que atingem a frente e os que não atingem nada, estão em [`validacao/amplitude_cabeca_fase6.json`](../validacao/amplitude_cabeca_fase6.json).

**Inspeção visual** ([`vistas_fase6/`](vistas_fase6/), 55 imagens):

- **De lado:** a mancha clara e irregular sob a mandíbula já aparece de leve a −10° ([`giro_-10_lado_esq.png`](vistas_fase6/giro_-10_lado_esq.png)) e a +15°. Fica nítida a ±25° ([`giro_-25_lado_esq.png`](vistas_fase6/giro_-25_lado_esq.png), [`giro_+25_lado_dir.png`](vistas_fase6/giro_+25_lado_dir.png)) e grande a −40°. **Não há um ângulo útil sem a falha nessa vista.**
- **Câmera do jogo, atrás:** o pescoço fica escondido pela aba do boné e pelo móbile até ±40° ([`giro_-40_jogo.png`](vistas_fase6/giro_-40_jogo.png)). Os poucos raios contados a −30° e −40° são de dentro da gola, sem destaque visual.
- **Câmera em curva:** escondido a ±25° ([`giro_-25_jogo_curva_dir.png`](vistas_fase6/giro_-25_jogo_curva_dir.png)). A ±40° aparece um pequeno recorte junto à gola ([`giro_-40_jogo_curva_dir.png`](vistas_fase6/giro_-40_jogo_curva_dir.png), [`giro_+40_jogo_curva_esq.png`](vistas_fase6/giro_+40_jogo_curva_esq.png)).
- A vista `frente` só foi medida, não renderizada.

## 5. Conclusão e decisão pendente

- Limitar o ângulo **não elimina** a falha nas vistas laterais nem na frontal: ela começa por volta de 10°.
- Limitar **resolve para a câmera de jogo**: até ±25° nada aparece, tanto atrás quanto em curva; a ±40° surge um recorte pequeno na curva.
- **Recomendação:** amplitude de **25°** nas ações de olhar para a direita e para a esquerda, e o mesmo teto na compensação da cabeça da Fase 8.
- **Fica em aberto:** se houver uma tela de seleção ou outra câmera que mostre o piloto de lado ou de frente com a cabeça girada, só a tampa resolve, e ela altera a topologia.
- A amplitude ainda não foi confirmada pelo usuário. Duração e FPS ainda não foram definidos.

## 6. Arquivos

| Artefato | SHA-256 |
| --- | --- |
| `validacao/amplitude_cabeca_fase6.json` | `6605b9e4e9574deab2c64faa7f0290555842570fbce257c5d8b7c82a42be3cff` |
| `registros/scripts_fase6/vistas_amplitude.py` | `74bddfba…a131b` (versão final, com `SO_ANGULOS`/`SO_VISTAS` opcionais, acrescentados depois de gerar o JSON para renderizar as vistas de curva; a medida não mudou) |
