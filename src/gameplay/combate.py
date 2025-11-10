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


def _aplicar_bonus_habilidade(atacante: Entidade, dano: int, mensagens: List[str]) -> int:
    """Verifica efeitos ativos que alteram o dano."""

    if atacante.efeitos_ativos.get("golpe_concentrado"):
        dano *= 2
        atacante.efeitos_ativos.pop("golpe_concentrado", None)
        mensagens.append(f"{atacante.nome} libera um golpe concentrado devastador!")
    return dano


def resolver_ataque(atacante: Entidade, defensor: Entidade, mensagens: List[str]) -> None:
    """Aplica o dano calculado e registra mensagens descritivas."""

    dano = calcular_dano(atacante, defensor)
    dano = _aplicar_bonus_habilidade(atacante, dano, mensagens)
    defensor.receber_dano(dano)
    mensagens.append(
        f"{atacante.nome} ataca {defensor.nome} causando {dano} de dano (HP {defensor.descricao_vida()})."
    )

    if not defensor.esta_vivo():
        mensagens.append(f"{defensor.nome} cai ao chão, derrotado.")


def resolver_ataques_distancia(atacante: Entidade, defensor: Entidade, mensagens: List[str]) -> None:
    """Executa um ataque a distância simples utilizando atributos."""

    dano = calcular_dano(atacante, defensor)
    defensor.receber_dano(dano)
    mensagens.append(
        f"{atacante.nome} dispara uma flecha em {defensor.nome} causando {dano} de dano (HP {defensor.descricao_vida()})."
    )

    if not defensor.esta_vivo():
        mensagens.append(f"{defensor.nome} é abatido à distância.")