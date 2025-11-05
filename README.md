# Jogo Roguelike ASCII

Projeto de roguelike em terminal inspirado em Warsim, Caves of Qud e Dwarf Fortress.

## Linguagem e Dependências

- **Linguagem:** Python 3.11+
- **Bibliotecas externas:** nenhuma (apenas biblioteca padrão do Python).

## Configuração (Windows + VS Code)

1. Instale o [Python 3.11](https://www.python.org/downloads/). Marque a opção *Add Python to PATH*.
2. Abra o projeto no VS Code (`Arquivo > Abrir Pasta...`).
3. Instale as extensões recomendadas:
   - Python (Microsoft).
4. Abra o terminal integrado (`Ctrl+``) e crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

5. Configure o interpretador no VS Code apontando para `.venv` (comando `Ctrl+Shift+P` → "Python: Select Interpreter").

## Como Executar

No terminal ativado (com ou sem ambiente virtual):

```bash
python -m src.main
```

## Controles Iniciais

- Movimentação: `W`, `A`, `S`, `D` ou setas direcionais.
- Sair: `Q`.

## Roadmap Inicial

- **v0.1.0 (atual):** mapa ASCII procedural, movimentação do jogador.
- **v0.2.0:** sistema de turnos, campo de visão e HUD.
- **v0.3.0:** inimigos, combate e itens básicos.

## Estrutura de Pastas

```
jogo-roguelike/
├── docs/
│   └── CHANGELOG.md
├── src/
│   ├── gameplay/
│   ├── mundo/
│   ├── util/
│   ├── entrada.py
│   ├── main.py
│   └── render.py
├── tests/
├── LICENSE
└── README.md
```

## Estado Atual

O jogo gera um mapa de salas interligadas, posiciona o jogador e permite movimentá-lo sem atravessar paredes.
