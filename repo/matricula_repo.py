from typing import Optional, List
from datetime import datetime

from model.matricula_model import Matricula
from model.turma_model import Turma
from model.usuario_model import Usuario
from sql.matricula_sql import *
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


def _row_get(row, key: str, default=None):
    """Helper para acessar valores de sqlite3.Row com fallback"""
    try:
        return row[key]
    except (KeyError, IndexError):
        return default


def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True


def verificar_matricula_existente(id_turma: int, id_aluno: int) -> bool:
    """Retorna True se já existir matrícula para (turma, aluno)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(VERIFICAR_MATRICULA_EXISTENTE, (id_turma, id_aluno))
        row = cursor.fetchone()
        return (row["qtd"] if isinstance(row, dict) and "qtd" in row.keys() else row[0]) > 0


def inserir(matricula: Matricula) -> Optional[int]:
    """Insere matrícula após verificar duplicação. Retorna id ou None se duplicada."""
    if verificar_matricula_existente(matricula.id_turma, matricula.id_aluno):
        return None

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            matricula.id_turma,
            matricula.id_aluno,
            matricula.valor_mensalidade,
            matricula.data_vencimento
        ))
        return cursor.lastrowid


def obter_por_aluno(id_aluno: int) -> List[Matricula]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ALUNO, (id_aluno,))
        rows = cursor.fetchall()
        result: List[Matricula] = []
        for row in rows:
            turma = Turma(
                id_turma=row["id_turma"],
                id_atividade=_row_get(row,"id_atividade", 0),
                id_professor=_row_get(row,"id_professor", 0),
                data_cadastro=None,
                atividade=None,
                professor=None
            )

            aluno = Usuario(
                id=_row_get(row,"id_aluno"),
                nome=_row_get(row,"aluno_nome") or "",
                email=_row_get(row,"aluno_email") or "",
                senha="",
                perfil="",
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )

            matricula = Matricula(
                id_matricula=row["id_matricula"],
                id_turma=row["id_turma"],
                id_aluno=row["id_aluno"],
                data_matricula=_converter_data(_row_get(row,"data_matricula")),
                valor_mensalidade=_row_get(row,"valor_mensalidade"),
                data_vencimento=_converter_data(_row_get(row,"data_vencimento")),
                turma=turma,
                aluno=aluno
            )
            result.append(matricula)
        return result


def obter_por_turma(id_turma: int) -> List[Matricula]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_TURMA, (id_turma,))
        rows = cursor.fetchall()
        result: List[Matricula] = []
        for row in rows:
            aluno = Usuario(
                id=_row_get(row,"id_aluno"),
                nome=_row_get(row,"aluno_nome") or "",
                email=_row_get(row,"aluno_email") or "",
                senha="",
                perfil="",
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )

            matricula = Matricula(
                id_matricula=row["id_matricula"],
                id_turma=row["id_turma"],
                id_aluno=row["id_aluno"],
                data_matricula=_converter_data(_row_get(row,"data_matricula")),
                valor_mensalidade=_row_get(row,"valor_mensalidade"),
                data_vencimento=_converter_data(_row_get(row,"data_vencimento")),
                turma=None,
                aluno=aluno
            )
            result.append(matricula)
        return result
