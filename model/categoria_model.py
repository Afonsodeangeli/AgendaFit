from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Categoria:
    """
    Model de categoria de atividades do AgendaFit.

    Attributes:
        id_categoria: Identificador único da categoria
        nome: Nome da categoria (único no sistema)
        descricao: Descrição detalhada da categoria
        data_cadastro: Data de cadastro da categoria (opcional)
    """
    id_categoria: int
    nome: str
    descricao: str
    data_cadastro: Optional[datetime] = None