from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.matricula_model import Matricula


@dataclass
class Pagamento:
    id_matricula: int
    id_aluno: int
    data_pagamento: datetime
    valor_pago: float

    matricula: Optional[Matricula]
    aluno: Optional[Matricula]