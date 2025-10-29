"""
Script para migrar schema do banco de dados para adicionar colunas de auditoria.
Adiciona data_cadastro e data_atualizacao nas tabelas tarefa, chamado e turma.
"""
from util.db_util import get_connection
from util.logger_config import logger
import sqlite3


def migrar_schema():
    """Aplica migrações de schema necessárias"""
    logger.info("Iniciando migração de schema...")

    with get_connection() as conn:
        cursor = conn.cursor()

        # Verificar e adicionar colunas na tabela tarefa
        try:
            cursor.execute("PRAGMA table_info(tarefa)")
            rows = cursor.fetchall()
            if rows:  # Tabela existe
                colunas_tarefa = [col[1] for col in rows]

                if 'data_cadastro' not in colunas_tarefa:
                    logger.info("Adicionando coluna data_cadastro na tabela tarefa")
                    cursor.execute("""
                        ALTER TABLE tarefa
                        ADD COLUMN data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    """)

                if 'data_atualizacao' not in colunas_tarefa:
                    logger.info("Adicionando coluna data_atualizacao na tabela tarefa")
                    cursor.execute("""
                        ALTER TABLE tarefa
                        ADD COLUMN data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    """)

                if 'data_conclusao' not in colunas_tarefa:
                    logger.info("Adicionando coluna data_conclusao na tabela tarefa")
                    cursor.execute("""
                        ALTER TABLE tarefa
                        ADD COLUMN data_conclusao TIMESTAMP
                    """)
        except sqlite3.OperationalError as e:
            if "no such table" not in str(e).lower():
                logger.warning(f"Erro ao migrar tabela tarefa: {e}")

        # Verificar e adicionar colunas na tabela chamado
        try:
            cursor.execute("PRAGMA table_info(chamado)")
            rows = cursor.fetchall()
            if rows:  # Tabela existe
                colunas_chamado = [col[1] for col in rows]

                if 'data_cadastro' not in colunas_chamado:
                    logger.info("Adicionando coluna data_cadastro na tabela chamado")
                    cursor.execute("""
                        ALTER TABLE chamado
                        ADD COLUMN data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    """)

                if 'data_atualizacao' not in colunas_chamado:
                    logger.info("Adicionando coluna data_atualizacao na tabela chamado")
                    cursor.execute("""
                        ALTER TABLE chamado
                        ADD COLUMN data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    """)

                if 'data_fechamento' not in colunas_chamado:
                    logger.info("Adicionando coluna data_fechamento na tabela chamado")
                    cursor.execute("""
                        ALTER TABLE chamado
                        ADD COLUMN data_fechamento TIMESTAMP
                    """)
        except sqlite3.OperationalError as e:
            if "no such table" not in str(e).lower():
                logger.warning(f"Erro ao migrar tabela chamado: {e}")

        # Verificar e adicionar colunas na tabela turma
        try:
            cursor.execute("PRAGMA table_info(turma)")
            rows = cursor.fetchall()
            if rows:  # Tabela existe
                colunas_turma = [col[1] for col in rows]

                if 'data_cadastro' not in colunas_turma:
                    logger.info("Adicionando coluna data_cadastro na tabela turma")
                    cursor.execute("""
                        ALTER TABLE turma
                        ADD COLUMN data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
                    """)

                if 'data_atualizacao' not in colunas_turma:
                    logger.info("Adicionando coluna data_atualizacao na tabela turma")
                    cursor.execute("""
                        ALTER TABLE turma
                        ADD COLUMN data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
                    """)
        except sqlite3.OperationalError as e:
            if "no such table" not in str(e).lower():
                logger.warning(f"Erro ao migrar tabela turma: {e}")

        # Verificar e adicionar colunas na tabela atividade
        try:
            cursor.execute("PRAGMA table_info(atividade)")
            rows = cursor.fetchall()
            if rows:  # Tabela existe
                colunas_atividade = [col[1] for col in rows]

                if 'data_atualizacao' not in colunas_atividade:
                    logger.info("Adicionando coluna data_atualizacao na tabela atividade")
                    cursor.execute("""
                        ALTER TABLE atividade
                        ADD COLUMN data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
                    """)
        except sqlite3.OperationalError as e:
            if "no such table" not in str(e).lower():
                logger.warning(f"Erro ao migrar tabela atividade: {e}")

        # Verificar e adicionar colunas na tabela categoria
        try:
            cursor.execute("PRAGMA table_info(categoria)")
            rows = cursor.fetchall()
            if rows:  # Tabela existe
                colunas_categoria = [col[1] for col in rows]

                if 'data_atualizacao' not in colunas_categoria:
                    logger.info("Adicionando coluna data_atualizacao na tabela categoria")
                    cursor.execute("""
                        ALTER TABLE categoria
                        ADD COLUMN data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
                    """)
        except sqlite3.OperationalError as e:
            if "no such table" not in str(e).lower():
                logger.warning(f"Erro ao migrar tabela categoria: {e}")

        conn.commit()

    logger.info("Migração de schema concluída!")


if __name__ == "__main__":
    migrar_schema()
