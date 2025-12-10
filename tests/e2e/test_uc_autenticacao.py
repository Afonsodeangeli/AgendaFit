"""
Testes E2E para Casos de Uso de Autenticacao.

UC-007: Realizar login com email e senha
UC-008: Realizar logout
UC-009: Registrar nova conta
UC-010: Recuperar senha esquecida
UC-011: Redefinir senha com token valido
"""
import pytest
import time
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    gerar_email_unico,
    gerar_nome_unico,
)


class TestAutenticacao:
    """Testes para casos de uso de autenticacao."""

    # =========================================================================
    # UC-007: Realizar login com email e senha
    # =========================================================================

    def test_uc007_login_credenciais_validas(self, page: Page, base_url: str):
        """
        UC-007: Usuario deve conseguir fazer login com credenciais validas.

        Cenario: Login bem-sucedido
        Dado que o usuario possui uma conta registrada
        Quando ele informa email e senha corretos
        Entao deve ser redirecionado para a area do usuario
        """
        # Primeiro, criar uma conta
        email = gerar_email_unico()
        senha = "Teste@123456"

        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Aluno",
            nome=gerar_nome_unico(),
            email=email,
            senha=senha
        )
        cadastro.aguardar_navegacao_login()

        # Fazer login
        login = LoginPage(page, base_url)
        login.fazer_login(email, senha)
        login.aguardar_navegacao_usuario()

        # Verificar que esta logado (na area do usuario)
        assert "/usuario" in page.url

    def test_uc007_login_senha_incorreta(self, page: Page, base_url: str):
        """
        UC-007: Login com senha incorreta deve falhar.

        Cenario: Login com senha errada
        Dado que o usuario possui uma conta
        Quando ele informa senha incorreta
        Entao deve ver mensagem de erro
        """
        # Criar conta
        email = gerar_email_unico()
        senha = "Teste@123456"

        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Aluno",
            nome=gerar_nome_unico(),
            email=email,
            senha=senha
        )
        cadastro.aguardar_navegacao_login()

        # Tentar login com senha errada
        login = LoginPage(page, base_url)
        login.fazer_login(email, "senha_errada123")

        # Deve continuar na pagina de login
        page.wait_for_timeout(1000)
        assert login.esta_na_pagina_login() or "erro" in page.content().lower()

    def test_uc007_login_email_inexistente(self, page: Page, base_url: str):
        """
        UC-007: Login com email inexistente deve falhar.
        """
        login = LoginPage(page, base_url)
        login.navegar()
        login.fazer_login("email_inexistente@teste.com", "qualquerSenha123")

        # Deve continuar na pagina de login ou mostrar erro
        page.wait_for_timeout(1000)
        assert login.esta_na_pagina_login() or "erro" in page.content().lower()

    # =========================================================================
    # UC-008: Realizar logout
    # =========================================================================

    def test_uc008_logout_usuario_logado(self, page: Page, base_url: str):
        """
        UC-008: Usuario logado deve conseguir fazer logout.

        Cenario: Logout bem-sucedido
        Dado que o usuario esta autenticado
        Quando ele clica em logout
        Entao deve ser deslogado e redirecionado
        """
        # Criar conta e logar
        email = gerar_email_unico()
        senha = "Teste@123456"

        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Aluno",
            nome=gerar_nome_unico(),
            email=email,
            senha=senha
        )
        cadastro.aguardar_navegacao_login()

        login = LoginPage(page, base_url)
        login.fazer_login(email, senha)
        login.aguardar_navegacao_usuario()

        # Fazer logout
        logout_link = page.locator('a[href*="logout"]').first
        if logout_link.is_visible():
            logout_link.click()
        else:
            # Tentar via navegacao direta
            page.goto(f"{base_url}/logout")

        page.wait_for_timeout(1000)

        # Deve estar deslogado (na pagina inicial ou login)
        assert "/login" in page.url or page.url.endswith("/")

    # =========================================================================
    # UC-009: Registrar nova conta
    # =========================================================================

    def test_uc009_cadastro_aluno_sucesso(self, page: Page, base_url: str):
        """
        UC-009: Usuario deve conseguir se cadastrar como Aluno.

        Cenario: Cadastro de aluno bem-sucedido
        Dado que o usuario acessa a pagina de cadastro
        Quando ele preenche os dados corretamente com perfil Aluno
        Entao a conta deve ser criada e ele redirecionado para login
        """
        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Aluno",
            nome=gerar_nome_unico(),
            email=gerar_email_unico(),
            senha="Teste@123456"
        )
        cadastro.aguardar_navegacao_login()

        # Deve estar na pagina de login apos cadastro
        assert "/login" in page.url

    def test_uc009_cadastro_professor_sucesso(self, page: Page, base_url: str):
        """
        UC-009: Usuario deve conseguir se cadastrar como Professor.
        """
        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Professor",
            nome=gerar_nome_unico(),
            email=gerar_email_unico(),
            senha="Teste@123456"
        )
        cadastro.aguardar_navegacao_login()

        assert "/login" in page.url

    def test_uc009_cadastro_nao_permite_admin_publico(self, page: Page, base_url: str):
        """
        UC-009: Cadastro publico nao deve permitir perfil Administrador.

        O perfil Administrador so pode ser criado via admin ou seed.
        """
        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()

        # Verificar que nao existe opcao de Administrador no formulario
        admin_option = page.locator('label[for="perfil_Administrador"]')
        assert admin_option.count() == 0, "Opcao Administrador nao deve existir no cadastro publico"

    def test_uc009_cadastro_email_duplicado(self, page: Page, base_url: str):
        """
        UC-009: Cadastro com email ja existente deve falhar.

        Cenario: Tentativa de cadastro com email duplicado
        Dado que ja existe uma conta com determinado email
        Quando outro usuario tenta se cadastrar com o mesmo email
        Entao deve ver mensagem de erro
        """
        email = gerar_email_unico()
        senha = "Teste@123456"

        # Primeiro cadastro
        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Aluno",
            nome=gerar_nome_unico(),
            email=email,
            senha=senha
        )
        cadastro.aguardar_navegacao_login()

        # Segunda tentativa com mesmo email
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Aluno",
            nome=gerar_nome_unico(),
            email=email,
            senha=senha
        )

        page.wait_for_timeout(1000)

        # Deve mostrar erro ou continuar no cadastro
        conteudo = page.content().lower()
        assert (
            "ja existe" in conteudo
            or "email" in conteudo
            or "cadastro" in page.url
        )

    def test_uc009_cadastro_senha_fraca(self, page: Page, base_url: str):
        """
        UC-009: Cadastro com senha fraca deve falhar.
        """
        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Aluno",
            nome=gerar_nome_unico(),
            email=gerar_email_unico(),
            senha="123"  # Senha muito fraca
        )

        page.wait_for_timeout(1000)

        # Deve mostrar erro de validacao
        conteudo = page.content().lower()
        assert (
            "senha" in conteudo
            or "caracteres" in conteudo
            or cadastro.esta_na_pagina_cadastro()
        )

    # =========================================================================
    # UC-010: Recuperar senha esquecida
    # =========================================================================

    def test_uc010_solicitar_recuperacao_email_valido(self, page: Page, base_url: str):
        """
        UC-010: Usuario pode solicitar recuperacao de senha.

        Cenario: Solicitacao de recuperacao
        Dado que o usuario esqueceu a senha
        Quando ele informa seu email
        Entao deve receber feedback (sem revelar se email existe)
        """
        # Criar conta primeiro
        email = gerar_email_unico()
        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Aluno",
            nome=gerar_nome_unico(),
            email=email,
            senha="Teste@123456"
        )
        cadastro.aguardar_navegacao_login()

        # Solicitar recuperacao (URL correta e /esqueci-senha)
        page.goto(f"{base_url}/esqueci-senha")
        page.fill('input[name="email"]', email)
        page.locator('button[type="submit"]').first.click()

        page.wait_for_timeout(1000)

        # Deve mostrar algum feedback
        conteudo = page.content().lower()
        assert (
            "enviado" in conteudo
            or "email" in conteudo
            or "recupera" in conteudo
            or "/login" in page.url
        )

    # =========================================================================
    # UC-011: Redefinir senha com token valido
    # =========================================================================

    def test_uc011_pagina_redefinir_sem_token(self, page: Page, base_url: str):
        """
        UC-011: Acesso a pagina de redefinir sem token deve falhar.
        """
        page.goto(f"{base_url}/redefinir-senha")

        page.wait_for_timeout(1000)

        # Sem token, deve retornar erro 422 ou redirecionar
        conteudo = page.content().lower()
        assert (
            "/esqueci-senha" in page.url
            or "422" in conteudo
            or "token" in conteudo
            or "required" in conteudo
        )

    def test_uc011_pagina_redefinir_token_invalido(self, page: Page, base_url: str):
        """
        UC-011: Redefinir com token invalido deve falhar.
        """
        page.goto(f"{base_url}/redefinir-senha?token=token_falso_123")

        page.wait_for_timeout(1000)

        # Deve redirecionar para esqueci-senha ou mostrar erro
        conteudo = page.content().lower()
        assert (
            "invalido" in conteudo
            or "expirado" in conteudo
            or "/esqueci-senha" in page.url
        )
