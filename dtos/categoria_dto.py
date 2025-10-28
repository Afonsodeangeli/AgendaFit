"""
DTOs para validação de dados de Categoria.

Fornece validação de campos para operações CRUD de categorias.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_string_obrigatoria,
    validar_comprimento,
    validar_id_positivo,
)


class CriarCategoriaDTO(BaseModel):
    """DTO para criação de categoria"""

    nome: str
    descricao: str = ""

    @field_validator("nome")
    @classmethod
    def _validar_nome(cls, v: str) -> str:
        return validar_string_obrigatoria(
            "Nome", tamanho_minimo=3, tamanho_maximo=100
        )(v)

    @field_validator("descricao")
    @classmethod
    def _validar_descricao(cls, v: str) -> str:
        return validar_comprimento(tamanho_maximo=500)(v)


class AlterarCategoriaDTO(BaseModel):
    """DTO para alteração de categoria"""

    id: int
    nome: str
    descricao: str = ""

    @field_validator("id")
    @classmethod
    def _validar_id(cls, v: int) -> int:
        return validar_id_positivo()(v)

    @field_validator("nome")
    @classmethod
    def _validar_nome(cls, v: str) -> str:
        return validar_string_obrigatoria(
            "Nome", tamanho_minimo=3, tamanho_maximo=100
        )(v)

    @field_validator("descricao")
    @classmethod
    def _validar_descricao(cls, v: str) -> str:
        return validar_comprimento(tamanho_maximo=500)(v)