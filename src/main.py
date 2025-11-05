"""Ponto de entrada do roguelike ASCII."""

from typing import List, Optional, Tuple

from .entrada import ler_comando
from .mundo.entidade import Entidade
from .mundo.gerador_mapa import Mapa, gerar_mapa_salas
from .render import renderizar

LARGURA_MAPA = 60
ALTURA_MAPA = 30
QUANTIDADE_SALAS = 10


def preparar_jogo() -> Tuple[Entidade, List[Entidade], Mapa]:
    """Configura o mapa e posiciona o jogador inicial."""
    mapa, (inicio_x, inicio_y) = gerar_mapa_salas(LARGURA_MAPA, ALTURA_MAPA, QUANTIDADE_SALAS)
    jogador = Entidade(x=inicio_x, y=inicio_y, simbolo="@")
    entidades = [jogador]
    return jogador, entidades, mapa


def processar_comando(jogador: Entidade, mapa: Mapa, comando: Tuple[str, int, int]) -> bool:
    """Executa o comando retornado pelo módulo de entrada."""
    acao, delta_x, delta_y = comando

    if acao == "sair":
        return False

    if acao == "mover":
        destino_x = jogador.x + delta_x
        destino_y = jogador.y + delta_y
        if not mapa.eh_parede(destino_x, destino_y):
            jogador.mover(delta_x, delta_y)

    return True


def aguardar_comando() -> Tuple[str, int, int]:
    """Obtém um comando válido do jogador, ignorando teclas desconhecidas."""
    comando: Optional[Tuple[str, int, int]] = None
    while comando is None:
        comando = ler_comando()
    return comando


def executar_jogo() -> None:
    """Laço principal responsável por rodar o jogo."""
    jogador, entidades, mapa = preparar_jogo()
    rodando = True

    while rodando:
        renderizar(mapa, entidades)
        comando = aguardar_comando()
        rodando = processar_comando(jogador, mapa, comando)


def main() -> None:
    """Inicializa e executa o jogo."""
    executar_jogo()


if __name__ == "__main__":
    main()
