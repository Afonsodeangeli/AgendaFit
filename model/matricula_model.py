from dataclasses import dataclass
from datetime import datetime

@dataclass
class Matricula:
    id_Matricula: int
    id_Turma: int
    id_Aluno: int
    Data_Matricula: datetime
    Valor_Mensalidade: int
    Data_Vencimento: datetime
