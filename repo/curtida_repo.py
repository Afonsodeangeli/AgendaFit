from typing import Optional
from model.curtida_model import Curtida
from sql.curtida_sql import *
from util.db_util import obter_conexao as get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(curtida: Curtida) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (curtida.id_usuario, curtida.id_atividade))
        return (cursor.rowcount > 0)

def excluir(id_usuario: int, id_atividade: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_usuario, id_atividade))
        return (cursor.rowcount > 0)

def obter_por_id(id_usuario: int, id_atividade: int) -> Optional[Curtida]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_usuario, id_atividade))
        row = cursor.fetchone()
        if row:
            return Curtida(
                id_usuario=row["id_usuario"],
                id_atividade=row["id_atividade"],
                data_curtida=row["data_curtida"]
            )
        return None

def obter_quantidade_por_atividade(id_atividade: int) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE_POR_ATIVIDADE, (id_atividade,))
        return cursor.fetchone()["quantidade"]