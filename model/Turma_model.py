from dataclasses import dataclass
from datetime import datetime


@dataclass
class Turma:
    id_atividade: int
    id_professor: int
    data_cadastro: datetime