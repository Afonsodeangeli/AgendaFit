"""
DTOs para validação de dados de Turma.

Fornece validação de campos para operações CRUD de turmas.
"""
from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import time
from dtos.validators import (
    validar_string_obrigatoria,
    validar_id_positivo,
)


def validar_horario(nome_campo: str = "Horário"):
    """Validador para horários em formato HH:MM"""

    def validator(cls, v):
        if not v:
            raise ValueError(f"{nome_campo} é obrigatório")

        # Se já é objeto time, retornar
        if isinstance(v, time):
            return v

        # Se é string, tentar converter
        if isinstance(v, str):
            try:
                partes = v.split(":")
                if len(partes) != 2:
                    raise ValueError(f"{nome_campo} deve estar no formato HH:MM")
                hora, minuto = int(partes[0]), int(partes[1])
                if not (0 <= hora <= 23 and 0 <= minuto <= 59):
                    raise ValueError(f"{nome_campo} inválido")
                return time(hour=hora, minute=minuto)
            except Exception:
                raise ValueError(f"{nome_campo} deve estar no formato HH:MM")

        raise ValueError(f"{nome_campo} inválido")

    return validator


class CriarTurmaDTO(BaseModel):
    """DTO para criação de turma"""

    nome: str
    id_atividade: int
    id_professor: int
    horario_inicio: time
    horario_fim: time
    dias_semana: str
    vagas: int

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_id_atividade = field_validator("id_atividade")(validar_id_positivo())
    _validar_id_professor = field_validator("id_professor")(validar_id_positivo())
    _validar_horario_inicio = field_validator("horario_inicio")(validar_horario("Horário de início"))
    _validar_horario_fim = field_validator("horario_fim")(validar_horario("Horário de fim"))
    _validar_dias_semana = field_validator("dias_semana")(
        validar_string_obrigatoria("Dias da semana", tamanho_minimo=1, tamanho_maximo=50)
    )

    @field_validator("vagas")
    def validar_vagas(cls, v):
        """Valida número de vagas"""
        if not isinstance(v, int) or v < 1:
            raise ValueError("Número de vagas deve ser maior que zero")
        if v > 100:
            raise ValueError("Número de vagas não pode ser maior que 100")
        return v

    @model_validator(mode='after')
    def validar_horarios(self):
        """Valida se horário de fim é posterior ao de início"""
        if self.horario_fim <= self.horario_inicio:
            raise ValueError("Horário de fim deve ser posterior ao horário de início")
        return self


class AlterarTurmaDTO(BaseModel):
    """DTO para alteração de turma"""

    id: int
    nome: str
    id_atividade: int
    id_professor: int
    horario_inicio: time
    horario_fim: time
    dias_semana: str
    vagas: int

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_id_atividade = field_validator("id_atividade")(validar_id_positivo())
    _validar_id_professor = field_validator("id_professor")(validar_id_positivo())
    _validar_horario_inicio = field_validator("horario_inicio")(validar_horario("Horário de início"))
    _validar_horario_fim = field_validator("horario_fim")(validar_horario("Horário de fim"))
    _validar_dias_semana = field_validator("dias_semana")(
        validar_string_obrigatoria("Dias da semana", tamanho_minimo=1, tamanho_maximo=50)
    )

    @field_validator("vagas")
    def validar_vagas(cls, v):
        """Valida número de vagas"""
        if not isinstance(v, int) or v < 1:
            raise ValueError("Número de vagas deve ser maior que zero")
        if v > 100:
            raise ValueError("Número de vagas não pode ser maior que 100")
        return v

    @model_validator(mode='after')
    def validar_horarios(self):
        """Valida se horário de fim é posterior ao de início"""
        if self.horario_fim <= self.horario_inicio:
            raise ValueError("Horário de fim deve ser posterior ao horário de início")
        return self
