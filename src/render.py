"""Responsável por desenhar o estado atual do jogo no terminal."""

import os
from typing import List

from .mundo.entidade import Entidade
from .mundo.gerador_mapa import Mapa


def limpar_tela() -> None:
    """Limpa o terminal de forma simples e multiplataforma."""
    os.system("cls" if os.name == "nt" else "clear")


def compor_grade(mapa: Mapa, entidades: List[Entidade]) -> List[str]:
    """Cria uma representação textual do mapa com as entidades."""
    grade = [linha.copy() for linha in mapa.grade]

    for entidade in entidades:
        if 0 <= entidade.x < mapa.largura and 0 <= entidade.y < mapa.altura:
            grade[entidade.y][entidade.x] = entidade.simbolo

    return ["".join(linha) for linha in grade]


def renderizar(mapa: Mapa, entidades: List[Entidade]) -> None:
    """Desenha o mapa e as entidades no terminal."""
    limpar_tela()
    grade_texto = compor_grade(mapa, entidades)
    for linha in grade_texto:
        print(linha)

    print("\nUse WASD ou setas para se mover. Pressione Q para sair.")
