"""Ferramentas para persistir estatísticas das expedições."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Dict

from ..mundo.entidade import Entidade


def salvar_estatisticas_execucao(
    jogador: Entidade, turno_final: int, estatisticas: Dict[str, int],
) -> str:
    """Persiste os dados da run em um arquivo CSV e retorna o caminho usado."""

    caminho = Path("docs/historico_runs.csv")
    novo_arquivo = not caminho.exists()
    caminho.parent.mkdir(parents=True, exist_ok=True)

    campos = [
        "data",
        "status",
        "turnos",
        "nivel",
        "vida",
        "energia",
        "inimigos_derrotados",
        "itens_coletados",
        "itens_usados",
        "perks_desbloqueadas",
        "habilidades_ativadas",
        "perks",
        "habilidades",
    ]

    registro = {
        "data": datetime.now().isoformat(timespec="seconds"),
        "status": "vivo" if jogador.esta_vivo() else "derrotado",
        "turnos": turno_final,
        "nivel": jogador.nivel,
        "vida": jogador.descricao_vida(),
        "energia": jogador.descricao_energia(),
        "inimigos_derrotados": estatisticas.get("inimigos_derrotados", 0),
        "itens_coletados": estatisticas.get("itens_coletados", 0),
        "itens_usados": estatisticas.get("itens_usados", 0),
        "perks_desbloqueadas": estatisticas.get("perks_desbloqueadas", 0),
        "habilidades_ativadas": estatisticas.get("habilidades_ativadas", 0),
        "perks": ", ".join(jogador.perks) if jogador.perks else "",
        "habilidades": ", ".join(jogador.habilidades) if jogador.habilidades else "",
    }

    with caminho.open("a", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        if novo_arquivo:
            escritor.writeheader()
        escritor.writerow(registro)

    return str(caminho)