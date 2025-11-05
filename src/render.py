"""Responsável por desenhar o estado atual do jogo no terminal."""

import os
from typing import Iterable, List, Sequence, Set, Tuple

from .mundo.entidade import Entidade
from .mundo.gerador_mapa import Mapa

Coordenada = Tuple[int, int]


def limpar_tela() -> None:
    """Limpa o terminal de forma simples e multiplataforma."""
    os.system("cls" if os.name == "nt" else "clear")


def compor_grade(
    mapa: Mapa, 
    entidades: Sequence[Entidade],
    visiveis: Set[Coordenada],
    reveladas: Sequence[Sequence[bool]],
) -> List[str]:
    """Cria uma representação textual considerando FOV e neblina de guerra."""

    grade = [[" " for _ in range(mapa.largura)] for _ in range(mapa.altura)]

    for y in range(mapa.altura):
        for x in range(mapa.largura):
            if (x, y) in visiveis:
                grade[y][x] = mapa.grade[y][x]
            elif reveladas[y][x]:
                grade[y][x] = mapa.grade[y][x].lower()

    for entidade in entidades:
        if (entidade.x, entidade.y) in visiveis:
            grade[entidade.y][entidade.x] = entidade.simbolo

    return ["".join(linha) for linha in grade]


def desenhar_hud(
    jogador: Entidade,
    turno: int,
    mensagens: Iterable[str],
    largura_mapa: int,
) -> None:
    """Exibe informações do jogador e o log rolante."""

    print("-" * largura_mapa)
    print(f"Turno: {turno}")
    print(f"HP: {jogador.descricao_vida()}  Energia: {jogador.descricao_energia()}  Nível: {jogador.nivel}")
    print("Mensagens:")
    for mensagem in mensagens:
        print(f" - {mensagem}")
    print("\nUse WASD ou setas para se mover. Pressione Q para sair.")


def renderizar(
    mapa: Mapa, 
    entidades: Sequence[Entidade],
    visiveis: Set[Coordenada],
    reveladas: Sequence[Sequence[bool]],
    mensagens: Sequence[str],
    jogador: Entidade,
    turno: int,
    limite_mensagens: int = 6,
) -> None:
    """Desenha o mapa, HUD e log no terminal."""

    limpar_tela()
    grade_texto = compor_grade(mapa, entidades, visiveis, reveladas)
    for linha in grade_texto:
        print(linha)

    log_recente = list(mensagens)[-limite_mensagens:]
    desenhar_hud(jogador, turno, log_recente, mapa.largura)