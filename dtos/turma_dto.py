from pydantic import BaseModel, field_validator
from dtos.validators import validar_id_positivo


class TurmaCreateDTO(BaseModel):
    """DTO para criação de turma"""

    id_atividade: int
    id_professor: int

    _validar_id_atividade = field_validator("id_atividade")(
        validar_id_positivo("ID da Atividade")
    )
    _validar_id_professor = field_validator("id_professor")(
        validar_id_positivo("ID do Professor")
    )
