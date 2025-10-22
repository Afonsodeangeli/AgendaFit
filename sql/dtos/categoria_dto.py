from pydantic import BaseModel, field_validator

class CategoriaCreateDTO(BaseModel):
    nome: str
    descricao: str

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Nome deve ter no mínimo 3 caracteres')
        if len(v) > 100:
            raise ValueError('Nome deve ter no máximo 100 caracteres')
        return v

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError('Descrição deve ter no mínimo 10 caracteres')
        if len(v) > 500:
            raise ValueError('Descrição deve ter no máximo 500 caracteres')
        return v

class CategoriaUpdateDTO(CategoriaCreateDTO):
    pass