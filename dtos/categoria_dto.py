from pydantic import BaseModel, field_validator
from dtos.validators import validar_string_obrigatoria

class CategoriaCreateDTO(BaseModel):
    """DTO para criação de categoria de atividades"""

    nome: str
    descricao: str

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_string_obrigatoria("Descrição", tamanho_minimo=10, tamanho_maximo=500)
    )

class CategoriaUpdateDTO(CategoriaCreateDTO):
    """DTO para atualização de categoria de atividades"""
    pass