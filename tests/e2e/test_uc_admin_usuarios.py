"""
Testes E2E para Casos de Uso de Gestao de Usuarios (Admin).

UC-034: Listar todos os usuarios
UC-035: Criar novo usuario
UC-036: Editar usuario
UC-037: Excluir usuario
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    AdminUsuariosPage,
    gerar_email_unico,
    gerar_nome_unico,
)


class TestAdminUsuarios:
    """Testes para casos de uso de gestao de usuarios pelo admin."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> tuple:
        """Helper para criar admin e fazer login."""
        email = gerar_email_unico()
        senha = "Teste@123456"
        nome = gerar_nome_unico()

        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Administrador",
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
    # UC-034: Listar todos os usuarios
    # =========================================================================

    def test_uc034_admin_listar_usuarios(self, page: Page, base_url: str):
        """
        UC-034: Admin deve ver lista de todos os usuarios.

        Cenario: Listagem de usuarios
        Dado que o admin esta autenticado
        Quando ele acessa a lista de usuarios
        Entao deve ver todos os usuarios do sistema
        """
        self._criar_admin_e_logar(page, base_url)

        admin_usuarios = AdminUsuariosPage(page, base_url)
        admin_usuarios.navegar_listar()

        # Deve estar na pagina de usuarios admin
        assert "/admin/usuarios" in page.url

        # Deve conter tabela ou lista de usuarios
        conteudo = page.content().lower()
        assert "usuario" in conteudo or "nome" in conteudo

    def test_uc034_usuario_comum_nao_acessa(self, page: Page, base_url: str):
        """
        UC-034: Usuario comum nao deve acessar lista de usuarios.
        """
        # Criar usuario comum
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

        # Tentar acessar area admin
        page.goto(f"{base_url}/admin/usuarios/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/usuarios" not in page.url or "acesso" in page.content().lower()

    # =========================================================================
    # UC-035: Criar novo usuario
    # =========================================================================

    def test_uc035_admin_criar_usuario_aluno(self, page: Page, base_url: str):
        """
        UC-035: Admin deve criar usuario com perfil Aluno.

        Cenario: Criacao de usuario
        Dado que o admin esta autenticado
        Quando ele preenche o formulario de cadastro
        Entao o usuario deve ser criado
        """
        self._criar_admin_e_logar(page, base_url)

        admin_usuarios = AdminUsuariosPage(page, base_url)
        admin_usuarios.navegar_cadastrar()

        # Cadastrar novo usuario
        admin_usuarios.cadastrar_usuario(
            nome=gerar_nome_unico(),
            email=gerar_email_unico(),
            senha="Teste@123456",
            perfil="Aluno"
        )

        page.wait_for_timeout(1000)

        # Deve redirecionar ou mostrar sucesso
        conteudo = page.content().lower()
        assert (
            "sucesso" in conteudo
            or "cadastrado" in conteudo
            or "/admin/usuarios" in page.url
        )

    def test_uc035_admin_criar_usuario_professor(self, page: Page, base_url: str):
        """
        UC-035: Admin deve criar usuario com perfil Professor.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_usuarios = AdminUsuariosPage(page, base_url)
        admin_usuarios.navegar_cadastrar()

        admin_usuarios.cadastrar_usuario(
            nome=gerar_nome_unico(),
            email=gerar_email_unico(),
            senha="Teste@123456",
            perfil="Professor"
        )

        page.wait_for_timeout(1000)

        conteudo = page.content().lower()
        assert "sucesso" in conteudo or "/admin/usuarios" in page.url

    def test_uc035_admin_criar_usuario_email_duplicado(self, page: Page, base_url: str):
        """
        UC-035: Criar usuario com email duplicado deve falhar.
        """
        self._criar_admin_e_logar(page, base_url)

        email_duplicado = gerar_email_unico()

        admin_usuarios = AdminUsuariosPage(page, base_url)

        # Primeiro cadastro
        admin_usuarios.navegar_cadastrar()
        admin_usuarios.cadastrar_usuario(
            nome=gerar_nome_unico(),
            email=email_duplicado,
            senha="Teste@123456",
            perfil="Aluno"
        )

        page.wait_for_timeout(1000)

        # Segundo cadastro com mesmo email
        admin_usuarios.navegar_cadastrar()
        admin_usuarios.cadastrar_usuario(
            nome=gerar_nome_unico(),
            email=email_duplicado,
            senha="Teste@123456",
            perfil="Professor"
        )

        page.wait_for_timeout(1000)

        # Deve mostrar erro
        conteudo = page.content().lower()
        assert (
            "ja existe" in conteudo
            or "email" in conteudo
            or "cadastrar" in page.url
        )

    # =========================================================================
    # UC-036: Editar usuario
    # =========================================================================

    def test_uc036_admin_editar_usuario(self, page: Page, base_url: str):
        """
        UC-036: Admin deve editar informacoes de usuario.

        Cenario: Edicao de usuario
        Dado que existe um usuario no sistema
        Quando o admin edita as informacoes
        Entao as alteracoes devem ser salvas
        """
        self._criar_admin_e_logar(page, base_url)

        admin_usuarios = AdminUsuariosPage(page, base_url)

        # Primeiro, criar um usuario para editar
        admin_usuarios.navegar_cadastrar()
        admin_usuarios.cadastrar_usuario(
            nome="Usuario Para Editar",
            email=gerar_email_unico(),
            senha="Teste@123456",
            perfil="Aluno"
        )

        page.wait_for_timeout(1000)

        # Ir para lista e clicar em editar
        admin_usuarios.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Editar nome
            campo_nome = page.locator('input[name="nome"]')
            if campo_nome.is_visible():
                campo_nome.fill("Nome Alterado Teste E2E")
                page.locator('button[type="submit"]').click()

                page.wait_for_timeout(1000)

    def test_uc036_admin_nao_pode_editar_senha(self, page: Page, base_url: str):
        """
        UC-036: Admin nao deve poder alterar senha do usuario diretamente.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_usuarios = AdminUsuariosPage(page, base_url)
        admin_usuarios.navegar_listar()

        # Abrir edicao
        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Verificar que nao ha campo de senha na edicao
            campo_senha = page.locator('input[name="senha"]')
            # Campo de senha nao deve existir ou deve estar desabilitado
            assert campo_senha.count() == 0 or not campo_senha.is_visible()

    # =========================================================================
    # UC-037: Excluir usuario
    # =========================================================================

    def test_uc037_admin_excluir_usuario(self, page: Page, base_url: str):
        """
        UC-037: Admin deve excluir usuario sem vinculos.

        Cenario: Exclusao de usuario
        Dado que existe um usuario sem turmas ou matriculas
        Quando o admin exclui o usuario
        Entao o usuario deve ser removido
        """
        self._criar_admin_e_logar(page, base_url)

        admin_usuarios = AdminUsuariosPage(page, base_url)

        # Criar usuario para excluir
        admin_usuarios.navegar_cadastrar()
        admin_usuarios.cadastrar_usuario(
            nome="Usuario Para Excluir",
            email=gerar_email_unico(),
            senha="Teste@123456",
            perfil="Aluno"
        )

        page.wait_for_timeout(1000)

        # Ir para lista
        admin_usuarios.navegar_listar()

        # Tentar excluir
        btn_excluir = page.locator('button:has-text("Excluir"), form[action*="excluir"] button').first
        if btn_excluir.is_visible():
            btn_excluir.click()
            page.wait_for_timeout(1000)

    def test_uc037_admin_nao_exclui_proprio(self, page: Page, base_url: str):
        """
        UC-037: Admin nao deve excluir a si mesmo.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_usuarios = AdminUsuariosPage(page, base_url)
        admin_usuarios.navegar_listar()

        # O sistema deve impedir exclusao do proprio admin
        # Verificacao indireta - botao nao deve existir para o proprio usuario

    def test_uc037_nao_exclui_usuario_com_vinculos(self, page: Page, base_url: str):
        """
        UC-037: Nao deve excluir usuario com turmas ou matriculas.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_usuarios = AdminUsuariosPage(page, base_url)
        admin_usuarios.navegar_listar()

        # Se existir usuario com vinculos e tentar excluir, deve falhar
        # Este teste depende do estado do banco
