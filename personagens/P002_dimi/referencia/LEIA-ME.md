# Referências — P002 — Dimi

Coloque nesta pasta os materiais de entrada do personagem:

- **Imagens de referência** (`.png`, `.jpg`): frente, lado, costas e detalhes, quando existirem. Nenhum ângulo é obrigatório.
- **Modelo 3D** (`.glb`, `.gltf`, `.fbx`, `.obj`, `.blend`), se já existir.
- **Texturas** do modelo, preferencialmente em uma subpasta `texturas/`.

Imagens são referência visual; elas não substituem um modelo 3D. O modelo que será efetivamente trabalhado é registrado na [ficha](../LEIA-ME.md) e importado como cópia no projeto exclusivo [`blender/dimi.blend`](../blender/dimi.blend); os originais desta pasta não são alterados.

## Inventário

Conferido em 15/10/2026. Os arquivos foram colocados nesta pasta pelo usuário; a origem detalhada não foi informada.

| Arquivo | Tipo | Função | Origem informada | Conferência |
| --- | --- | --- | --- | --- |
| `Dimi.glb` | Modelo 3D glTF binário v2, 61,1 MB | **Modelo de entrada** a ser trabalhado | Colocado pelo usuário (metadados indicam geração pelo Tripo) | SHA-256 `b36848cb…8023bf1`; 1 malha, 995.477 vértices, 1.881.354 faces, 1 material, 3 texturas 4096² embutidas (`Dimi_basecolor.jpg`, `Dimi_normal.png`, `Dimi_rm.jpg`); sem armature nem animações |
| `Dimi.png` | Imagem PNG 2048×2048 | Referência visual (vista frontal ¾) | Colocado pelo usuário | SHA-256 `a4916860…19ae216c`; bebê de boné vermelho/branco e chupeta num kart prateado nº 1 com 4 rodas translúcidas, grades coloridas, mamadeira, molas e móbile com hélice |

Não há texturas soltas: as três ficam embutidas no GLB e foram incorporadas ao `.blend`.
