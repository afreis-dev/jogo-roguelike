"""Rotinas responsáveis por interpretar a entrada do jogador."""

import os
import sys
from typing import Optional, Tuple

Comando = Optional[Tuple[str, int, int]]

MAPEAMENTO_MOVIMENTO = {
    "w": ("mover", 0, -1),
    "W": ("mover", 0, -1),
    "UP": ("mover", 0, -1),
    "s": ("mover", 0, 1),
    "S": ("mover", 0, 1),
    "DOWN": ("mover", 0, 1),
    "a": ("mover", -1, 0),
    "A": ("mover", -1, 0),
    "LEFT": ("mover", -1, 0),
    "d": ("mover", 1, 0),
    "D": ("mover", 1, 0),
    "RIGHT": ("mover", 1, 0),
    "q": ("sair", 0, 0),
    "Q": ("sair", 0, 0),
}


def ler_comando() -> Comando:
    """Bloqueia até que uma tecla relevante seja pressionada."""
    tecla = _ler_tecla()
    return MAPEAMENTO_MOVIMENTO.get(tecla)


def _ler_tecla() -> str:
    """Lê uma tecla simples ou setas de maneira multiplataforma."""
    if os.name == "nt":
        return _ler_tecla_windows()
    return _ler_tecla_unix()


def _ler_tecla_windows() -> str:
    """Captura uma tecla no Windows utilizando `msvcrt`."""
    import msvcrt

    while True:
        tecla = msvcrt.getch()
        if tecla in (b"\x00", b"\xe0"):
            tecla_especial = msvcrt.getch()
            mapa_especial = {b"H": "UP", b"P": "DOWN", b"K": "LEFT", b"M": "RIGHT"}
            retorno = mapa_especial.get(tecla_especial)
            if retorno:
                return retorno
        else:
            try:
                return tecla.decode("utf-8")
            except UnicodeDecodeError:
                continue


def _ler_tecla_unix() -> str:
    """Captura uma tecla em sistemas Unix usando `termios`."""
    import termios
    import tty

    fd = sys.stdin.fileno()
    configuracao_antiga = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        tecla = sys.stdin.read(1)
        if tecla == "\x1b":
            sequencia = tecla + sys.stdin.read(2)
            mapa_especial = {"\x1b[A": "UP", "\x1b[B": "DOWN", "\x1b[D": "LEFT", "\x1b[C": "RIGHT"}
            retorno = mapa_especial.get(sequencia)
            if retorno:
                return retorno
            return ""
        return tecla
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, configuracao_antiga)