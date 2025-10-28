"""
DTOs para operações de configuração do sistema.

Este módulo define os Data Transfer Objects para validação de dados
de configuração do AgendaFit, seguindo o padrão estabelecido pelos
demais DTOs da aplicação.
"""

from pydantic import BaseModel, field_validator
from dtos.validators import validar_string_obrigatoria, validar_comprimento


class AlterarConfiguracaoDTO(BaseModel):
    """
    DTO para alteração de configuração do sistema.

    Attributes:
        chave: Chave única da configuração (ex: "nome_sistema", "email_contato")
        valor: Valor da configuração
        descricao: Descrição opcional da configuração (para documentação)
    """
    chave: str
    valor: str
    descricao: str = ""

    _validar_chave = field_validator("chave")(
        validar_string_obrigatoria("Chave", tamanho_minimo=3, tamanho_maximo=50)
    )

    _validar_valor = field_validator("valor")(
        validar_string_obrigatoria("Valor", tamanho_minimo=1, tamanho_maximo=500)
    )

    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=200)
    )
