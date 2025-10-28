from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.turma_model import Turma
from model.usuario_model import Usuario

@dataclass
class Matricula:
    id_matricula: int
    id_turma: int
    id_aluno: int
    data_matricula: datetime
    valor_mensalidade: float
    data_vencimento: datetime

    turma: Optional[Turma]
    aluno: Optional[Usuario]