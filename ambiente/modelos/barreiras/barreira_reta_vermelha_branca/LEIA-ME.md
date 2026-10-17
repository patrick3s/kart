# Barreira reta vermelha e branca

| Campo | Estado |
| --- | --- |
| Categoria | Barreiras e guarda-corpos |
| Nome seguro | `barreira_reta_vermelha_branca` |
| Estado | Modelo preparado, exportado e aplicado nas duas bordas da PI001 (16/10/2026) |
| Referência | [Imagem fornecida](<referencia/Barreira reta de autódromo vermelha e branca.png>) |
| Modelo recebido | [`referencia/Barreira reta de autódromo vermelha e branca.glb`](<referencia/Barreira reta de autódromo vermelha e branca.glb>): Tripo, 1.908.132 faces, 0,98 × 0,18 × 0,27 m, texturas 4K (cor, normal, rugosidade/metal). Preservado sem alteração |
| Projeto Blender | [`blender/barreira_reta_vermelha_branca.blend`](blender/barreira_reta_vermelha_branca.blend) |
| Dimensões | **3,50 × 0,66 × 0,98 m** (comprimento X × profundidade Y × altura Z); escala uniforme ×3,572 do original |
| Pivô | Centro da base (Z = 0). Comprimento em X; a frente (−Y local) fica voltada para a pista |
| Encaixe | Módulos ponta a ponta a cada ~3,5 m; nas curvas, o comprimento é ajustado pela escala X (0,90–1,00) |
| Malha de jogo | Decimada para 12.000 triângulos; texturas reduzidas para 1K em [`texturas/`](texturas/) |
| Exportação Godot | [`jogo/ambiente/modelos/barreiras/barreira_reta_vermelha_branca/barreira_reta_vermelha_branca.glb`](../../../../jogo/ambiente/modelos/barreiras/barreira_reta_vermelha_branca/) |

## Como aplicar em uma pista

1. Com o `.blend` da pista aberto no Blender MCP, execute uma cópia de [`posicionar_barreiras.py`](../../../../pistas/PI001_primeira_pista/registros/posicionar_barreiras.py), ajustando `PREFIXO`, `EIXO`, `COLECAO`, `AFASTAMENTO`, `ALTURA_CHAO` e `SAIDA_JSON`. O script desloca o eixo fechado para os dois lados, remove os trechos que invadiriam a pista nas curvas fechadas, distribui módulos com instâncias ligadas (uma única malha) e grava `barreiras.json` com as transformações na Godot.
2. Na Godot, chame `_barreiras(raiz, "res://pistas/<pista>/barreiras.json")` em `ferramentas/construir_cenas.gd`. A função cria um `MeshInstance3D` por módulo, com descarte a 220 m, e uma `BoxShape3D` de 1,3 m de altura por 0,6 m de profundidade, 0,3 m mais longa que o módulo, num `StaticBody3D` que impede os karts de sair.

## Limitações

- Módulo reto: nas curvas, as emendas abrem pequenas frestas visuais no lado convexo. A colisão é contínua, porque as caixas se sobrepõem.
- O glTF usa a mesma amostragem para as três texturas (aviso do exportador); o material importado foi conferido apenas visualmente.
- Modelo gerado por IA: licença/origem informada pelo usuário; arestas e parafusos simplificados pela decimação.
