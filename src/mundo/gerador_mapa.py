"""Rotinas de geração procedural do mapa principal."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Tuple

PAREDE = "#"
CHAO = "."


@dataclass
class Sala:
    """Representa uma sala retangular no mapa."""

    x: int
    y: int
    largura: int
    altura: int

    def centro(self) -> Tuple[int, int]:
        """Retorna o ponto central inteiro da sala."""
        centro_x = self.x + self.largura // 2
        centro_y = self.y + self.altura // 2
        return centro_x, centro_y


@dataclass
class Mapa:
    """Estrutura básica do mapa composto por células ASCII."""

    largura: int
    altura: int
    grade: List[List[str]] = field(init=False)

    def __post_init__(self) -> None:
        """Inicializa a grade cheia de paredes."""
        self.grade = [[PAREDE for _ in range(self.largura)] for _ in range(self.altura)]

    def esculpir(self, x: int, y: int) -> None:
        """Transforma a posição informada em chão caminhável."""
        if 0 <= x < self.largura and 0 <= y < self.altura:
            self.grade[y][x] = CHAO

    def eh_parede(self, x: int, y: int) -> bool:
        """Retorna se a célula é uma parede sólida."""
        if 0 <= x < self.largura and 0 <= y < self.altura:
            return self.grade[y][x] == PAREDE
        return True


def _criar_sala(mapa: Mapa, sala: Sala) -> None:
    """Esculpe uma sala retangular dentro do mapa."""
    for y in range(sala.y, sala.y + sala.altura):
        for x in range(sala.x, sala.x + sala.largura):
            mapa.esculpir(x, y)


def _conectar_centros(mapa: Mapa, origem: Tuple[int, int], destino: Tuple[int, int]) -> None:
    """Liga dois pontos através de corredores em L."""
    x1, y1 = origem
    x2, y2 = destino

    if random.random() < 0.5:
        _escavar_corredor_horizontal(mapa, x1, x2, y1)
        _escavar_corredor_vertical(mapa, y1, y2, x2)
    else:
        _escavar_corredor_vertical(mapa, y1, y2, x1)
        _escavar_corredor_horizontal(mapa, x1, x2, y2)


def _escavar_corredor_horizontal(mapa: Mapa, x1: int, x2: int, y: int) -> None:
    """Cria um corredor horizontal entre duas coordenadas x."""
    for x in range(min(x1, x2), max(x1, x2) + 1):
        mapa.esculpir(x, y)


def _escavar_corredor_vertical(mapa: Mapa, y1: int, y2: int, x: int) -> None:
    """Cria um corredor vertical entre duas coordenadas y."""
    for y in range(min(y1, y2), max(y1, y2) + 1):
        mapa.esculpir(x, y)


def gerar_mapa_salas(largura: int, altura: int, quantidade_salas: int = 8) -> Tuple[Mapa, Tuple[int, int]]:
    """Gera um mapa com salas aleatórias e retorna o centro inicial."""
    mapa = Mapa(largura=largura, altura=altura)
    salas: List[Sala] = []

    for _ in range(quantidade_salas):
        largura_sala = random.randint(5, 9)
        altura_sala = random.randint(5, 9)
        x = random.randint(1, max(1, mapa.largura - largura_sala - 1))
        y = random.randint(1, max(1, mapa.altura - altura_sala - 1))
        nova_sala = Sala(x=x, y=y, largura=largura_sala, altura=altura_sala)

        if any(_salas_se_intersectam(nova_sala, sala_existente) for sala_existente in salas):
            continue

        _criar_sala(mapa, nova_sala)

        if salas:
            centro_anterior = salas[-1].centro()
            _conectar_centros(mapa, centro_anterior, nova_sala.centro())

        salas.append(nova_sala)

    if not salas:
        sala_central = Sala(
            x=mapa.largura // 2 - 2,
            y=mapa.altura // 2 - 2,
            largura=4,
            altura=4,
        )
        _criar_sala(mapa, sala_central)
        salas.append(sala_central)

    posicao_inicial = salas[0].centro()
    return mapa, posicao_inicial


def _salas_se_intersectam(sala_a: Sala, sala_b: Sala) -> bool:
    """Determina se duas salas possuem interseção."""
    return not (
        sala_a.x + sala_a.largura < sala_b.x
        or sala_b.x + sala_b.largura < sala_a.x
        or sala_a.y + sala_a.altura < sala_b.y
        or sala_b.y + sala_b.altura < sala_a.y
    )