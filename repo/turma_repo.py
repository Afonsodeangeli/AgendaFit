"""
Repositório de acesso a dados para a entidade Turma.

Turmas representam classes de atividades ministradas por professores.
Possui relacionamentos com Atividade e Usuario (professor).

Padrão de Implementação:
    - Queries com JOIN para buscar atividade e professor relacionados
    - Constrói objetos Turma, Atividade e Usuario (professor)
    - Tratamento robusto de campos opcionais com _row_get()
    - Query especializada: obter_por_professor()

Exemplo de uso:
    >>> turma = obter_por_id(1)
    >>> print(f"{turma.atividade.nome} - Prof. {turma.professor.nome}")
"""

from typing import Optional
from datetime import datetime

from model.turma_model import Turma
from model.atividade_model import Atividade
from model.usuario_model import Usuario
from sql.turma_sql import *
from util.db_util import get_connection


def _converter_data(data_str: Optional[str]) -> Optional[datetime]:
    """Converte string de data do banco em objeto datetime"""
    if not data_str:
        return None
    # Se já é datetime, retorna direto
    if isinstance(data_str, datetime):
        return data_str
    try:
        # SQLite retorna datas no formato 'YYYY-MM-DD HH:MM:SS'
        return datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
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
                id_atividade=_row_get(row,"id_atividade"),
                id_categoria=_row_get(row,"id_categoria", 0),
                nome=_row_get(row,"atividade_nome") or _row_get(row,"nome"),
                descricao=_row_get(row,"atividade_descricao") or _row_get(row,"descricao"),
                data_cadastro=_converter_data(_row_get(row,"data_cadastro")),
                data_atualizacao=None,
                categoria=None
            )

            # Montar objeto Usuario (professor) com campos mínimos
            professor = Usuario(
                id=_row_get(row,"id_professor") or _row_get(row,"professor_id") or 0,
                nome=_row_get(row,"professor_nome") or "",
                email=_row_get(row,"professor_email") or "",
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
                data_cadastro=_converter_data(_row_get(row,"data_cadastro")),
                data_atualizacao=_converter_data(_row_get(row,"data_atualizacao")),
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
                id_atividade=_row_get(row,"id_atividade"),
                id_categoria=_row_get(row,"id_categoria", 0),
                nome=_row_get(row,"atividade_nome") or _row_get(row,"nome"),
                descricao=_row_get(row,"atividade_descricao") or _row_get(row,"descricao"),
                data_cadastro=None,
                data_atualizacao=None,
                categoria=None
            )

            professor = Usuario(
                id=_row_get(row,"id_professor") or _row_get(row,"professor_id") or 0,
                nome=_row_get(row,"professor_nome") or "",
                email=_row_get(row,"professor_email") or "",
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
                data_cadastro=_converter_data(_row_get(row,"data_cadastro")),
                data_atualizacao=_converter_data(_row_get(row,"data_atualizacao")),
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
                data_cadastro=_converter_data(_row_get(row,"data_cadastro")),
                data_atualizacao=_converter_data(_row_get(row,"data_atualizacao")),
                atividade=None,
                professor=None
            )
            for row in rows
        ]
