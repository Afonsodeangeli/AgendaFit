from pydantic import BaseModel, field_validator
from datetime import datetime


class MatriculaCreateDTO(BaseModel):
    id_turma: int
    id_aluno: int
    valor_mensalidade: float
    data_vencimento: str

    @field_validator('valor_mensalidade')
    @classmethod
    def validar_valor(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v

    @field_validator('data_vencimento')
    @classmethod
    def validar_data(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
            return v
        except:
            raise ValueError('Data inválida')
