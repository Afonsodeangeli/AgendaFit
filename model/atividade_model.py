from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Atividade:
    """
    Model de atividade física/esportiva do AgendaFit.

    Attributes:
        id_atividade: Identificador único da atividade
        id_categoria: FK para a categoria da atividade
        nome: Nome da atividade
        descricao: Descrição detalhada da atividade
        data_cadastro: Data de cadastro da atividade
        data_atualizacao: Data da última atualização da atividade
        categoria_nome: Nome da categoria (preenchido via JOIN)
    """
    id_atividade: int
    id_categoria: Optional[int]
    nome: str
    descricao: str
    data_cadastro: datetime
    data_atualizacao: Optional[datetime] = None
    categoria_nome: Optional[str] = None
