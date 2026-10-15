# Personagem — receita de criação

Esta é a receita genérica para preparar personagens do projeto. **Cada personagem tem a sua própria pasta em [`personagens/`](../personagens/)**, com tudo que pertence a ele: ficha e histórico (`LEIA-ME.md`), referências, arquivo do Blender, backups, relatórios de validação e registros detalhados de cada etapa.

```
personagens/P00N_nome/
  LEIA-ME.md     ficha e histórico de etapas do personagem
  referencia/    imagens e modelos de entrada
  blender/       arquivo de trabalho (.blend) e instruções do rig
  backups/       cópias anteriores a cada edição e dados originais de geometria
  validacao/     relatórios numéricos (JSON) e manifestos
  registros/     documento detalhado de cada etapa
```

O que for exportado para o jogo fica em `jogo/personagens/<nome>/`, porque a Godot só enxerga arquivos dentro do projeto dela.

Primeiro personagem: [P001 — Jake](../personagens/P001_jake/LEIA-ME.md). A receita nasceu em **15/10/2026** a partir do preparo dele e foi separada da ficha do personagem na reorganização de **15/10/2026**.

## 0. Prompt original deste chat para os próximos personagens

O pedido abaixo deu origem à **primeira etapa de preparação e rig do P001 — Jake**. Ele fica registrado como prompt reutilizável para os próximos personagens que já tenham uma malha pronta e precisem de separação de cabeça, esqueleto, pesos rígidos e pivô, com preservação da geometria.

### Pedido para copiar e reutilizar

> Atue como um artista técnico sênior de 3D e especialista em Blender. Utilizando as ferramentas do **Blender MCP**, pegue a malha (mesh) existente do personagem e estruture o esqueleto e a separação de partes **sem alterar absolutamente nenhum vértice, proporção ou geometria da malha original** (a malha deve ser tratada como geometria estática intocável). Siga estas regras:
>
> 1. **Preservação Total da Geometria:** Não modifique o formato, a topologia ou o design do personagem. Apenas separe o que já existe em objetos distintos (se necessário) ou atribua os pesos corretos.
> 2. **Isolamento de Cabeça e Corpo:** Separe fisicamente o objeto da **cabeça** em relação ao **corpo** (caso estejam unidos em uma única malha, faça um corte limpo na base do pescoço sem deformar o rosto ou o torso) para que sejam malhas independentes.
> 3. **Rigging e Pesos (Vertex Groups):** Crie a Armature e aplique os pesos de forma limpa, garantindo que o osso da cabeça controle 100% da malha da cabeça e os ossos do torso controlem o corpo, sem vazamentos de peso que deformem o modelo.
> 4. **Ponto de Pivô:** Ajuste a origem da cabeça na base do pescoço para rotações limpas.

### Como usar o pedido em um novo personagem

1. Informar o nome e o identificador do personagem, o arquivo de entrada e o objeto de malha a trabalhar. Usar a pasta própria descrita no início desta receita.
2. Informar quais objetos são acessórios ou veículo e se precisam permanecer independentes. O prompt original não definiu controles separados para o kart; no primeiro rig, ele ficou no conjunto do corpo.
3. Reutilizar o pedido acima e seguir os **Passos 1 a 6** desta receita: inspeção, backup, separação, pivô, esqueleto, pesos e validação. As animações do Passo 7 são uma etapa posterior, não uma exigência do pedido original.
4. Medir novamente as partes, o pivô e os eixos do novo modelo. Não copiar coordenadas, índices de ilhas ou limites de altura do Jake como regra de seleção.
5. Salvar o resultado, o relatório de validação e o registro detalhado na pasta do novo personagem. Referenciar esses arquivos no `LEIA-ME.md` dele e acrescentar à receita os aprendizados reutilizáveis.

### Referência das quatro regras ao trabalho deste chat

As evidências abaixo pertencem ao **rig inicial**, antes das animações e da separação posterior das rodas. Os registros posteriores continuam nas demais seções da receita e na ficha do P001.

| Regra do pedido | O que foi feito no primeiro personagem | Documento de referência |
| --- | --- | --- |
| 1. Preservação total da geometria | Cópia anterior à edição, registro dos arrays originais e identificadores dos elementos; comparação de contagens, conectividade, UVs, flags de suavização, índices de materiais e coordenadas mundiais | [Preservação e rastreamento](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#4-cópia-de-segurança-e-registro-da-geometria) e [validação numérica original](../personagens/P001_jake/validacao/validacao_rig.json) |
| 2. Cabeça e corpo independentes | Separação de 86 ilhas existentes em `Cabeca`, com 160.046 vértices, e restante em `Corpo_Kart`, com 874.925; sem novo plano de corte ou fechamento do pescoço | [Seleção e separação da cabeça](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#5-inspeção-e-identificação-da-cabeça) |
| 3. Armature e pesos exclusivos | Criação de `Personagem_Rig`, com hierarquia raiz → torso → pescoço → cabeça; peso 1.0 de toda a cabeça em `Head_Bone` e de todo o conjunto corpo/kart em `Torso_Bone`, sem pesos automáticos ou envelopes | [Estrutura da armature](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#8-armature-criada) e [atribuição dos pesos](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#9-pesos-parentesco-e-modificadores) |
| 4. Pivô na base do pescoço | Origem da cabeça e início de `Head_Bone` em `(0, -0.0625, 0.4375)` no espaço mundial; teste temporário de rotação de 25° com movimento medido do corpo igual a zero e restauração da pose | [Ajuste da origem](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#7-origem-e-pivô-da-cabeça) e [teste de preservação](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#10-validação-executada) |

O [registro completo deste chat](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md) detalha também as tentativas intermediárias desfeitas e as limitações. O [manifesto histórico do rig](../personagens/P001_jake/validacao/manifesto-artefatos-rig.json) identifica os artefatos daquela etapa; seus hashes não identificam automaticamente o arquivo após trabalhos posteriores.

### Cuidados para cumprir o pedido sem alterar o modelo

- **Separação e corte:** para preservar a topologia, priorizar ilhas ou partes existentes. Um corte que cria vértices ou subdivide faces não pode ser apresentado como preservação exata da topologia. No primeiro personagem não foi necessário esse corte; se a nova malha não permitir a mesma estratégia, registrar o impedimento e a diferença em relação a esta receita.
- **Origem e coordenadas:** mover a origem com compensação muda a representação local dos vértices. Conferir a forma e as posições no espaço mundial e informar o arredondamento medido. No rig inicial do Jake, o maior desvio mundial da malha-base da cabeça foi `7.450580596923828e-9` unidade, e o maior desvio avaliado em repouso foi `2.9802322387695312e-8`. Não registrar esses valores como deslocamento numérico absolutamente zero.
- **Pesos:** conferir todos os vértices da cabeça, inclusive detalhes e acessórios que devam acompanhá-la. A rotação de teste deve manter o restante do modelo estável e não criar deformação interna da cabeça. Testar separadamente os outros controles que forem entregues.
- **Resultado documentado:** registrar exatamente quais partes ficaram independentes, o que cada osso controla e o que foi testado. No rig inicial, corpo e kart ficaram unidos. A separação das rodas foi um trabalho posterior, fora do escopo deste prompt de referência.

### Segundo prompt — rotação da cabeça para a direita

Este pedido deu origem à etapa **P001.02 — animação da cabeça**, depois da preparação e do rig. O texto original solicitava a rotação e deixava os keyframes opcionais; o complemento abaixo tornou explícita a animação de ida e volta.

#### Pedido original para copiar e reutilizar

> Atue como um desenvolvedor técnico no Blender. Utilizando o **Blender MCP**, aplique uma rotação na cabeça do personagem para que ele olhe **para a direita**. Siga estas instruções:
>
> 1. **Alvo:** Selecione a malha da cabeça (ou o osso `Head_Bone` da Armature, caso esteja usando o esqueleto).
> 2. **Rotação:** Gire a cabeça para a direita em relação à visão frontal do personagem (aproximadamente **30 a 45 graus** no eixo Z/local correto).
> 3. **Preservação:** Garanta que a rotação seja feita suavemente sem deslocar o ponto de origem (pivot) do pescoço e sem deformar a malha do corpo.
> 4. **Keyframe (Opcional):** Se estiver criando uma animação, insira um keyframe de rotação na posição inicial e outro na posição virada.

#### Complemento enviado para animar o retorno

> mais a cabeca deveria ir e voltar a posicao original na animacao

Ao reutilizar o pedido para uma animação, incluir também esse complemento: o movimento deve ter **posição original → virada para a direita → retorno à posição original**, com transições suaves.

#### Aplicação e referências do segundo prompt

- **Alvo e eixo:** foi usado `Head_Bone` em `Personagem_Rig`. A inspeção mostrou que o eixo vertical correspondia ao **Y local do osso**, aproximadamente alinhado ao Z mundial; esse eixo deve ser conferido em cada novo personagem.
- **Resultado:** primeiro foi aplicada uma pose estática de **+40°**; após o complemento, foi criada a ação `Cabeca_Direita_Ida_e_Volta`, com **0° → 40° → 0°** nos quadros **1 → 25 → 49**, interpolação Bézier e alças automáticas limitadas. A prévia repetia o intervalo de 1 a 49, sem modificador de ciclos na curva.
- **Preservação:** nos quadros 1, 13, 25, 37 e 49, o deslocamento medido do pivô e a maior diferença por componente nos vértices avaliados do corpo foram `0.0`. Esses resultados pertencem à configuração daquela etapa, anterior à separação posterior das rodas.
- **Duração:** a animação foi criada em 24 FPS, com dois segundos entre os keyframes inicial e final. Ao alterar o FPS, redistribuir os keyframes para manter a duração, conforme o [Passo 7](#passo-7--criar-uma-primeira-animação-simples).

**Referências:** [rotação e eixo correto](../personagens/P001_jake/registros/registro-animacao-cabeca-2026-10-15.md#3-rotação-estática-de-40), [ação e keyframes de ida e volta](../personagens/P001_jake/registros/registro-animacao-cabeca-2026-10-15.md#4-animação-de-ida-e-volta), [verificações de preservação](../personagens/P001_jake/registros/registro-animacao-cabeca-2026-10-15.md#5-verificações-de-preservação) e [ficha e histórico do P001](../personagens/P001_jake/LEIA-ME.md).

### Terceiro prompt — rotação da cabeça para a esquerda

Este pedido deu origem à etapa **P001.04 — cabeça para a esquerda**, espelhando a animação anterior. É o **terceiro prompt prático** desta sequência; o identificador P001.03 corresponde à consolidação documental, e não a um novo movimento do personagem.

#### Pedido original para copiar e reutilizar

> Atue como um artista técnico sênior de 3D no Blender. Com base nas diretrizes de rig e estrutura já estabelecidas no arquivo **PERSONAGEM.md** (que contém a animação anterior da cabeça virando para a direita), utilize o **Blender MCP** para criar uma nova animação ou estado onde a cabeça do personagem se movimenta **para a esquerda**. Siga estritamente estas regras:
>
> 1. **Consistência com o PERSONAGEM.md:** Respeite a hierarquia de objetos, os nomes dos ossos (`Head_Bone` ou equivalentes) e os limites de rotação especificados no documento.
> 2. **Espelhamento / Inversão:** Aplique uma rotação no sentido oposto (olhando para a esquerda do personagem, mantendo a mesma amplitude de graus usada no movimento para a direita).
> 3. **Integridade da Malha:** Garanta que a rotação ocorra puramente a partir do ponto de pivô do pescoço, sem causar *stretching* (esticamento) ou deformação indesejada na geometria da cabeça ou do corpo.
> 4. **Keyframe / Execução:** Insira os keyframes necessários na timeline do Blender de forma limpa, garantindo que o movimento seja fluido.

O nome `PERSONAGEM.md` foi mantido no texto como referência histórica do pedido. Depois da reorganização, ao reutilizar este prompt, indicar a **ficha `LEIA-ME.md` do personagem** e o registro da animação para a direita. Para o Jake, consultar a [ficha do P001](../personagens/P001_jake/LEIA-ME.md) e o [registro da ação anterior](../personagens/P001_jake/registros/registro-animacao-cabeca-2026-10-15.md).

#### Aplicação e referências do terceiro prompt

- **Espelhamento:** a ação `Cabeca_Direita_Ida_e_Volta` foi duplicada como `Cabeca_Esquerda_Ida_e_Volta`, invertendo o sinal dos valores e das alças Bézier no canal Y local de `Head_Bone`. A ação original foi preservada e marcada para continuar salva mesmo sem estar ativa.
- **Movimento entregue:** **0° → −40° → 0°** nos quadros **1 → 25 → 49**, com interpolação Bézier, alças automáticas limitadas e extrapolação constante. A cena estava em **30 FPS**, mantidos nesta etapa, com **1,6 segundo** entre o início e o retorno e prévia de 1 a 49.
- **Preservação:** hierarquia, pivô do pescoço, pesos e malhas mantidos. O pivô e as matrizes dos demais ossos permaneceram iguais nos 49 quadros inteiros; o corpo não se moveu nas cinco amostras de geometria completa. A maior variação de comprimento das arestas da cabeça foi aproximadamente `3.61e-8` unidade, dentro da tolerância numérica de `2e-7`. Esses resultados pertencem à configuração dessa etapa, anterior à separação das rodas.
- **Reutilização:** conferir a ação existente, a orientação e o eixo local no novo personagem antes de inverter o sinal. Preservar a ação de origem, o pivô, a amplitude e os tempos; validar também os quadros intermediários e registrar os resultados na pasta dele.

**Referências:** [procedimento e verificações da animação para a esquerda](../personagens/P001_jake/registros/registro-animacao-cabeca-esquerda-2026-10-15.md), [relatório numérico](../personagens/P001_jake/validacao/validacao_animacao_cabeca_esquerda.json) e [ficha e histórico do P001](../personagens/P001_jake/LEIA-ME.md).

### Quarto prompt — separação das quatro rodas

Este pedido deu origem à etapa **P001.05 — rodas independentes**, após o rig e as animações da cabeça. O texto abaixo preserva o pedido original deste chat para reutilização em personagens com veículo.

#### Pedido original para copiar e reutilizar

> Atue como um artista técnico sênior de 3D e especialista em Blender. Utilizando as ferramentas do **Blender MCP**, pegue a malha do modelo do carro e separe as **quatro rodas** em **quatro objetos totalmente independentes**, seguindo estritamente estas regras:
>
> 1. **Preservação Absoluta da Malha:** Não modifique, redimensione, altere a topologia ou deforme a geometria de nenhuma das rodas. A malha de cada roda deve permanecer exatamente como foi modelada originalmente.
> 2. **Isolamento Geométrico:** Separe fisicamente cada roda do corpo principal do carro (caso estejam unidas na mesma malha), fazendo um corte/desanexação limpa (*mesh separation*).
> 3. **Pontos de Pivô (Origins):** Posicione o ponto de origem (*origin point*) de cada uma das quatro rodas exatamente no **centro geométrico de cada roda**, garantindo que futuros comandos de rotação (para girar ou esterçar) ocorram de forma perfeita e sem deslocamentos estranhos.
> 4. **Organização e Nomenclatura:** Renomeie os quatro objetos de forma padronizada e limpa (ex: `Wheel_Front_Left`, `Wheel_Front_Right`, `Wheel_Rear_Left`, `Wheel_Rear_Right`) para facilitar a exportação para a Godot e o controle via script.

#### Aplicação e referências do quarto prompt

- **Separação:** as rodas do Jake foram isoladas por conjuntos completos de ilhas existentes de `Corpo_Kart`, sem criar, remover ou subdividir os elementos originais. Cada objeto `Wheel_*` recebeu uma malha exclusiva.
- **Pivôs e lados:** foi adotado o centro da caixa delimitadora da geometria de cada roda (`ORIGIN_GEOMETRY`, `BOUNDS`). Neste modelo, a frente é **−Y**, a esquerda do piloto é **+X**, o giro usa **X local** e o esterço usa **Z local**. Conferir novamente a orientação e o critério de centro ao reutilizar o prompt.
- **Rig existente:** as rodas mantiveram o acompanhamento de `Torso_Bone` por parentesco com compensação das transformações, sem o modificador Armature herdado. Continuam independentes como objetos e malhas, embora acompanhem o osso do torso.
- **Validação:** todos os elementos originais foram encontrados exatamente uma vez entre o corpo restante e as quatro rodas; conectividade, UVs, materiais e dados codificados de normais foram preservados. Testes temporários de giro e esterço tiveram deslocamento medido do pivô igual a zero e foram restaurados. As tolerâncias numéricas e as amostras da animação estão no relatório.
- **Reutilização:** salvar um backup, conferir pneus, aros, cubos e suspensão e priorizar ilhas existentes para cumprir a preservação de topologia. Registrar qualquer impedimento antes de usar um corte que crie vértices ou subdivida faces. A exportação e o controle na Godot exigem uma etapa própria de validação.

**Referências:** [procedimento da separação das rodas](../personagens/P001_jake/registros/registro-rodas-independentes-2026-10-15.md), [relatório numérico](../personagens/P001_jake/validacao/verificacao_rodas_independentes.json) e [ficha e histórico do P001](../personagens/P001_jake/LEIA-ME.md).

### Quinto prompt — jogo na Godot, rodas, suspensão e equilíbrio da cabeça

O pedido abaixo foi usado para iniciar a configuração do jogo em `jogo/`. A auditoria **P001.07** executou a implementação existente e encontrou atendimento parcial: a cabeça compensa em regime estabilizado, mas o requisito de ficar **sempre** no lado oposto não é cumprido durante todas as transições e vibrações.

#### Pedido original para copiar e reutilizar

> Estou marcando a pasta do projeto. Dentro dela existem os arquivos 3D correspondentes aos personagens do jogo e o executável do Godot. Inicie a configuração de um jogo onde seja possível escolher um dos personagens e andar com ele em um cenário quadriculado.
>
> Use o CLI do Godot para fazer toda a configuração do projeto.
>
> A câmera deve ficar atrás do personagem e se mover dinamicamente.
>
> **Estrutura dos arquivos 3D:**
>
> - 4 objetos correspondem às rodas do carro
> - 1 objeto corresponde ao corpo do carro
> - 1 objeto corresponde ao personagem
>
> **Regras e Mecânicas:**
>
> 1. Todas as rodas precisam funcionar dinamicamente, girando enquanto o carro se movimenta.
> 2. Faça uma simulação de suspensão e vibração: quando o carro fizer uma curva para a esquerda, a suspensão precisa pender para a direita (simulando inércia).
> 3. Na estrutura de bones (ossos) do personagem (1 osso para o corpo e 1 osso para a cabeça), a cabeça deve sempre girar para o lado inverso da inclinação da suspensão (se o carro joga para um lado, a cabeça pende para o outro tentando equilibrar).

#### Aplicação, validação e limites do quinto prompt

- **Projeto existente:** seleção de Jake, pista com shader quadriculado, movimento arcade e câmera de perseguição em `jogo/`. Há somente um piloto cadastrado; a escolha entre pilotos diferentes ainda não foi validada.
- **Rodas e suspensão:** as quatro rodas giram com velocidade e raio, invertem em ré e param quando a velocidade é zero. As dianteiras esterçam; a carroceria inclina para fora da curva por uma mola visual. Os pivôs das rodas permaneceram fixos nos testes isolados de inclinação.
- **Cabeça:** a meta relativa é `−1,7 × rolagem`, com mola própria. Em uma curva constante sem ruído, o corpo estabilizou em cerca de **+6,875°** e a cabeça em **−4,812°** no espaço do esqueleto; a curva oposta inverteu os sinais. Porém, a 60 passos/s houve **18 quadros no mesmo lado** ao iniciar a curva e **15** ao inverter. A compensação ignora o tremor da carroceria, produzindo outras violações em reta. A palavra **sempre** permanece como requisito pendente, não como comportamento comprovado. **Atualização (T001, 15/10/2026):** a mecânica passou a usar a rolagem total (com o tremor) e uma faixa de oposição por quadro. Com isso, foram 0 quadros no mesmo lado no Dimi e no Jake (cópia do verificador), com 60 e 120 passos/s, com e sem ruído. Ver [T001](../jogo/tarefas/T001-cabeca-sempre-oposta.md).
- **Estrutura real do Jake:** quatro malhas de roda, `Cabeca` e `Corpo_Kart`. O torso do piloto ainda está junto do carro; não há um objeto exclusivo para o personagem inteiro e outro exclusivo para o carro. O GLB tem quatro ossos; `Torso_Bone` e `Head_Bone` são os dois controles usados pela mecânica.
- **Reutilização:** conferir a estrutura e os eixos do GLB importado, testar os dois sentidos, ré, parada, entrada e inversão de curva e vibração. Medir a inclinação global da cabeça, considerando a inclinação herdada do corpo. Definir se o efeito desejado admite atraso de mola ou exige oposição em todo quadro.

**Referências:** [auditoria das regras na Godot](../personagens/P001_jake/registros/registro-validacao-godot-2026-10-15.md), [relatório da execução](../personagens/P001_jake/validacao/validacao_godot_jake.json), [verificador reproduzível](../jogo/ferramentas/validar_mecanicas_jake.gd) e [instruções do jogo](../jogo/LEIA-ME.md).

## 1. Receita para preparar outros personagens

Esta é a **versão 1 da receita**, derivada do primeiro personagem. Ela é um procedimento documentado, ainda sem um script único de execução automática. Os passos abaixo devem ser adaptados à anatomia, à orientação e à estrutura de cada novo modelo.

### Passo 1 — Identificar o personagem e reunir os materiais

1. Criar a pasta `personagens/P00N_nome/` com o próximo identificador, começando por `P002`, e as subpastas da estrutura acima. A ficha do personagem é o `LEIA-ME.md` dessa pasta.
2. Registrar nome, referências visuais, modelo de entrada, arquivo de trabalho e objetivo da primeira etapa.
3. Descrever o que já existe e o que será criado: malha pronta, importação, modelagem, rig ou animação.
4. Definir quais partes precisam de controles independentes. Se houver veículo ou acessórios, registrar se acompanharão o corpo ou terão controles próprios.

**Referência do primeiro caso:** [ficha P001](../personagens/P001_jake/LEIA-ME.md) e [estado inicial do rig](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#2-estado-inicial-observado).

### Passo 2 — Inspecionar e preservar a entrada

1. Consultar a cena real pelo Blender MCP: objetos, transformações, pais, materiais, UVs, modificadores, grupos de vértices, shape keys e animações existentes.
2. Conferir visualmente o personagem e sua orientação.
3. Salvar uma cópia anterior à edição e registrar o caminho.
4. Registrar contagens e coordenadas originais, conectividade, UVs e demais dados necessários à comparação.
5. Adicionar identificadores de rastreamento quando a separação ou a reorganização exigir correspondência entre os elementos originais e finais.

Para uma tarefa de preservação como a do P001, manter a forma e as proporções originais durante a preparação. A referência intacta serve para demonstrar o que foi preservado.

**Referência:** [cópia e registro da geometria](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#4-cópia-de-segurança-e-registro-da-geometria), [backup do P001](../personagens/P001_jake/backups/kart_antes_do_rig_20261015_120547.blend) e [arrays originais do P001](../personagens/P001_jake/backups/geometria_original.npz).

### Passo 3 — Identificar e separar as partes existentes

1. Examinar as ilhas conectadas, as faces e os limites anatômicos, conferindo frente, lado e detalhes relevantes.
2. Aproveitar partes já desconectadas quando isso permitir a separação sem acrescentar ou remover geometria.
3. Separar a cabeça completa, incluindo os elementos que devem acompanhá-la, como olhos, boca e acessórios.
4. Conferir as partes isoladamente e juntas para detectar fragmentos ausentes, partes atribuídas ao conjunto errado e alterações de aparência.
5. Registrar o método efetivamente adotado e as tentativas descartadas. Se uma separação adicional não funcionar, documentar o limite em vez de considerá-la concluída.

No P001, a cabeça foi separada usando **86 ilhas existentes**, sem corte planar ou tampa nova. As tentativas iniciais de separar corpo e kart foram desfeitas. Posteriormente, em **P001.05**, as rodas foram isoladas por conjuntos de ilhas existentes; o corpo e o restante do kart continuam unidos. Para veículos, conferir também pneus, aros, cubos e suspensão antes de atribuir as ilhas a cada roda.

**Referência:** [identificação da cabeça](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#5-inspeção-e-identificação-da-cabeça) e [diagnósticos intermediários](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#6-diagnósticos-e-separações-intermediárias-de-corpo-e-kart).

### Passo 4 — Posicionar os pivôs e construir o esqueleto

1. Localizar a base do pescoço no novo modelo.
2. Ajustar a origem da cabeça com compensação da transformação para preservar sua posição mundial.
3. Colocar o início do osso da cabeça nesse mesmo pivô.
4. Criar a hierarquia necessária. Para um personagem com o mesmo comportamento rígido do P001, usar como referência raiz → torso → pescoço → cabeça.
5. Registrar nomes, posições de repouso, relações de parentesco e quais ossos deformam.

Os valores do pivô devem ser medidos no novo personagem. A mudança de origem altera a representação local dos vértices; medir a preservação no espaço mundial e informar qualquer arredondamento numérico.

**Referência:** [origem e pivô](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#7-origem-e-pivô-da-cabeça) e [armature criada](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#8-armature-criada).

### Passo 5 — Atribuir os pesos e ligar as malhas

1. Para uma parte que deva permanecer rígida, atribuir peso 1.0 a todos os seus vértices no osso responsável.
2. Conferir que nenhum vértice dessa parte recebeu influência de outro osso.
3. Ligar os objetos à armature preservando suas transformações mundiais.
4. Usar o modificador Armature com grupos de vértices e sem envelopes para repetir a configuração do P001.
5. Manter o modificador na pilha e registrar a configuração adotada.

Esse método produz partes rígidas. Um personagem que precise dobrar cotovelos, joelhos ou outras articulações exige uma etapa própria de rig e pesos, com novos testes e referências na ficha do personagem.

**Referência:** [pesos, parentesco e modificadores](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#9-pesos-parentesco-e-modificadores) e [instruções resumidas do rig](../personagens/P001_jake/blender/LEIA-ME_Rig.txt).

Para acessórios que precisam girar como objetos, a etapa **P001.05** oferece outra configuração: malha exclusiva, origem própria e parentesco direto com o osso responsável, com compensação da transformação. As rodas usam essa configuração sem modificador Armature. Medir novamente o acompanhamento do rig e a estabilidade dos pivôs ao aplicar o método em outro modelo; ver o [procedimento das rodas](../personagens/P001_jake/registros/registro-rodas-independentes-2026-10-15.md).

### Passo 6 — Validar antes de animar

1. Comparar elementos originais e finais, verificando presença, contagens, conectividade e UVs.
2. Comparar as coordenadas mundiais da malha-base e da malha avaliada em repouso.
3. Conferir exclusividade e valores dos pesos.
4. Aplicar uma rotação temporária de teste no osso da cabeça e medir se o corpo e o pivô permanecem estáveis.
5. Restaurar a pose de referência após o teste.
6. Salvar o relatório numérico e registrar o que foi verificado visualmente e o que não foi testado.

No primeiro rig, o teste foi de **25°**, sem movimento medido do corpo/kart. O relatório preservou as contagens e mostrou diferenças numéricas de até `2.9802322387695312e-8` unidade na avaliação em repouso. Esses são resultados do P001, não garantias para qualquer outro modelo.

**Referência:** [validação original em JSON](../personagens/P001_jake/validacao/validacao_rig.json) e [descrição dos testes](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#10-validação-executada).

### Passo 7 — Criar uma primeira animação simples

1. Identificar o eixo local correto do osso no novo personagem.
2. Criar uma ação com nome claro e animar apenas o canal necessário.
3. Para repetir a ideia do P001, usar posição inicial → virada → retorno, ajustando o ângulo ao modelo e ao movimento desejado.
4. Definir o FPS e a duração desejada antes de posicionar os keyframes.
5. Conferir keyframes e quadros intermediários, medindo isolamento do corpo e estabilidade do pivô.
6. Configurar o intervalo de prévia e, separadamente, o intervalo de renderização quando houver exportação.

No P001, o canal correto foi Y local de `Head_Bone`, com **0° → 40° → 0°** nos quadros **1 → 25 → 49**. Esse eixo e esses números não devem ser copiados sem conferência.

Para manter a duração ao trocar o FPS, redistribuir os keyframes. Os exemplos já documentados para dois segundos entre início e retorno são 1/25/49 a 24 FPS, 1/31/61 a 30 FPS e 1/61/121 a 60 FPS.

**Referência:** [animação de ida e volta](../personagens/P001_jake/registros/registro-animacao-cabeca-2026-10-15.md#4-animação-de-ida-e-volta), [verificações](../personagens/P001_jake/registros/registro-animacao-cabeca-2026-10-15.md#5-verificações-de-preservação) e [FPS](../personagens/P001_jake/registros/registro-animacao-cabeca-2026-10-15.md#6-orientação-sobre-fps).

### Passo 8 — Salvar, documentar e preparar a próxima etapa

1. Salvar o arquivo de trabalho e preservar os arquivos de entrada e os registros anteriores.
2. Criar um documento detalhado para a etapa executada, com resultado, testes, arquivos e limitações.
3. Acrescentar a etapa ao `LEIA-ME.md` do personagem e colocar o link no índice da documentação.
4. Quando uma alteração modificar o arquivo principal, manter o significado histórico dos relatórios e hashes anteriores. Um hash do rig anterior não identifica o arquivo depois de animado.
5. Quando houver renderização ou exportação, criar uma etapa específica, com formato, destino e validação do resultado. Até essa etapa ocorrer, registrar a exportação como não realizada.

**Referência:** [arquivos do rig](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md#14-arquivos-entregues-e-rastreabilidade), [limites do registro da animação](../personagens/P001_jake/registros/registro-animacao-cabeca-2026-10-15.md#9-arquivos-e-limites-do-registro) e [manifesto histórico do rig](../personagens/P001_jake/validacao/manifesto-artefatos-rig.json).

## 2. O que reaproveitar e o que medir novamente

| Reaproveitar como método | Adaptar ou medir no novo personagem |
| --- | --- |
| Backup e registro anterior às alterações | Caminhos, identidade e origem do modelo |
| Inspeção das partes e validação da separação | Anatomia, ilhas, limites e partes independentes |
| Pivô da cabeça na base do pescoço | Coordenadas do pivô e tamanho dos ossos |
| Hierarquia e pesos exclusivos para partes rígidas | Quantidade de ossos e necessidade de deformação articulada |
| Teste de isolamento entre cabeça e corpo | Eixo local, sentido, amplitude e limites de rotação |
| Comparação numérica e visual | Escala, tolerâncias e resultados medidos |
| Registro por etapas com referências | Ações, FPS, duração e formato de entrega |

Em particular, **não reutilizar como regra geral** os índices de ilhas `294` e `589`, o limite de altura `0.49`, as contagens da malha, o pivô do P001 ou seu eixo de animação. Esses valores vieram da inspeção específica do primeiro modelo.

## 3. Como manter a documentação dos personagens

- Para cada novo personagem, criar uma pasta própria em `personagens/` com identificador sequencial (`P002`, `P003` etc.) e nome. Não substituir nem misturar os arquivos do P001 com os de outro personagem.
- Para cada trabalho no personagem existente, acrescentar uma etapa ao histórico dele. Registrar também ajustes, correções e tentativas relevantes que não ficaram no resultado.
- Incluir em cada etapa: data, pedido, mudança realizada, estado do resultado, testes, limitações e links para o documento detalhado e os artefatos.
- Quando surgir uma técnica reutilizável, atualizar a receita e indicar de qual personagem e etapa ela veio. Um teste em um modelo deve continuar identificado como evidência daquele modelo.
- Preservar os relatos históricos. Se uma informação anterior mudar, acrescentar a evolução e sua referência, deixando claro qual estado foi observado em cada etapa.
- Usar links relativos ao próprio arquivo para que a documentação continue navegável após clonar o projeto.

Modelo de `LEIA-ME.md` para a pasta do próximo personagem:

```markdown
# Personagem P00N — Nome

Primeiro registro: DD/MM/AAAA.
Objetivo e descrição:
Referências visuais:
Modelo de entrada:
Arquivo de trabalho:
Partes e controles independentes:
Estado documentado:

| Etapa | Data | Mudança realizada | Documento e artefatos | Validação e limites |
| --- | --- | --- | --- | --- |
| P00N.01 | DD/MM/AAAA | Descrever | Vincular arquivos | Informar evidências |

Aprendizados que entram na receita:
Próxima etapa ou entregas ainda não realizadas:
```

## 4. Mapa dos documentos de referência

| Documento | Para que consultar |
| --- | --- |
| [Índice da documentação](README.md) | Navegar pelos registros do projeto |
| [Registro do rig](../personagens/P001_jake/registros/registro-rig-personagem-2026-10-15.md) | Reconstituir as operações do primeiro preparo, inclusive tentativas e limites |
| [Validação original do rig](../personagens/P001_jake/validacao/validacao_rig.json) | Conferir os números medidos na etapa de rig |
| [Manifesto histórico](../personagens/P001_jake/validacao/manifesto-artefatos-rig.json) | Identificar as versões dos artefatos na documentação original do rig |
| [Instruções resumidas do rig](../personagens/P001_jake/blender/LEIA-ME_Rig.txt) | Consultar controles e configuração da etapa inicial |
| [Registro da animação](../personagens/P001_jake/registros/registro-animacao-cabeca-2026-10-15.md) | Repetir o movimento de ida e volta, entender FPS e distinguir prévia de exportação |
| [Animação para a esquerda](../personagens/P001_jake/registros/registro-animacao-cabeca-esquerda-2026-10-15.md) | Consultar o espelhamento da ação e as verificações de pivô, rig e malha |
| [Rodas independentes — P001.05](../personagens/P001_jake/registros/registro-rodas-independentes-2026-10-15.md) | Consultar separação por ilhas, nomenclatura, pivôs, parentesco e verificações das rodas |
| [Validação das rodas](../personagens/P001_jake/validacao/verificacao_rodas_independentes.json) | Conferir preservação dos elementos, centros, amostras da animação e testes de giro e esterço |

O registro inicial e suas instruções descrevem o rig antes dos keyframes. A evolução posterior está nos registros de animação e de separação das rodas. Esta atualização documental consulta as evidências salvas das etapas e não constitui uma nova inspeção da cena aberta nem modifica o Blender.
