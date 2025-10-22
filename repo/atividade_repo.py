from typing import Optional
from datetime import datetime
from model.atividade_model import Atividade
from model.categoria_model import Categoria
from sql.atividade_sql import *
from util.db_util import get_connection


def _converter_data(data_str: Optional[str]) -> Optional[datetime]:
    """Converte string de data do banco em objeto datetime"""
    if not data_str:
        return None
    try:
        # SQLite retorna datas no formato 'YYYY-MM-DD HH:MM:SS'
        return datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
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

def inserir(atividade: Atividade) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            atividade.id_categoria,
            atividade.nome,
            atividade.descricao
        ))
        return cursor.lastrowid

def alterar(atividade: Atividade) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            atividade.id_categoria,
            atividade.nome,
            atividade.descricao,
            atividade.id_atividade
        ))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0

def obter_por_id(id: int) -> Optional[Atividade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            categoria = Categoria(
                id_categoria=row["id_categoria"],
                nome=row["categoria_nome"],
                descricao=row["categoria_descricao"],
                data_cadastro=None
            )
            return Atividade(
                id_atividade=row["id_atividade"],
                id_categoria=row["id_categoria"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_cadastro=_converter_data(_row_get(row, "data_cadastro")),
                categoria=categoria
            )
        return None

def obter_todas() -> list[Atividade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Atividade(
                id_atividade=row["id_atividade"],
                id_categoria=row["id_categoria"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_cadastro=_converter_data(_row_get(row, "data_cadastro")),
                categoria=Categoria(
                    id_categoria=row["id_categoria"],
                    nome=row["categoria_nome"],
                    descricao=row["categoria_descricao"],
                    data_cadastro=None
                )
            )
            for row in rows
        ]

def obter_por_categoria(id_categoria: int) -> list[Atividade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CATEGORIA, (id_categoria,))
        rows = cursor.fetchall()
        return [
            Atividade(
                id_atividade=row["id_atividade"],
                id_categoria=row["id_categoria"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_cadastro=_converter_data(_row_get(row, "data_cadastro")),
                categoria=Categoria(
                    id_categoria=row["id_categoria"],
                    nome=row["categoria_nome"],
                    descricao=row["categoria_descricao"],
                    data_cadastro=None
                )
            )
            for row in rows
        ]

def obter_quantidade() -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0