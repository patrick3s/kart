# Documentação do projeto

## Animação da cabeça — 15/10/2026

- [Registro completo deste chat](registro-animacao-cabeca-2026-10-15.md): rotação de 40°, animação de ida e volta, preservação do pescoço e corpo, verificações, ajustes de FPS e diferença entre prévia e exportação.

A ação `Cabeca_Direita_Ida_e_Volta` anima somente a rotação Y local de `Head_Bone`, com keyframes nos quadros **1 → 25 → 49**, correspondendo a **0° → 40° → 0°**. Foi criada em 24 FPS; na consulta realizada durante a documentação, a cena estava em **30 FPS**, com prévia de 1 a 49 e intervalo principal de 1 a 250.

## Rig do personagem — 15/10/2026

- [Registro completo das operações](registro-rig-personagem-2026-10-15.md): estado inicial, separação da malha, tentativas intermediárias, esqueleto, pesos, pivô, testes e limitações.
- [Manifesto dos artefatos](manifesto-artefatos-rig.json): caminhos, tamanhos e hashes SHA-256 calculados na documentação original do rig, antes das alterações de animação. O hash histórico do `.blend` não representa a versão posterior com a animação.
- [Validação numérica original](../rigging/validacao_rig.json).
- [Arquivo final do Blender](../kart_modular_rig.blend).

O resultado tem duas malhas: `Cabeca` e `Corpo_Kart`. **O kart continua unido ao corpo e acompanha o controle do torso.** A cabeça tem controle independente.

A preservação de geometria foi verificada por identificadores dos elementos originais. O ajuste de origem e a avaliação da armature apresentam arredondamento de ponto flutuante; os valores exatos estão no registro e no relatório de validação.

Esta documentação registra o trabalho já realizado. Sua criação não modifica o arquivo `.blend`.

## Arquivos do Blender no repositório

Os arquivos `.blend` usam **Git LFS**. Ao clonar o projeto, tenha o Git LFS instalado e execute `git lfs pull` na pasta do repositório para conferir o download dos arquivos completos. Backups automáticos como `.blend1` ficam locais e são ignorados pelo Git.
