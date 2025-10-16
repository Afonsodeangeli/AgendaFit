from dataclasses import dataclass
from datetime import datetime


@dataclass
class Atividade:
    idcategoria: int
    nome: str
    descricao: str
    DataCadastro: datetime
