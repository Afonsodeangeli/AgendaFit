from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.turma_model import Turma
from model.usuario_model import Usuario

@dataclass
class Matricula:
    """
    Model de matrícula do AgendaFit.

    Representa o vínculo entre um aluno e uma turma, com informações financeiras.

    Attributes:
        id_matricula: Identificador único da matrícula
        id_turma: FK para turma
        id_aluno: FK para usuario (perfil 'aluno')
        data_matricula: Data de criação da matrícula (auto)
        valor_mensalidade: Valor da mensalidade acordado
        data_vencimento: Dia de vencimento da mensalidade
        turma: Objeto Turma relacionado (opcional, depende da query)
        aluno: Objeto Usuario relacionado (opcional, depende da query)

    Constraints:
        - UNIQUE (id_turma, id_aluno): Previne duplicação
        - ON DELETE RESTRICT em ambos FKs: Não pode excluir turma/aluno com matriculas

    Padrão:
        Verificar duplicidade antes de inserir via matricula_repo.verificar_matricula_existente()
    """
    id_matricula: int
    id_turma: int
    id_aluno: int
    data_matricula: datetime
    valor_mensalidade: float
    data_vencimento: datetime

    turma: Optional[Turma]
    aluno: Optional[Usuario]