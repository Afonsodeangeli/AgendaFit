"""
DTOs para validação de dados de Pagamento.

Fornece validação de campos para operações CRUD de pagamentos.
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


class CriarPagamentoDTO(BaseModel):
    """DTO para criação de pagamento"""

    id_matricula: int
    valor_pago: float

    _validar_id_matricula = field_validator("id_matricula")(validar_id_positivo())
    _validar_valor_pago = field_validator("valor_pago")(
        validar_valor_positivo("Valor pago")
    )


class AlterarPagamentoDTO(BaseModel):
    """DTO para alteração de pagamento"""

    id: int
    valor_pago: float

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_valor_pago = field_validator("valor_pago")(
        validar_valor_positivo("Valor pago")
    )
