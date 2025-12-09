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

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=500)
    )


class AlterarCategoriaDTO(BaseModel):
    """DTO para alteração de categoria"""

    id: int
    nome: str
    descricao: str = ""

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=500)
    )
