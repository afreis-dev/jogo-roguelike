"""Funções utilitárias relacionadas ao campo de visão."""

from typing import Generator, Iterable, List, Set, Tuple

from ..mundo.gerador_mapa import Mapa

Coordenada = Tuple[int, int]


def _bresenham(x0: int, y0: int, x1: int, y1: int) -> Generator[Coordenada, None, None]:
    """Gera os pontos de uma linha usando o algoritmo de Bresenham."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    erro = dx + dy

    x, y = x0, y0
    while True:
        yield x, y
        if x == x1 and y == y1:
            break
        e2 = 2 * erro
        if e2 >= dy:
            erro += dy
            x += sx
        if e2 <= dx:
            erro += dx
            y += sy


def calcular_fov(mapa: Mapa, origem: Coordenada, raio: int) -> Set[Coordenada]:
    """Retorna um conjunto de coordenadas visíveis a partir da origem."""
    visiveis: Set[Coordenada] = set()
    origem_x, origem_y = origem

    for x in range(origem_x - raio, origem_x + raio + 1):
        for y in range(origem_y - raio, origem_y + raio + 1):
            if not _esta_dentro_do_mapa(mapa, x, y):
                continue
            if (x - origem_x) ** 2 + (y - origem_y) ** 2 > raio ** 2:
                continue
            for passo_x, passo_y in _bresenham(origem_x, origem_y, x, y):
                visiveis.add((passo_x, passo_y))
                if mapa.eh_parede(passo_x, passo_y) and (passo_x, passo_y) != (origem_x, origem_y):
                    break

    return visiveis


def atualizar_celulas_reveladas(
    reveladas: List[List[bool]], visiveis: Iterable[Coordenada]
) -> None:
    """Atualiza a matriz de células já vistas pelo jogador."""
    for x, y in visiveis:
        reveladas[y][x] = True


def _esta_dentro_do_mapa(mapa: Mapa, x: int, y: int) -> bool:
    """Verifica se as coordenadas pertencem aos limites do mapa."""
    return 0 <= x < mapa.largura and 0 <= y < mapa.altura