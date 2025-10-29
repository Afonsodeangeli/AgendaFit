"""
Repositório de acesso a dados para a entidade Categoria.

Este módulo implementa o padrão Repository, fornecendo uma camada de abstração
entre a lógica de negócio e o acesso aos dados da tabela 'categoria'.

Padrão de Implementação:
    - Usa queries parametrizadas de categoria_sql.py
    - Context manager para gerenciar conexões
    - Função privada _row_to_categoria() para conversão
    - Type hints em todas as funções
    - Docstrings completas

Exemplo de uso:
    >>> from repo import categoria_repo
    >>> categoria = Categoria(id=0, nome="Musculação", descricao="...")
    >>> id_inserido = categoria_repo.inserir(categoria)
    >>> categoria_obtida = categoria_repo.obter_por_id(id_inserido)
"""

from typing import Optional
from model.categoria_model import Categoria
from sql.categoria_sql import *
from util.db_util import get_connection


def _row_to_categoria(row) -> Categoria:
    """Converte uma linha do banco de dados em um objeto Categoria."""
    return Categoria(
        id=row["id"],
        nome=row["nome"],
        descricao=row["descricao"],
        data_cadastro=row["data_cadastro"],
        data_atualizacao=row["data_atualizacao"],
    )


def criar_tabela():
    """Cria a tabela de categorias no banco de dados."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)


def inserir(categoria: Categoria) -> Optional[int]:
    """
    Insere uma nova categoria no banco de dados.

    Args:
        categoria: Objeto Categoria com os dados a serem inseridos

    Returns:
        ID da categoria inserida ou None em caso de erro
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (categoria.nome, categoria.descricao))
        return cursor.lastrowid


def alterar(categoria: Categoria) -> bool:
    """
    Altera uma categoria existente no banco de dados.

    Args:
        categoria: Objeto Categoria com os dados atualizados

    Returns:
        True se a categoria foi alterada, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (categoria.nome, categoria.descricao, categoria.id))
        return cursor.rowcount > 0


def excluir(id: int) -> bool:
    """
    Exclui uma categoria do banco de dados.

    Args:
        id: ID da categoria a ser excluída

    Returns:
        True se a categoria foi excluída, False caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0


def obter_por_id(id: int) -> Optional[Categoria]:
    """
    Obtém uma categoria pelo seu ID.

    Args:
        id: ID da categoria a ser buscada

    Returns:
        Objeto Categoria se encontrado, None caso contrário
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return _row_to_categoria(row)
        return None


def obter_todos() -> list[Categoria]:
    """
    Obtém todas as categorias cadastradas.

    Returns:
        Lista de objetos Categoria ordenados por nome
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        return [_row_to_categoria(row) for row in rows]


def obter_quantidade() -> int:
    """
    Obtém a quantidade total de categorias cadastradas.

    Returns:
        Número total de categorias
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0