# Pistas

Arquivos de criação das pistas: referências, modelos do Blender, texturas, backups e registros. Os recursos usados pela Godot ficam em [`jogo/pistas/`](../jogo/pistas/).

Para a primeira pista, coloque as imagens diretamente em [`PI001_primeira_pista/referencia/`](PI001_primeira_pista/referencia/). A ficha fica em [`PI001_primeira_pista/LEIA-ME.md`](PI001_primeira_pista/LEIA-ME.md); o nome é provisório.

A pasta [`referencia/revisar/`](referencia/revisar/) continua como entrada para referências que ainda não têm uma pista definida. Depois de identificar a pista, mova os arquivos para a pasta `referencia/` dela, mantendo os originais. A pasta `_modelo/` deve ficar sem referências específicas, pois serve para criar outras pistas.

Para iniciar uma pista, copie [`_modelo/`](_modelo/) para `PI001_nome_da_pista/`. Nas próximas, use `PI002_nome_da_pista/`, `PI003_nome_da_pista/` e assim por diante. O prefixo `PI` diferencia as pistas dos personagens (`P001`, `P002` etc.).

```text
pistas/
├── LEIA-ME.md
├── PI001_primeira_pista/    # Primeira pista; mesma estrutura do modelo abaixo
├── referencia/
│   └── revisar/             # Referências ainda sem pista definida
└── _modelo/                 # Copiar para PI001_nome_da_pista
    ├── LEIA-ME.md           # Ficha da pista
    ├── referencia/          # Traçado, imagens e modelos recebidos
    ├── blender/             # Arquivo .blend de trabalho
    ├── texturas/            # Texturas de trabalho específicas da pista
    ├── backups/             # Cópias anteriores às alterações
    ├── validacao/           # Relatórios e imagens de conferência
    └── registros/           # Histórico e scripts de produção
```

Os recursos comuns de céu, iluminação e superfícies continuam em [`ambiente/`](../ambiente/LEIA-ME.md). Guarde em cada pista apenas o material específico dela.

Ao integrar uma pista, crie `jogo/pistas/nome_da_pista/` com a cena `.tscn`, os modelos exportados e os materiais necessários. A pista atual permanece em `jogo/cenas/pista.tscn`; esta estrutura ainda não cria nem integra uma nova pista.
