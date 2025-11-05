"""Módulo que define as entidades básicas do jogo."""

from dataclasses import dataclass


@dataclass
class Entidade:
    """Representa qualquer ser ou objeto posicionado no mapa."""

    x: int
    y: int
    simbolo: str
    vida_atual: int = 10
    vida_maxima: int = 10
    energia_atual: int = 5
    energia_maxima: int = 5
    nivel: int = 1

    def mover(self, delta_x: int, delta_y: int) -> None:
        """Atualiza a posição da entidade somando os deltas informados."""
        self.x += delta_x
        self.y += delta_y

def descricao_vida(self) -> str:
    """Retorna uma descrição curta dos pontos de vida atuais da entidade."""
    return f"{self.vida_atual}/{self.vida_maxima}"

def descricao_energia(self) -> str:
    """Retorna uma descrição curta da energia atual."""
    return f"{self.energia_atual}/{self.energia_maxima}"