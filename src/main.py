"""Ponto de entrada do roguelike ASCII."""

import random
from typing import Dict, List, Optional, Sequence, Set, Tuple

from .entrada import ler_comando
from .gameplay.combate import resolver_ataque
from .mundo.entidade import Entidade
from .mundo.gerador_mapa import Mapa, gerar_mapa_salas, listar_posicoes_caminhaveis
from .mundo.sistema_turnos import SistemaTurnos
from .render import mostrar_resumo_final, renderizar
from .util.fov import atualizar_celulas_reveladas, calcular_fov

LARGURA_MAPA = 100
ALTURA_MAPA = 60
QUANTIDADE_SALAS = 18
RAIO_FOV = 12
QUANTIDADE_GOBLINS = 8


def preparar_jogo() -> Tuple[
    Entidade, 
    List[Entidade], 
    Mapa, 
    SistemaTurnos, 
    List[str], 
    List[List[bool]],
    Dict[str, int],
]:
    """Configura o mapa, jogador, goblins e estruturas auxiliares."""

    mapa, (inicio_x, inicio_y) = gerar_mapa_salas(LARGURA_MAPA, ALTURA_MAPA, QUANTIDADE_SALAS)
    jogador = Entidade(
        x=inicio_x,
        y=inicio_y,
        simbolo="@",
        nome="Explorador",
        vida_maxima=18,
        vida_atual=18,
        energia_maxima=6,
        energia_atual=6,
        nivel=1,
        forca=5,
        defesa=2,
        agilidade=2,
    )

    entidades: List [Entidade] = [jogador]
    posicoes_livres = listar_posicoes_caminhaveis(mapa)
    goblins = _criar_goblins(posicoes_livres, jogador)
    entidades.extend(goblins)

    sistema_turnos = SistemaTurnos()
    mensagens: List[str] = ["Você desperta em um lugar desconhecido.", "Passos apressados ecoam nas sombras..."]
    reveladas = [[False for _ in range(mapa.largura)] for _ in range(mapa.altura)]
    estatisticas = {"inimigos_derrotados": 0, "pocoes_coletadas": 0}
    return jogador, entidades, mapa, sistema_turnos, mensagens, reveladas, estatisticas


def _criar_goblins(posicoes_livres: Sequence[Tuple[int, int]], jogador: Entidade) -> List[Entidade]:
    """Distribui goblins pelo mapa longe da posição inicial do jogador."""

    goblins: List[Entidade] = []
    posicoes_embaralhadas = list(posicoes_livres)
    random.shuffle(posicoes_embaralhadas)
    for x, y in posicoes_embaralhadas:
        if len(goblins) >= QUANTIDADE_GOBLINS:
            break
        if abs(x - jogador.x) + abs(y - jogador.y) < 6:
            continue
        goblins.append(
            Entidade(
                x=x,
                y=y,
                simbolo="g",
                nome="Goblin",
                vida_maxima=8,
                vida_atual=8,
                energia_maxima=4,
                energia_atual=4,
                nivel=1,
                forca=4,
                defesa=1,
                agilidade=3,
                hostil=True,
            )
        )
    return goblins


def processar_comando(
    jogador: Entidade,
    entidades: List[Entidade],
    mapa: Mapa, 
    comando: Tuple[str, int, int],
    mensagens: list[str],
    estatisticas: Dict[str, int],
) -> bool:
    """Executa o comando retornado pelo módulo de entrada."""

    acao, delta_x, delta_y = comando

    if acao == "sair":
        mensagens.append("Você decide encerrar a exploração.")
        return False

    if acao == "mover":
        destino_x = jogador.x + delta_x
        destino_y = jogador.y + delta_y
        entidade_alvo = _encontrar_entidade(entidades, destino_x, destino_y, ignorar=jogador)
        if entidade_alvo:
            resolver_ataque(jogador, entidade_alvo, mensagens)
            if not entidade_alvo.esta_vivo():
                estatisticas["inimigos_derrotados"] += 1
                mensagens.append("Você coleta uma pequena poção deixada pelo goblin.")
                jogador.inventario.append("Poção menor de cura")
                estatisticas["pocoes_coletadas"] += 1
                entidades.remove(entidade_alvo)
        if mapa.eh_parede(destino_x, destino_y):
            mensagens.append("Uma parede bloqueia seu caminho.")
        else:
            jogador.mover(delta_x, delta_y)
            mensagens.append(_descrever_movimento(delta_x, delta_y))

    return True


def _encontrar_entidade(
    entidades: Sequence[Entidade], x: int, y: int, ignorar: Optional[Entidade] = None
) -> Optional[Entidade]:
    """Procura por qualquer entidade na posição informada."""

    for entidade in entidades:
        if entidade is ignorar:
            continue
        if entidade.x == x and entidade.y == y and entidade.esta_vivo():
            return entidade
    return None


def _descrever_movimento(delta_x: int, delta_y: int) -> str:
    """Retorna uma frase curta descrevendo a direção do movimento."""

    direcoes = {
        (0, -1): "Você avança para o norte.",
        (0, 1): "Você segue para o sul.",
        (-1, 0): "Você se desloca para o oeste.",
        (1, 0): "Você caminha para o leste.",
        (-1, -1): "Você avança para noroeste.",
        (1, -1): "Você avança para nordeste.",
        (-1, 1): "Você segue para sudoeste.",
        (1, 1): "Você segue para sudeste.",
    }
    return direcoes.get((delta_x, delta_y), "Você se movimenta cautelosamente.")


def aguardar_comando() -> Tuple[str, int, int]:
    """Obtém um comando válido do jogador, ignorando teclas desconhecidas."""

    comando: Optional[Tuple[str, int, int]] = None
    while comando is None:
        comando = ler_comando()
    return comando


def atualizar_visibilidade(
    mapa: Mapa,
    jogador: Entidade,
    reveladas: List[List[bool]],
) -> Tuple[Set[Tuple[int, int]], List[List[bool]]]:
    """Calcula as células visíveis e atualiza as reveladas."""

    visiveis = calcular_fov(mapa, (jogador.x, jogador.y), RAIO_FOV)
    atualizar_celulas_reveladas(reveladas, visiveis)
    return visiveis, reveladas


def executar_jogo() -> None:
    """Laço principal responsável por rodar o jogo."""

    (
        jogador,
        entidades,
        mapa,
        sistema_turnos,
        mensagens,
        reveladas,
        estatisticas,
    )= preparar_jogo()
    rodando = True
    jogador_vivo = True

    while rodando and jogador_vivo:
        visiveis, reveladas = atualizar_visibilidade(mapa, jogador, reveladas)
        renderizar(
            mapa,
            entidades,
            visiveis,
            reveladas,
            mensagens,
            jogador,
            sistema_turnos.turno_atual,
        )
        comando = aguardar_comando()
        rodando = processar_comando(jogador, entidades, mapa, comando, mensagens, estatisticas)
        if rodando:
            sistema_turnos.avancar(entidades, jogador, mapa, mensagens)
            if not jogador.esta_vivo():
                mensagens.append("Sua visão escurece... Esta jornada terminou.")
                jogador_vivo = False
                break

    mostrar_resumo_final(jogador, sistema_turnos.turno_atual, estatisticas, mensagens)


def main() -> None:
    """Inicializa e executa o jogo."""
    
    executar_jogo()


if __name__ == "__main__":
    main()