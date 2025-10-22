from repo import usuario_repo
from model.usuario_model import Usuario
from util.security import criar_hash_senha
from util.logger_config import logger
from util.perfis import Perfil

def inicializar_dados():
    """
    Inicializa dados iniciais do AgendaFit no banco de dados.

    Cria:
    - 1 administrador padrão
    - 1 professor exemplo
    - 1 aluno exemplo
    - Categorias de atividades padrão (quando implementadas)
    """
    from util.security import criar_hash_senha
    from util.perfis import Perfil
    from model.usuario_model import Usuario
    from repo import usuario_repo

    logger.info("Verificando dados iniciais do AgendaFit...")

    # Verificar se já existem usuários
    qtd_usuarios = usuario_repo.obter_quantidade()

    if qtd_usuarios == 0:
        logger.info("Nenhum usuário encontrado. Criando usuários padrão...")

        # 1. ADMINISTRADOR
        admin = Usuario(
            id=0,
            nome="Administrador",
            email="admin@agendafit.com",
            senha=criar_hash_senha("admin123"),
            perfil=Perfil.ADMIN.value
        )
        admin_id = usuario_repo.inserir(admin)
        if admin_id:
            logger.info(f"✅ Administrador criado (ID: {admin_id})")

        # 2. PROFESSOR EXEMPLO
        professor = Usuario(
            id=0,
            nome="Prof. Carlos Oliveira",
            email="professor@agendafit.com",
            senha=criar_hash_senha("prof123"),
            perfil=Perfil.PROFESSOR.value
        )
        prof_id = usuario_repo.inserir(professor)
        if prof_id:
            logger.info(f"✅ Professor exemplo criado (ID: {prof_id})")

        # 3. ALUNO EXEMPLO
        aluno = Usuario(
            id=0,
            nome="Ana Paula Costa",
            email="aluno@agendafit.com",
            senha=criar_hash_senha("aluno123"),
            perfil=Perfil.ALUNO.value
        )
        aluno_id = usuario_repo.inserir(aluno)
        if aluno_id:
            logger.info(f"✅ Aluno exemplo criado (ID: {aluno_id})")

        logger.info("✅ Dados iniciais do AgendaFit criados com sucesso!")
        logger.info("=" * 60)
        logger.info("CREDENCIAIS PADRÃO:")
        logger.info("  Admin:     admin@agendafit.com / admin123")
        logger.info("  Professor: professor@agendafit.com / prof123")
        logger.info("  Aluno:     aluno@agendafit.com / aluno123")
        logger.info("=" * 60)
    else:
        logger.info(f"Banco já possui {qtd_usuarios} usuário(s). Seed não necessário.")

    # TODO: Quando implementar categorias, adicionar seeds de categorias padrão
    # Exemplos: Yoga, Musculação, Pilates, Spinning, Crossfit, etc.