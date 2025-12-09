"""
Repositório de acesso a dados para a entidade Matricula.

Matriculas representam o vínculo entre alunos (usuarios) e turmas, com informações financeiras.

Padrão de Implementação:
    - Queries com JOIN para buscar turma e aluno relacionados
    - Verificação de duplicidade: verificar_matricula_existente()
    - Queries especializadas por contexto: obter_por_aluno(), obter_por_turma()
    - Campos financeiros: valor_mensalidade, data_vencimento
    - Helpers robustos: _row_get() e _converter_data()

Características:
    - Constraint UNIQUE (id_turma, id_aluno) previne duplicação no banco
    - inserir() verifica duplicidade antes de inserir (retorna None se duplicada)
    - Timestamps automáticos: data_matricula via DEFAULT CURRENT_TIMESTAMP
    - ON DELETE RESTRICT em ambos FKs (não pode excluir turma/aluno com matriculas)

Relacionamentos:
    - turma: Turma completa (em obter_por_aluno) ou None (em obter_por_turma)
    - aluno: Usuario com campos mínimos (nome, email)

Exemplo de uso:
    >>> # Verificar antes de inserir
    >>> if not verificar_matricula_existente(turma_id=1, aluno_id=5):
    ...     id = inserir(matricula)
    >>>
    >>> # Listar por contexto
    >>> matriculas_aluno = obter_por_aluno(aluno_id=5)
    >>> matriculas_turma = obter_por_turma(turma_id=1)
"""

from typing import Optional, List
from datetime import datetime

from model.matricula_model import Matricula
from model.turma_model import Turma
from model.usuario_model import Usuario
from sql.matricula_sql import *
from util.db_util import obter_conexao as get_connection


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


def obter_todas() -> List[Matricula]:
    """Retorna todas as matrículas com turma e aluno carregados"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        result: List[Matricula] = []
        for row in rows:
            turma = Turma(
                id_turma=row["id_turma"],
                nome=_row_get(row, "turma_nome") or "",
                id_atividade=_row_get(row, "id_atividade", 0),
                id_professor=_row_get(row, "id_professor", 0),
                horario_inicio=None,
                horario_fim=None,
                dias_semana=_row_get(row, "dias_semana") or "",
                vagas=_row_get(row, "vagas", 0),
                data_cadastro=None,
                atividade=None,
                professor=None
            )

            aluno = Usuario(
                id=_row_get(row, "id_aluno"),
                nome=_row_get(row, "aluno_nome") or "",
                email=_row_get(row, "aluno_email") or "",
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
                data_matricula=_converter_data(_row_get(row, "data_matricula")),
                valor_mensalidade=_row_get(row, "valor_mensalidade"),
                data_vencimento=_converter_data(_row_get(row, "data_vencimento")),
                turma=turma,
                aluno=aluno
            )
            result.append(matricula)
        return result


def obter_todos() -> List[Matricula]:
    """Alias para obter_todas() - mantém consistência de nomenclatura"""
    return obter_todas()


def obter_por_id(id_matricula: int) -> Optional[Matricula]:
    """Retorna uma matrícula específica com turma e aluno carregados"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_matricula,))
        row = cursor.fetchone()
        if row:
            turma = Turma(
                id_turma=row["id_turma"],
                nome=_row_get(row, "turma_nome") or "",
                id_atividade=_row_get(row, "id_atividade", 0),
                id_professor=_row_get(row, "id_professor", 0),
                horario_inicio=None,
                horario_fim=None,
                dias_semana=_row_get(row, "dias_semana") or "",
                vagas=_row_get(row, "vagas", 0),
                data_cadastro=None,
                atividade=None,
                professor=None
            )

            aluno = Usuario(
                id=_row_get(row, "id_aluno"),
                nome=_row_get(row, "aluno_nome") or "",
                email=_row_get(row, "aluno_email") or "",
                senha="",
                perfil="",
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None
            )

            return Matricula(
                id_matricula=row["id_matricula"],
                id_turma=row["id_turma"],
                id_aluno=row["id_aluno"],
                data_matricula=_converter_data(_row_get(row, "data_matricula")),
                valor_mensalidade=_row_get(row, "valor_mensalidade"),
                data_vencimento=_converter_data(_row_get(row, "data_vencimento")),
                turma=turma,
                aluno=aluno
            )
        return None


def obter_por_aluno_e_turma(id_aluno: int, id_turma: int) -> Optional[Matricula]:
    """Verifica e retorna matrícula existente para aluno/turma"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ALUNO_E_TURMA, (id_aluno, id_turma))
        row = cursor.fetchone()
        if row:
            return Matricula(
                id_matricula=row["id_matricula"],
                id_turma=row["id_turma"],
                id_aluno=row["id_aluno"],
                data_matricula=_converter_data(_row_get(row, "data_matricula")),
                valor_mensalidade=_row_get(row, "valor_mensalidade"),
                data_vencimento=_converter_data(_row_get(row, "data_vencimento")),
                turma=None,
                aluno=None
            )
        return None


def alterar(matricula: Matricula) -> bool:
    """Atualiza uma matrícula existente"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            matricula.id_turma,
            matricula.id_aluno,
            matricula.valor_mensalidade,
            matricula.data_vencimento,
            matricula.id_matricula
        ))
        return cursor.rowcount > 0


def excluir(id_matricula: int) -> bool:
    """Remove uma matrícula"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_matricula,))
        return cursor.rowcount > 0


def obter_quantidade() -> int:
    """Retorna a quantidade total de matrículas"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["total"] if row else 0
