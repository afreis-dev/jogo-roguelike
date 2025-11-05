"""Gerencia a ordem de execução dos turnos do jogo."""

from dataclasses import dataclass, field
from typing import List, Optional

from ..gameplay.combate import resolver_ataque
from .entidade import Entidade
from .gerador_mapa import Mapa


@dataclass
class SistemaTurnos:
    """Controla a contagem de turnos e ações globais."""

    turno_atual: int = 1
    historico_turnos: List[str] = field(default_factory=list)

    def registrar_evento(self, mensagem: str) -> None:
        """Armazena um texto descritivo do turno atual."""
        self.historico_turnos.append(mensagem)

    def avancar(
        self,
        entidades: List[Entidade],
        jogador: Entidade,
        mapa: Mapa,
        mensagens: List[str],
    ) -> None:
        """Avança o contador de turnos e executa ações das entidades hostis."""

        self.turno_atual += 1
        for entidade in list(entidades):
            if entidade is jogador or not entidade.hostil or not entidade.esta_vivo():
                continue
            if not jogador.esta_vivo():
                break

            dx = jogador.x - entidade.x
            dy = jogador.y - entidade.y
            passo_x = 0 if dx == 0 else (1 if dx > 0 else -1)
            passo_y = 0 if dy == 0 else (1 if dy > 0 else -1)

            if abs(dx) <= 1 and abs(dy) <= 1:
                resolver_ataque(entidade, jogador, mensagens)
                continue

            candidato_x = entidade.x + passo_x
            candidato_y = entidade.y + passo_y

            if mapa.eh_parede(candidato_x, candidato_y):
                continue

            ocupante = _encontrar_primeiro_vivo(entidades, candidato_x, candidato_y, ignorar=entidade)
            if ocupante is None:
                entidade.mover(passo_x, passo_y)


def _encontrar_primeiro_vivo(
    entidades: List[Entidade], x: int, y: int, ignorar: Optional[Entidade] = None
) -> Optional[Entidade]:
    """Localiza uma entidade viva na posição solicitada."""

    for entidade in entidades:
        if entidade is ignorar:
            continue
        if entidade.x == x and entidade.y == y and entidade.esta_vivo():
            return entidade
    return None