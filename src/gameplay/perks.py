"""Sistema simples de perks e habilidades do jogador."""

from dataclasses import dataclass
from typing import Dict, List, Sequence

from ..mundo.entidade import Entidade


@dataclass
class Perk:
    """Representa uma vantagem permanente que pode ser adquirida."""

    identificador: str
    nome: str
    descricao: str

    def aplicar(self, jogador: Entidade, mensagens: List[str]) -> None:
        """Executa o efeito permanente da perk."""
        if self.identificador == "resiliencia_instintiva":
            jogador.vida_maxima += 4
            jogador.curar(4)
            mensagens.append("Sua pele se fortalece, ampliando seus pontos de vida.")
        elif self.identificador == "foco_letal":
            jogador.forca += 2
            mensagens.append("Sua força se intensifica, golpes ficam mais pesados.")
        elif self.identificador == "disciplina_guerreira":
            jogador.registrar_habilidade("golpe_concentrado")
            jogador.energia_maxima += 1
            jogador.regenerar_energia(1)
            mensagens.append("Você aprende a canalizar energia em um golpe devastador.")
        else:
            mensagens.append("Nada parece acontecer...")

        jogador.adicionar_perk(self.identificador, self.nome)


PERKS_DISPONIVEIS: Dict[str, Perk] = {
    "resiliencia_instintiva": Perk(
        identificador="resiliencia_instintiva",
        nome="Resiliência Instintiva",
        descricao="+4 HP máximo e cura imediata dessa quantidade.",
    ),
    "foco_letal": Perk(
        identificador="foco_letal",
        nome="Foco Letal",
        descricao="+2 Força permanente.",
    ),
    "disciplina_guerreira": Perk(
        identificador="disciplina_guerreira",
        nome="Disciplina Guerreira",
        descricao="Desbloqueia Golpe Concentrado e +1 energia máxima.",
    ),
}


def listar_perks_disponiveis(jogador: Entidade) -> Sequence[Perk]:
    """Retorna as perks que ainda não foram obtidas."""
    return [perk for perk in PERKS_DISPONIVEIS.values() if not jogador.tem_perk(perk.identificador)]


def escolher_perk_interativamente(
    jogador: Entidade, mensagens: List[str], estatisticas: Dict[str, int]
) -> None:
    """Apresenta um menu simples para gastar pontos de talento."""

    if jogador.pontos_talento <= 0:
        mensagens.append("Nenhum ponto de talento disponível no momento.")
        return

    opcoes = listar_perks_disponiveis(jogador)
    if not opcoes:
        mensagens.append("Você já dominou todas as perks disponíveis.")
        return

    print("\n=== Seleção de Perks ===")
    for indice, perk in enumerate(opcoes, start=1):
        print(f"{indice}) {perk.nome} - {perk.descricao}")
    print("Digite o número da perk desejada ou pressione Enter para cancelar.")

    escolha = input("> ").strip()
    if not escolha:
        mensagens.append("Você adia a escolha do talento.")
        return

    if not escolha.isdigit():
        mensagens.append("Entrada inválida, seleção cancelada.")
        return

    indice = int(escolha) - 1
    if indice < 0 or indice >= len(opcoes):
        mensagens.append("Nenhuma perk corresponde à escolha informada.")
        return

    perk = opcoes[indice]
    perk.aplicar(jogador, mensagens)
    jogador.pontos_talento -= 1
    estatisticas.setdefault("perks_desbloqueadas", 0)
    estatisticas["perks_desbloqueadas"] += 1
    mensagens.append(f"Perk adquirida: {perk.nome}.")