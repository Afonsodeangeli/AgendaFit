from pydantic import BaseModel, field_validator
from dtos.validators import validar_string_obrigatoria, validar_id_positivo

class AtividadeCreateDTO(BaseModel):
    """DTO para criação de atividade física/esportiva"""

    id_categoria: int
    nome: str
    descricao: str

    _validar_id_categoria = field_validator("id_categoria")(
        validar_id_positivo("ID da Categoria")
    )
    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_string_obrigatoria("Descrição", tamanho_minimo=10, tamanho_maximo=1000)
    )

class AtividadeUpdateDTO(AtividadeCreateDTO):
    """DTO para atualização de atividade física/esportiva"""
    pass