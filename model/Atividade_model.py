from dataclasses import dataclass
from datetime import datetime


@dataclass
class Atividade:
    id_categoria: int
    nome: str
    descricao: str
    data_cadastro: datetime
