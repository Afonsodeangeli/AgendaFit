"""
Repositório de acesso a dados para a entidade Pagamento.

Pagamentos representam registros financeiros de mensalidades pagas por alunos.

Padrão de Implementação:
    - Queries com JOIN para buscar matrícula e aluno relacionados
    - Construção de objetos Pagamento, Matricula e Usuario
    - Helpers robustos: _row_get() e _converter_data()

Características:
    - CRUD completo conforme solicitado pelo administrador
    - ON DELETE RESTRICT em FKs (não pode excluir matricula/aluno com pagamentos)
    - Timestamps automáticos: data_pagamento via DEFAULT CURRENT_TIMESTAMP

Exemplo de uso:
    >>> pagamentos = obter_por_aluno(aluno_id=5)
    >>> for p in pagamentos:
    ...     print(f"R$ {p.valor_pago} - {p.data_pagamento}")
"""

from typing import Optional, List
from datetime import datetime

from model.pagamento_model import Pagamento
from model.matricula_model import Matricula
from model.usuario_model import Usuario
from model.turma_model import Turma
from sql.pagamento_sql import *
from util.db_util import obter_conexao as get_connection


def _converter_data(data_str: Optional[str]) -> Optional[datetime]:
    """Converte string de data do banco em objeto datetime"""
    if not data_str:
        return None
    if isinstance(data_str, datetime):
        return data_str
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


def _construir_pagamento(row) -> Pagamento:
    """Constrói objeto Pagamento a partir de uma row do banco"""
    # Construir objeto Turma mínimo com dados do JOIN
    turma = Turma(
        id_turma=_row_get(row, "id_turma", 0),
        nome=_row_get(row, "turma_nome") or "",
        id_atividade=0,
        id_professor=0,
        horario_inicio=None,
        horario_fim=None,
        dias_semana="",
        vagas=0,
        data_cadastro=None,
        data_atualizacao=None,
        atividade=None,
        professor=None
    )

    matricula = Matricula(
        id_matricula=row["id_matricula"],
        id_turma=_row_get(row, "id_turma", 0),
        id_aluno=row["id_aluno"],
        data_matricula=None,
        valor_mensalidade=_row_get(row, "valor_mensalidade", 0.0),
        data_vencimento=None,
        turma=turma,
        aluno=None
    )

    aluno = Usuario(
        id=row["id_aluno"],
        nome=_row_get(row, "aluno_nome") or "",
        email=_row_get(row, "aluno_email") or "",
        senha="",
        perfil="",
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None
    )

    return Pagamento(
        id_pagamento=row["id_pagamento"],
        id_matricula=row["id_matricula"],
        id_aluno=row["id_aluno"],
        data_pagamento=_converter_data(_row_get(row, "data_pagamento")),
        valor_pago=_row_get(row, "valor_pago", 0.0),
        matricula=matricula,
        aluno=aluno
    )


def criar_tabela() -> bool:
    """Cria a tabela de pagamentos se não existir"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
    return True


def inserir(pagamento: Pagamento) -> Optional[int]:
    """Insere um novo pagamento e retorna o id"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            pagamento.id_matricula,
            pagamento.id_aluno,
            pagamento.valor_pago
        ))
        return cursor.lastrowid


def alterar(pagamento: Pagamento) -> bool:
    """Atualiza o valor de um pagamento existente"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            pagamento.valor_pago,
            pagamento.id_pagamento
        ))
        return cursor.rowcount > 0


def excluir(id_pagamento: int) -> bool:
    """Remove um pagamento"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_pagamento,))
        return cursor.rowcount > 0


def obter_todos() -> List[Pagamento]:
    """Retorna todos os pagamentos com matrícula e aluno carregados"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [_construir_pagamento(row) for row in rows]


def obter_por_id(id_pagamento: int) -> Optional[Pagamento]:
    """Retorna um pagamento específico com matrícula e aluno carregados"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_pagamento,))
        row = cursor.fetchone()
        if row:
            return _construir_pagamento(row)
        return None


def obter_por_aluno(id_aluno: int) -> List[Pagamento]:
    """Retorna todos os pagamentos de um aluno"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ALUNO, (id_aluno,))
        rows = cursor.fetchall()
        return [_construir_pagamento(row) for row in rows]


def obter_por_matricula(id_matricula: int) -> List[Pagamento]:
    """Retorna todos os pagamentos de uma matrícula"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_MATRICULA, (id_matricula,))
        rows = cursor.fetchall()
        return [_construir_pagamento(row) for row in rows]


def obter_quantidade() -> int:
    """Retorna a quantidade total de pagamentos"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["total"] if row else 0
