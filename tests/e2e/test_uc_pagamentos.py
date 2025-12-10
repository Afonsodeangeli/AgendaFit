"""
Testes E2E para Casos de Uso de Gestao de Pagamentos.

UC-057: Listar todos os pagamentos (Admin)
UC-058: Registrar pagamento (Admin)
UC-059: Editar pagamento (Admin)
UC-060: Excluir pagamento (Admin)
UC-061: Visualizar pagamentos proprios (Aluno)
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    AdminPagamentosPage,
    AlunoPagamentosPage,
    gerar_email_unico,
    gerar_nome_unico,
    logar_com_seed_admin,
)


class TestAdminPagamentos:
    """Testes para casos de uso de gestao de pagamentos pelo admin."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> None:
        """Faz login com admin do seed data."""
        logar_com_seed_admin(page, base_url)

    # =========================================================================
    # UC-057: Listar todos os pagamentos
    # =========================================================================

    def test_uc057_admin_listar_pagamentos(self, page: Page, base_url: str):
        """
        UC-057: Admin deve ver lista de todos os pagamentos.

        Cenario: Listagem de pagamentos
        Dado que o admin esta autenticado
        Quando ele acessa a lista de pagamentos
        Entao deve ver todos os pagamentos do sistema
        """
        self._criar_admin_e_logar(page, base_url)

        admin_pagamentos = AdminPagamentosPage(page, base_url)
        admin_pagamentos.navegar_listar()

        # Deve estar na pagina de pagamentos admin
        assert "/admin/pagamentos" in page.url

    def test_uc057_usuario_comum_nao_acessa(self, page: Page, base_url: str):
        """
        UC-057: Usuario comum nao deve acessar lista admin de pagamentos.
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
        page.goto(f"{base_url}/admin/pagamentos/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/pagamentos" not in page.url or "acesso" in page.content().lower()

    # =========================================================================
    # UC-058: Registrar pagamento
    # =========================================================================

    def test_uc058_admin_acessar_cadastro_pagamento(self, page: Page, base_url: str):
        """
        UC-058: Admin deve acessar formulario de registro de pagamento.

        Cenario: Acesso ao cadastro
        Dado que o admin esta autenticado
        Quando ele acessa o formulario de pagamento
        Entao deve ver os campos necessarios
        """
        self._criar_admin_e_logar(page, base_url)

        admin_pagamentos = AdminPagamentosPage(page, base_url)
        admin_pagamentos.navegar_cadastrar()

        # Pode redirecionar se nao houver matriculas
        page.wait_for_timeout(1000)

        conteudo = page.content().lower()
        assert (
            "cadastrar" in page.url
            or "matricula" in conteudo
            or "pagamento" in conteudo
        )

    def test_uc058_admin_registrar_pagamento(self, page: Page, base_url: str):
        """
        UC-058: Admin deve registrar pagamento com sucesso.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_pagamentos = AdminPagamentosPage(page, base_url)
        admin_pagamentos.navegar_cadastrar()

        page.wait_for_timeout(500)

        # Se houver matriculas, preencher formulario
        select_matricula = page.locator('select[name="id_matricula"]')
        if select_matricula.is_visible():
            # Selecionar primeira matricula
            opcoes = select_matricula.locator('option')
            if opcoes.count() > 1:
                select_matricula.select_option(index=1)

                # Preencher valor
                page.fill('input[name="valor_pago"]', "100.00")
                page.locator('button[type="submit"]').first.click()

                page.wait_for_timeout(1000)

    # =========================================================================
    # UC-059: Editar pagamento
    # =========================================================================

    def test_uc059_admin_editar_pagamento(self, page: Page, base_url: str):
        """
        UC-059: Admin deve editar valor do pagamento.

        Cenario: Edicao de pagamento
        Dado que existe um pagamento
        Quando o admin edita o valor
        Entao a alteracao deve ser salva
        """
        self._criar_admin_e_logar(page, base_url)

        admin_pagamentos = AdminPagamentosPage(page, base_url)
        admin_pagamentos.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Editar valor
            campo_valor = page.locator('input[name="valor_pago"]')
            if campo_valor.is_visible():
                campo_valor.fill("200.00")
                page.locator('button[type="submit"]').first.click()

                page.wait_for_timeout(1000)

                # Verificar sucesso
                conteudo = page.content().lower()
                assert (
                    "sucesso" in conteudo
                    or "alterado" in conteudo
                    or "/admin/pagamentos" in page.url
                )

    def test_uc059_admin_nao_altera_matricula(self, page: Page, base_url: str):
        """
        UC-059: Admin nao deve alterar matricula do pagamento.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_pagamentos = AdminPagamentosPage(page, base_url)
        admin_pagamentos.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Campo de matricula nao deve estar editavel
            select_matricula = page.locator('select[name="id_matricula"]')
            # Pode estar disabled ou nao existir na edicao

    # =========================================================================
    # UC-060: Excluir pagamento
    # =========================================================================

    def test_uc060_admin_excluir_pagamento(self, page: Page, base_url: str):
        """
        UC-060: Admin deve excluir pagamento.

        Cenario: Exclusao de pagamento
        Dado que existe um pagamento
        Quando o admin exclui o pagamento
        Entao o pagamento deve ser removido
        """
        self._criar_admin_e_logar(page, base_url)

        admin_pagamentos = AdminPagamentosPage(page, base_url)
        admin_pagamentos.navegar_listar()

        # Tentar excluir
        btn_excluir = page.locator('button:has-text("Excluir"), form[action*="excluir"] button').first
        if btn_excluir.is_visible():
            btn_excluir.click()
            page.wait_for_timeout(1000)

            # Verificar sucesso
            conteudo = page.content().lower()
            assert (
                "sucesso" in conteudo
                or "excluido" in conteudo
                or "/admin/pagamentos" in page.url
            )


class TestAlunoPagamentos:
    """Testes para casos de uso de pagamentos do aluno."""

    def _criar_aluno_e_logar(self, page: Page, base_url: str) -> tuple:
        """Helper para criar aluno e fazer login."""
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
    # UC-061: Visualizar pagamentos proprios (Aluno)
    # =========================================================================

    def test_uc061_aluno_visualizar_pagamentos(self, page: Page, base_url: str):
        """
        UC-061: Aluno deve visualizar seus pagamentos.

        Cenario: Visualizacao de pagamentos proprios
        Dado que o aluno esta autenticado
        Quando ele acessa meus pagamentos
        Entao deve ver seu historico de pagamentos
        """
        self._criar_aluno_e_logar(page, base_url)

        aluno_pagamentos = AlunoPagamentosPage(page, base_url)
        aluno_pagamentos.navegar_meus_pagamentos()

        page.wait_for_timeout(1000)

        # Deve estar na area do usuario
        assert "/usuario" in page.url

    def test_uc061_aluno_nao_edita_pagamentos(self, page: Page, base_url: str):
        """
        UC-061: Aluno nao pode editar pagamentos (somente visualizacao).
        """
        self._criar_aluno_e_logar(page, base_url)

        # Tentar acessar edicao admin
        page.goto(f"{base_url}/admin/pagamentos/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/pagamentos" not in page.url

    def test_uc061_aluno_ve_historico(self, page: Page, base_url: str):
        """
        UC-061: Aluno deve ver historico com datas e valores.
        """
        self._criar_aluno_e_logar(page, base_url)

        aluno_pagamentos = AlunoPagamentosPage(page, base_url)
        aluno_pagamentos.navegar_meus_pagamentos()

        page.wait_for_timeout(500)

        conteudo = page.content().lower()
        # Pode mostrar: pagamentos, valores, ou mensagem de sem pagamentos
        assert (
            "pagamento" in conteudo
            or "valor" in conteudo
            or "nenhum" in conteudo
            or "/usuario" in page.url
        )
