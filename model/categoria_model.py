from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Categoria:
    """
    Model de categoria de atividades do AgendaFit.

    Attributes:
        id: Identificador único da categoria
        nome: Nome da categoria (único no sistema)
        descricao: Descrição detalhada da categoria
        data_cadastro: Data de cadastro da categoria (opcional)
        data_atualizacao: Data da última atualização (opcional)
    """
    id: int
    nome: str
    descricao: Optional[str] = None
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None