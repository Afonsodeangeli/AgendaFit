from dataclasses import dataclass
from datetime import datetime

@dataclass
class Matricula:
    idTurma: int
    idAluno: int
    DataMatricula: datetime
    ValorMensalidade: int
    DataVencimento: datetime
