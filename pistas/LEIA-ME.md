# Pistas

Arquivos de criação das pistas: referências, projetos Blender exclusivos, texturas, backups, validações e registros. Os recursos usados pela Godot ficam em [`jogo/pistas/`](../jogo/pistas/).

## Criar ou retomar uma pista

Use o [prompt de nova pista](../documentacao/PROMPT_NOVA_PISTA.md), seguindo a [receita de produção e integração](../documentacao/RECEITA_PISTA.md). O fluxo mantém uma ficha, um checklist por fases e um checkpoint por pista, como no fluxo de personagens.

> Execute o fluxo de `documentacao/PROMPT_NOVA_PISTA.md` para a pista “NOME”.

O pedido acima inicia a organização e o projeto Blender exclusivo. Para produzir até ficar jogável, acrescente esse objetivo expressamente; o prompt contém exemplos de produção completa e retomada.

Consulte as pastas reais e reserve o próximo identificador depois do maior número ocupado: `PI001`, `PI002` etc. Não copie para um identificador já existente. O prefixo `PI` diferencia pistas de personagens (`P001`, `P002` etc.). A pasta [`_modelo/`](_modelo/) contém a [ficha](_modelo/LEIA-ME.md), o [checklist](_modelo/CHECKLIST.md) e o [inventário de referências](_modelo/referencia/LEIA-ME.md); gere o checkpoint a partir do [modelo próprio](../documentacao/MODELO_CHECKPOINT_PISTA.md), preenchendo dados reais.

```text
pistas/
├── LEIA-ME.md
├── PI00N_nome/
│   ├── LEIA-ME.md           # Identidade, decisões e histórico
│   ├── CHECKLIST.md         # Tarefas e critérios por fase
│   ├── CHECKPOINT.md        # Estado atual e próximo passo
│   ├── referencia/          # Inventário, traçado, imagens e originais
│   ├── blender/nome.blend   # Projeto real e exclusivo, criado via Blender MCP
│   ├── texturas/            # Texturas de trabalho específicas da pista
│   ├── backups/             # Cópias anteriores às alterações
│   ├── validacao/           # Pastas datadas de relatórios, logs e imagens
│   └── registros/           # Decisões e scripts de produção
├── referencia/revisar/      # Entrada ainda sem pista definida
└── _modelo/                # Documentos genéricos; sem referências específicas
```

`PI00N_nome` é um exemplo, não uma pasta a criar literalmente. O `.blend` só é considerado criado depois de salvar e conferir seu carregamento. Na retomada, leia `CHECKPOINT.md` → `CHECKLIST.md` → `LEIA-ME.md` e reconfira os arquivos relevantes; não dependa do estado antigo de uma sessão.

A pasta [`referencia/revisar/`](referencia/revisar/) continua como entrada para materiais sem pista definida. Depois de identificar a pista, organize cópias na pasta `referencia/` dela, preservando os originais e a origem informada. Não coloque referências específicas em `_modelo/`.

## Pistas existentes

- [PI001 — Primeira pista](PI001_primeira_pista/LEIA-ME.md): modelo e integração jogável usados como referência deste fluxo; [checkpoint](PI001_primeira_pista/CHECKPOINT.md) e [relatório de integração](PI001_primeira_pista/validacao/integracao_20261016/RELATORIO.md). Os resultados e parâmetros documentados pertencem à versão auditada dessa pista.

## Integração no jogo

Crie `jogo/pistas/nome/` na exportação, com a cena, modelos, percurso e materiais necessários. Use o eixo real para a IA, configure os adversários antes de `_ready()` e atualize menu e gerador sem remover pistas anteriores. A arena original permanece em `jogo/cenas/pista.tscn`; a PI001 está acessível no menu. Veja a [organização dos recursos Godot](../jogo/pistas/LEIA-ME.md).

Os recursos comuns de céu e iluminação continuam em [`ambiente/`](../ambiente/LEIA-ME.md) e `jogo/ambiente/`. Guarde em cada pista apenas o material específico dela.

A entrega distingue testes headless, simulação das voltas e conferência visual no renderizador. Preserve evidências anteriores e registre medidas provisórias, limitações e pendências.
