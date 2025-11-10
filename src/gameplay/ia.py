"""Comportamentos de IA para inimigos do roguelike."""

from __future__ import annotations

import random
from typing import List, Optional

from ..mundo.entidade import Entidade
from ..mundo.gerador_mapa import Mapa
from .combate import resolver_ataque, resolver_ataques_distancia


def executar_turno_inimigo(
    entidade: Entidade,
    jogador: Entidade,
    mapa: Mapa,
    entidades: List[Entidade],
    mensagens: List[str],
) -> None:
    """Decide qual ação o inimigo irá executar no turno atual."""

    if entidade.comportamento == "goblin_guerreiro":
        _agir_goblin_guerreiro(entidade, jogador, mapa, entidades, mensagens)
    elif entidade.comportamento == "goblin_arqueiro":
        _agir_goblin_arqueiro(entidade, jogador, mapa, entidades, mensagens)
    else:
        _agir_basico(entidade, jogador, mapa, entidades, mensagens)


def _agir_goblin_guerreiro(
    entidade: Entidade,
    jogador: Entidade,
    mapa: Mapa,
    entidades: List[Entidade],
    mensagens: List[str],
) -> None:
    """Implementa patrulha, perseguição e fuga de goblins guerreiros."""

    distancia = _distancia_manhattan(entidade, jogador)

    if entidade.vida_atual <= entidade.vida_maxima // 3 and distancia <= 4:
        if _mover_longe(entidade, jogador, mapa, entidades):
            mensagens.append(f"{entidade.nome} recua assustado!")
        return
    
    if distancia <= entidade.alcance_ataque:
        resolver_ataque(entidade, jogador, mensagens)
        return
    
    if distancia <= entidade.raio_deteccao:
        if not _aproximar(entidade, jogador, mapa, entidades):
            _perambular(entidade, mapa, entidades)
    else:
        _perambular(entidade, mapa, entidades)


def _agir_goblin_arqueiro(
    entidade: Entidade,
    jogador: Entidade,
    mapa: Mapa,
    entidades: List[Entidade],
    mensagens: List[str],
) -> None:
    """Controla goblins arqueiros que mantêm distância e disparam flechas."""

    distancia = _distancia_manhattan(entidade, jogador)

    if distancia <= 1:
        if _mover_longe(entidade, jogador, mapa, entidades):
            mensagens.append(f"{entidade.nome} se reposiciona rapidamente.")
            return
        resolver_ataque(entidade, jogador, mensagens)
        return
    
    if distancia <= entidade.alcance_ataque:
        resolver_ataques_distancia(entidade, jogador, mensagens)
        return
    
    if distancia <= entidade.raio_deteccao:
        # arqueiros preferem manter uma distância segura
        if distancia < entidade.alcance_ataque - 1:
            _mover_longe(entidade, jogador, mapa, entidades)
        else:
            _aproximar(entidade, jogador, mapa, entidades)
    else:
        _perambular(entidade, mapa, entidades)


def _agir_basico(
    entidade: Entidade,
    jogador: Entidade,
    mapa: Mapa,
    entidades: List[Entidade],
    mensagens: List[str],
) -> None:
    """Fallback simples para inimigos sem comportamento definido."""

    if _distancia_manhattan(entidade, jogador) <= entidade. alcance_ataque:
        resolver_ataque(entidade, jogador, mensagens)
    else:
        _aproximar(entidade, mapa, entidades)


def _perambular(entidade: Entidade, mapa: Mapa, entidades: List[Entidade]) -> None:
    """Move o inimigo aleatoriamente mantendo-se em terreno livre."""

    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(direcoes)
    for dx, dy in direcoes:
        if _tentar_mover(entidade, entidade.x + dx, entidade.y + dy, mapa, entidades):
            break


def _aproximar(
    entidade: Entidade,
    jogador: Entidade,
    mapa: Mapa,
    entidades: List[Entidade],
) -> bool:
    """Tenta aproximar a entidade do jogador retornando sucesso."""

    dx = jogador.x - entidade.x
    dy = jogador.y - entidade.y
    passo_x = 0 if dx == 0 else (1 if dx > 0 else -1)
    passo_y = 0 if dy == 0 else (1 if dy > 0 else -1)

    candidatos = [
        (entidade.x + passo_x, entidade.y),
        (entidade.x, entidade.y + passo_y),
        (entidade.x + passo_x, entidade.y + passo_y),
    ]

    for destino_x, destino_y in candidatos:
        if _tentar_mover(entidade, destino_x, destino_y, mapa, entidades):
            return True
    return False


def _mover_longe(
    entidade: Entidade,
    jogador: Entidade,
    mapa: Mapa,
    entidades: List[Entidade],
) -> bool:
    """Afasta a entidade do jogador, se possível."""

    dx = entidade.x - jogador.x
    dy = entidade.y - jogador.y
    passo_x = 0 if dx == 0 else (1 if dx > 0 else -1)
    passo_y = 0 if dy == 0 else (1 if dy > 0 else -1)

    candidatos = [
        (entidade.x + passo_x, entidade.y),
        (entidade.x, entidade.y + passo_y),
        (entidade.x + passo_x, entidade.y + passo_y),
    ]

    for destino_x, destino_y in candidatos:
        if _tentar_mover(entidade, destino_x, destino_y, mapa, entidades):
            return True

    return False


def _tentar_mover(
    entidade: Entidade,
    destino_x: int,
    destino_y: int,
    mapa: Mapa,
    entidades: List[Entidade],
) -> bool:
    """Verifica colisões antes de mover a entidade."""

    if mapa.eh_parede(destino_x, destino_y):
        return False

    if _encontrar_ocupante(entidades, destino_x, destino_y, ignorar=entidade):
        return False

    entidade.x = destino_x
    entidade.y = destino_y
    return True


def _encontrar_ocupante(
    entidades: List[Entidade], destino_x: int, destino_y: int, ignorar: Optional[Entidade] = None
) -> Optional[Entidade]:
    """Retorna a primeira entidade viva na posição informada."""

    for candidato in entidades:
        if candidato is ignorar:
            continue
        if not candidato.esta_vivo():
            continue
        if candidato.x == destino_x and candidato.y == destino_y:
            return candidato
    return None


def _distancia_manhattan(a: Entidade, b: Entidade) -> int:
    """Calcula a distância de Manhattan entre duas entidades."""

    return abs(a.x - b.x) + abs(a.y - b.y)