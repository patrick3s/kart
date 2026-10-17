# Ambiente — referências e modelos reutilizáveis

Pasta das referências visuais e dos modelos reutilizáveis de ambiente do jogo, compartilhados por pilotos e pistas. Criada em 16/10/2026.

As imagens e os arquivos recebidos em `referencia/` são preservados como originais. Os objetos reutilizáveis têm projetos próprios em [`modelos/`](modelos/LEIA-ME.md), separados por categoria. O que o jogo usar de fato (HDRI, modelos, texturas e materiais finais) é copiado ou produzido em `jogo/ambiente/`. Assim, a Godot importa apenas recursos de uso no jogo, mantendo as fontes de criação separadas.

## Onde colocar cada arquivo

| Pasta | Conteúdo |
| --- | --- |
| [`referencia/iluminacao/`](referencia/iluminacao/) | Fotos ou prints de luz e clima: horário, direção e cor do sol, sombras, neblina, luzes noturnas |
| [`referencia/ceu/`](referencia/ceu/) | Imagens de céu, nuvens e HDRIs (`.hdr`, `.exr`, `.jpg`, `.png`) |
| [`referencia/textura/`](referencia/textura/) | Fotos e mapas de superfície: asfalto, grama, terra, muros, zebras, guard-rails (`basecolor`, `normal`, `roughness` etc.) |
| `referencia/revisar/` | Entrada para triagem: arquivos novos que ainda serão organizados. Após a conferência, registre o destino; ao copiar uma referência para um modelo, preserve o original e identifique a cópia |

Mantenha os nomes originais dos arquivos quando possível. Se uma textura vier com vários mapas, use uma subpasta com o nome do material (por exemplo, `referencia/textura/asfalto_01/`).

## Inventário

Conferido em 16/10/2026. Arquivo colocado pelo usuário em `referencia/revisar/` e movido sem alteração (mesmo SHA-256).

| Arquivo | Pasta | Tipo | Função | Origem informada | Conferência |
| --- | --- | --- | --- | --- | --- |
| [`kloofendal_48d_partly_cloudy_puresky_4k.exr`](referencia/ceu/kloofendal_48d_partly_cloudy_puresky_4k.exr) | `ceu/` | HDRI OpenEXR, panorama equirretangular 4096×2048 (2:1), RGBA em float 32 bits, compressão PIZ, 75,6 MB | Céu de dia parcialmente nublado e **iluminação ambiente** do cenário (o HDRI ilumina a cena e também aparece como fundo) | Colocado pelo usuário. Pelo nome e pelos metadados, é o “Kloofendal 48d Partly Cloudy (Pure Sky)” do Poly Haven (render de 2022 no Cycles). A licença do Poly Haven é CC0, mas ela não está registrada no arquivo | SHA-256 `c63773fc…19313a16`; cabeçalho lido; imagem não visualizada. A versão “Pure Sky” tem só o céu, sem chão fotografado; a metade de baixo não foi conferida |

O HDRI fica em `ceu/` porque também é a fonte de iluminação. A pasta `iluminacao/` é para referências de aparência (fotos de como a luz deve ficar), não para uma segunda cópia do mesmo arquivo.

**Uso no jogo (16/10/2026):** o HDRI é o céu e a luz ambiente da pista e do menu. Veja a seção [Céu no jogo](#céu-no-jogo).

**Versionamento:** `.exr` não está no Git LFS (`.gitattributes` cobre só `.blend`). Com 75,6 MB, o arquivo cabe no limite de 100 MB do GitHub, mas pesa no histórico. Convém incluir `*.exr` e `*.hdr` no LFS antes do commit.

## Céu no jogo

Aplicado em 16/10/2026, a pedido do usuário.

- **Cópia no jogo:** [`jogo/ambiente/kloofendal_48d_partly_cloudy_puresky_4k.exr`](../jogo/ambiente/kloofendal_48d_partly_cloudy_puresky_4k.exr), idêntica à referência (SHA-256 `c63773fc…19313a16`). Importada pela Godot 4.7.2 com compressão de VRAM (`compress/mode=2`, BC6H), como as texturas dos pilotos, para não ocupar ~64 MB de memória de vídeo sem compressão.
- **Cenas:** a função `_ambiente()` de [`jogo/ferramentas/construir_cenas.gd`](../jogo/ferramentas/construir_cenas.gd) trocou o `ProceduralSkyMaterial` por um `PanoramaSkyMaterial` com o HDRI. `cenas/pista.tscn` e `cenas/selecao_personagem.tscn` foram regeneradas. Fora os identificadores internos que o gerador recria, só mudaram o céu, a neblina e a luz `Sol`.
- **Sol:** medido nos pixels do HDRI, a 47,9° de altura. A luz `Sol` passou de `(−55°, −35°, 0)` para `(−47,9°, −34,3°, 0)`. Renderizado com exposição baixa, o disco do sol no céu fica a **~0,3°** da direção da luz, sem girar o céu (`sky_rotation` = 0). A sombra cai do mesmo lado que antes.
- **Neblina:** cor = média da faixa do horizonte no HDRI (linear `0,436 / 0,469 / 0,567`); `fog_sky_affect = 0`, para a neblina esconder a borda do piso sem cobrir o céu. Densidade mantida (0,004).
- **Regressão:** `validar_mecanicas_bryan.gd` (saída no rascunho) com todas as conclusões verdadeiras; só o instantâneo `percurso` variou, como em qualquer execução. As cenas não entram nos hashes dos verificadores.
- **Imagens:** [`registros/vistas_ceu/`](registros/vistas_ceu/), tiradas por `capturar_vistas_bryan.gd` com a pasta no rascunho.
- **Limitações:**
  - no menu, atrás do pedestal, aparece a metade de baixo do HDRI “Pure Sky”, um chão liso e desfocado que reflete as nuvens;
  - as imagens das Fases 8 dos pilotos e da T001 foram feitas com o céu antigo e não foram refeitas (as mecânicas não dependem do céu);
  - o HDRI de 4K pesa 75,6 MB no repositório; a versão 2K bastaria para um fundo de jogo.


## Modelos reutilizáveis — estrutura criada em 16/10/2026

A biblioteca [modelos/](modelos/LEIA-ME.md) possui categorias para barreiras/guarda-corpos, obstáculos, árvores e túneis, além de um modelo de estrutura com ficha, checkpoint e pastas de referência, Blender, texturas, backups, validação e registros.

A [barreira reta vermelha e branca](modelos/barreiras/barreira_reta_vermelha_branca/LEIA-ME.md) já tem sua pasta própria e uma cópia conferida da imagem fornecida. O original continua em `referencia/revisar/`; o modelo 3D ainda será recebido. As categorias correspondentes de [jogo/ambiente/modelos/](../jogo/ambiente/modelos/LEIA-ME.md) estão preparadas para futuras exportações.
