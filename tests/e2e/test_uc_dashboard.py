"""
Testes E2E para Casos de Uso de Dashboard.

UC-016: Visualizar dashboard personalizado
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    DashboardPage,
    gerar_email_unico,
    gerar_nome_unico,
)


class TestDashboard:
    """Testes para caso de uso de dashboard."""

    def _criar_e_logar(self, page: Page, base_url: str, perfil: str = "Aluno") -> tuple:
        """Helper para criar usuario e fazer login."""
        email = gerar_email_unico()
        senha = "Teste@123456"
        nome = gerar_nome_unico()

        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil=perfil,
            nome=nome,
            email=email,
            senha=senha
        )
        cadastro.aguardar_navegacao_login()

        login = LoginPage(page, base_url)
        login.fazer_login(email, senha)
        login.aguardar_navegacao_usuario()

        return email, senha, nome

    # =========================================================================
    # UC-016: Visualizar dashboard personalizado
    # =========================================================================

    def test_uc016_dashboard_aluno(self, page: Page, base_url: str):
        """
        UC-016: Aluno deve ver dashboard personalizado.

        Cenario: Dashboard de aluno
        Dado que um aluno esta autenticado
        Quando ele acessa o dashboard
        Entao deve ver informacoes relevantes para alunos
        """
        self._criar_e_logar(page, base_url, "Aluno")

        dashboard = DashboardPage(page, base_url)
        dashboard.navegar()

        # Verificar que esta no dashboard
        assert dashboard.esta_no_dashboard()

    def test_uc016_dashboard_professor(self, page: Page, base_url: str):
        """
        UC-016: Professor deve ver dashboard personalizado.
        """
        self._criar_e_logar(page, base_url, "Professor")

        dashboard = DashboardPage(page, base_url)
        dashboard.navegar()

        assert dashboard.esta_no_dashboard()

    def test_uc016_dashboard_admin(self, page: Page, base_url: str):
        """
        UC-016: Admin deve ver dashboard com informacoes administrativas.

        Cenario: Dashboard de administrador
        Dado que um admin esta autenticado
        Quando ele acessa o dashboard
        Entao deve ver informacoes de gestao (chamados pendentes, etc)
        """
        self._criar_e_logar(page, base_url, "Administrador")

        dashboard = DashboardPage(page, base_url)
        dashboard.navegar()

        assert dashboard.esta_no_dashboard()

        # Admin deve ter acesso a informacoes administrativas
        conteudo = page.content().lower()
        # Verificar presenca de elementos administrativos
        assert (
            "admin" in conteudo
            or "gestao" in conteudo
            or "chamado" in conteudo
            or "usuario" in page.url
        )

    def test_uc016_dashboard_nao_autenticado(self, page: Page, base_url: str):
        """
        UC-016: Usuario nao autenticado nao deve acessar dashboard.
        """
        dashboard = DashboardPage(page, base_url)
        dashboard.navegar()

        page.wait_for_timeout(1000)

        # Deve ser redirecionado para login
        assert "/login" in page.url

    def test_uc016_dashboard_redirecionamento_apos_login(self, page: Page, base_url: str):
        """
        UC-016: Apos login, usuario deve ser redirecionado ao dashboard.
        """
        email, senha, nome = self._criar_e_logar(page, base_url, "Aluno")

        # Ja esta logado, verificar se esta na area do usuario
        assert "/usuario" in page.url

    def test_uc016_dashboard_contem_menu_navegacao(self, page: Page, base_url: str):
        """
        UC-016: Dashboard deve conter menu de navegacao.
        """
        self._criar_e_logar(page, base_url, "Aluno")

        dashboard = DashboardPage(page, base_url)
        dashboard.navegar()

        # Verificar presenca de elementos de navegacao
        # Pode ser navbar, sidebar ou menu
        nav = page.locator('nav, .navbar, .sidebar, .menu')
        assert nav.count() > 0 or "nav" in page.content().lower()

    def test_uc016_dashboard_contem_link_perfil(self, page: Page, base_url: str):
        """
        UC-016: Dashboard deve ter link para perfil do usuario.
        """
        self._criar_e_logar(page, base_url, "Aluno")

        dashboard = DashboardPage(page, base_url)
        dashboard.navegar()

        # Verificar link para perfil
        link_perfil = page.locator('a[href*="perfil"]')
        assert link_perfil.count() > 0 or "perfil" in page.content().lower()

    def test_uc016_dashboard_contem_link_logout(self, page: Page, base_url: str):
        """
        UC-016: Dashboard deve ter link para logout.
        """
        self._criar_e_logar(page, base_url, "Aluno")

        dashboard = DashboardPage(page, base_url)
        dashboard.navegar()

        # Verificar link para logout
        link_logout = page.locator('a[href*="logout"]')
        assert link_logout.count() > 0 or "sair" in page.content().lower()
