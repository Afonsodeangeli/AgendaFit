from dataclasses import dataclass
from datetime import datetime


@dataclass
class Pagamento:
    id_matricula: int
    id_aluno: int
    data_pagamento: datetime
    valor_pago: float