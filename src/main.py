"""Ponto de entrada do roguelike ASCII."""

from typing import List, Optional, Set, Tuple

from .entrada import ler_comando
from .mundo.entidade import Entidade
from .mundo.gerador_mapa import Mapa, gerar_mapa_salas
from .mundo.sistema_turnos import SistemaTurnos
from .render import renderizar
from .util.fov import atualizar_celulas_reveladas, calcular_fov

LARGURA_MAPA = 100
ALTURA_MAPA = 60
QUANTIDADE_SALAS = 18
RAIO_FOV = 12


def preparar_jogo() -> Tuple[Entidade, List[Entidade], Mapa, SistemaTurnos, List[str], List[List[bool]]]:
    """Configura o mapa, jogador, sistema de turnos e estruturas auxiliares."""

    mapa, (inicio_x, inicio_y) = gerar_mapa_salas(LARGURA_MAPA, ALTURA_MAPA, QUANTIDADE_SALAS)
    jogador = Entidade(x=inicio_x, y=inicio_y, simbolo="@")
    entidades = [jogador]
    sistema_turnos = SistemaTurnos()
    mensagens: List[str] = ["Você desperta em um lugar desconhecido."]
    reveladas = [[False for _ in range(mapa.largura)] for _ in range(mapa.altura)]
    return jogador, entidades, mapa, sistema_turnos, mensagens, reveladas


def processar_comando(
    jogador: Entidade,
    mapa: Mapa, 
    comando: Tuple[str, int, int],
    mensagens: list[str],
) -> bool:
    """Executa o comando retornado pelo módulo de entrada."""

    acao, delta_x, delta_y = comando

    if acao == "sair":
        mensagens.append("Você decide encerrar a exploração.")
        return False

    if acao == "mover":
        destino_x = jogador.x + delta_x
        destino_y = jogador.y + delta_y
        if mapa.eh_parede(destino_x, destino_y):
            mensagens.append("Uma parede bloqueia seu caminho.")
        else:
            jogador.mover(delta_x, delta_y)
            mensagens.append(_descrever_movimento(delta_x, delta_y))

    return True


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

    jogador, entidades, mapa, sistema_turnos, mensagens, reveladas = preparar_jogo()
    rodando = True

    while rodando:
        visiveis, reveladas = atualizar_visibilidade(mapa, jogador, reveladas)
        renderizar(mapa, entidades, visiveis, reveladas, mensagens, jogador, sistema_turnos.turno_atual)
        comando = aguardar_comando()
        rodando = processar_comando(jogador, mapa, comando, mensagens)
        if rodando:
            sistema_turnos.avancar(entidades)


def main() -> None:
    """Inicializa e executa o jogo."""
    
    executar_jogo()


if __name__ == "__main__":
    main()