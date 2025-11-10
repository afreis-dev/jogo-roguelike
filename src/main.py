"""Ponto de entrada do roguelike ASCII."""

import random
from typing import Dict, List, Optional, Sequence, Set, Tuple

from .entrada import ler_comando
from .gameplay.combate import resolver_ataque
from .gameplay.inventario import (
    Item,
    criar_bomba_fumaca,
    criar_pocao_cura,
    criar_pocao_energia,
    usar_item_por_indice,
)
from .gameplay.perks import escolher_perk_interativamente
from .mundo.entidade import Entidade
from .mundo.gerador_mapa import Mapa, gerar_mapa_salas, listar_posicoes_caminhaveis
from .mundo.sistema_turnos import SistemaTurnos
from .render import mostrar_resumo_final, renderizar
from .util.fov import atualizar_celulas_reveladas, calcular_fov
from .util.registro import salvar_estatisticas_execucao

LARGURA_MAPA = 100
ALTURA_MAPA = 60
QUANTIDADE_SALAS = 18
RAIO_FOV = 12
QUANTIDADE_GOBLINS_GUERREIROS = 6
QUANTIDADE_GOBLINS_ARQUEIROS = 3
DISTANCIA_MINIMA_SPAWN = 6


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
        vida_maxima=20,
        vida_atual=20,
        energia_maxima=7,
        energia_atual=7,
        nivel=1,
        forca=5,
        defesa=2,
        agilidade=3,
        raio_deteccao=10,
        alcance_ataque=1,
    )
    jogador.inventario.extend([criar_pocao_cura(),criar_pocao_energia()])

    entidades: List [Entidade] = [jogador]
    posicoes_livres = listar_posicoes_caminhaveis(mapa)
    inimigos = _criar_inimigos(posicoes_livres, jogador)
    entidades.extend(inimigos)

    sistema_turnos = SistemaTurnos()
    mensagens: List[str] = [
        "Você desperta em um lugar desconhecido.",
        "Passos apressados ecoam nas sombras...",
        "Use números (1-9) para consumir itens rápidos, P para perks e F para Golpe Concentrado (quando disponível).",
    ]
    reveladas = [[False for _ in range(mapa.largura)] for _ in range(mapa.altura)]
    estatisticas = {
        "inimigos_derrotados": 0,
        "pocoes_coletadas": 0,
        "itens_coletados": 0,
        "itens_usados": 0,
        "habilidades_ativadas": 0,
        "perks_desbloqueadas": 0,
    }
    return jogador, entidades, mapa, sistema_turnos, mensagens, reveladas, estatisticas


def _criar_inimigos(posicoes_livres: Sequence[Tuple[int, int]], jogador: Entidade) -> List[Entidade]:
    """Distribui inimigos pelo mapa, evitando a posição inicial do jogador."""

    posicoes_embaralhadas = list(posicoes_livres)
    random.shuffle(posicoes_embaralhadas)
    tipos_restantes = [
        *["guerreiro"] * QUANTIDADE_GOBLINS_GUERREIROS,
        *["arqueiro"] * QUANTIDADE_GOBLINS_ARQUEIROS,
    ]
    inimigos: List[Entidade] = []

    for x, y in posicoes_embaralhadas:
        if not tipos_restantes:
            break
        if abs(x - jogador.x) + abs(y - jogador.y) < DISTANCIA_MINIMA_SPAWN:
            continue
        tipo = random.choice(tipos_restantes)
        tipos_restantes.remove(tipo)
        if tipo == "guerreiro":
            inimigos.append(_novo_goblin_guerreiro(x, y))
        else:
            inimigos.append(_novo_goblin_arqueiro(x, y))

    return inimigos


def _novo_goblin_guerreiro(x: int, y: int) -> Entidade:
    """Cria um goblin guerreiro agressivo de combate corpo a corpo."""

    return Entidade(
        x=x,
        y=y,
        simbolo="g",
        nome="Goblin saqueador",
        vida_maxima=10,
        vida_atual=10,
        energia_maxima=4,
        energia_atual=4,
        nivel=1,
        forca=4,
        defesa=2,
        agilidade=3,
        hostil=True,
        comportamento="goblin_guerreiro",
        raio_deteccao=9,
        alcance_ataque=1,
        experiencia_entregue=6,
    )


def _novo_goblin_arqueiro(x: int, y: int) -> Entidade:
    """Cria um goblin arqueiro com ataques à distância."""

    return Entidade(
        x=x,
        y=y,
        simbolo="G",
        nome="Goblin arqueiro",
        vida_maxima=8,
        vida_atual=8,
        energia_maxima=5,
        energia_atual=5,
        nivel=2,
        forca=3,
        defesa=1,
        agilidade=4,
        hostil=True,
        comportamento="goblin_arqueiro",
        raio_deteccao=11,
        alcance_ataque=5,
        experiencia_entregue=8,
    )


def processar_comando(
    jogador: Entidade,
    entidades: List[Entidade],
    mapa: Mapa, 
    comando: Tuple[str, int, int],
    mensagens: list[str],
    estatisticas: Dict[str, int],
) -> bool:
    """Executa o comando retornado pelo módulo de entrada."""

    acao, valor_a, _valor_b = comando

    if acao == "sair":
        mensagens.append("Você decide encerrar a exploração.")
        return False

    if acao == "mover":
        destino_x = jogador.x + valor_a
        destino_y = jogador.y + _valor_b
        entidade_alvo = _encontrar_entidade(entidades, destino_x, destino_y, ignorar=jogador)
        if entidade_alvo:
            resolver_ataque(jogador, entidade_alvo, mensagens)
            if not entidade_alvo.esta_vivo():
                _processar_derrota_inimigo(entidade_alvo,entidades, jogador, mensagens, estatisticas)
        elif mapa.eh_parede(destino_x, destino_y):
            mensagens.append("Uma parede irregular bloqueia seu caminho.")
        else:
            jogador.mover(valor_a, _valor_b)
            mensagens.append(_descrever_movimento(valor_a, _valor_b))
        return True

    if acao == "esperar":
        jogador.regenerar_energia(1)
        mensagens.append("Você aguarda o momento certo, recuperando um pouco de energia.")
        return True
    
    if acao == "usar_item":
        derrotados = usar_item_por_indice(jogador, valor_a, entidades, mapa, mensagens, estatisticas)
        for inimigo in list(derrotados):
            if inimigo in entidades:
                _processar_derrota_inimigo(inimigo, entidades, jogador, mensagens, estatisticas)
        return True
    
    if acao == "perks":
        escolher_perk_interativamente(jogador, mensagens, estatisticas)
        return True
    
    if acao == "habilidade":
        usar_habilidade_especial(jogador, mensagens, estatisticas)
        return True
    
    mensagens.append("Você hesita por um instante, sem tomar decisão.")
    return True


def _processar_derrota_inimigo(
    inimigo: Entidade,
    entidades: List[Entidade],
    jogador: Entidade,
    mensagens: List[str],
    estatisticas: Dict[str, int],
) -> None:
    """Atualiza estado e estatísticas após eliminar um inimigo."""

    estatisticas["inimigos_derrotados"] += 1
    if inimigo.experiencia_entregue:
        jogador.ganhar_experiencia(inimigo.experiencia_entregue, mensagens)
    drop = _gerar_drop_inimigo(inimigo)
    if drop:
        jogador.inventario.append(drop)
        estatisticas["itens_coletados"] += 1
        mensagens.append(f"Você coleta {drop.nome} deixado pelo inimigo.")
        if "Poção" in drop.nome:
            estatisticas["pocoes_coletadas"] += 1
    entidades.remove(inimigo)


def _gerar_drop_inimigo(inimigo: Entidade) -> Optional[Item]:
    """Define itens que podem ser derrubados após o combate."""

    chance = random.random()
    if inimigo.comportamento == "goblin_guerreiro":
        if chance < 0.5:
            return criar_pocao_cura()
        if chance < 0.65:
            return criar_bomba_fumaca()
    elif inimigo.comportamento == "goblin_arqueiro":
        if chance < 0.5:
            return criar_pocao_energia()
        if chance < 0.7:
            return criar_bomba_fumaca()
    return None


def usar_habilidade_especial(jogador: Entidade, mensagens: List[str], estatisticas: Dict[str, int]) -> None:
    """Aciona uma habilidade ativa caso esteja disponível."""

    if not jogador.tem_habilidade("golpe_concentrado"):
        mensagens.append("Você ainda não domina nenhuma habilidade ativa.")
        return

    if jogador.efeitos_ativos.get("golpe_concentrado"):
        mensagens.append("Você já está concentrado para um golpe poderoso.")
        return

    custo = 2
    if not jogador.consumir_energia(custo):
        mensagens.append("Energia insuficiente para canalizar o golpe.")
        return

    jogador.efeitos_ativos["golpe_concentrado"] = 1
    estatisticas["habilidades_ativadas"] += 1
    mensagens.append("Você concentra sua força; o próximo ataque será devastador!")


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

    caminho_registro = salvar_estatisticas_execucao(jogador, sistema_turnos.turno_atual, estatisticas)
    mostrar_resumo_final(jogador, sistema_turnos.turno_atual, estatisticas, mensagens)


def main() -> None:
    """Inicializa e executa o jogo."""
    
    executar_jogo()


if __name__ == "__main__":
    main()