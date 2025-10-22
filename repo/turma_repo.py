from typing import Optional
from datetime import datetime

from model.Turma_model import Turma
from model.atividade_model import Atividade
from model.usuario_model import Usuario
from model.sql.turma_sql import *
from util.db_util import get_connection


def _converter_data(data_str: Optional[str]) -> Optional[datetime]:
    if not data_str:
        return None
    try:
        return datetime.fromisoformat(data_str)
    except Exception:
        try:
            return datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
        except Exception:
            return None


def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True


def inserir(turma: Turma) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            turma.id_atividade,
            turma.id_professor
        ))
        return cursor.lastrowid


def alterar(turma: Turma) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            turma.id_atividade,
            turma.id_professor,
            turma.id_turma
        ))
        return cursor.rowcount > 0


def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0


def obter_por_id(id: int) -> Optional[Turma]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            # Montar objeto Atividade mínimo com os campos disponíveis
            atividade = Atividade(
                id_atividade=row.get("id_atividade"),
                id_categoria=row.get("id_categoria", 0),
                nome=row.get("atividade_nome") or row.get("nome"),
                descricao=row.get("atividade_descricao") or row.get("descricao"),
                data_cadastro=_converter_data(row.get("data_cadastro")),
                categoria=None
            )

            # Montar objeto Usuario (professor) com campos mínimos
            professor = Usuario(
                id=row.get("id_professor") or row.get("professor_id") or 0,
                nome=row.get("professor_nome") or "",
                email=row.get("professor_email") or "",
                senha="",
                perfil="",
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )

            return Turma(
                id_turma=row["id_turma"],
                id_atividade=row["id_atividade"],
                id_professor=row["id_professor"],
                data_cadastro=_converter_data(row.get("data_cadastro")),
                atividade=atividade,
                professor=professor
            )
        return None


def obter_todas() -> list[Turma]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        result: list[Turma] = []
        for row in rows:
            atividade = Atividade(
                id_atividade=row.get("id_atividade"),
                id_categoria=row.get("id_categoria", 0),
                nome=row.get("atividade_nome") or row.get("nome"),
                descricao=row.get("atividade_descricao") or row.get("descricao"),
                data_cadastro=None,
                categoria=None
            )

            professor = Usuario(
                id=row.get("id_professor") or row.get("professor_id") or 0,
                nome=row.get("professor_nome") or "",
                email=row.get("professor_email") or "",
                senha="",
                perfil="",
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )

            turma = Turma(
                id_turma=row["id_turma"],
                id_atividade=row["id_atividade"],
                id_professor=row["id_professor"],
                data_cadastro=_converter_data(row.get("data_cadastro")),
                atividade=atividade,
                professor=professor
            )
            result.append(turma)
        return result


def obter_por_professor(id_professor: int) -> list[Turma]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_PROFESSOR, (id_professor,))
        rows = cursor.fetchall()
        return [
            Turma(
                id_turma=row["id_turma"],
                id_atividade=row["id_atividade"],
                id_professor=row["id_professor"],
                data_cadastro=_converter_data(row.get("data_cadastro")),
                atividade=None,
                professor=None
            )
            for row in rows
        ]
