"""Funções e estruturas relacionadas a itens utilizáveis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from ..mundo.entidade import Entidade
from ..mundo.gerador_mapa import Mapa

AcaoItem = Callable[[Entidade, List[Entidade], Mapa, List[str]], None]


@dataclass
class Item:
    """Representa um item consumível ou utilitário."""

    nome: str
    descricao: str
    categoria: str
    acao: AcaoItem

    def usar(self, usuario: Entidade, entidades: List[Entidade], mapa: Mapa, mensagens: List[str]) -> None:
        """Executa o efeito associado ao item."""
        self.acao(usuario, entidades, mapa, mensagens)


def criar_pocao_cura() -> Item:
    """Gera uma poção de cura moderada."""

    def _efeito(usuario: Entidade, _entidades: List[Entidade], _mapa: Mapa, mensagens: List[str]) -> None:
        cura = 7
        vida_antes = usuario.vida_atual
        usuario.curar(cura)
        recuperado = usuario.vida_atual - vida_antes
        mensagens.append(f"Você bebe a poção e recupera {recuperado} de vida.")

    return Item(
        nome="Poção menor de cura",
        descricao="Restaura uma quantia moderada de pontos de vida.",
        categoria="consumível",
        acao=_efeito,
    )


def criar_pocao_energia() -> Item:
    """Cria uma poção que revitaliza a energia do usuário."""

    def _efeito(usuario: Entidade, _entidades: List[Entidade], _mapa: Mapa, mensagens: List[str]) -> None:
        energia = 3
        energia_antes = usuario.energia_atual
        usuario.regenerar_energia(energia)
        recuperado = usuario.energia_atual - energia_antes
        mensagens.append(f"A poção brilhante restaura {recuperado} de energia.")

    return Item(
        nome="Poção tônica",
        descricao="Revigora a energia, permitindo o uso de habilidades.",
        categoria="consumível",
        acao=_efeito,
    )


def criar_bomba_fumaca() -> Item:
    """Produz uma bomba que enfraquece inimigos próximos."""

    def _efeito(usuario: Entidade, entidades: List[Entidade], mapa: Mapa, mensagens: List[str]) -> None:
        alcance = 2
        dano = 3
        acertou = False
        for entidade in list(entidades):
            if entidade is usuario or not entidade.hostil or not entidade.esta_vivo():
                continue
            distancia = abs(entidade.x - usuario.x) + abs(entidade.y - usuario.y)
            if distancia <= alcance and not mapa.eh_parede(entidade.x, entidade.y):
                entidade.receber_dano(dano)
                acertou = True
                mensagens.append(
                    f"A bomba de fumaça sufoca {entidade.nome}, causando {dano} de dano (HP {entidade.descricao_vida()})."
                )
                if not entidade.esta_vivo():
                    mensagens.append(f"{entidade.nome} sucumbe à fumaça espessa.")
        if not acertou:
            mensagens.append("A fumaça se dissipa sem atingir nenhum inimigo.")

    return Item(
        nome="Bomba de fumaça",
        descricao="Dano leve em área contra inimigos próximos.",
        categoria="arremessável",
        acao=_efeito,
    )


def usar_item_por_indice(
    jogador: Entidade,
    indice: int,
    entidades: List[Entidade],
    mapa: Mapa,
    mensagens: List[str],
    estatisticas: Dict[str, int],
) -> List[Entidade]:
    """Consome um item do inventário pelo índice informado."""

    if not jogador.inventario:
        mensagens.append("Seu inventário está vazio.")
        return []

    if indice < 0 or indice >= len(jogador.inventario):
        mensagens.append("Não há item associado a essa tecla.")
        return []

    item = jogador.inventario.pop(indice)
    mensagens.append(f"Você usa {item.nome}.")
    mortos_antes = {id(entidade) for entidade in entidades if not entidade.esta_vivo()}
    item.usar(jogador, entidades, mapa, mensagens)
    estatisticas.setdefault("itens_usados", 0)
    estatisticas["itens_usados"] += 1
    derrotados: List[Entidade] = []
    for entidade in entidades:
        if entidade is jogador:
            continue
        if not entidade.hostil:
            continue
        if entidade.esta_vivo():
            continue
        if id(entidade) in mortos_antes:
            continue
        derrotados.append(entidade)
    return derrotados


def encontrar_item_por_nome(nome: str) -> Optional[Item]:
    """Retorna uma instância de item conhecida pelo nome informado."""

    catalogo = {
        "Poção menor de cura": criar_pocao_cura,
        "Poção tônica": criar_pocao_energia,
        "Bomba de fumaça": criar_bomba_fumaca,
    }
    fabrica = catalogo.get(nome)
    return fabrica() if fabrica else None