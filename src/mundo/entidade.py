"""Módulo que define as entidades básicas do jogo."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:  # Importação apenas para tipagem estática.
    from ..gameplay.inventario import Item


@dataclass
class Entidade:
    """Representa qualquer ser ou objeto posicionado no mapa."""

    x: int
    y: int
    simbolo: str
    nome: str
    vida_atual: int = 10
    vida_maxima: int = 10
    energia_atual: int = 5
    energia_maxima: int = 5
    nivel: int = 1
    forca: int = 3
    defesa: int = 1
    agilidade: int = 1
    hostil: bool = False
    comportamento: str = "neutro"
    estado: str = "patrulha"
    raio_deteccao: int = 5
    alcance_ataque: int = 1
    experiencia: int = 0
    experiencia_para_nivel: int = 12
    pontos_talento: int = 0
    experiencia_entregue: int = 0
    inventario: List["Item"] = field(default_factory=list)
    perks: List[str] = field(default_factory=list)
    perks_ids: Set[str] = field(default_factory=set)
    habilidades: List[str] = field(default_factory=list)
    efeitos_ativos: Dict[str, int] = field(default_factory=dict)

    def mover(self, delta_x: int, delta_y: int) -> None:
        """Atualiza a posição da entidade somando os deltas informados."""
        self.x += delta_x
        self.y += delta_y

    def descricao_vida(self) -> str:
        """Retorna uma descrição curta dos pontos de vida atuais."""
        return f"{self.vida_atual}/{self.vida_maxima}"

    def descricao_energia(self) -> str:
        """Retorna uma descrição curta da energia atual."""
        return f"{self.energia_atual}/{self.energia_maxima}"
    
    def esta_vivo(self) -> bool:
        """Indica se a entidade ainda possui pontos de vida."""
        return self.vida_atual > 0

    def receber_dano(self, quantidade: int) -> None:
        """Reduz a vida atual limitada ao mínimo de zero."""
        self.vida_atual = max(0, self.vida_atual - quantidade)

    def curar(self, quantidade: int) -> None:
        """Recupera pontos de vida sem ultrapassar o máximo."""
        self.vida_atual = min(self.vida_maxima, self.vida_atual + quantidade)
        
    def regenerar_energia(self, quantidade: int) -> None:
        """Recupera energia até o limite máximo."""
        self.energia_atual = min(self.energia_maxima, self.energia_atual + quantidade)

    def consumir_energia(self, quantidade: int) -> bool:
        """Tenta consumir energia e retorna se a operação foi bem-sucedida."""
        if self.energia_atual < quantidade:
            return False
        self.energia_atual -= quantidade
        return True

    def ganhar_experiencia(self, quantidade: int, mensagens: List[str]) -> None:
        """Acumula experiência e gerencia subida de nível e talentos."""
        self.experiencia += quantidade
        while self.experiencia >= self.experiencia_para_nivel:
            self.experiencia -= self.experiencia_para_nivel
            self.nivel += 1
            self.pontos_talento += 1
            self.experiencia_para_nivel += 8
            mensagens.append(
                f"Você atinge o nível {self.nivel}! Um ponto de talento está disponível (pressione P)."
            )

    def adicionar_perk(self, identificador: str, nome_exibicao: Optional[str] = None) -> None:
        """Registra uma nova perk caso ainda não tenha sido adquirida."""
        if identificador in self.perks_ids:
            return
        self.perks_ids.add(identificador)
        self.perks.append(nome_exibicao or identificador)

    def tem_perk(self, identificador: str) -> bool:
        """Informa se a perk já está cadastrada."""
        return identificador in self.perks_ids

    def registrar_habilidade(self, identificador: str) -> None:
        """Disponibiliza uma habilidade ativa para a entidade."""
        if identificador not in self.habilidades:
            self.habilidades.append(identificador)

    def tem_habilidade(self, identificador: str) -> bool:
        """Indica se a habilidade está liberada."""
        return identificador in self.habilidades