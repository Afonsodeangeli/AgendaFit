from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.categoria_model import Categoria


@dataclass
class Atividade:
    id_atividade: int
    id_categoria: int
    nome: str
    descricao: str
    data_cadastro: datetime
    
    categoria: Optional[Categoria]
