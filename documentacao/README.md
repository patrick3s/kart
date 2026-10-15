# Documentação do projeto

## Rig do personagem — 15/10/2026

- [Registro completo das operações](registro-rig-personagem-2026-10-15.md): estado inicial, separação da malha, tentativas intermediárias, esqueleto, pesos, pivô, testes e limitações.
- [Manifesto dos artefatos](manifesto-artefatos-rig.json): caminhos, tamanhos e hashes SHA-256 dos arquivos relacionados ao trabalho, calculados ao produzir esta documentação.
- [Validação numérica original](../rigging/validacao_rig.json).
- [Arquivo final do Blender](../kart_modular_rig.blend).

O resultado tem duas malhas: `Cabeca` e `Corpo_Kart`. **O kart continua unido ao corpo e acompanha o controle do torso.** A cabeça tem controle independente.

A preservação de geometria foi verificada por identificadores dos elementos originais. O ajuste de origem e a avaliação da armature apresentam arredondamento de ponto flutuante; os valores exatos estão no registro e no relatório de validação.

Esta documentação registra o trabalho já realizado. Sua criação não modifica o arquivo `.blend`.
