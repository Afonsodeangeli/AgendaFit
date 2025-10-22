from dataclasses import dataclass
from datetime import datetime
from typing import Optional



from model.atividade_model import Atividade
from model.usuario_model import Usuario


@dataclass
class Turma:
    """
    Model de turma do AgendaFit.

    Representa uma turma de uma atividade específica ministrada por um professor.

    Attributes:
        id_turma: Identificador único da turma
        id_atividade: ID da atividade desta turma
        id_professor: ID do professor responsável pela turma
        data_cadastro: Data de cadastro da turma
        atividade: Objeto Atividade relacionado (opcional, carregado via JOIN)
        professor: Objeto Usuario do professor (opcional, carregado via JOIN)
    """
    id_turma: int
    id_atividade: int
    id_professor: int
    data_cadastro: datetime

    atividade: Optional[Atividade]
    professor: Optional[Usuario] 