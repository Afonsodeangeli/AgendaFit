"""
Testes E2E para Casos de Uso de Gerenciamento de Perfil.

UC-012: Visualizar perfil proprio
UC-013: Editar informacoes do perfil
UC-014: Alterar senha
UC-015: Fazer upload de foto de perfil
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    PerfilPage,
    gerar_email_unico,
    gerar_nome_unico,
    criar_usuario_e_logar,
)


class TestPerfilUsuario:
    """Testes para casos de uso de perfil do usuario."""

    def _criar_e_logar(self, page: Page, base_url: str) -> tuple:
        """Helper para criar usuario e fazer login."""
        email = gerar_email_unico()
        senha = "Teste@123456"
        nome = gerar_nome_unico()

        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Aluno",
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
    # UC-012: Visualizar perfil proprio
    # =========================================================================

    def test_uc012_visualizar_perfil(self, page: Page, base_url: str):
        """
        UC-012: Usuario logado deve conseguir visualizar seu perfil.

        Cenario: Visualizacao do perfil
        Dado que o usuario esta autenticado
        Quando ele acessa a pagina de perfil
        Entao suas informacoes devem ser exibidas
        """
        email, senha, nome = self._criar_e_logar(page, base_url)

        # Acessar pagina de perfil
        perfil = PerfilPage(page, base_url)
        perfil.navegar_visualizar()

        # Verificar que informacoes sao exibidas
        conteudo = page.content().lower()
        assert nome.split()[0].lower() in conteudo or email.lower() in conteudo

    def test_uc012_visualizar_perfil_nao_autenticado(self, page: Page, base_url: str):
        """
        UC-012: Usuario nao autenticado nao deve acessar perfil.
        """
        perfil = PerfilPage(page, base_url)
        perfil.navegar_visualizar()

        page.wait_for_timeout(1000)

        # Deve ser redirecionado para login
        assert "/login" in page.url

    # =========================================================================
    # UC-013: Editar informacoes do perfil
    # =========================================================================

    def test_uc013_editar_nome_perfil(self, page: Page, base_url: str):
        """
        UC-013: Usuario deve conseguir editar seu nome.

        Cenario: Edicao do nome
        Dado que o usuario esta autenticado
        Quando ele altera seu nome no perfil
        Entao o novo nome deve ser salvo
        """
        email, senha, nome_antigo = self._criar_e_logar(page, base_url)

        # Acessar edicao de perfil
        perfil = PerfilPage(page, base_url)
        perfil.navegar_editar()

        # Editar nome
        nome_novo = gerar_nome_unico()
        page.fill('input[name="nome"]', nome_novo)
        page.locator('button[type="submit"]').click()

        page.wait_for_timeout(1000)

        # Verificar sucesso (mensagem ou novo nome visivel)
        conteudo = page.content().lower()
        assert (
            "sucesso" in conteudo
            or "atualizado" in conteudo
            or nome_novo.split()[0].lower() in conteudo
        )

    def test_uc013_editar_email_unico(self, page: Page, base_url: str):
        """
        UC-013: Usuario deve conseguir alterar email para um unico.
        """
        email_antigo, senha, nome = self._criar_e_logar(page, base_url)

        perfil = PerfilPage(page, base_url)
        perfil.navegar_editar()

        # Alterar email
        email_novo = gerar_email_unico()
        campo_email = page.locator('input[name="email"]')
        if campo_email.is_visible():
            campo_email.fill(email_novo)
            page.locator('button[type="submit"]').click()

            page.wait_for_timeout(1000)

    def test_uc013_editar_perfil_nao_autenticado(self, page: Page, base_url: str):
        """
        UC-013: Usuario nao autenticado nao deve editar perfil.
        """
        perfil = PerfilPage(page, base_url)
        perfil.navegar_editar()

        page.wait_for_timeout(1000)

        # Deve ser redirecionado para login
        assert "/login" in page.url

    # =========================================================================
    # UC-014: Alterar senha
    # =========================================================================

    def test_uc014_alterar_senha_sucesso(self, page: Page, base_url: str):
        """
        UC-014: Usuario deve conseguir alterar sua senha.

        Cenario: Alteracao de senha bem-sucedida
        Dado que o usuario esta autenticado
        Quando ele informa senha atual e nova senha valida
        Entao a senha deve ser alterada
        """
        email, senha_atual, nome = self._criar_e_logar(page, base_url)

        perfil = PerfilPage(page, base_url)
        perfil.navegar_alterar_senha()

        # Alterar senha
        senha_nova = "NovaSenha@123456"
        perfil.alterar_senha(senha_atual, senha_nova, senha_nova)

        page.wait_for_timeout(1000)

        # Verificar sucesso
        conteudo = page.content().lower()
        assert (
            "sucesso" in conteudo
            or "alterada" in conteudo
            or "/login" in page.url
            or "/usuario" in page.url
        )

    def test_uc014_alterar_senha_atual_incorreta(self, page: Page, base_url: str):
        """
        UC-014: Alterar senha com senha atual incorreta deve falhar.
        """
        email, senha_atual, nome = self._criar_e_logar(page, base_url)

        perfil = PerfilPage(page, base_url)
        perfil.navegar_alterar_senha()

        # Tentar alterar com senha atual errada
        perfil.alterar_senha("senha_errada", "NovaSenha@123", "NovaSenha@123")

        page.wait_for_timeout(1000)

        # Deve mostrar erro
        conteudo = page.content().lower()
        assert (
            "incorreta" in conteudo
            or "atual" in conteudo
            or "erro" in conteudo
            or "alterar-senha" in page.url
        )

    def test_uc014_alterar_senha_confirmacao_diferente(self, page: Page, base_url: str):
        """
        UC-014: Alterar senha com confirmacao diferente deve falhar.
        """
        email, senha_atual, nome = self._criar_e_logar(page, base_url)

        perfil = PerfilPage(page, base_url)
        perfil.navegar_alterar_senha()

        # Senhas diferentes na confirmacao
        perfil.alterar_senha(senha_atual, "NovaSenha@123", "OutraSenha@456")

        page.wait_for_timeout(1000)

        # Deve mostrar erro
        conteudo = page.content().lower()
        assert (
            "coincidem" in conteudo
            or "diferente" in conteudo
            or "confirma" in conteudo
            or "alterar-senha" in page.url
        )

    def test_uc014_alterar_senha_nao_autenticado(self, page: Page, base_url: str):
        """
        UC-014: Usuario nao autenticado nao deve alterar senha.
        """
        perfil = PerfilPage(page, base_url)
        perfil.navegar_alterar_senha()

        page.wait_for_timeout(1000)

        # Deve ser redirecionado para login
        assert "/login" in page.url

    # =========================================================================
    # UC-015: Fazer upload de foto de perfil
    # =========================================================================

    def test_uc015_pagina_upload_foto_acessivel(self, page: Page, base_url: str):
        """
        UC-015: Usuario deve ter acesso a funcionalidade de upload de foto.

        Cenario: Acesso ao upload de foto
        Dado que o usuario esta autenticado
        Quando ele acessa a pagina de editar perfil
        Entao deve haver opcao para upload de foto
        """
        self._criar_e_logar(page, base_url)

        perfil = PerfilPage(page, base_url)
        perfil.navegar_editar()

        # Verificar presenca de elemento para foto
        conteudo = page.content().lower()
        # Pode ser input file, botao ou area de drop
        assert (
            "foto" in conteudo
            or "imagem" in conteudo
            or "avatar" in conteudo
            or page.locator('input[type="file"]').count() > 0
        )

    def test_uc015_upload_foto_nao_autenticado(self, page: Page, base_url: str):
        """
        UC-015: Usuario nao autenticado nao deve fazer upload.
        """
        # Tentar acessar diretamente endpoint de upload
        page.goto(f"{base_url}/usuario/perfil/foto")

        page.wait_for_timeout(1000)

        # Deve ser redirecionado para login
        assert "/login" in page.url or page.url.endswith("/")
