from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from util.perfis import Perfil
from dtos.validators import (
    validar_email,
    validar_senha_forte,
    validar_nome_pessoa,
    validar_id_positivo,
    validar_tipo,
    validar_comprimento,
)


def validar_telefone():
    """Valida formato do telefone (opcional)"""
    def validator(value: str) -> str:
        if not value:
            return value
        # Remove caracteres não numéricos para validação
        numeros = ''.join(c for c in value if c.isdigit())
        if len(numeros) > 0 and (len(numeros) < 10 or len(numeros) > 11):
            raise ValueError("Telefone deve ter 10 ou 11 dígitos")
        return value
    return validator


def validar_data_nascimento():
    """Valida data de nascimento (opcional)"""
    def validator(value: Optional[date]) -> Optional[date]:
        if value is None:
            return value
        hoje = date.today()
        if value > hoje:
            raise ValueError("Data de nascimento não pode ser no futuro")
        idade = (hoje - value).days // 365
        if idade > 120:
            raise ValueError("Data de nascimento inválida")
        return value
    return validator


class CriarUsuarioDTO(BaseModel):
    """DTO para criação de usuário pelo administrador."""

    nome: str = Field(..., description="Nome completo do usuário")
    email: str = Field(..., description="E-mail do usuário")
    senha: str = Field(..., description="Senha do usuário")
    perfil: str = Field(..., description="Perfil/Role do usuário")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")
    numero_documento: str = Field("", description="Número do documento (CPF, RG)")
    telefone: str = Field("", description="Telefone de contato")

    _validar_nome = field_validator("nome")(validar_nome_pessoa())
    _validar_email = field_validator("email")(validar_email())
    _validar_senha = field_validator("senha")(validar_senha_forte())
    _validar_perfil = field_validator("perfil")(validar_tipo("Perfil", Perfil))
    _validar_data_nascimento = field_validator("data_nascimento")(validar_data_nascimento())
    _validar_numero_documento = field_validator("numero_documento")(validar_comprimento(tamanho_maximo=20))
    _validar_telefone = field_validator("telefone")(validar_telefone())


class AlterarUsuarioDTO(BaseModel):
    """DTO para alteração de usuário pelo administrador."""

    id: int = Field(..., description="ID do usuário a ser alterado")
    nome: str = Field(..., description="Nome completo do usuário")
    email: str = Field(..., description="E-mail do usuário")
    perfil: str = Field(..., description="Perfil/Role do usuário")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")
    numero_documento: str = Field("", description="Número do documento (CPF, RG)")
    telefone: str = Field("", description="Telefone de contato")

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(validar_nome_pessoa())
    _validar_email = field_validator("email")(validar_email())
    _validar_perfil = field_validator("perfil")(validar_tipo("Perfil", Perfil))
    _validar_data_nascimento = field_validator("data_nascimento")(validar_data_nascimento())
    _validar_numero_documento = field_validator("numero_documento")(validar_comprimento(tamanho_maximo=20))
    _validar_telefone = field_validator("telefone")(validar_telefone())
