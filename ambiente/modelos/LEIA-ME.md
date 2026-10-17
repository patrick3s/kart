# Modelos reutilizáveis de ambiente

Biblioteca de criação dos objetos que podem ser usados em várias pistas. Cada categoria contém uma pasta por recurso; o modelo pronto para o jogo fica separado em [jogo/ambiente/modelos/](../../jogo/ambiente/modelos/).

| Categoria | Conteúdo |
| --- | --- |
| [barreiras/](barreiras/) | Barreiras retas/curvas e guarda-corpos |
| [obstaculos/](obstaculos/) | Cones, pneus, caixas, pedras e demais obstáculos |
| [arvores/](arvores/) | Árvores e variações de vegetação |
| [tuneis/](tuneis/) | Entradas, saídas e módulos de túneis |

## Como adicionar um modelo

1. Escolha a categoria e copie [_modelo/](_modelo/) para `CATEGORIA/nome_do_modelo/`.
2. Use nome em minúsculas, sem acentos e com `_` entre palavras; preserve o nome de exibição na ficha. Se a pasta existir, retome-a em vez de sobrescrever.
3. Coloque imagens e modelos originais recebidos em `referencia/`, com suas texturas/dependências. Preserve os originais.
4. Use `blender/` para o projeto real de trabalho, `texturas/` para produção e as demais pastas para backups, validações e registros. Preencha `LEIA-ME.md` e `CHECKPOINT.md` com o estado real.
5. Quando exportar e integrar, crie `jogo/ambiente/modelos/CATEGORIA/nome_do_modelo/` com `.glb`, `.tscn`, materiais e texturas necessários. As pistas instanciam essa cena, sem copiar o recurso para cada pista.

```text
nome_do_modelo/
├── LEIA-ME.md
├── CHECKPOINT.md
├── referencia/    # Imagens e modelos originais recebidos
├── blender/       # Projeto .blend de trabalho
├── texturas/      # Texturas de produção
├── backups/
├── validacao/
└── registros/
```

As pastas vazias têm `.gitkeep` para poderem ser versionadas. O modelo de organização não inclui arquivos 3D fictícios. A estrutura foi preparada; a criação e a validação de cada recurso ocorrem depois que o modelo estiver disponível.

## Primeiro recurso organizado

- [Barreira reta vermelha e branca](barreiras/barreira_reta_vermelha_branca/LEIA-ME.md): referência copiada e conferida; aguardando modelo 3D.

As pastas das outras categorias estão prontas para receber recursos. Para objetos de outra família, adicione uma categoria seguindo a mesma organização.
