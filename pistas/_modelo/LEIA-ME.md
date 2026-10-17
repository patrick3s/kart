# {{ID}} — {{NOME}}

Modelo para iniciar uma pista pelo [prompt de nova pista](../../documentacao/PROMPT_NOVA_PISTA.md) e pela [receita](../../documentacao/RECEITA_PISTA.md). Reserve o próximo identificador disponível, substitua os campos e remova estas instruções da ficha preenchida. Esta pasta genérica não contém uma pista produzida.

| Item | Definição |
| --- | --- |
| Identificador | {{ID}} |
| Nome de exibição | {{NOME}} |
| Nome seguro/pasta | {{SLUG}} / `pistas/{{PASTA}}/` |
| Data local de criação | A informar |
| Objetivo e escopo autorizado | A informar |
| Tema e cenário | A informar |
| Referência/modelo de entrada | A informar |
| Traçado e sentido | A informar |
| Unidades e escala | A informar; identificar quando provisórias |
| Dimensões e largura útil | A informar |
| Zebras e terreno | A informar |
| Largada, chegada e grid | A informar |
| Regras de corrida, se solicitadas | A informar; eixo de IA não equivale a regulamento |
| Projeto Blender exclusivo | Previsto em `blender/{{SLUG}}.blend`; ainda não criado |
| Estado salvo/conferência do projeto | Não executada |
| Cena na Godot | Prevista em `jogo/pistas/{{SLUG}}/{{SLUG}}.tscn`; ainda não criada |
| Estado geral/fase atual | Planejamento; produção não iniciada |
| Próximo passo concreto | A informar |

## Estado e acompanhamento

Use o [checklist por fases](CHECKLIST.md) e gere `CHECKPOINT.md` a partir do [modelo de checkpoint](../../documentacao/MODELO_CHECKPOINT_PISTA.md). Depois de criá-lo, inclua o link real nesta ficha. Registre somente o que foi executado; organização documental, projeto salvo, modelo validado, recurso importado e pista jogável são estados distintos.

## Organização

- `referencia/`: [inventário](referencia/LEIA-ME.md), desenhos, imagens, modelos e texturas originais recebidos.
- `blender/`: arquivo de trabalho real, exclusivo desta pista, criado/conferido pelo Blender MCP.
- `texturas/`: texturas e mapas específicos de produção.
- `backups/`: cópias conferidas antes de alterações.
- `validacao/`: pastas datadas com medições, logs, imagens e relatórios; sem sobrescrever auditorias anteriores.
- `registros/`: decisões, tentativas e scripts utilizados.

## Validação

Ainda não executada. Ao produzir, registrar separadamente geometria/materiais, importação, controles, colisões/pneus, voltas da IA, regressões dos personagens, preservação do menu/gerador e conferência visual. Vincular somente evidências existentes e correspondentes à versão atual.

## Decisões, limitações e pendências

A informar. Identificar premissas provisórias, materiais equivalentes, critérios de saída da pista e validações ainda necessárias. Não reutilizar valores ou resultados da PI001 como se fossem desta pista.

## Histórico

Adicionar cada etapa realmente concluída com data, resultado e links para arquivos existentes. A cópia deste modelo não comprova criação do `.blend` ou execução de testes.
