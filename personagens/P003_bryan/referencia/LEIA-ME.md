# Referências — P003 — Bryan

Coloque nesta pasta os materiais de entrada do personagem:

- **Imagens de referência** (`.png`, `.jpg`): frente, lado, costas e detalhes, quando existirem. Nenhum ângulo é obrigatório.
- **Modelo 3D** (`.glb`, `.gltf`, `.fbx`, `.obj`, `.blend`), se já existir.
- **Texturas** do modelo, preferencialmente em uma subpasta `texturas/`.

Imagens são referência visual; elas não substituem um modelo 3D. O modelo que será efetivamente trabalhado é registrado na [ficha](../LEIA-ME.md) e importado como cópia no projeto exclusivo [`blender/bryan.blend`](../blender/bryan.blend); os originais desta pasta não são alterados.

## Inventário

Conferido em 15/10/2026. Os arquivos foram colocados nesta pasta pelo usuário; a origem detalhada não foi informada.

| Arquivo | Tipo | Função | Origem informada | Conferência |
| --- | --- | --- | --- | --- |
| `bryan.glb` | Modelo 3D glTF binário v2, 61,4 MB | **Modelo de entrada** a ser trabalhado | Colocado pelo usuário (metadados indicam geração pelo Tripo) | SHA-256 `14fcb6a4…6cfcf2`; 1 malha, 986.320 vértices, 1.854.601 triângulos, 1 material, 3 texturas 4096² embutidas (`bryan_basecolor.jpg`, `bryan_normal.png`, `bryan_rm.jpg`); sem armature nem animações |
| `bryan.png` | Imagem PNG 1254×1254 | Referência visual (vista frontal ¾) | Colocado pelo usuário | SHA-256 `3d9a0fac…aca553d9`; policial de quepe, óculos escuros, colete tático e luvas num kart de polícia preto/azul “POLÍCIA 190” com 4 rodas de aro azul iluminado, giroflex, antena, câmera, holofote, tablet, extintor, guincho e gaiola traseira |

Não há texturas soltas: as três ficam embutidas no GLB e foram incorporadas ao `.blend`.
