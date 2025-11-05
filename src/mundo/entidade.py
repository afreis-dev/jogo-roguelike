"""Módulo que define as entidades básicas do jogo."""

from dataclasses import dataclass


@dataclass
class Entidade:
    """Representa qualquer ser ou objeto posicionado no mapa."""

    x: int
    y: int
    simbolo: str

    def mover(self, delta_x: int, delta_y: int) -> None:
        """Atualiza a posição da entidade somando os deltas informados."""
        self.x += delta_x
        self.y += delta_y
