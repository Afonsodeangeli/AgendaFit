"""
DTOs para validação de dados de Matrícula.

Fornece validação de campos para operações CRUD de matrículas.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import validar_id_positivo


def validar_valor_positivo(nome_campo: str = "Valor"):
    """Validador para valores monetários positivos"""
    def validator(cls, v):
        if v is None:
            raise ValueError(f"{nome_campo} é obrigatório")
        if not isinstance(v, (int, float)) or v <= 0:
            raise ValueError(f"{nome_campo} deve ser maior que zero")
        return float(v)
    return validator


def validar_dia_vencimento():
    """Validador para dia de vencimento (1 a 31)"""
    def validator(cls, v):
        if v is None:
            raise ValueError("Dia de vencimento é obrigatório")
        if not isinstance(v, int) or v < 1 or v > 31:
            raise ValueError("Dia de vencimento deve ser entre 1 e 31")
        return v
    return validator


class CriarMatriculaDTO(BaseModel):
    """DTO para criação de matrícula"""

    id_aluno: int
    id_turma: int
    valor_mensalidade: float
    dia_vencimento: int

    _validar_id_aluno = field_validator("id_aluno")(validar_id_positivo())
    _validar_id_turma = field_validator("id_turma")(validar_id_positivo())
    _validar_valor_mensalidade = field_validator("valor_mensalidade")(
        validar_valor_positivo("Valor da mensalidade")
    )
    _validar_dia_vencimento = field_validator("dia_vencimento")(validar_dia_vencimento())


class AlterarMatriculaDTO(BaseModel):
    """DTO para alteração de matrícula"""

    id: int
    id_aluno: int
    id_turma: int
    valor_mensalidade: float
    dia_vencimento: int

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_id_aluno = field_validator("id_aluno")(validar_id_positivo())
    _validar_id_turma = field_validator("id_turma")(validar_id_positivo())
    _validar_valor_mensalidade = field_validator("valor_mensalidade")(
        validar_valor_positivo("Valor da mensalidade")
    )
    _validar_dia_vencimento = field_validator("dia_vencimento")(validar_dia_vencimento())
