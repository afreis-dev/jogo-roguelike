"""Responsável por desenhar o estado atual do jogo no terminal."""

import os
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .mundo.entidade import Entidade
from .mundo.gerador_mapa import Mapa

Coordenada = Tuple[int, int]


def limpar_tela() -> None:
    """Limpa o terminal de forma simples e multiplataforma."""
    os.system("cls" if os.name == "nt" else "clear")


def compor_grade(
    mapa: Mapa, 
    entidades: Sequence[Entidade],
    visiveis: Set[Coordenada],
    reveladas: Sequence[Sequence[bool]],
) -> List[str]:
    """Cria a malha textual considerando FOV e neblina de guerra."""

    grade = [[" " for _ in range(mapa.largura)] for _ in range(mapa.altura)]

    for y in range(mapa.altura):
        for x in range(mapa.largura):
            if (x, y) in visiveis:
                grade[y][x] = mapa.grade[y][x]
            elif reveladas[y][x]:
                grade[y][x] = mapa.grade[y][x].lower()

    for entidade in entidades:
        if (entidade.x, entidade.y) in visiveis:
            grade[entidade.y][entidade.x] = entidade.simbolo

    return ["".join(linha) for linha in grade]


def desenhar_hud(
    jogador: Entidade,
    turno: int,
    mensagens: Iterable[str],
    largura_mapa: int,
) -> None:
    """Exibe informações do jogador, inventário rápido e o log rolante."""

    print("-" * largura_mapa)
    print(f"Turno: {turno}")
    print(
        f"HP: {jogador.descricao_vida()}  Energia: {jogador.descricao_energia()}  Nível: {jogador.nivel}"
    )
    if jogador.pontos_talento > 0:
        print(f"Pontos de talento disponíveis: {jogador.pontos_talento} (pressione P para gastar)")
    if jogador.inventario:
        itens_formatados = ", ".join(
            f"{indice + 1}:{item.nome}" for indice, item in enumerate(jogador.inventario[:5])
        )
    else:
        itens_formatados = "vazio"
    print(f"Inventário rápido: {itens_formatados}")
    if jogador.perks:
        nomes_perks = ", ".join(jogador.perks)
    else:
        nomes_perks = "nenhuma"
    print(f"Perks ativas: {nomes_perks}")
    print("Mensagens:")
    for mensagem in mensagens:
        print(f" - {mensagem}")
    print(
        "\nComandos: WASD/setas para mover, Q para sair, Espaço/E para esperar, números para itens, F para habilidade."
    )


def renderizar(
    mapa: Mapa, 
    entidades: Sequence[Entidade],
    visiveis: Set[Coordenada],
    reveladas: Sequence[Sequence[bool]],
    mensagens: Sequence[str],
    jogador: Entidade,
    turno: int,
    limite_mensagens: int = 6,
) -> None:
    """Desenha o mapa, HUD e log no terminal."""

    limpar_tela()
    grade_texto = compor_grade(mapa, entidades, visiveis, reveladas)
    for linha in grade_texto:
        print(linha)

    log_recente = list(mensagens)[-limite_mensagens:]
    desenhar_hud(jogador, turno, log_recente, mapa.largura)


def mostrar_resumo_final(
    jogador: Entidade,
    turno_final: int,
    estatisticas: Dict[str, int],
    mensagens: Sequence[str],
    caminho_registro: Optional[str] = None,
) -> None:
    """Exibe uma tela de resumo aguardando confirmação do jogador."""

    limpar_tela()
    status_final = "Vivo" if jogador.esta_vivo() else "Derrotado"
    print("=== Resumo da Expedição ===")
    print(f"Status final: {status_final} (HP {jogador.descricao_vida()})")
    print(f"Turnos percorridos: {turno_final}")
    print(f"Inimigos derrotados: {estatisticas.get('inimigos_derrotados', 0)}")
    print(f"Itens coletados: {estatisticas.get('itens_coletados', 0)}")
    print(f"Itens usados: {estatisticas.get('itens_usados', 0)}")
    print(f"Perks desbloqueadas: {estatisticas.get('perks_desbloqueadas', 0)}")
    print(f"Habilidades ativadas: {estatisticas.get('habilidades_ativadas', 0)}")
    if jogador.perks:
        print(f"Perks obtidas: {', '.join(jogador.perks)}")
    if jogador.habilidades:
        print(f"Habilidades conhecidas: {', '.join(jogador.habilidades)}")
    if caminho_registro:
        print(f"Registro salvo em: {caminho_registro}")
    print("\nÚltimas memórias:")
    for mensagem in list(mensagens)[-8:]:
        print(f" - {mensagem}")

    try:
        input("\nPressione Enter para encerrar.")
    except EOFError:
        # Permite encerrar silenciosamente em ambientes sem stdin interativo.
        pass
    finally:
        print()