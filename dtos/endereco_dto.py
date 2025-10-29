from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_string_obrigatoria,
    validar_comprimento,
    validar_id_positivo,
)


class CriarEnderecoDTO(BaseModel):
    """
    DTO para criar um novo endereço.

    Endereços são sempre vinculados a um usuário.
    """

    id_usuario: int
    titulo: str
    logradouro: str
    numero: int
    complemento: str = ""
    bairro: str
    cidade: str
    uf: str
    cep: int

    _validar_id_usuario = field_validator("id_usuario")(
        validar_id_positivo("ID do usuário")
    )
    _validar_titulo = field_validator("titulo")(
        validar_string_obrigatoria("Título", tamanho_minimo=3, tamanho_maximo=50)
    )
    _validar_logradouro = field_validator("logradouro")(
        validar_string_obrigatoria("Logradouro", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_numero = field_validator("numero")(
        validar_id_positivo("Número")
    )
    _validar_complemento = field_validator("complemento")(
        validar_comprimento(tamanho_maximo=50)
    )
    _validar_bairro = field_validator("bairro")(
        validar_string_obrigatoria("Bairro", tamanho_minimo=3, tamanho_maximo=50)
    )
    _validar_cidade = field_validator("cidade")(
        validar_string_obrigatoria("Cidade", tamanho_minimo=3, tamanho_maximo=50)
    )

    @field_validator("uf")
    @classmethod
    def validar_uf(cls, v: str) -> str:
        """Valida que UF tem exatamente 2 letras maiúsculas."""
        if not v or len(v) != 2:
            raise ValueError("UF deve ter exatamente 2 caracteres")
        if not v.isupper():
            raise ValueError("UF deve estar em letras maiúsculas")
        if not v.isalpha():
            raise ValueError("UF deve conter apenas letras")
        return v

    @field_validator("cep")
    @classmethod
    def validar_cep(cls, v: int) -> int:
        """Valida que CEP é um número de 8 dígitos."""
        if v <= 0:
            raise ValueError("CEP deve ser maior que zero")
        if len(str(v)) != 8:
            raise ValueError("CEP deve ter exatamente 8 dígitos")
        return v


class AlterarEnderecoDTO(BaseModel):
    """
    DTO para alterar um endereço existente.

    O id_usuario não pode ser alterado.
    """

    id_endereco: int
    titulo: str
    logradouro: str
    numero: int
    complemento: str = ""
    bairro: str
    cidade: str
    uf: str
    cep: int

    _validar_id_endereco = field_validator("id_endereco")(
        validar_id_positivo("ID do endereço")
    )
    _validar_titulo = field_validator("titulo")(
        validar_string_obrigatoria("Título", tamanho_minimo=3, tamanho_maximo=50)
    )
    _validar_logradouro = field_validator("logradouro")(
        validar_string_obrigatoria("Logradouro", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_numero = field_validator("numero")(
        validar_id_positivo("Número")
    )
    _validar_complemento = field_validator("complemento")(
        validar_comprimento(tamanho_maximo=50)
    )
    _validar_bairro = field_validator("bairro")(
        validar_string_obrigatoria("Bairro", tamanho_minimo=3, tamanho_maximo=50)
    )
    _validar_cidade = field_validator("cidade")(
        validar_string_obrigatoria("Cidade", tamanho_minimo=3, tamanho_maximo=50)
    )

    @field_validator("uf")
    @classmethod
    def validar_uf(cls, v: str) -> str:
        """Valida que UF tem exatamente 2 letras maiúsculas."""
        if not v or len(v) != 2:
            raise ValueError("UF deve ter exatamente 2 caracteres")
        if not v.isupper():
            raise ValueError("UF deve estar em letras maiúsculas")
        if not v.isalpha():
            raise ValueError("UF deve conter apenas letras")
        return v

    @field_validator("cep")
    @classmethod
    def validar_cep(cls, v: int) -> int:
        """Valida que CEP é um número de 8 dígitos."""
        if v <= 0:
            raise ValueError("CEP deve ser maior que zero")
        if len(str(v)) != 8:
            raise ValueError("CEP deve ter exatamente 8 dígitos")
        return v
