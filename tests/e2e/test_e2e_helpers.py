"""
Funcoes auxiliares e Page Objects para testes E2E.

Fornece helpers para interacoes comuns com a UI.
"""
from typing import Optional

from playwright.sync_api import Page, expect


# =============================================================================
# BASE PAGE OBJECT
# =============================================================================


class BasePage:
    """Page Object base com funcionalidades comuns."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navegar(self, path: str = "") -> None:
        """Navega para uma URL relativa."""
        self.page.goto(f"{self.base_url}{path}")

    def obter_mensagem_flash(self) -> Optional[str]:
        """Obtem mensagem flash (toast ou alert)."""
        toast = self.page.locator('.toast-body').first
        if toast.is_visible():
            return toast.text_content()

        alert = self.page.locator('.alert').first
        if alert.is_visible():
            return alert.text_content()

        return None

    def aguardar_carregamento(self, timeout: int = 5000) -> None:
        """Aguarda carregamento da pagina."""
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def esta_logado(self) -> bool:
        """Verifica se usuario esta logado."""
        return "/login" not in self.page.url

    def conteudo_pagina(self) -> str:
        """Retorna conteudo da pagina em lowercase."""
        return self.page.content().lower()


# =============================================================================
# PAGE OBJECTS DE AUTENTICACAO
# =============================================================================


class CadastroPage:
    """Page Object para a pagina de cadastro."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.url = f"{base_url}/cadastrar"

    def navegar(self) -> None:
        """Navega para a pagina de cadastro."""
        self.page.goto(self.url)

    def preencher_formulario(
        self,
        perfil: str,
        nome: str,
        email: str,
        senha: str,
        confirmar_senha: Optional[str] = None
    ) -> None:
        """
        Preenche o formulario de cadastro.

        Args:
            perfil: "Aluno" ou "Professor"
            nome: Nome completo
            email: E-mail
            senha: Senha
            confirmar_senha: Confirmacao de senha (usa senha se nao informado)
        """
        if confirmar_senha is None:
            confirmar_senha = senha

        # Selecionar perfil (radio button com estilo de botao Bootstrap)
        # Precisamos clicar no label pois o input esta escondido
        self.page.locator(f'label[for="perfil_{perfil}"]').click()

        # Preencher campos
        self.page.fill('input[name="nome"]', nome)
        self.page.fill('input[name="email"]', email)
        self.page.fill('input[name="senha"]', senha)
        self.page.fill('input[name="confirmar_senha"]', confirmar_senha)

    def submeter(self) -> None:
        """Submete o formulario."""
        self.page.get_by_role("button", name="Criar Conta").click()

    def cadastrar(
        self,
        perfil: str,
        nome: str,
        email: str,
        senha: str,
        confirmar_senha: Optional[str] = None
    ) -> None:
        """
        Realiza cadastro completo: preenche e submete.
        """
        self.preencher_formulario(perfil, nome, email, senha, confirmar_senha)
        self.submeter()

    def obter_mensagem_erro_campo(self, campo: str) -> Optional[str]:
        """
        Obtem mensagem de erro de um campo especifico.

        Args:
            campo: Nome do campo (nome, email, senha, confirmar_senha)

        Returns:
            Texto da mensagem de erro ou None
        """
        seletor = f'input[name="{campo}"] ~ .invalid-feedback'
        elemento = self.page.locator(seletor).first

        if elemento.is_visible():
            return elemento.text_content()
        return None

    def obter_mensagem_flash(self) -> Optional[str]:
        """
        Obtem mensagem flash (toast ou alert).

        Returns:
            Texto da mensagem ou None
        """
        toast = self.page.locator('.toast-body').first
        if toast.is_visible():
            return toast.text_content()

        alert = self.page.locator('.alert').first
        if alert.is_visible():
            return alert.text_content()

        return None

    def aguardar_navegacao_login(self, timeout: int = 5000) -> bool:
        """
        Aguarda redirecionamento para pagina de login.

        Args:
            timeout: Tempo maximo em ms

        Returns:
            True se redirecionou, False caso contrario
        """
        try:
            self.page.wait_for_url("**/login**", timeout=timeout)
            return True
        except Exception:
            return False


class LoginPage:
    """Page Object para a pagina de login."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.url = f"{base_url}/login"

    def navegar(self) -> None:
        """Navega para a pagina de login."""
        self.page.goto(self.url)

    def preencher_formulario(self, email: str, senha: str) -> None:
        """Preenche o formulario de login sem submeter."""
        self.page.wait_for_selector('input[name="email"]')
        self.page.fill('input[name="email"]', email)
        self.page.fill('input[name="senha"]', senha)

    def submeter(self) -> None:
        """Submete o formulario de login."""
        self.page.locator('form button[type="submit"]').first.click()

    def fazer_login(self, email: str, senha: str) -> None:
        """Preenche e submete formulario de login."""
        self.preencher_formulario(email, senha)
        self.submeter()

    def esta_na_pagina_login(self) -> bool:
        """Verifica se esta na pagina de login."""
        return "/login" in self.page.url

    def aguardar_navegacao_usuario(self, timeout: int = 10000) -> bool:
        """
        Aguarda redirecionamento para area do usuario.

        Args:
            timeout: Tempo maximo em ms

        Returns:
            True se redirecionou, False caso contrario
        """
        try:
            self.page.wait_for_url("**/usuario**", timeout=timeout)
            return True
        except Exception:
            # Pode ter ido para /home
            return "/usuario" in self.page.url or "/home" in self.page.url

    def obter_mensagem_flash(self) -> Optional[str]:
        """
        Obtem mensagem flash (toast ou alert).

        Returns:
            Texto da mensagem ou None
        """
        toast = self.page.locator('.toast-body').first
        if toast.is_visible():
            return toast.text_content()

        alert = self.page.locator('.alert').first
        if alert.is_visible():
            return alert.text_content()

        return None


def verificar_mensagem_sucesso_cadastro(page: Page) -> bool:
    """
    Verifica se a mensagem de sucesso do cadastro foi exibida.

    A mensagem esperada e: "Cadastro realizado com sucesso!"
    """
    try:
        toast = page.locator('.toast-body')
        if toast.is_visible():
            texto = toast.text_content() or ""
            return "cadastro realizado com sucesso" in texto.lower()

        alert = page.locator('.alert-success')
        if alert.is_visible():
            texto = alert.text_content() or ""
            return "cadastro realizado com sucesso" in texto.lower()
    except Exception:
        pass

    return False


def verificar_erro_email_duplicado(page: Page) -> bool:
    """
    Verifica se apareceu erro de e-mail duplicado.

    A mensagem esperada contem: "e-mail ja esta cadastrado"
    """
    try:
        conteudo = page.content().lower()
        return "e-mail" in conteudo and "cadastrado" in conteudo
    except Exception:
        return False


def verificar_erro_senhas_diferentes(page: Page) -> bool:
    """
    Verifica se apareceu erro de senhas nao coincidentes.

    A mensagem esperada: "As senhas nao coincidem."
    """
    try:
        conteudo = page.content().lower()
        return "senhas" in conteudo and "coincidem" in conteudo
    except Exception:
        return False


# =============================================================================
# PAGE OBJECTS PARA PAGINAS PUBLICAS
# =============================================================================


class HomePage(BasePage):
    """Page Object para a pagina inicial."""

    def navegar(self) -> None:
        """Navega para a pagina inicial."""
        self.page.goto(f"{self.base_url}/")

    def esta_na_pagina_inicial(self) -> bool:
        """Verifica se esta na pagina inicial."""
        return self.page.url == f"{self.base_url}/" or self.page.url.endswith("/index")


class SobrePage(BasePage):
    """Page Object para a pagina sobre."""

    def navegar(self) -> None:
        """Navega para a pagina sobre."""
        self.page.goto(f"{self.base_url}/sobre")

    def esta_na_pagina_sobre(self) -> bool:
        """Verifica se esta na pagina sobre."""
        return "/sobre" in self.page.url


class RecuperarSenhaPage(BasePage):
    """Page Object para a pagina de recuperacao de senha."""

    def navegar(self) -> None:
        """Navega para a pagina de recuperacao de senha."""
        self.page.goto(f"{self.base_url}/recuperar-senha")

    def solicitar_recuperacao(self, email: str) -> None:
        """Solicita recuperacao de senha."""
        self.page.fill('input[name="email"]', email)
        self.page.locator('button[type="submit"]').click()

    def esta_na_pagina_recuperacao(self) -> bool:
        """Verifica se esta na pagina de recuperacao."""
        return "/recuperar-senha" in self.page.url


# =============================================================================
# PAGE OBJECTS PARA AREA DO USUARIO
# =============================================================================


class DashboardPage(BasePage):
    """Page Object para o dashboard do usuario."""

    def navegar(self) -> None:
        """Navega para o dashboard."""
        self.page.goto(f"{self.base_url}/usuario")

    def esta_no_dashboard(self) -> bool:
        """Verifica se esta no dashboard."""
        return "/usuario" in self.page.url and "/perfil" not in self.page.url


class PerfilPage(BasePage):
    """Page Object para paginas de perfil."""

    def navegar_visualizar(self) -> None:
        """Navega para visualizar perfil."""
        self.page.goto(f"{self.base_url}/usuario/perfil/visualizar")

    def navegar_editar(self) -> None:
        """Navega para editar perfil."""
        self.page.goto(f"{self.base_url}/usuario/perfil/editar")

    def navegar_alterar_senha(self) -> None:
        """Navega para alterar senha."""
        self.page.goto(f"{self.base_url}/usuario/perfil/alterar-senha")

    def editar_perfil(self, nome: str, email: str) -> None:
        """Edita dados do perfil."""
        self.page.fill('input[name="nome"]', nome)
        self.page.fill('input[name="email"]', email)
        self.page.locator('button[type="submit"]').click()

    def alterar_senha(self, senha_atual: str, senha_nova: str, confirmar: str) -> None:
        """Altera senha do usuario."""
        self.page.fill('input[name="senha_atual"]', senha_atual)
        self.page.fill('input[name="senha_nova"]', senha_nova)
        self.page.fill('input[name="confirmar_senha"]', confirmar)
        self.page.locator('button[type="submit"]').click()


# =============================================================================
# PAGE OBJECTS PARA CHAMADOS
# =============================================================================


class ChamadosPage(BasePage):
    """Page Object para gerenciamento de chamados."""

    def navegar_listar(self) -> None:
        """Navega para lista de chamados."""
        self.page.goto(f"{self.base_url}/chamados/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de chamado."""
        self.page.goto(f"{self.base_url}/chamados/cadastrar")

    def criar_chamado(self, titulo: str, descricao: str, prioridade: str = "Media") -> None:
        """Cria um novo chamado."""
        self.page.fill('input[name="titulo"]', titulo)
        self.page.fill('textarea[name="descricao"]', descricao)
        self.page.select_option('select[name="prioridade"]', prioridade)
        self.page.locator('button[type="submit"]').click()

    def visualizar_chamado(self, chamado_id: int) -> None:
        """Visualiza detalhes de um chamado."""
        self.page.goto(f"{self.base_url}/chamados/{chamado_id}/visualizar")

    def responder_chamado(self, chamado_id: int, mensagem: str) -> None:
        """Responde a um chamado."""
        self.page.goto(f"{self.base_url}/chamados/{chamado_id}/visualizar")
        self.page.fill('textarea[name="mensagem"]', mensagem)
        self.page.locator('button[type="submit"]').click()


# =============================================================================
# PAGE OBJECTS PARA ADMIN
# =============================================================================


class AdminUsuariosPage(BasePage):
    """Page Object para gerenciamento de usuarios (Admin)."""

    def navegar_listar(self) -> None:
        """Navega para lista de usuarios."""
        self.page.goto(f"{self.base_url}/admin/usuarios/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de usuario."""
        self.page.goto(f"{self.base_url}/admin/usuarios/cadastrar")

    def cadastrar_usuario(
        self, nome: str, email: str, senha: str, perfil: str,
        data_nascimento: str = "", documento: str = "", telefone: str = ""
    ) -> None:
        """Cadastra um novo usuario."""
        self.page.fill('input[name="nome"]', nome)
        self.page.fill('input[name="email"]', email)
        self.page.fill('input[name="senha"]', senha)
        self.page.select_option('select[name="perfil"]', perfil)
        if data_nascimento:
            self.page.fill('input[name="data_nascimento"]', data_nascimento)
        if documento:
            self.page.fill('input[name="numero_documento"]', documento)
        if telefone:
            self.page.fill('input[name="telefone"]', telefone)
        self.page.locator('button[type="submit"]').click()

    def editar_usuario(self, usuario_id: int) -> None:
        """Navega para edicao de usuario."""
        self.page.goto(f"{self.base_url}/admin/usuarios/editar/{usuario_id}")


class AdminCategoriasPage(BasePage):
    """Page Object para gerenciamento de categorias (Admin)."""

    def navegar_listar(self) -> None:
        """Navega para lista de categorias."""
        self.page.goto(f"{self.base_url}/admin/categorias/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de categoria."""
        self.page.goto(f"{self.base_url}/admin/categorias/cadastrar")

    def cadastrar_categoria(self, nome: str, descricao: str = "") -> None:
        """Cadastra uma nova categoria."""
        self.page.fill('input[name="nome"]', nome)
        if descricao:
            self.page.fill('textarea[name="descricao"]', descricao)
        self.page.locator('button[type="submit"]').click()

    def editar_categoria(self, categoria_id: int) -> None:
        """Navega para edicao de categoria."""
        self.page.goto(f"{self.base_url}/admin/categorias/editar/{categoria_id}")


class AdminAtividadesPage(BasePage):
    """Page Object para gerenciamento de atividades (Admin)."""

    def navegar_listar(self) -> None:
        """Navega para lista de atividades."""
        self.page.goto(f"{self.base_url}/admin/atividades/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de atividade."""
        self.page.goto(f"{self.base_url}/admin/atividades/cadastrar")

    def cadastrar_atividade(self, nome: str, descricao: str = "", id_categoria: str = "") -> None:
        """Cadastra uma nova atividade."""
        self.page.fill('input[name="nome"]', nome)
        if descricao:
            self.page.fill('textarea[name="descricao"]', descricao)
        if id_categoria:
            self.page.select_option('select[name="id_categoria"]', id_categoria)
        self.page.locator('button[type="submit"]').click()


class AdminTurmasPage(BasePage):
    """Page Object para gerenciamento de turmas (Admin)."""

    def navegar_listar(self) -> None:
        """Navega para lista de turmas."""
        self.page.goto(f"{self.base_url}/admin/turmas/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de turma."""
        self.page.goto(f"{self.base_url}/admin/turmas/cadastrar")

    def cadastrar_turma(
        self, nome: str, id_atividade: str, id_professor: str,
        horario_inicio: str, horario_fim: str, dias_semana: str, vagas: str
    ) -> None:
        """Cadastra uma nova turma."""
        self.page.fill('input[name="nome"]', nome)
        self.page.select_option('select[name="id_atividade"]', id_atividade)
        self.page.select_option('select[name="id_professor"]', id_professor)
        self.page.fill('input[name="horario_inicio"]', horario_inicio)
        self.page.fill('input[name="horario_fim"]', horario_fim)
        self.page.fill('input[name="dias_semana"]', dias_semana)
        self.page.fill('input[name="vagas"]', vagas)
        self.page.locator('button[type="submit"]').click()


class AdminMatriculasPage(BasePage):
    """Page Object para gerenciamento de matriculas (Admin)."""

    def navegar_listar(self) -> None:
        """Navega para lista de matriculas."""
        self.page.goto(f"{self.base_url}/admin/matriculas/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de matricula."""
        self.page.goto(f"{self.base_url}/admin/matriculas/cadastrar")

    def cadastrar_matricula(
        self, id_aluno: str, id_turma: str, valor_mensalidade: str, dia_vencimento: str
    ) -> None:
        """Cadastra uma nova matricula."""
        self.page.select_option('select[name="id_aluno"]', id_aluno)
        self.page.select_option('select[name="id_turma"]', id_turma)
        self.page.fill('input[name="valor_mensalidade"]', valor_mensalidade)
        self.page.fill('input[name="dia_vencimento"]', dia_vencimento)
        self.page.locator('button[type="submit"]').click()


class AdminPagamentosPage(BasePage):
    """Page Object para gerenciamento de pagamentos (Admin)."""

    def navegar_listar(self) -> None:
        """Navega para lista de pagamentos."""
        self.page.goto(f"{self.base_url}/admin/pagamentos/listar")

    def navegar_cadastrar(self) -> None:
        """Navega para cadastro de pagamento."""
        self.page.goto(f"{self.base_url}/admin/pagamentos/cadastrar")

    def cadastrar_pagamento(self, id_matricula: str, valor_pago: str) -> None:
        """Cadastra um novo pagamento."""
        self.page.select_option('select[name="id_matricula"]', id_matricula)
        self.page.fill('input[name="valor_pago"]', valor_pago)
        self.page.locator('button[type="submit"]').click()


class AdminConfiguracoesPage(BasePage):
    """Page Object para gerenciamento de configuracoes (Admin)."""

    def navegar(self) -> None:
        """Navega para pagina de configuracoes."""
        self.page.goto(f"{self.base_url}/admin/configuracoes")

    def esta_na_pagina_configuracoes(self) -> bool:
        """Verifica se esta na pagina de configuracoes."""
        return "/admin/configuracoes" in self.page.url


class AdminTemaPage(BasePage):
    """Page Object para gerenciamento de temas (Admin)."""

    def navegar(self) -> None:
        """Navega para pagina de temas."""
        self.page.goto(f"{self.base_url}/admin/tema")

    def aplicar_tema(self, tema: str) -> None:
        """Aplica um tema."""
        self.page.click(f'[data-tema="{tema}"]')
        self.page.locator('button[type="submit"]').click()

    def esta_na_pagina_temas(self) -> bool:
        """Verifica se esta na pagina de temas."""
        return "/admin/tema" in self.page.url


class AdminBackupsPage(BasePage):
    """Page Object para gerenciamento de backups (Admin)."""

    def navegar_listar(self) -> None:
        """Navega para lista de backups."""
        self.page.goto(f"{self.base_url}/admin/backups/listar")

    def criar_backup(self) -> None:
        """Cria um novo backup."""
        self.page.locator('button:has-text("Criar Backup")').click()

    def esta_na_pagina_backups(self) -> bool:
        """Verifica se esta na pagina de backups."""
        return "/admin/backups" in self.page.url


class AdminAuditoriaPage(BasePage):
    """Page Object para pagina de auditoria/logs (Admin)."""

    def navegar(self) -> None:
        """Navega para pagina de auditoria."""
        self.page.goto(f"{self.base_url}/admin/auditoria")

    def filtrar_logs(self, data: str, nivel: str) -> None:
        """Filtra logs por data e nivel."""
        self.page.fill('input[name="data"]', data)
        self.page.select_option('select[name="nivel"]', nivel)
        self.page.locator('button[type="submit"]').click()

    def esta_na_pagina_auditoria(self) -> bool:
        """Verifica se esta na pagina de auditoria."""
        return "/admin/auditoria" in self.page.url


class AdminChamadosPage(BasePage):
    """Page Object para gerenciamento de chamados (Admin)."""

    def navegar_listar(self) -> None:
        """Navega para lista de chamados."""
        self.page.goto(f"{self.base_url}/admin/chamados/listar")

    def responder_chamado(self, chamado_id: int, mensagem: str, status: str) -> None:
        """Responde a um chamado."""
        self.page.goto(f"{self.base_url}/admin/chamados/{chamado_id}/responder")
        self.page.fill('textarea[name="mensagem"]', mensagem)
        self.page.select_option('select[name="status_chamado"]', status)
        self.page.locator('button[type="submit"]').click()

    def fechar_chamado(self, chamado_id: int) -> None:
        """Fecha um chamado."""
        self.page.goto(f"{self.base_url}/admin/chamados/{chamado_id}/responder")
        self.page.locator('button:has-text("Fechar")').click()


# =============================================================================
# PAGE OBJECTS PARA PROFESSOR
# =============================================================================


class ProfessorTurmasPage(BasePage):
    """Page Object para turmas do professor."""

    def navegar_minhas_turmas(self) -> None:
        """Navega para minhas turmas."""
        self.page.goto(f"{self.base_url}/usuario/minhas-turmas")

    def visualizar_alunos(self, turma_id: int) -> None:
        """Visualiza alunos de uma turma."""
        self.page.goto(f"{self.base_url}/usuario/turma/{turma_id}/alunos")


# =============================================================================
# PAGE OBJECTS PARA ALUNO
# =============================================================================


class AlunoMatriculasPage(BasePage):
    """Page Object para matriculas do aluno."""

    def navegar_minhas_matriculas(self) -> None:
        """Navega para minhas matriculas."""
        self.page.goto(f"{self.base_url}/usuario/minhas-matriculas")


class AlunoPagamentosPage(BasePage):
    """Page Object para pagamentos do aluno."""

    def navegar_meus_pagamentos(self) -> None:
        """Navega para meus pagamentos."""
        self.page.goto(f"{self.base_url}/usuario/meus-pagamentos")


# =============================================================================
# FUNCOES AUXILIARES
# =============================================================================


def criar_usuario_e_logar(
    page: Page, base_url: str, perfil: str, nome: str, email: str, senha: str
) -> None:
    """
    Cria um usuario via cadastro e faz login.

    Args:
        page: Pagina Playwright
        base_url: URL base do servidor
        perfil: Perfil do usuario (Aluno, Professor, Admin)
        nome: Nome completo
        email: E-mail
        senha: Senha
    """
    # Cadastrar usuario
    cadastro = CadastroPage(page, base_url)
    cadastro.navegar()
    cadastro.cadastrar(perfil=perfil, nome=nome, email=email, senha=senha)
    cadastro.aguardar_navegacao_login()

    # Fazer login
    login = LoginPage(page, base_url)
    login.fazer_login(email, senha)
    login.aguardar_navegacao_usuario()


def criar_admin_e_logar(page: Page, base_url: str, nome: str, email: str, senha: str) -> None:
    """
    Cria um admin via cadastro e faz login.
    Nota: No sistema real, admin pode precisar ser criado de outra forma.
    """
    criar_usuario_e_logar(page, base_url, "Administrador", nome, email, senha)
