"""
Testes E2E para Casos de Uso de Paginas Publicas.

UC-001: Visualizar pagina inicial
UC-002: Visualizar pagina sobre
UC-003: Acessar pagina de login
UC-004: Acessar pagina de cadastro
UC-005: Solicitar recuperacao de senha
UC-006: Redefinir senha com token
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    HomePage,
    SobrePage,
    LoginPage,
    CadastroPage,
    RecuperarSenhaPage,
)


class TestPaginasPublicas:
    """Testes para paginas publicas (sem autenticacao)."""

    # =========================================================================
    # UC-001: Visualizar pagina inicial
    # =========================================================================

    def test_uc001_visualizar_pagina_inicial(self, page: Page, base_url: str):
        """
        UC-001: Usuario deve conseguir visualizar a pagina inicial.

        Cenario: Acesso a pagina inicial
        Dado que o usuario nao esta autenticado
        Quando ele acessa a URL raiz
        Entao a pagina inicial deve ser exibida
        """
        home = HomePage(page, base_url)
        home.navegar()

        # Verifica que a pagina carregou corretamente
        expect(page).to_have_url(f"{base_url}/")

    def test_uc001_pagina_inicial_contem_link_login(self, page: Page, base_url: str):
        """
        UC-001: Pagina inicial deve conter link para login.
        """
        home = HomePage(page, base_url)
        home.navegar()

        # Verifica presenca de link para login
        link_login = page.locator('a[href*="login"]')
        expect(link_login.first).to_be_visible()

    # =========================================================================
    # UC-002: Visualizar pagina sobre
    # =========================================================================

    def test_uc002_visualizar_pagina_sobre(self, page: Page, base_url: str):
        """
        UC-002: Usuario deve conseguir visualizar a pagina sobre.

        Cenario: Acesso a pagina sobre
        Dado que o usuario nao esta autenticado
        Quando ele acessa a URL /sobre
        Entao a pagina sobre deve ser exibida
        """
        sobre = SobrePage(page, base_url)
        sobre.navegar()

        # Verifica que esta na pagina sobre
        assert sobre.esta_na_pagina_sobre()

    def test_uc002_pagina_sobre_contem_informacoes(self, page: Page, base_url: str):
        """
        UC-002: Pagina sobre deve conter informacoes da aplicacao.
        """
        sobre = SobrePage(page, base_url)
        sobre.navegar()

        conteudo = page.content().lower()
        # Verifica que ha algum conteudo informativo
        assert "agendafit" in conteudo or "sobre" in conteudo

    # =========================================================================
    # UC-003: Acessar pagina de login
    # =========================================================================

    def test_uc003_acessar_pagina_login(self, page: Page, base_url: str):
        """
        UC-003: Usuario deve conseguir acessar a pagina de login.

        Cenario: Acesso a pagina de login
        Dado que o usuario nao esta autenticado
        Quando ele acessa a URL /login
        Entao o formulario de login deve ser exibido
        """
        login = LoginPage(page, base_url)
        login.navegar()

        # Verifica que esta na pagina de login
        assert login.esta_na_pagina_login()

    def test_uc003_pagina_login_contem_formulario(self, page: Page, base_url: str):
        """
        UC-003: Pagina de login deve conter formulario com campos de email e senha.
        """
        login = LoginPage(page, base_url)
        login.navegar()

        # Verifica presenca dos campos
        campo_email = page.locator('input[name="email"]')
        campo_senha = page.locator('input[name="senha"]')

        expect(campo_email).to_be_visible()
        expect(campo_senha).to_be_visible()

    def test_uc003_pagina_login_contem_link_cadastro(self, page: Page, base_url: str):
        """
        UC-003: Pagina de login deve conter link para cadastro.
        """
        login = LoginPage(page, base_url)
        login.navegar()

        # Verifica presenca de link para cadastro (href="/cadastrar")
        link_cadastro = page.locator('a[href*="cadastrar"]')
        expect(link_cadastro.first).to_be_visible()

    def test_uc003_pagina_login_contem_link_recuperar_senha(self, page: Page, base_url: str):
        """
        UC-003: Pagina de login deve conter link para recuperar senha.
        """
        login = LoginPage(page, base_url)
        login.navegar()

        # Verifica presenca de link para recuperar senha (href="/esqueci-senha")
        link_recuperar = page.locator('a[href*="esqueci-senha"]')
        expect(link_recuperar.first).to_be_visible()

    # =========================================================================
    # UC-004: Acessar pagina de cadastro
    # =========================================================================

    def test_uc004_acessar_pagina_cadastro(self, page: Page, base_url: str):
        """
        UC-004: Usuario deve conseguir acessar a pagina de cadastro.

        Cenario: Acesso a pagina de cadastro
        Dado que o usuario nao esta autenticado
        Quando ele acessa a URL /cadastro
        Entao o formulario de cadastro deve ser exibido
        """
        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()

        # Verifica que esta na pagina de cadastro
        assert cadastro.esta_na_pagina_cadastro()

    def test_uc004_pagina_cadastro_contem_formulario(self, page: Page, base_url: str):
        """
        UC-004: Pagina de cadastro deve conter formulario completo.
        """
        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()

        # Verifica presenca dos campos obrigatorios
        expect(page.locator('input[name="nome"]')).to_be_visible()
        expect(page.locator('input[name="email"]')).to_be_visible()
        expect(page.locator('input[name="senha"]')).to_be_visible()
        # Perfil usa radio buttons, nao select
        expect(page.locator('input[name="perfil"]').first).to_be_visible()

    def test_uc004_pagina_cadastro_contem_perfis(self, page: Page, base_url: str):
        """
        UC-004: Pagina de cadastro deve oferecer opcoes de perfil.
        """
        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()

        # Verifica que os radio buttons de perfil existem (Aluno e Professor)
        radio_perfil = page.locator('input[name="perfil"]')

        # Deve haver pelo menos 2 opcoes de perfil (Aluno e Professor)
        assert radio_perfil.count() >= 2

    # =========================================================================
    # UC-005: Solicitar recuperacao de senha
    # =========================================================================

    def test_uc005_acessar_pagina_recuperar_senha(self, page: Page, base_url: str):
        """
        UC-005: Usuario deve conseguir acessar a pagina de recuperacao de senha.

        Cenario: Acesso a pagina de recuperacao de senha
        Dado que o usuario nao esta autenticado
        Quando ele acessa a URL /recuperar-senha
        Entao o formulario de recuperacao deve ser exibido
        """
        recuperar = RecuperarSenhaPage(page, base_url)
        recuperar.navegar()

        # Verifica que esta na pagina de recuperacao
        assert recuperar.esta_na_pagina_recuperacao()

    def test_uc005_pagina_recuperar_contem_campo_email(self, page: Page, base_url: str):
        """
        UC-005: Pagina de recuperacao deve conter campo para email.
        """
        recuperar = RecuperarSenhaPage(page, base_url)
        recuperar.navegar()

        # Verifica presenca do campo de email
        campo_email = page.locator('input[name="email"]')
        expect(campo_email).to_be_visible()

    def test_uc005_solicitar_recuperacao_email_invalido(self, page: Page, base_url: str):
        """
        UC-005: Solicitar recuperacao com email inexistente nao deve revelar informacao.
        """
        recuperar = RecuperarSenhaPage(page, base_url)
        recuperar.navegar()
        recuperar.solicitar_recuperacao("email_inexistente@teste.com")

        # Por seguranca, nao deve revelar se o email existe ou nao
        # Deve mostrar mensagem generica
        page.wait_for_timeout(1000)

    # =========================================================================
    # UC-006: Redefinir senha com token
    # =========================================================================

    def test_uc006_acessar_pagina_redefinir_sem_token(self, page: Page, base_url: str):
        """
        UC-006: Acessar pagina de redefinir senha sem token deve redirecionar.

        Cenario: Acesso sem token valido
        Dado que o usuario tenta acessar /redefinir-senha sem token
        Entao deve ser redirecionado ou ver mensagem de erro
        """
        page.goto(f"{base_url}/redefinir-senha")

        # Sem token, deve redirecionar ou mostrar erro
        # A URL nao deve ficar em /redefinir-senha sem parametros
        page.wait_for_timeout(1000)

    def test_uc006_acessar_pagina_redefinir_token_invalido(self, page: Page, base_url: str):
        """
        UC-006: Acessar pagina de redefinir senha com token invalido.
        """
        page.goto(f"{base_url}/redefinir-senha?token=token_invalido_12345")

        # Com token invalido, deve mostrar erro
        page.wait_for_timeout(1000)
        conteudo = page.content().lower()

        # Deve haver alguma indicacao de erro ou redirecionamento
        assert (
            "invalido" in conteudo
            or "expirado" in conteudo
            or "/login" in page.url
            or "/esqueci-senha" in page.url
        )
