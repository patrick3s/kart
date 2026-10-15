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
