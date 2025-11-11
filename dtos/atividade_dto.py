"""
DTOs para validação de dados de Atividade.

Fornece validação de campos para operações CRUD de atividades.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_string_obrigatoria,
    validar_comprimento,
    validar_id_positivo,
)


class CriarAtividadeDTO(BaseModel):
    """DTO para criação de atividade"""

    nome: str
    descricao: str = ""

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=1000)
    )


class AlterarAtividadeDTO(BaseModel):
    """DTO para alteração de atividade"""

    id: int
    nome: str
    descricao: str = ""

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=1000)
    )
