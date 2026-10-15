# P001.07 — Validação das regras do Jake na Godot

Data: **15/10/2026**. Resultado: **atendimento parcial ao prompt**. O pedido original está na [receita, quinto prompt](../../../documentacao/RECEITA_PERSONAGEM.md#quinto-prompt--jogo-na-godot-rodas-suspensão-e-equilíbrio-da-cabeça).

Foram auditados os scripts existentes em `jogo/` e o GLB importado do Jake. Esta etapa adiciona um verificador e documentação; não altera a mecânica, o modelo ou as cenas do jogo. Não houve commit ou envio remoto desta auditoria.

## Método e reprodução

Executado com **Godot 4.7.2**, pela linha de comando, sem janela. A abertura/importação do projeto como editor terminou sem erros. O verificador instancia o GLB real, chama os métodos reais de `VisualKart`, mede as poses globais dos ossos e depois executa o menu, a troca para a pista e um percurso com ações de entrada no motor de física.

Na raiz do repositório:

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --editor --quit
/Applications/Godot.app/Contents/MacOS/Godot --headless --path jogo --fixed-fps 60 --script res://ferramentas/validar_mecanicas_jake.gd
```

O [verificador](../../../jogo/ferramentas/validar_mecanicas_jake.gd) grava [validacao_godot_jake.json](../validacao/validacao_godot_jake.json), com nomes de malhas e ossos, amostras, conclusões e hashes SHA-256 dos scripts principais, do GLB e da configuração. O término da auditoria com código zero significa que o relatório foi produzido; o resultado das regras está em `conclusao`, com estado `parcial`.

As curvas isoladas usam entradas constantes por três segundos em cada fase: esquerda, direita e reta, com velocidade de 10 m/s. Há casos com e sem ruído a 60 passos/s e com ruído a 120 passos/s. O ruído dos casos isolados usa uma semente fixa. O percurso completo usa o ruído aleatório original; pequenas diferenças de ângulo entre execuções são esperadas.

## Resultados por requisito

| Requisito | Resultado observado | Situação |
| --- | --- | --- |
| Escolher personagem | Menu mostra Jake e o botão de jogar abre a pista; o catálogo contém somente um piloto | Jake validado; seleção entre pilotos distintos pendente |
| Andar em cenário quadriculado | Aceleração por entrada percorreu cerca de 24,017 unidades em dois segundos; o piso referencia `quadriculado.gdshader` | Movimento validado; aparência do quadriculado não inspecionada por pixels |
| Câmera dinâmica atrás | Após a curva, produto escalar entre deslocamento da câmera e eixo traseiro do kart de aproximadamente +4,328; FOV aumentou de 68° para 80,501° no trecho em movimento | Validado numericamente nas amostras |
| Quatro rodas dinâmicas | Giro proporcional à velocidade/raio, giro inverso em ré e ausência de giro com velocidade zero nas quatro rodas; esterço de 28° apenas nas dianteiras | Validado |
| Inércia e vibração | Esquerda produz rolagem positiva para a direita do piloto; direita produz o sinal oposto, após estabilizar. Ruído altera posição vertical e rolagem | Efeito visual implementado; sem suspensão física individual |
| Cabeça sempre oposta | Oposição após estabilizar, mas mesmo lado na entrada/inversão de curvas e ao herdar tremor não compensado | **Não cumpre literalmente “sempre”** |
| Estrutura solicitada | Quatro rodas, `Cabeca` e `Corpo_Kart`; este último reúne torso do piloto e carro. Quatro ossos no GLB, dos quais dois usados pela mecânica | A divisão carro/personagem não corresponde literalmente ao prompt |

## Rodas e suspensão

[`kart.gd`](../../../jogo/scripts/kart.gd) recebe as entradas e produz velocidade e giro; [`visual_kart.gd`](../../../jogo/scripts/visual_kart.gd) aplica as transformações visuais. O giro da roda em cada passo é `velocidade / escala / raio × delta`. Os testes verificaram a transformação resultante de cada malha, a reversão e a parada. As rodas dianteiras têm pivôs próprios para o esterço.

Ao montar o visual, as rodas são retiradas do acompanhamento do esqueleto e colocadas em pivôs no modelo. A carroceria se inclina pelos ossos e as rodas permanecem na base. O deslocamento dos pivôs foi zero nos casos isolados de rolagem. Isso não é uma suspensão física com curso individual, contato de pneus ou raycasts.

A meta de rolagem depende de `giro × velocidade`, com ganho 0,012 e limite de 14°. Há uma mola amortecida e tremor adicional; o limite de 14° é da **meta**, não um limite rígido do ângulo final somado ao ruído. Na troca rápida de direção, a mola também pode manter a inclinação anterior por alguns quadros.

## Por que a cabeça não fica sempre oposta

A meta da cabeça é `−1,7 × rolagem`, aplicada com outra mola amortecida. A cabeça herda a inclinação do torso, portanto uma rotação local negativa não garante, sozinha, inclinação global oposta. Em regime estabilizado e sem tremor, a inclinação global é aproximadamente `rolagem − 1,7 × rolagem = −0,7 × rolagem`.

Na curva constante à esquerda, sem ruído, o corpo terminou em **+6,875°** e a cabeça em **−4,812°**; a curva à direita inverteu os sinais. Entretanto, a 60 passos/s:

- Entrada da primeira curva: **18 quadros** com corpo e cabeça no mesmo lado.
- Inversão para a direita: **15 quadros** com corpo e cabeça no mesmo lado.
- Retorno à reta, ainda sem ruído: **16 quadros** com o mesmo problema enquanto as molas retornavam.

Essas contagens ignoram a zona de corpo entre −0,05° e +0,05° para não classificar arredondamentos próximos da vertical como falha. São contagens de quadros que violam o critério, não uma promessa de intervalos sempre contínuos.

A carroceria usa `rolagem + tremor`; a meta da cabeça usa somente `rolagem`. Um teste adicional começa diretamente em reta a 10 m/s, sem curva anterior: a cabeça acompanha o tremor do corpo no mesmo sentido, em vez de compensá-lo. O relatório contém um exemplo com as poses globais e a compensação relativa zero. A simulação a 120 passos/s também encontrou violações nas transições.

Para satisfazer a leitura literal do pedido, uma futura correção precisa considerar a inclinação efetivamente aplicada ao torso, inclusive tremor, e garantir o sinal global oposto também nos transitórios. Se o atraso for um efeito artístico desejado, o requisito deve admitir esse atraso explicitamente. Nenhuma dessas decisões foi aplicada nesta auditoria.

## Estrutura importada e limites da evidência

O GLB contém as malhas `Wheel_Front_Left`, `Wheel_Front_Right`, `Wheel_Rear_Left`, `Wheel_Rear_Right`, `Cabeca` e `Corpo_Kart`. As duas últimas têm skin; as rodas não. Os ossos encontrados são `Root_Bone`, `Torso_Bone`, `Neck_Bone` e `Head_Bone`. O código usa `Torso_Bone` e `Head_Bone` como os dois controles dinâmicos.

Não foi feita uma separação nova entre o torso do piloto e o veículo. O formato do catálogo permite cadastrar outros pilotos, mas não havia outro para validar a alternância real.

A auditoria executou o código e as transformações no motor, sem renderizar imagens para inspeção visual. Não comprova aparência do piso, qualidade visual da suspensão ou câmera em todas as colisões. O gerador de cenas por CLI existe em `jogo/ferramentas/construir_cenas.gd`, mas não foi reexecutado, para preservar as cenas existentes. A forma como a configuração original foi criada não foi reconstruída como evidência histórica.
