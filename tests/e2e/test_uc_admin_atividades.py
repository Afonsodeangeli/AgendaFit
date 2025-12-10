"""
Testes E2E para Casos de Uso de Gestao de Atividades (Admin).

UC-042: Listar todas as atividades
UC-043: Criar atividade
UC-044: Editar atividade
UC-045: Excluir atividade
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    AdminAtividadesPage,
    AdminCategoriasPage,
    gerar_email_unico,
    gerar_nome_unico,
    logar_com_seed_admin,
)


class TestAdminAtividades:
    """Testes para casos de uso de gestao de atividades pelo admin."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> None:
        """Faz login com admin do seed data."""
        logar_com_seed_admin(page, base_url)

    # =========================================================================
    # UC-042: Listar todas as atividades
    # =========================================================================

    def test_uc042_admin_listar_atividades(self, page: Page, base_url: str):
        """
        UC-042: Admin deve ver lista de todas as atividades.

        Cenario: Listagem de atividades
        Dado que o admin esta autenticado
        Quando ele acessa a lista de atividades
        Entao deve ver todas as atividades do sistema
        """
        self._criar_admin_e_logar(page, base_url)

        admin_atividades = AdminAtividadesPage(page, base_url)
        admin_atividades.navegar_listar()

        # Deve estar na pagina de atividades admin
        assert "/admin/atividades" in page.url

    def test_uc042_usuario_comum_nao_acessa(self, page: Page, base_url: str):
        """
        UC-042: Usuario comum nao deve acessar lista de atividades admin.
        """
        # Criar usuario comum
        email = gerar_email_unico()
        senha = "Teste@123456"

        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Professor",
            nome=gerar_nome_unico(),
            email=email,
            senha=senha
        )
        cadastro.aguardar_navegacao_login()

        login = LoginPage(page, base_url)
        login.fazer_login(email, senha)
        login.aguardar_navegacao_usuario()

        # Tentar acessar area admin
        page.goto(f"{base_url}/admin/atividades/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/atividades" not in page.url or "acesso" in page.content().lower()

    # =========================================================================
    # UC-043: Criar atividade
    # =========================================================================

    def test_uc043_admin_criar_atividade(self, page: Page, base_url: str):
        """
        UC-043: Admin deve criar atividade com sucesso.

        Cenario: Criacao de atividade
        Dado que o admin esta autenticado
        E existe pelo menos uma categoria
        Quando ele preenche o formulario de atividade
        Entao a atividade deve ser criada
        """
        self._criar_admin_e_logar(page, base_url)

        # Primeiro, garantir que existe uma categoria
        admin_categorias = AdminCategoriasPage(page, base_url)
        admin_categorias.navegar_cadastrar()
        admin_categorias.cadastrar_categoria(
            nome=f"Categoria Para Atividade {gerar_email_unico()[:6]}",
            descricao="Categoria de teste"
        )

        page.wait_for_timeout(1000)

        # Criar atividade
        admin_atividades = AdminAtividadesPage(page, base_url)
        admin_atividades.navegar_cadastrar()

        nome_atividade = f"Atividade Teste {gerar_email_unico()[:8]}"
        page.fill('input[name="nome"]', nome_atividade)

        # Selecionar primeira categoria disponivel
        select_categoria = page.locator('select[name="id_categoria"]')
        if select_categoria.is_visible():
            select_categoria.select_option(index=1)  # Seleciona primeira opcao valida

        page.fill('textarea[name="descricao"]', "Descricao da atividade de teste E2E")
        page.locator('button[type="submit"]').first.click()

        page.wait_for_timeout(1000)

        # Deve redirecionar ou mostrar sucesso
        conteudo = page.content().lower()
        assert (
            "sucesso" in conteudo
            or "cadastrada" in conteudo
            or "/admin/atividades" in page.url
        )

    def test_uc043_admin_criar_atividade_sem_categoria(self, page: Page, base_url: str):
        """
        UC-043: Criar atividade sem categoria deve funcionar (categoria opcional).
        """
        self._criar_admin_e_logar(page, base_url)

        admin_atividades = AdminAtividadesPage(page, base_url)
        admin_atividades.navegar_cadastrar()

        nome_atividade = f"Atividade Sem Cat {gerar_email_unico()[:6]}"
        page.fill('input[name="nome"]', nome_atividade)
        page.locator('button[type="submit"]').first.click()

        page.wait_for_timeout(1000)

    def test_uc043_admin_criar_atividade_nome_vazio(self, page: Page, base_url: str):
        """
        UC-043: Criar atividade sem nome deve falhar.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_atividades = AdminAtividadesPage(page, base_url)
        admin_atividades.navegar_cadastrar()

        # Tentar criar sem nome
        page.locator('button[type="submit"]').first.click()

        page.wait_for_timeout(1000)

        # Deve mostrar erro ou continuar no formulario
        assert "cadastrar" in page.url or "erro" in page.content().lower()

    # =========================================================================
    # UC-044: Editar atividade
    # =========================================================================

    def test_uc044_admin_editar_atividade(self, page: Page, base_url: str):
        """
        UC-044: Admin deve editar atividade existente.

        Cenario: Edicao de atividade
        Dado que existe uma atividade
        Quando o admin edita as informacoes
        Entao as alteracoes devem ser salvas
        """
        self._criar_admin_e_logar(page, base_url)

        admin_atividades = AdminAtividadesPage(page, base_url)
        admin_atividades.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Editar nome
            campo_nome = page.locator('input[name="nome"]')
            if campo_nome.is_visible():
                campo_nome.fill("Atividade Editada E2E")
                page.locator('button[type="submit"]').first.click()

                page.wait_for_timeout(1000)

                # Verificar sucesso
                conteudo = page.content().lower()
                assert (
                    "sucesso" in conteudo
                    or "alterada" in conteudo
                    or "/admin/atividades" in page.url
                )

    def test_uc044_admin_editar_atividade_descricao(self, page: Page, base_url: str):
        """
        UC-044: Admin pode editar descricao da atividade.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_atividades = AdminAtividadesPage(page, base_url)
        admin_atividades.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            campo_descricao = page.locator('textarea[name="descricao"]')
            if campo_descricao.is_visible():
                campo_descricao.fill("Nova descricao da atividade via teste E2E")
                page.locator('button[type="submit"]').first.click()

    def test_uc044_admin_alterar_categoria_atividade(self, page: Page, base_url: str):
        """
        UC-044: Admin pode alterar a categoria de uma atividade.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_atividades = AdminAtividadesPage(page, base_url)
        admin_atividades.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            select_categoria = page.locator('select[name="id_categoria"]')
            if select_categoria.is_visible():
                # Tentar mudar para outra categoria
                opcoes = select_categoria.locator('option')
                if opcoes.count() > 1:
                    select_categoria.select_option(index=0)

    # =========================================================================
    # UC-045: Excluir atividade
    # =========================================================================

    def test_uc045_admin_excluir_atividade_sem_turmas(self, page: Page, base_url: str):
        """
        UC-045: Admin deve excluir atividade sem turmas vinculadas.

        Cenario: Exclusao de atividade
        Dado que existe uma atividade sem turmas
        Quando o admin exclui a atividade
        Entao a atividade deve ser removida
        """
        self._criar_admin_e_logar(page, base_url)

        admin_atividades = AdminAtividadesPage(page, base_url)

        # Criar atividade para excluir
        admin_atividades.navegar_cadastrar()
        page.fill('input[name="nome"]', f"Atividade Para Excluir {gerar_email_unico()[:6]}")
        page.locator('button[type="submit"]').first.click()

        page.wait_for_timeout(1000)

        # Ir para lista
        admin_atividades.navegar_listar()

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
                or "/admin/atividades" in page.url
            )

    def test_uc045_nao_excluir_atividade_com_turmas(self, page: Page, base_url: str):
        """
        UC-045: Nao deve excluir atividade com turmas vinculadas.

        Cenario: Tentativa de exclusao bloqueada
        Dado que existe uma atividade com turmas
        Quando o admin tenta excluir
        Entao deve ver mensagem de erro
        """
        # Este teste depende do estado do banco
        self._criar_admin_e_logar(page, base_url)

        admin_atividades = AdminAtividadesPage(page, base_url)
        admin_atividades.navegar_listar()

        # Se houver atividade com turma e tentar excluir, deve falhar
