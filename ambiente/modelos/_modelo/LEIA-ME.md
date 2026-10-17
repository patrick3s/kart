# {{NOME_DO_MODELO}}

Copie esta estrutura para `ambiente/modelos/CATEGORIA/nome_do_modelo/` e preencha os campos. Este é um modelo de organização; não contém um objeto 3D produzido.

| Campo | Estado |
| --- | --- |
| Nome de exibição | A informar |
| Nome seguro e categoria | A informar |
| Criado em | A informar |
| Estado | Estrutura criada; aguardando modelo |
| Referência principal | A informar |
| Modelo original recebido | A informar |
| Projeto Blender | Ainda não criado |
| Texturas/dependências | A informar |
| Dimensões, unidade e orientação | A medir |
| Pivô e pontos de encaixe | A definir |
| Colisões | A definir e testar na Godot |
| Exportação para Godot | Ainda não criada |

## Onde colocar os arquivos

- `referencia/`: imagens e modelos originais recebidos (`.glb`, `.fbx`, `.obj`, `.blend` etc.), preservados.
- `blender/`: `.blend` real de trabalho, criado quando houver etapa de preparação/modelagem no Blender.
- `texturas/`: texturas e mapas de produção, preservando os originais recebidos em `referencia/`.
- `backups/`: cópias anteriores a alterações.
- `validacao/`: relatórios, logs e imagens de verificações efetivamente executadas, separados por data/versão.
- `registros/`: decisões, scripts e histórico detalhado.

Mantenha o estado em [CHECKPOINT.md](CHECKPOINT.md). Um nome de arquivo previsto não comprova criação de um `.blend`, exportação ou validação.

## Uso na Godot

Quando houver exportação real, coloque-a em `jogo/ambiente/modelos/CATEGORIA/nome_do_modelo/`. O `.glb` contém o modelo e a `.tscn` reutilizável reúne visual, materiais e colisões. Cada pista instancia essa cena compartilhada.

## Histórico

Preencher com data, ações realizadas e evidências existentes.
