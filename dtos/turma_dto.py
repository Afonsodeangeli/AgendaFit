from pydantic import BaseModel, field_validator


class TurmaCreateDTO(BaseModel):
    id_atividade: int
    id_professor: int

    @field_validator('id_atividade', 'id_professor')
    @classmethod
    def validar_ids(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('ID inválido')
        return v
