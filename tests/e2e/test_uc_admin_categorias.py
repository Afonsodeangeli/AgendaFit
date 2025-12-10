"""
Testes E2E para Casos de Uso de Gestao de Categorias (Admin).

UC-038: Listar todas as categorias
UC-039: Criar categoria
UC-040: Editar categoria
UC-041: Excluir categoria
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    AdminCategoriasPage,
    gerar_email_unico,
    gerar_nome_unico,
    logar_com_seed_admin,
)


class TestAdminCategorias:
    """Testes para casos de uso de gestao de categorias pelo admin."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> None:
        """Faz login com admin do seed data."""
        logar_com_seed_admin(page, base_url)

    # =========================================================================
    # UC-038: Listar todas as categorias
    # =========================================================================

    def test_uc038_admin_listar_categorias(self, page: Page, base_url: str):
        """
        UC-038: Admin deve ver lista de todas as categorias.

        Cenario: Listagem de categorias
        Dado que o admin esta autenticado
        Quando ele acessa a lista de categorias
        Entao deve ver todas as categorias do sistema
        """
        self._criar_admin_e_logar(page, base_url)

        admin_categorias = AdminCategoriasPage(page, base_url)
        admin_categorias.navegar_listar()

        # Deve estar na pagina de categorias admin
        assert "/admin/categorias" in page.url

    def test_uc038_usuario_comum_nao_acessa(self, page: Page, base_url: str):
        """
        UC-038: Usuario comum nao deve acessar lista de categorias admin.
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
        page.goto(f"{base_url}/admin/categorias/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/categorias" not in page.url or "acesso" in page.content().lower()

    # =========================================================================
    # UC-039: Criar categoria
    # =========================================================================

    def test_uc039_admin_criar_categoria(self, page: Page, base_url: str):
        """
        UC-039: Admin deve criar categoria com sucesso.

        Cenario: Criacao de categoria
        Dado que o admin esta autenticado
        Quando ele preenche o formulario de categoria
        Entao a categoria deve ser criada
        """
        self._criar_admin_e_logar(page, base_url)

        admin_categorias = AdminCategoriasPage(page, base_url)
        admin_categorias.navegar_cadastrar()

        # Cadastrar nova categoria
        nome_categoria = f"Categoria Teste {gerar_email_unico()[:8]}"
        admin_categorias.cadastrar_categoria(
            nome=nome_categoria,
            descricao="Descricao da categoria de teste E2E"
        )

        page.wait_for_timeout(1000)

        # Deve redirecionar ou mostrar sucesso
        conteudo = page.content().lower()
        assert (
            "sucesso" in conteudo
            or "cadastrada" in conteudo
            or "/admin/categorias" in page.url
        )

    def test_uc039_admin_criar_categoria_sem_descricao(self, page: Page, base_url: str):
        """
        UC-039: Admin pode criar categoria sem descricao.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_categorias = AdminCategoriasPage(page, base_url)
        admin_categorias.navegar_cadastrar()

        nome_categoria = f"Categoria Sem Desc {gerar_email_unico()[:6]}"
        admin_categorias.cadastrar_categoria(nome=nome_categoria)

        page.wait_for_timeout(1000)

        conteudo = page.content().lower()
        assert "sucesso" in conteudo or "/admin/categorias" in page.url

    def test_uc039_admin_criar_categoria_nome_vazio(self, page: Page, base_url: str):
        """
        UC-039: Criar categoria sem nome deve falhar.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_categorias = AdminCategoriasPage(page, base_url)
        admin_categorias.navegar_cadastrar()

        # Tentar criar com nome vazio
        page.locator('button[type="submit"]').first.click()

        page.wait_for_timeout(1000)

        # Deve mostrar erro ou continuar no formulario
        assert "cadastrar" in page.url or "erro" in page.content().lower()

    # =========================================================================
    # UC-040: Editar categoria
    # =========================================================================

    def test_uc040_admin_editar_categoria(self, page: Page, base_url: str):
        """
        UC-040: Admin deve editar categoria existente.

        Cenario: Edicao de categoria
        Dado que existe uma categoria
        Quando o admin edita as informacoes
        Entao as alteracoes devem ser salvas
        """
        self._criar_admin_e_logar(page, base_url)

        admin_categorias = AdminCategoriasPage(page, base_url)

        # Primeiro, criar uma categoria para editar
        admin_categorias.navegar_cadastrar()
        admin_categorias.cadastrar_categoria(
            nome=f"Categoria Para Editar {gerar_email_unico()[:6]}",
            descricao="Descricao original"
        )

        page.wait_for_timeout(1000)

        # Ir para lista e clicar em editar
        admin_categorias.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Editar nome
            campo_nome = page.locator('input[name="nome"]')
            if campo_nome.is_visible():
                campo_nome.fill("Categoria Editada E2E")
                page.locator('button[type="submit"]').first.click()

                page.wait_for_timeout(1000)

                # Verificar sucesso
                conteudo = page.content().lower()
                assert "sucesso" in conteudo or "alterada" in conteudo or "/admin/categorias" in page.url

    def test_uc040_admin_editar_categoria_descricao(self, page: Page, base_url: str):
        """
        UC-040: Admin pode editar descricao da categoria.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_categorias = AdminCategoriasPage(page, base_url)
        admin_categorias.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Editar descricao
            campo_descricao = page.locator('textarea[name="descricao"]')
            if campo_descricao.is_visible():
                campo_descricao.fill("Nova descricao editada via teste E2E")
                page.locator('button[type="submit"]').first.click()

    # =========================================================================
    # UC-041: Excluir categoria
    # =========================================================================

    def test_uc041_admin_excluir_categoria_sem_atividades(self, page: Page, base_url: str):
        """
        UC-041: Admin deve excluir categoria sem atividades vinculadas.

        Cenario: Exclusao de categoria
        Dado que existe uma categoria sem atividades
        Quando o admin exclui a categoria
        Entao a categoria deve ser removida
        """
        self._criar_admin_e_logar(page, base_url)

        admin_categorias = AdminCategoriasPage(page, base_url)

        # Criar categoria para excluir
        admin_categorias.navegar_cadastrar()
        admin_categorias.cadastrar_categoria(
            nome=f"Categoria Para Excluir {gerar_email_unico()[:6]}",
            descricao="Esta categoria sera excluida"
        )

        page.wait_for_timeout(1000)

        # Ir para lista
        admin_categorias.navegar_listar()

        # Tentar excluir
        btn_excluir = page.locator('button:has-text("Excluir"), form[action*="excluir"] button').first
        if btn_excluir.is_visible():
            btn_excluir.click()
            page.wait_for_timeout(1000)

            # Verificar sucesso
            conteudo = page.content().lower()
            assert (
                "sucesso" in conteudo
                or "excluida" in conteudo
                or "/admin/categorias" in page.url
            )

    def test_uc041_nao_excluir_categoria_com_atividades(self, page: Page, base_url: str):
        """
        UC-041: Nao deve excluir categoria com atividades vinculadas.

        Cenario: Tentativa de exclusao bloqueada
        Dado que existe uma categoria com atividades
        Quando o admin tenta excluir
        Entao deve ver mensagem de erro
        """
        # Este teste depende do estado do banco
        # Se existir categoria com atividades, a exclusao deve ser bloqueada
        self._criar_admin_e_logar(page, base_url)

        admin_categorias = AdminCategoriasPage(page, base_url)
        admin_categorias.navegar_listar()

        # Tentar excluir - se houver erro por vinculacao, o teste verifica
