"""Regras básicas de combate corpo a corpo."""

import random
from typing import List

from ..mundo.entidade import Entidade


def calcular_dano(atacante: Entidade, defensor: Entidade) -> int:
    """Determina o dano final considerando atributos ofensivos e defensivos."""

    variacao = random.randint(0, max(1, atacante.agilidade))
    bruto = atacante.forca + variacao
    mitigacao = defensor.defesa
    return max(1, bruto - mitigacao)


def resolver_ataque(atacante: Entidade, defensor: Entidade, mensagens: List[str]) -> None:
    """Aplica o dano calculado e registra mensagens descritivas."""

    dano = calcular_dano(atacante, defensor)
    defensor.receber_dano(dano)
    mensagens.append(
        f"{atacante.nome} ataca {defensor.nome} causando {dano} de dano (HP {defensor.descricao_vida()})."
    )

    if not defensor.esta_vivo():
        mensagens.append(f"{defensor.nome} cai ao chão, derrotado.")