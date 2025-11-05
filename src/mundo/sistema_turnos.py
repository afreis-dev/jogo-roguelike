"""Gerencia a ordem de execução dos turnos do jogo."""

from dataclasses import dataclass, field
from typing import List

from .entidade import Entidade


@dataclass
class SistemaTurnos:
    """Controla a contagem de turnos e ações globais."""

    turno_atual: int = 1
    historico_turnos: List[str] = field(default_factory=list)

    def registrar_evento(self, mensagem: str) -> None:
        """Armazena um texto descritivo do turno atual."""
        self.historico_turnos.append(mensagem)

    def avancar(self, entidades: List[Entidade]) -> None:
        """Avança o contador de turnos e atualiza entidades, se necessário."""
        self.turno_atual += 1
        # Futuramente este método acionará IA de inimigos e sistemas globais.
        _ = entidades  # Mantém a assinatura até que haja NPCs.