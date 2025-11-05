"""Módulo que define as entidades básicas do jogo."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Entidade:
    """Representa qualquer ser ou objeto posicionado no mapa."""

    x: int
    y: int
    simbolo: str
    nome: str
    vida_atual: int = 10
    vida_maxima: int = 10
    energia_atual: int = 5
    energia_maxima: int = 5
    nivel: int = 1
    forca: int = 3
    defesa: int = 1
    agilidade: int = 1
    hostil: bool = False
    inventario: List[str] = field(default_factory=list)

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
    
    def esta_vivo(self) -> bool:
        """Indica se a entidade ainda possui pontos de vida."""
        return self.vida_atual > 0

    def receber_dano(self, quantidade: int) -> None:
        """Reduz a vida atual limitada ao mínimo de zero."""
        self.vida_atual = max(0, self.vida_atual - quantidade)

    def curar(self, quantidade: int) -> None:
        """Recupera pontos de vida sem ultrapassar o máximo."""
        self.vida_atual = min(self.vida_maxima, self.vida_atual + quantidade)