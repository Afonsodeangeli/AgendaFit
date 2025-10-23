"""
DTOs para validação de dados de Aluno.

Fornece validação de campos para operações CRUD de alunos.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_nome_pessoa,
    validar_email,
    validar_senha_forte,
    validar_id_positivo,
)


class CriarAlunoDTO(BaseModel):
    """DTO para criação de aluno"""

    nome: str
    email: str
    senha: str

    @field_validator("nome")
    @classmethod
    def _validar_nome(cls, v: str) -> str:
        return validar_nome_pessoa()(v)

    @field_validator("email")
    @classmethod
    def _validar_email(cls, v: str) -> str:
        return validar_email()(v)

    @field_validator("senha")
    @classmethod
    def _validar_senha(cls, v: str) -> str:
        return validar_senha_forte()(v)


class AlterarAlunoDTO(BaseModel):
    """DTO para alteração de aluno"""

    id: int
    nome: str
    email: str

    @field_validator("id")
    @classmethod
    def _validar_id(cls, v: int) -> int:
        return validar_id_positivo()(v)

    @field_validator("nome")
    @classmethod
    def _validar_nome(cls, v: str) -> str:
        return validar_nome_pessoa()(v)

    @field_validator("email")
    @classmethod
    def _validar_email(cls, v: str) -> str:
        return validar_email()(v)
