# Modelos compartilhados na Godot

Destino das exportações utilizadas pelo jogo. Arquivos de criação, referências e backups ficam em [ambiente/modelos/](../../../ambiente/modelos/LEIA-ME.md).

Categorias preparadas: [barreiras/](barreiras/), [obstaculos/](obstaculos/), [arvores/](arvores/) e [tuneis/](tuneis/). Elas estão vazias, reservadas para exportações futuras.

Ao integrar um recurso, use:

```text
CATEGORIA/nome_do_modelo/
├── nome_do_modelo.glb
├── nome_do_modelo.tscn
├── materiais/             # Quando houver materiais externos
└── texturas/              # Quando houver texturas externas
```

Crie apenas os arquivos e dependências reais. A cena `.tscn` deve reunir visual, configurações e colisões adequadas, para ser instanciada por diferentes pistas. Confira escala, orientação, pivô, encaixes, materiais e passagem livre de túneis antes de considerá-la pronta. Esta estrutura não adiciona objetos às pistas nem comprova importação de um modelo.
