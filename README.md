# Jogo Roguelike

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
- Ataque corpo a corpo: mova-se na direção do inimigo.
- Sair: `Q`.

## Roadmap Inicial

- **v0.1.0:** mapa ASCII procedural, movimentação do jogador.
- **v0.2.0:** sistema de turnos, campo de visão clássico e HUD com log rolante.
- **v0.3.0 (atual):** inimigos goblins, combate com atributos e drops simples.

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

- Mapa amplo (100x60) com geração procedural de salas e corredores.
- Campo de visão clássico com neblina de guerra persistente.
- Sistema de turnos sincronizado com a entrada do jogador.
- HUD com HP, energia, nível, inventário rápido e log de mensagens rolante.
- Goblins hostis que perseguem o jogador e atacam com base em atributos.
- Itens simples (poções) obtidos como drop e tela de resumo ao final da expedição.