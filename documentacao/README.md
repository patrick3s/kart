# Documentação do projeto

## Personagens — arquivo central e receita

- [PERSONAGEM.md](PERSONAGEM.md): registra o primeiro personagem, reúne sua evolução e define a receita para preparar outros personagens. Novas etapas de personagem devem ser resumidas nesse arquivo, com referências aos documentos e artefatos correspondentes.

## Rodas independentes — 15/10/2026

- [Separação das quatro rodas — P001.05](registro-rodas-independentes-2026-10-15.md): método, nomes dos objetos, pivôs, preservação da geometria e acompanhamento do rig. [Validação numérica](../rigging/verificacao_rodas_independentes.json).

Após esta etapa, o modelo tem seis malhas: `Cabeca`, `Corpo_Kart` e quatro objetos `Wheel_*`, cada roda com malha exclusiva. As rodas acompanham `Torso_Bone` por parentesco e têm pivôs próprios. O modelo, o relatório e o backup estão no commit local `e2a2848`; esta documentação textual é posterior a ele. A exportação e o controle na Godot ainda não foram validados.

## Animação da cabeça — 15/10/2026

- [Cabeça para a esquerda — P001.04](registro-animacao-cabeca-esquerda-2026-10-15.md): nova ação `Cabeca_Esquerda_Ida_e_Volta`, ativa no arquivo principal, com **0° → −40° → 0°** nos quadros **1 → 25 → 49**, 30 FPS e preservação da ação da direita. [Validação numérica](../rigging/validacao_animacao_cabeca_esquerda.json).
- [Registro completo deste chat](registro-animacao-cabeca-2026-10-15.md): rotação de 40°, animação de ida e volta, preservação do pescoço e corpo, verificações, ajustes de FPS e diferença entre prévia e exportação.

A ação `Cabeca_Direita_Ida_e_Volta` anima somente a rotação Y local de `Head_Bone`, com keyframes nos quadros **1 → 25 → 49**, correspondendo a **0° → 40° → 0°**. Foi criada em 24 FPS; na consulta realizada durante a documentação, a cena estava em **30 FPS**, com prévia de 1 a 49 e intervalo principal de 1 a 250.

## Rig do personagem — 15/10/2026

- [Registro completo das operações](registro-rig-personagem-2026-10-15.md): estado inicial, separação da malha, tentativas intermediárias, esqueleto, pesos, pivô, testes e limitações.
- [Manifesto dos artefatos](manifesto-artefatos-rig.json): caminhos, tamanhos e hashes SHA-256 calculados na documentação original do rig, antes das alterações de animação. O hash histórico do `.blend` não representa a versão posterior com a animação.
- [Validação numérica original](../rigging/validacao_rig.json).
- [Arquivo final do Blender](../kart_modular_rig.blend).

O resultado original do rig tinha duas malhas: `Cabeca` e `Corpo_Kart`, com o kart unido ao corpo. A etapa **P001.05** separou as quatro rodas; o restante do kart continua unido ao corpo e acompanha o controle do torso. A cabeça mantém seu controle independente.

A preservação de geometria foi verificada por identificadores dos elementos originais. O ajuste de origem e a avaliação da armature apresentam arredondamento de ponto flutuante; os valores exatos estão no registro e no relatório de validação.

Os registros distinguem as etapas históricas. A etapa P001.04 salva a nova ação no `.blend`; a criação dos documentos, por si só, não altera a cena.

## Arquivos do Blender no repositório

Os arquivos `.blend` usam **Git LFS**. Ao clonar o projeto, tenha o Git LFS instalado e execute `git lfs pull` na pasta do repositório para conferir o download dos arquivos completos. Backups automáticos como `.blend1` ficam locais e são ignorados pelo Git.
