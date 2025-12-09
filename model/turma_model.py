from dataclasses import dataclass
from datetime import datetime, time
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
        nome: Nome identificador da turma (ex: "Turma A - Manhã")
        id_atividade: ID da atividade desta turma
        id_professor: ID do professor responsável pela turma
        horario_inicio: Horário de início das aulas
        horario_fim: Horário de término das aulas
        dias_semana: Dias da semana das aulas (ex: "Seg, Qua, Sex")
        vagas: Número máximo de vagas disponíveis
        data_cadastro: Data de cadastro da turma
        data_atualizacao: Data da última atualização da turma
        atividade: Objeto Atividade relacionado (opcional, carregado via JOIN)
        professor: Objeto Usuario do professor (opcional, carregado via JOIN)
    """
    id_turma: int
    nome: str
    id_atividade: int
    id_professor: int
    horario_inicio: time
    horario_fim: time
    dias_semana: str
    vagas: int
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None

    atividade: Optional[Atividade] = None
    professor: Optional[Usuario] = None 