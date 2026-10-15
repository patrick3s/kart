# Registro da rotação e da animação da cabeça

Data: **15/10/2026**, no fuso de São Paulo.

Projeto: `/Users/patricksoares/Documents/jogos/kart`.

Arquivo trabalhado e salvo: [`kart_modular_rig.blend`](../blender/jake.blend).

Este documento registra os pedidos, as operações, as verificações e as orientações deste chat. O rig e a separação das malhas já existiam quando esta conversa começou; sua criação está descrita no [registro anterior](registro-rig-personagem-2026-10-15.md). Esse registro anterior descreve uma etapa histórica, em que ainda não havia keyframes.

## 1. Pedidos e resultado

1. Girar a cabeça para a direita em relação à vista frontal, aproximadamente 30° a 45°, selecionando a cabeça ou `Head_Bone`, preservando o pivô do pescoço e o corpo. Os keyframes eram opcionais nesse primeiro pedido.
2. Após a pose estática, o usuário esclareceu que a cabeça deveria virar e retornar à posição original na animação.
3. Explicar como aumentar o FPS.
4. Explicar se uma prévia que mostra apenas 2 a 3 quadros por segundo fica mais rápida quando exportada.
5. Documentar todo o trabalho deste chat na pasta `documentacao`.

O resultado foi uma ação que gira a cabeça de 0° a 40° para a direita e retorna a 0°, com interpolação suave, sem movimento do pivô do pescoço nem dos vértices do corpo nas verificações realizadas.

## 2. Inspeção inicial pelo Blender MCP

Foram consultados o inventário da cena, os detalhes dos objetos, os ossos, as matrizes de pose e repouso, as rotações, os pesos e os dados de animação. A viewport foi capturada antes e depois da rotação.

| Elemento | Estado observado |
| --- | --- |
| Cena e espaço de trabalho | `Scene`, `Layout` |
| Armature | `Personagem_Rig` |
| Dados da armature | `Personagem_Rig_Armature` |
| Modo | Pose |
| Osso da cabeça | `Head_Bone`, filho de `Neck_Bone` |
| Hierarquia | `Root_Bone` → `Torso_Bone` → `Neck_Bone` → `Head_Bone` |
| Modo de rotação da cabeça | Euler `XYZ` |
| Pose inicial da cabeça | Rotação e localização zeradas; escala unitária |
| Ação e trilhas NLA | Nenhuma ação e nenhuma trilha NLA |
| Reprodução | Ativa durante a inspeção; pausada antes das edições |

As duas malhas já estavam separadas e vinculadas à armature:

| Objeto | Dados da malha | Vértices | Único grupo | Pesos |
| --- | --- | ---: | --- | --- |
| `Cabeca` | `Cabeca_Geometria_Original` | 160.046 | `Head_Bone` | Todos iguais a 1,0 |
| `Corpo_Kart` | `Corpo_Kart_Geometria_Original` | 874.925 | `Torso_Bone` | Todos iguais a 1,0 |

Cada malha tinha o modificador Armature `Rig_Rigido_Sem_Deformacao`. O corpo e o kart permanecem um único objeto: esta conversa não alterou essa estrutura.

## 3. Rotação estática de 40°

Foi escolhido o osso `Head_Bone`, preservando a malha-base, os pesos e a origem dos objetos.

O eixo vertical do personagem corresponde ao **Y local de `Head_Bone`**, aproximadamente alinhado ao Z mundial nessa pose. Por isso, a rotação correta foi feita em Y local, em vez de usar diretamente o Z local do osso.

- Ângulo aplicado: **+40°**, aproximadamente `0.6981317008` radianos.
- Canal alterado: `Head_Bone.rotation_euler.y`.
- Pivô mundial preservado: **`(0, -0.0625, 0.4375)`**.
- Localização do osso mantida: `(0, 0, 0)`.
- Escala do osso mantida: `(1, 1, 1)`.
- Direção frontal após a rotação: aproximadamente `(0.642788, -0.766044, 0)` no espaço mundial, partindo de `(0, -1, 0)`. Esse registro define o sentido de direita adotado em relação à vista frontal.

A rotação foi conferida visualmente. Não foram acrescentados keyframes nessa primeira etapa, e o `.blend` foi salvo com a pose estática. Essa pose foi posteriormente substituída pela animação solicitada pelo usuário.

### Compatibilidade encontrada

A primeira tentativa de selecionar o osso via `Bone.select` falhou porque essa propriedade não existia na API do Blender conectado. A falha ocorreu antes de aplicar a rotação. Foi consultada a API disponível e usada a propriedade **`PoseBone.select`**, com `Head_Bone` definido como osso ativo. A rotação foi então aplicada uma única vez.

Foram inseridos pontos de desfazer antes da edição e após a pose, usando o histórico do Blender.

## 4. Animação de ida e volta

Após o esclarecimento do usuário, foi criada a ação **`Cabeca_Direita_Ida_e_Volta`**. Antes disso, uma nova inspeção confirmou que não havia ações, trilhas NLA ou drivers nos objetos da cena.

Foi animado somente este canal:

```text
pose.bones["Head_Bone"].rotation_euler
índice 1 = eixo Y local
```

| Quadro | Rotação | Posição |
| ---: | ---: | --- |
| 1 | 0° | Original, olhando para a frente |
| 25 | 40° | Virada para a direita |
| 49 | 0° | Retorno à posição original |

Configuração da curva:

- Interpolação dos três keyframes: **Bézier** (`BEZIER`).
- Alças dos dois lados: **automáticas limitadas** (`AUTO_CLAMPED`), para suavizar a aceleração e a desaceleração sem ultrapassar os ângulos dos keyframes.
- Extrapolação: **constante** (`CONSTANT`); fora dos keyframes, o canal mantém o valor da extremidade correspondente.
- Prévia ativada entre os quadros **1 e 49**, para repetir o movimento durante a reprodução.
- Intervalo principal da cena preservado em **1 a 250**.

O loop visto no Blender foi obtido pelo intervalo de prévia. Não foi adicionado modificador de ciclos à curva. Portanto, após o quadro 49, a cabeça permanece em 0° quando a cena é avaliada fora da prévia.

O arquivo foi salvo no quadro 1 com a animação criada. Em seguida, a reprodução foi iniciada para mostrar a ida e a volta em loop.

## 5. Verificações de preservação

As verificações foram executadas dentro do Blender pelo MCP, usando `bpy`, o grafo de dependências e arrays NumPy das coordenadas avaliadas da malha.

### Pose estática

| Medição antes/depois da rotação | Resultado |
| --- | ---: |
| Maior diferença por componente nos 874.925 vértices avaliados de `Corpo_Kart` | `0.0` |
| Deslocamento do pivô mundial da cabeça | `0.0` |
| Maior diferença nas matrizes dos demais ossos | `0.0` |
| Mudança na localização ou escala de `Head_Bone` | Nenhuma |

### Animação

Foram avaliados os keyframes e os pontos intermediários:

| Quadro | Ângulo observado, aproximado | Maior diferença nos vértices do corpo | Deslocamento do pivô |
| ---: | ---: | ---: | ---: |
| 1 | 0° | `0.0` | `0.0` |
| 13 | 20° | `0.0` | `0.0` |
| 25 | 40° | `0.0` | `0.0` |
| 37 | 20° | `0.0` | `0.0` |
| 49 | 0° | `0.0` | `0.0` |

A matriz mundial de `Corpo_Kart` também permaneceu igual nos quadros avaliados. As verificações exigiram diferenças menores que `1e-7`; as diferenças medidas acima foram zero. O valor numérico de 40° retornado pela API foi aproximadamente `39.9999988364°`, devido à representação de ponto flutuante.

Esses resultados demonstram a preservação nos estados medidos. A inspeção visual cobriu a pose inicial e a virada na viewport; não foi feito um render final do movimento inteiro nesta conversa. Os pesos integrais de um único osso mantêm o comportamento rígido da cabeça.

## 6. Orientação sobre FPS

Na criação da animação e na consulta feita ao responder sobre FPS, a cena estava em **24 FPS**, com base `1.0`.

Foi explicado como alterar a taxa no Blender:

1. Abrir **Propriedades de saída**, no painel Propriedades.
2. Localizar **Formato → Taxa de quadros**.
3. Selecionar a taxa desejada, como 30 ou 60 FPS.

Também foi explicado que aumentar o FPS sem reposicionar os keyframes encurta o tempo do movimento:

| FPS | Tempo entre o quadro inicial 1 e o retorno no quadro 49 |
| ---: | ---: |
| 24 | 2,0 segundos |
| 30 | 1,6 segundo |
| 60 | 0,8 segundo |

Os tempos dessa tabela usam os **48 intervalos entre os quadros 1 e 49**. A duração de uma sequência exportada com os 49 quadros inclusivos é `49 / FPS`, ligeiramente maior.

Para manter dois segundos entre os keyframes inicial e final:

| FPS | Original | Virada | Retorno | Fim da prévia |
| ---: | ---: | ---: | ---: | ---: |
| 24 | 1 | 25 | 49 | 49 |
| 30 | 1 | 31 | 61 | 61 |
| 60 | 1 | 61 | 121 | 121 |

A orientação dada no chat usou o exemplo de 60 FPS. **Não foi executada pelo agente uma mudança de FPS nem uma redistribuição dos keyframes.**

## 7. Prévia lenta e exportação

O usuário relatou que a reprodução mostrava **2 a 3 quadros por segundo**. Esse valor foi informado pelo usuário, sem uma medição de desempenho adicional nesta conversa.

Foi esclarecida a diferença entre:

- **FPS da cena:** determina a duração temporal dos quadros no resultado renderizado.
- **FPS efetivo da viewport:** indica quantos quadros o computador consegue exibir por segundo enquanto avalia e desenha a cena.

Uma viewport lenta não obriga o vídeo renderizado a reproduzir na mesma lentidão. Ao renderizar, o Blender pode gastar o tempo necessário em cada quadro, e o vídeo reproduz na taxa configurada ao gerar o arquivo. Aumentar o FPS da cena, sozinho, não melhora o desempenho da viewport.

A resposta original mencionou cerca de dois segundos porque, naquele momento, a configuração consultada era de 24 FPS. A duração muda se o FPS ou a posição dos keyframes for alterado.

**Não houve renderização, codificação nem exportação de vídeo neste chat.** A explicação sobre a reprodução final descreve o comportamento esperado de uma animação renderizada, não um vídeo exportado e validado.

## 8. Estado consultado durante a documentação

Foi feita uma consulta de leitura ao Blender ao produzir este registro:

| Propriedade | Valor observado |
| --- | --- |
| Arquivo aberto | `kart_modular_rig.blend` |
| Ação | `Cabeca_Direita_Ida_e_Volta` |
| Canal animado | Y local de `Head_Bone` |
| Keyframes | 1: 0°; 25: 40°; 49: 0° |
| Interpolação e alças | `BEZIER`, `AUTO_CLAMPED` |
| FPS / base | **30 / 1.0** |
| Intervalo principal | 1 a 250 |
| Prévia | Ativa, 1 a 49 |
| Reprodução naquele instante | Pausada |
| Resolução configurada | 1920 × 1080 |
| Formato de saída configurado | `PNG` |

O FPS observado agora é diferente dos 24 FPS anteriores. Não há operação do agente neste chat que tenha realizado essa mudança para 30; este registro não atribui sua origem nem confirma se ela já foi salva no disco. A ação e seus três keyframes continuam presentes na cena aberta.

O intervalo de prévia não deve ser confundido com o intervalo usado para renderizar a cena. Para exportar somente a ida e a volta atual, é necessário conferir o fim do intervalo de renderização: a configuração principal observada ainda vai até **250**, enquanto o movimento termina em **49**. Além disso, `PNG` produz imagens; a configuração observada não está preparada diretamente para um arquivo de vídeo.

## 9. Arquivos e limites do registro

- O `.blend` principal foi salvo após a pose estática e novamente após a criação da animação.
- O histórico de criação do rig, a validação original em `rigging/validacao_rig.json` e o manifesto anterior pertencem à etapa de rigging. Eles não foram reescritos como se fossem validações desta animação.
- O manifesto anterior contém hashes históricos, inclusive do `.blend` antes dessas edições; seu hash não comprova a versão posterior animada.
- As verificações numéricas de rotação e animação descritas aqui vieram dos retornos do Blender MCP no chat. Não foi criado um novo relatório JSON ou script autônomo dessas operações.
- As capturas de viewport foram exibidas no chat, sem novos arquivos de imagem entregues na pasta do projeto.
- Na etapa de documentação foram criados este registro e o link no índice. A consulta ao Blender foi somente de leitura; não alterou a cena, os FPS, o intervalo, a ação ou o `.blend`.
- Não houve commit, publicação, novo rig, alteração dos pesos, novo ajuste de origem ou exportação para outro formato nesta conversa.

## 10. Como visualizar o resultado

1. Abrir `kart_modular_rig.blend` no Blender.
2. Conferir a ação `Cabeca_Direita_Ida_e_Volta` em `Personagem_Rig`.
3. Usar o intervalo de prévia **1 a 49**.
4. Reproduzir a animação na linha do tempo: a cabeça sai da posição original, vira 40° para a direita e retorna.
5. Para alterar a duração mantendo o ângulo, reposicionar os keyframes conforme o FPS desejado e ajustar o fim da prévia e, se for renderizar, o intervalo de renderização.
