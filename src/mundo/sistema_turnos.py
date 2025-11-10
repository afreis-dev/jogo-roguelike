"""Gerencia a ordem de execução dos turnos do jogo."""

from dataclasses import dataclass, field
from typing import List

from ..gameplay.ia import executar_turno_inimigo
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

            executar_turno_inimigo(entidade, jogador, mapa, entidades, mensagens)