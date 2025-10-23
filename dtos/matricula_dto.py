"""
DTOs para validação de dados de Matrícula.

Fornece validação de campos para operações CRUD de matrículas.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import validar_id_positivo


class CriarMatriculaDTO(BaseModel):
    """DTO para criação de matrícula"""

    id_aluno: int
    id_turma: int

    _validar_id_aluno = field_validator("id_aluno")(validar_id_positivo())
    _validar_id_turma = field_validator("id_turma")(validar_id_positivo())


class AlterarMatriculaDTO(BaseModel):
    """DTO para alteração de matrícula"""

    id: int
    id_aluno: int
    id_turma: int

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_id_aluno = field_validator("id_aluno")(validar_id_positivo())
    _validar_id_turma = field_validator("id_turma")(validar_id_positivo())
