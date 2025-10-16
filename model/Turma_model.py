from dataclasses import dataclass
from datetime import datetime


@dataclass
class Turma:
    idatividade: int
    idprofessor: int
    datacadastro: datetime