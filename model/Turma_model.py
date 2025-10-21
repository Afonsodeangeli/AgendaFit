from dataclasses import dataclass
from datetime import datetime
from typing import Optional



from model.atividade_model import Atividade
from model.usuario_model import Usuario


@dataclass
class Turma:
    id_turma: int
    id_atividade: int
    id_professor: int
    data_cadastro: datetime

    atividade: Optional[Atividade]
    professor: Optional[Usuario] 