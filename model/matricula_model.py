from dataclasses import dataclass
from datetime import datetime

@dataclass
class Matricula:
    id_matricula: int
    id_turma: int
    id_aluno: int
    data_matricula: datetime
    valor_mensalidade: float
    data_vencimento: datetime
