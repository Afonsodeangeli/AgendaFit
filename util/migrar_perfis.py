"""
Script de migração de perfis para o AgendaFit.

Este script converte os perfis antigos (Cliente, Vendedor)
para os novos perfis (Aluno, Professor).

IMPORTANTE: Execute este script APENAS UMA VEZ antes de atualizar util/perfis.py
"""

from util.db_util import get_connection
from util.logger_config import logger

def migrar_perfis():
    """
    Migra perfis antigos para os novos do AgendaFit.

    Conversão:
    - "Cliente" -> "Aluno"
    - "Vendedor" -> "Professor"  (ou deletar se não houver vendedores reais)
    - "Administrador" -> mantém "Administrador"
    """

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Verificar quantos usuários de cada perfil existem
            cursor.execute("SELECT perfil, COUNT(*) as qtd FROM usuario GROUP BY perfil")
            perfis_atuais = cursor.fetchall()

            logger.info("=== PERFIS ATUAIS NO BANCO ===")
            for row in perfis_atuais:
                logger.info(f"  {row['perfil']}: {row['qtd']} usuário(s)")

            # Migrar Cliente -> Aluno
            cursor.execute("""
                UPDATE usuario
                SET perfil = 'Aluno'
                WHERE perfil = 'Cliente'
            """)
            qtd_clientes = cursor.rowcount
            logger.info(f"✅ Migrados {qtd_clientes} usuário(s) de 'Cliente' para 'Aluno'")

            # Decisão sobre Vendedor:
            # Opção 1: Converter para Professor
            cursor.execute("""
                UPDATE usuario
                SET perfil = 'Professor'
                WHERE perfil = 'Vendedor'
            """)
            qtd_vendedores = cursor.rowcount
            logger.info(f"✅ Migrados {qtd_vendedores} usuário(s) de 'Vendedor' para 'Professor'")

            # Opção 2 (alternativa): Deletar vendedores se não fizerem sentido
            # cursor.execute("DELETE FROM usuario WHERE perfil = 'Vendedor'")
            # qtd_deletados = cursor.rowcount
            # logger.info(f"❌ Deletados {qtd_deletados} usuário(s) com perfil 'Vendedor'")

            conn.commit()

            # Verificar resultado final
            cursor.execute("SELECT perfil, COUNT(*) as qtd FROM usuario GROUP BY perfil")
            perfis_novos = cursor.fetchall()

            logger.info("=== PERFIS APÓS MIGRAÇÃO ===")
            for row in perfis_novos:
                logger.info(f"  {row['perfil']}: {row['qtd']} usuário(s)")

            logger.info("✅ Migração de perfis concluída com sucesso!")
            return True

    except Exception as e:
        logger.error(f"❌ Erro ao migrar perfis: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    """
    Execute este script diretamente:
    python -m util.migrar_perfis
    """
    logger.info("=" * 60)
    logger.info("INICIANDO MIGRAÇÃO DE PERFIS DO AGENDAFIT")
    logger.info("=" * 60)

    sucesso = migrar_perfis()

    if sucesso:
        logger.info("=" * 60)
        logger.info("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        logger.info("Agora você pode atualizar util/perfis.py com segurança")
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("❌ MIGRAÇÃO FALHOU!")
        logger.error("Verifique os logs acima e corrija os erros")
        logger.error("=" * 60)