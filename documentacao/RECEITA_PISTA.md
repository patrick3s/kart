# Receita — criar e integrar uma pista de kart

Este procedimento organiza a criação de novas pistas, do recebimento das referências à execução na Godot. Foi elaborado a partir da modelagem e integração da [PI001](../pistas/PI001_primeira_pista/LEIA-ME.md) e do [fluxo de novos personagens](PROMPT_NOVO_PERSONAGEM.md).

Para iniciar, use o [prompt de nova pista](PROMPT_NOVA_PISTA.md). O [checklist por fases](../pistas/_modelo/CHECKLIST.md) define entregáveis e critérios de conclusão; o [modelo de checkpoint](MODELO_CHECKPOINT_PISTA.md) define o estado necessário para retomar em outra conversa.

## 1. Organização e escopo

Use `PI001`, `PI002` etc. depois do maior identificador realmente existente em `pistas/`, sem reutilizar números ocupados. Preserve o nome de exibição e gere um nome de pasta em minúsculas, sem acentos, com `_` entre palavras. Confira também colisões de nome em `jogo/pistas/`.

```text
pistas/PI00N_nome/
  LEIA-ME.md
  CHECKLIST.md
  CHECKPOINT.md
  referencia/
    LEIA-ME.md
  blender/
    nome.blend
  texturas/
  backups/
  validacao/
    AAAAMMDD_HHMM_descricao/
  registros/
```

`PI00N_nome` e `nome` são exemplos a substituir. O `.blend` deve ser um arquivo Blender real, criado e conferido na inicialização; documentos e pastas não comprovam sua existência. A subpasta de validação é criada quando houver uma execução real. A pasta de runtime `jogo/pistas/nome/` é criada na exportação, com a cena e os recursos efetivamente usados pelo jogo.

Confira `git status` antes de editar e preserve as alterações existentes. As referências recebidas ficam intactas; use cópias de trabalho. Registre data, origem informada, função, tamanho e hashes quando medidos. Recursos comuns de iluminação e céu pertencem a `ambiente/` e `jogo/ambiente/`.

A inicialização organiza os arquivos, cria/confere o projeto exclusivo e planeja as fases. Um pedido para produzir e integrar até ficar jogável autoriza avançar pelas fases necessárias. O checklist e o checkpoint não ampliam o pedido atual. Commit e publicação dependem de solicitação própria.

## 2. Blender MCP e preservação

Use a instância aberta do Blender pelo **Blender MCP** em todas as fases de modelagem, preparação e exportação. Confira caminho aberto, alterações não salvas, modo, cena, coleções e objetos antes de operar. Não inicie outra instância nem use Blender pela CLI como substituto silencioso.

Se outro projeto estiver aberto, preserve primeiro o trabalho dele em uma cópia identificada, sem sobrescrever o original. Só troque o arquivo na mesma sessão depois de conferir a preservação. Se não houver destino seguro para o trabalho pendente, esclareça essa informação com o usuário. Crie o projeto vazio com `wm.read_homefile(use_empty=True)` somente depois desses cuidados; salve no destino exclusivo e recarregue do disco para confirmar caminho e conteúdo. Não deixe cubo, câmera ou luz de exemplo como se fossem parte da pista.

Quando a entrada for `.blend`, preserve o recebido em `referencia/` e prepare uma cópia de trabalho. Com GLB/GLTF/FBX/OBJ, importe uma cópia no projeto exclusivo. Com imagens apenas, crie/confira o projeto vazio e registre **“Projeto criado, aguardando modelo”**; modelar o traçado pertence à fase de produção. Não aplique ajustes automáticos à geometria recebida durante a organização inicial.

Faça backups próprios antes das edições. Uma cópia automática `.blend1` pode ajudar numa recuperação, mas não substitui backup planejado e conferido. Se houver mudança inesperada no arquivo, preserve as versões encontradas, compare hashes e registre a recuperação; não escolha uma versão apenas pelo nome ou horário.

Antes de exportar, confira se a fonte é a versão salva ou a cena aberta com mudanças; registre essa escolha. Prepare a exportação numa cópia/cena temporária pelo MCP, mantendo o projeto original intacto. Restaure seleção, cena e nomes temporários ao finalizar, inclusive se houver falha. Delimite **cena ativa e seleção** para evitar que objetos selecionados em outra cena entrem no GLB.

Sem conexão MCP, registre o bloqueio nas fases dependentes do Blender e continue a documentação possível. Não fabrique um `.blend`, não declare uma exportação executada e não abra uma instância alternativa para contornar a restrição.

## 3. Referências, medidas e eixo

Uma imagem de traçado não determina escala, largura, altitude ou sentido. Registre o que foi informado e o que é provisório. Pergunte apenas por dados indispensáveis sem uma hipótese razoável; decisões reversíveis podem avançar com premissas explícitas.

Para desenhos, extraia um eixo ordenado e fechado, preserve o desenho original e documente o método e as adaptações necessárias para acomodar a largura. Salve os pontos e a convenção de coordenadas em um arquivo próprio, por exemplo `validacao/.../tracado_extraido.json`. Para modelos existentes, extraia o eixo real da curva ou da geometria; não substitua o percurso por uma aproximação circular.

Confira extensão, limites, largura útil, raios de curva, continuidade, fechamento, alturas e possíveis cruzamentos das bordas. Cruzamentos deliberados em níveis diferentes precisam de tratamento de altura e projeção; a busca global pelo ponto mais próximo usada na PI001 não deve ser assumida suficiente para pontes ou trechos muito próximos.

Defina a largada numa região dirigível, preferencialmente uma reta. Registre posição no eixo e sentido pela tangente. Linha quadriculada, malha, percurso e grid devem compartilhar a mesma transformação. Havendo um modelo pronto, não redesenhe nem altere sua escala provisória sem necessidade demonstrada e registrada.

## 4. Modelo e materiais

Organize asfalto, zebras, sinalização e terreno em objetos identificáveis. Adapte a composição à referência; elementos não aplicáveis precisam de justificativa. Eixo e referências devem ficar separados dos objetos exportáveis. Câmeras e luzes de apresentação não entram no recurso do jogo.

Verifique normais, faces degeneradas, arestas abertas inesperadas, espessura, emendas e sobreposições. Use o critério adequado à malha: uma superfície aberta deliberada não deve ser reprovada apenas por não ser um sólido fechado. Capture vista superior e perspectiva e compare com a referência.

Texturas procedurais do Blender não são transportadas integralmente pelo glTF. Escolha e registre uma estratégia: bake de texturas ou material/shader equivalente na Godot. Confira cor, rugosidade, normais/relevo, transparência e sinais no recurso importado e no renderizador real. Diferencie equivalência visual de reprodução exata. Não declare materiais completos pela simples presença de nomes no GLB.

## 5. Exportação e contrato de coordenadas

Exporte recursos para `jogo/pistas/nome/`, incluindo geometria visível, materiais e dependências. Leve o eixo para um `Path3D/Curve3D` fechado ou recurso equivalente, com pontos e unidades documentados. Exporte só os objetos necessários; confirme também os nós reais do GLB final.

A PI001 usou metros, escala 1:1 e a conversão Blender `(x,y,z)` → Godot `(x,z,-y)`. Confira as configurações do exportador e as transformações desta pista antes de aplicar essa convenção; não converta o eixo duas vezes. Compare pontos/limites da malha e do eixo após importar. Verifique fechamento sem trecho faltando ou duplicação indevida.

Guarde manifesto da exportação com arquivos, hashes, contagens, transformações, materiais e exclusões. O `.blend` salvo, o GLB exportado e o recurso importado são três estados distintos e precisam de evidências próprias.

## 6. Cena jogável e catálogo

Crie `jogo/pistas/nome/nome.tscn`, com colisões estáticas adequadas para asfalto, zebras e terreno. Malhas estáticas complexas podem usar colisão por triângulos; verifique custo e normais. Sinalização pintada não precisa de outra colisão coincidente com o asfalto.

Reutilize kart, câmera de perseguição, HUD, controles, personagens e ambiente HDRI existentes. Mantenha a arena antiga e as pistas já cadastradas acessíveis. Inspecione o catálogo/menu atuais antes de adicionar a pista: não replique o seletor fixo de duas opções da PI001 de uma forma que esconda pistas anteriores. Se ele precisar evoluir, registre e valide o novo mapeamento entre opção e cena.

Posicione jogador e adversários pela tangente do eixo, acima do piso, com folga suficiente entre os volumes de colisão e as partes visíveis. Confirme o grid com todos os participantes e personagens; distância entre centros, isoladamente, não prova ausência de sobreposição.

Meça os desníveis entre terreno, asfalto e zebra. Teste subir, descer e retornar do terreno. Na PI001 foi necessário habilitar a transposição de pequenos degraus; o valor precisa ser medido para cada pista. Não use uma elevação indiscriminada que permita atravessar karts, barreiras ou saltar o traçado. Preserve o comportamento padrão da arena.

Inclua a pista e seu acesso em `jogo/ferramentas/construir_cenas.gd` ou no mecanismo de geração vigente. Regenerar as cenas deve manter a nova integração e todas as anteriores. Compare recursos e comportamento; IDs gerados pelo editor podem mudar sem significar alteração funcional.

## 7. IA pelo percurso

Em `jogo/scripts/kart_ia.gd`, o modo legado circular é reservado à arena. Nas pistas de corrida, forneça o eixo real; não use `raio_circuito` como substituto. Preserve a opção legada quando não houver percurso.

Configure **percurso, sentido, personagem, faixa, velocidades e transform de largada antes de `add_child()`**, porque `_ready()` inicializa a IA. Garanta que o percurso já esteja utilizável. A referência aos demais participantes pode ser completada depois que todos existirem, antes da simulação depender dela.

A IA deve antecipar curvas, frear com distância suficiente, manter um único sentido e tratar o progresso com fechamento da volta. Espaçamento e contorno precisam considerar o percurso, não apenas a direção instantânea do kart. Perseguição ou agressividade não podem apontar para fora da via; um jogador parado no grid não deve bloquear indefinidamente a corrida. Ultrapassagens precisam caber na largura útil e considerar a faixa ocupada.

Para ensaios, registre progresso acumulado sem confundir a passagem da linha com retorno ao início. Não teletransporte participantes durante a volta medida. Se houver recuperação ou reposicionamento, conte e informe o evento; não o contabilize como volta limpa.

## 8. Validação e critérios de entrega

Use uma pasta nova por execução relevante em `pistas/PI00N_nome/validacao/`. Grave logs e resultados reais; preserve relatórios anteriores. As ferramentas da PI001 têm destinos e caminhos específicos: adapte entradas e saídas antes de reutilizá-las em outra pista.

| Verificação | Evidência mínima |
| --- | --- |
| Importação e scripts | Execução headless com versão da Godot, comandos, saídas e erros examinados; código zero sozinho não basta |
| Modelo/eixo/largada | Dimensões, coordenadas, fechamento e grid conferidos no recurso importado |
| Controles | Aceleração, frenagem, ré e curvas nos dois sentidos, usando a física real |
| Superfícies | Travessia de zebras, ida ao terreno e retorno, sem travamento indevido |
| Pneus e colisões | Medição dos pneus contra o piso, tolerância explícita e choque com transferência de impulso entre karts |
| IA | Cada adversário por pelo menos uma volta completa, registrando tempo, progresso, desvio, contramão, saídas, colisões e recuperações |
| Personagens | Regressões de todos os pilotos cadastrados; rodas, suspensão, cabeça, câmera e escolha no menu |
| Preservação | Arena/pistas anteriores continuam acessíveis; regeneração mantém as integrações; fontes preservadas conforme o escopo |
| Visual | Jogo aberto no renderizador real e imagens inspecionadas de menu, grid, materiais, escala, câmera e pneus |

Defina “saída da pista”: centro além da meia largura, pneus fora da superfície ou volume da carroceria fora do perímetro são medidas diferentes. Registre o critério e suas limitações. Em vias de largura variável, compare com a largura local em vez de um número fixo.

Uma captura não comprova continuidade de uma volta e um teste headless não comprova aparência. Distinga controles automatizados de pilotagem manual e identificações por nome de medições geométricas. Se um critério obrigatório falhar, corrija e repita os ensaios afetados ou entregue como parcial com o impedimento concreto. Alterações posteriores invalidam as verificações que dependem delas.

## 9. Referência concreta: PI001

A [integração da PI001](../pistas/PI001_primeira_pista/validacao/integracao_20261016/RELATORIO.md) registrou sete malhas, eixo com 1.000 pontos, asfalto de 8 m, zebras de 0,8 m, cinco IAs e os três pilotos. Nas execuções documentadas, cada adversário concluiu a volta em cada escolha de jogador, sem saída pelo critério do centro nem contramão. Esses resultados pertencem à versão auditada, não às próximas pistas.

Valores como 0,28 m de transposição de degrau, filas a 7 m, faixas laterais, antecipação, velocidade e número de pontos são soluções específicas dessa pista, não padrões a copiar sem medição. Os scripts de exportação e validação também contêm caminhos específicos da PI001.

A experiência mostrou a necessidade de conferir seleção em outras cenas, adaptar os materiais procedurais, evitar colisões de largada por convergência de faixa, antecipar a frenagem, permitir contornar um jogador parado e testar o retorno do gramado ao asfalto.

## 10. Estado, retomada e entrega

Mantenha `LEIA-ME.md` como ficha/histórico, `CHECKLIST.md` como tarefas por fase, `CHECKPOINT.md` como resumo atual e `registros/` como detalhamento das decisões e tentativas. Atualize-os após avanços, testes, falhas relevantes e antes de aguardar referências.

Para retomar: leia checkpoint → checklist → ficha; confira arquivos e versões reais; consulte a ferramenta quando o próximo passo depender da sessão. A falta de um checkpoint numa pista antiga autoriza documentar evidências existentes, não inventar execuções ou reiniciar a pista.

A entrega deve apontar cena jogável, opção no menu, controles, artefatos, evidências numéricas e visuais, limitações e próximo passo. Escala/sentido/largada podem continuar provisórios se isso estiver explícito. Classificação, cronômetro e regras de checkpoints/antiatalho são escopo adicional; seguir um eixo não implementa um regulamento de corrida.
