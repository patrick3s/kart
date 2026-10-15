# Modelo — checkpoint de personagem

Copie a partir do título “Checkpoint” abaixo para `personagens/P00N_nome/CHECKPOINT.md` ao executar o [prompt de novo personagem](PROMPT_NOVO_PERSONAGEM.md). Substitua os campos `{{...}}` por dados reais; informações ainda desconhecidas ficam como **“A informar”**. Não copie estas instruções introdutórias para o arquivo do personagem.

O exemplo é um estado inicial sem referências recebidas. Ajuste-o se o usuário já tiver fornecido os arquivos. Substitua `{{SLUG}}` pelo nome seguro usado para o arquivo Blender. Registre o resultado real da criação do projeto: vazio, com modelo carregado ou bloqueado. Ao atualizar um checkpoint existente, preserve os resultados confirmados e substitua o resumo pelo estado atual.

---

# Checkpoint — {{ID}} — {{NOME}}

| Campo | Estado |
| --- | --- |
| Identificador | {{ID}} |
| Nome de exibição | {{NOME}} |
| Pasta no repositório | `personagens/{{PASTA}}/` |
| Atualizado em | {{DATA_HORA_LOCAL_COM_FUSO}} |
| Estado | Aguardando referências |
| Fase atual | Fase 1 — Referências e escopo |
| Tarefa atual | Receber e conferir as referências |
| Último passo confirmado | {{ULTIMA_ACAO_REALMENTE_CONCLUIDA}} |
| Próximo passo | Conferir os arquivos recebidos em `referencia/` e atualizar o inventário |
| Receita consultada | {{REVISAO_DA_RECEITA_E_ESTADO_LOCAL}} |
| Projeto Blender exclusivo | `blender/{{SLUG}}.blend` |
| Estado do projeto Blender | {{ESTADO_REAL_DO_PROJETO_BLENDER}} |

## Objetivo e escopo

{{OBJETIVO_E_ESCOPO_INFORMADOS_PELO_USUARIO}}

Na inicialização, o trabalho consiste em organizar o personagem, criar e conferir seu projeto Blender exclusivo, solicitar referências, preparar uma cópia do modelo de entrada quando disponível e montar o planejamento. As demais fases permanecem no checklist; registre aqui mudanças posteriores de escopo comunicadas pelo usuário.

## Arquivos e evidências

Preencha cada estado após conferir o arquivo. Só crie um link quando o destino existir; para saídas futuras, registre “Ainda não criado”.

| Item | Caminho relativo ao checkpoint | Estado ou evidência |
| --- | --- | --- |
| Ficha | `LEIA-ME.md` | {{ESTADO_DA_FICHA}} |
| Checklist | `CHECKLIST.md` | {{ESTADO_DO_CHECKLIST}} |
| Inventário das referências | `referencia/LEIA-ME.md` | {{ESTADO_DO_INVENTARIO}} |
| Referências recebidas | A informar | Aguardando arquivos |
| Modelo de entrada | A informar | Ainda não identificado |
| Arquivo de trabalho | `blender/{{SLUG}}.blend` | {{ESTADO_REAL_DO_ARQUIVO_DE_TRABALHO}} |
| Conferência do `.blend` em disco | {{EVIDENCIA_EXISTENTE_OU_NAO_EXECUTADA}} | {{RESULTADO_DA_ABERTURA_ISOLADA}} |
| Backup do modelo | A informar | Ainda não criado |
| Exportação para o jogo | A informar | Ainda não criada |
| Última validação | A informar | Ainda não executada |

## Estado das ferramentas e dos artefatos

- **Blender:** {{FERRAMENTA_OU_INSTANCIA_UTILIZADA_E_RESULTADO}}.
- **Arquivo salvo versus cena aberta:** {{CAMINHO_SALVO_CONFERIDO_E_ESTADO_DA_SESSAO_OU_NAO_VERIFICADO}}.
- **Conteúdo do projeto:** {{CENA_VAZIA_MODELO_CARREGADO_OU_CRIACAO_BLOQUEADA}}.
- **Modelo de origem e dependências:** {{ENTRADA_PRESERVADA_TEXTURAS_CONFERIDAS_E_PENDENCIAS_OU_A_INFORMAR}}.
- **Godot:** importação e execução deste personagem ainda não verificadas.
- **Revisão/hash dos artefatos:** ainda não medidos.
- **Validações a refazer:** a definir após identificar o modelo e suas alterações.

Ao trabalhar nos modelos, substitua este resumo pelo último estado observado: arquivo e versão usados, salvamento confirmado, alterações não salvas, testes e relatórios correspondentes. A existência de um arquivo não comprova que ele foi aberto ou validado.

## Decisões e restrições

- Preservar o nome de exibição e usar a pasta exclusiva deste personagem.
- Manter o `.blend` de trabalho separado das referências originais e dos projetos dos outros personagens.
- Não reaproveitar medidas, índices de ilhas ou resultados do Jake como se fossem deste modelo.
- Registrar aqui as decisões específicas já tomadas; dúvidas continuam em pendências.

## Pendências e impedimentos

- **Material aguardado:** imagens disponíveis, modelo 3D se existir e suas texturas.
- **Solicitação ao usuário:** {{SOLICITACAO_FEITA_E_CAMINHO_DAS_REFERENCIAS}}.
- **Pergunta sem resposta:** {{PERGUNTA_PENDENTE_OU_NENHUMA}}.
- **Impedimento técnico conhecido:** {{IMPEDIMENTO_COMPROVADO_OU_NENHUM_IDENTIFICADO}}.

## Última tentativa e resultado

- **Ação:** {{ULTIMA_ACAO_EXECUTADA}}.
- **Resultado observado:** {{RESULTADO_CONFIRMADO}}.
- **Evidência:** {{ARQUIVO_OU_REGISTRO_EXISTENTE_OU_NAO_SE_APLICA}}.
- **Em caso de falha:** {{FALHA_OBSERVADA_OU_NAO_SE_APLICA}}. Uma tentativa que falhou não substitui o último passo confirmado no resumo.

## Como retomar

1. Ler este checkpoint, `CHECKLIST.md` e `LEIA-ME.md`.
2. Conferir se os arquivos relevantes existem e correspondem às versões registradas.
3. Verificar se as referências ou respostas pendentes chegaram; consultar o Blender/Godot quando o próximo passo depender do estado deles.
4. Executar o próximo passo dentro do pedido atual e registrar o resultado real, sem repetir etapas já verificadas.
5. Atualizar checkpoint, checklist e ficha com estado, evidências e próximo passo consistentes.
