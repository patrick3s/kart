# Modelo — checkpoint de pista

Use o conteúdo a partir de “Checkpoint” em `pistas/PI00N_nome/CHECKPOINT.md` ao executar o [prompt de nova pista](PROMPT_NOVA_PISTA.md). Substitua `{{...}}` pelos dados reais. Informações desconhecidas ficam como **“A informar”** e saídas futuras como **“Ainda não criado”**. Não copie estas instruções introdutórias para a pista.

O modelo descreve a organização inicial. Ajuste fase, estado e próximo passo ao resultado observado; não registre criação do `.blend` se a operação estiver bloqueada. Links para arquivos específicos só devem ser criados depois de conferir sua existência.

---

# Checkpoint — {{ID}} — {{NOME}}

| Campo | Estado |
| --- | --- |
| Identificador | {{ID}} |
| Nome de exibição | {{NOME}} |
| Pasta | `pistas/{{PASTA}}/` |
| Atualizado em | {{DATA_HORA_LOCAL_COM_FUSO}} |
| Estado geral | {{ESTADO_REAL}} |
| Fase e tarefa atuais | {{FASE_E_TAREFA}} |
| Último passo confirmado | {{ULTIMA_ACAO_COM_EVIDENCIA}} |
| Próximo passo concreto | {{PROXIMA_ACAO}} |
| Receita consultada | {{REVISAO_DA_RECEITA_E_ESTADO_LOCAL}} |
| Projeto Blender exclusivo | `blender/{{SLUG}}.blend` |
| Estado do projeto | {{VAZIO_MODELO_CARREGADO_OU_CRIACAO_BLOQUEADA}} |
| Cena Godot | {{CAMINHO_REAL_OU_AINDA_NAO_CRIADA}} |

## Objetivo e escopo autorizado

{{PEDIDO_DO_USUARIO_E_LIMITES_ATUAIS}}

Diferencie inicialização, modelagem, integração e validação completa. O planejamento não amplia o pedido. Na retomada, prevalece a solicitação atual do usuário.

## Traçado, medidas e largada

| Item | Decisão ou pendência |
| --- | --- |
| Referência principal e origem | {{ARQUIVO_RECEBIDO_E_ORIGEM_OU_A_INFORMAR}} |
| Modelo/eixo de entrada | {{ENTRADA_REAL_OU_A_INFORMAR}} |
| Tema e terreno | {{DEFINICAO_OU_A_INFORMAR}} |
| Unidade e escala | {{VALOR_E_SE_E_PROVISORIO}} |
| Largura útil e zebras | {{VALORES_MEDIDOS_OU_A_INFORMAR}} |
| Extensão e fechamento | {{MEDICAO_E_EVIDENCIA_OU_NAO_VERIFICADO}} |
| Sentido | {{SENTIDO_E_CONVENCAO_OU_A_INFORMAR}} |
| Largada e grid | {{POSICAO_TANGENTE_ESPACAMENTO_OU_A_INFORMAR}} |
| Adaptações do desenho | {{MUDANCAS_JUSTIFICADAS_OU_NENHUMA}} |
| Transformação Blender → Godot | {{CONVENCAO_CONFERIDA_OU_NAO_VERIFICADA}} |

## Arquivos e versões observadas

Os caminhos abaixo são relativos a este checkpoint. Registre tamanho/revisão/hash somente quando conferidos. Preserve os originais e diferencie a cópia de trabalho.

| Item | Caminho | Estado e evidência |
| --- | --- | --- |
| Ficha | `LEIA-ME.md` | {{ESTADO}} |
| Checklist | `CHECKLIST.md` | {{ESTADO}} |
| Inventário | `referencia/LEIA-ME.md` | {{ESTADO}} |
| Referência/modelo original | {{CAMINHO_OU_A_INFORMAR}} | {{PRESERVACAO_CONFERIDA_OU_NAO_VERIFICADA}} |
| Projeto de trabalho | `blender/{{SLUG}}.blend` | {{EXISTENCIA_TAMANHO_RECARGA_OU_BLOQUEIO}} |
| Backup anterior à edição | {{CAMINHO_OU_AINDA_NAO_CRIADO}} | {{RESULTADO_DA_CONFERENCIA}} |
| Eixo da pista | {{CAMINHO_OU_AINDA_NAO_CRIADO}} | {{PONTOS_UNIDADES_FECHAMENTO_E_VERSAO}} |
| Exportação | {{CAMINHO_OU_AINDA_NAO_CRIADA}} | {{HASH_E_RESULTADO_OU_NAO_EXECUTADA}} |
| Cena jogável | {{CAMINHO_OU_AINDA_NAO_CRIADA}} | {{RESULTADO_OU_NAO_EXECUTADA}} |
| Última pasta de validação | {{CAMINHO_OU_AINDA_NAO_CRIADA}} | {{ARTEFATO_A_QUE_SE_REFERE}} |

## Estado das ferramentas

- **Blender MCP:** {{SESSAO_CONSULTADA_ARQUIVO_MODO_E_CONEXAO_OU_NAO_VERIFICADO}}.
- **Salvamento:** {{ARQUIVO_EM_DISCO_E_ALTERACOES_NAO_SALVAS_OBSERVADAS}}.
- **Preservação de outra sessão:** {{COPIA_CONFERIDA_OU_NAO_SE_APLICA}}.
- **Godot:** {{VERSAO_IMPORTACAO_EXECUCAO_E_ARTEFATO_OBSERVADOS_OU_NAO_VERIFICADO}}.
- **Menu e gerador:** {{CADASTRO_DA_PISTA_E_ESTADO_DA_REGENERACAO_OU_NAO_VERIFICADO}}.

Este estado é uma observação datada; não comprova que uma ferramenta ainda esteja aberta na retomada.

## Validações executadas

Não preencha resultados com metas ou com evidências de outra versão.

| Área | Resultado observado | Evidência e limitações |
| --- | --- | --- |
| Geometria e materiais no Blender | Não executada | A informar |
| Exportação, escala e alinhamento | Não executada | A informar |
| Importação/scripts headless | Não executada | A informar |
| Colisões, controles, zebras e terreno | Não executada | A informar |
| Pneus e colisões entre karts | Não executada | A informar |
| Volta de cada IA | Não executada | A informar |
| Regressões dos personagens | Não executada | A informar |
| Menu, pistas anteriores e regeneração | Não executada | A informar |
| Conferência visual renderizada | Não executada | A informar |
| Pilotagem manual | Não executada | A informar |

Para a IA, registre participantes, duração, progresso, voltas, critério de saída, desvios, contramão e recuperações. Para os pneus, registre método e tolerância. Diferencie código, renderização e inspeção visual efetiva.

**Validações a refazer após mudanças:** {{LISTA_E_MOTIVO_OU_NENHUMA_IDENTIFICADA}}.

## Decisões e preservação

- {{DECISOES_ESPECIFICAS_E_PREMISSAS_PROVISORIAS}}.
- {{ARQUIVOS_ANTERIORES_E_PISTAS_PERSONAGENS_QUE_DEVEM_SER_PRESERVADOS}}.
- {{ESTRATEGIA_DE_MATERIAIS_E_DESNIVEIS_OU_A_DEFINIR}}.
- {{LIMITACOES_CONHECIDAS_SEM_CONVERTER_EM_SUCESSO}}.

## Pendências e impedimentos

- **Material aguardado:** {{ARQUIVOS_OU_NENHUM}}.
- **Pedido/pergunta ao usuário:** {{PERGUNTA_E_CAMINHO_DAS_REFERENCIAS_OU_NENHUMA}}.
- **Impedimento técnico:** {{FALHA_COMPROVADA_OU_NENHUM_IDENTIFICADO}}.
- **Ação para destravar:** {{ACAO_CONCRETA_OU_NAO_SE_APLICA}}.
- **Pendências de produto:** {{APROVACAO_MEDIDAS_CENARIO_REGRAS_OU_NENHUMA}}.

## Última tentativa

- **Ação executada:** {{ACAO}}.
- **Resultado:** {{OBSERVACAO_CONFIRMADA}}.
- **Evidência:** {{CAMINHO_EXISTENTE_OU_NAO_SE_APLICA}}.
- **Falha, se houver:** {{FALHA_E_ESTADO_PRESERVADO}}.

Uma tentativa malsucedida não substitui o último passo confirmado no resumo.

## Como retomar

1. Ler `CHECKPOINT.md`, `CHECKLIST.md` e `LEIA-ME.md` da pista.
2. Conferir existência, versão e hashes relevantes dos arquivos; consultar as ferramentas quando o próximo passo depender delas.
3. Verificar se as referências/respostas pendentes chegaram e registrar divergências do estado anterior.
4. Executar o próximo passo dentro do pedido atual, preservando os originais e as etapas comprovadas.
5. Atualizar ficha, checklist, evidências e este checkpoint antes de encerrar ou aguardar material.
