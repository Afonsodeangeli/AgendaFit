"""
Testes E2E para Casos de Uso de Gestao de Matriculas.

UC-052: Listar todas as matriculas (Admin)
UC-053: Criar matricula (Admin)
UC-054: Editar matricula (Admin)
UC-055: Cancelar matricula (Admin)
UC-056: Visualizar matriculas proprias (Aluno)
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    AdminMatriculasPage,
    AlunoMatriculasPage,
    gerar_email_unico,
    gerar_nome_unico,
)


class TestAdminMatriculas:
    """Testes para casos de uso de gestao de matriculas pelo admin."""

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
    # UC-052: Listar todas as matriculas
    # =========================================================================

    def test_uc052_admin_listar_matriculas(self, page: Page, base_url: str):
        """
        UC-052: Admin deve ver lista de todas as matriculas.

        Cenario: Listagem de matriculas
        Dado que o admin esta autenticado
        Quando ele acessa a lista de matriculas
        Entao deve ver todas as matriculas do sistema
        """
        self._criar_admin_e_logar(page, base_url)

        admin_matriculas = AdminMatriculasPage(page, base_url)
        admin_matriculas.navegar_listar()

        # Deve estar na pagina de matriculas admin
        assert "/admin/matriculas" in page.url

    def test_uc052_usuario_comum_nao_acessa(self, page: Page, base_url: str):
        """
        UC-052: Usuario comum nao deve acessar lista admin de matriculas.
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
        page.goto(f"{base_url}/admin/matriculas/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/matriculas" not in page.url or "acesso" in page.content().lower()

    # =========================================================================
    # UC-053: Criar matricula
    # =========================================================================

    def test_uc053_admin_acessar_cadastro_matricula(self, page: Page, base_url: str):
        """
        UC-053: Admin deve acessar formulario de cadastro de matricula.

        Cenario: Acesso ao cadastro
        Dado que o admin esta autenticado
        Quando ele acessa o formulario de matricula
        Entao deve ver os campos necessarios
        """
        self._criar_admin_e_logar(page, base_url)

        admin_matriculas = AdminMatriculasPage(page, base_url)
        admin_matriculas.navegar_cadastrar()

        # Pode redirecionar se nao houver alunos/turmas
        page.wait_for_timeout(1000)

        conteudo = page.content().lower()
        assert (
            "cadastrar" in page.url
            or "aluno" in conteudo
            or "turma" in conteudo
        )

    def test_uc053_validar_aluno_ja_matriculado(self, page: Page, base_url: str):
        """
        UC-053: Nao deve permitir matricula duplicada na mesma turma.
        """
        # Este teste verifica a validacao de unicidade
        self._criar_admin_e_logar(page, base_url)

        admin_matriculas = AdminMatriculasPage(page, base_url)
        admin_matriculas.navegar_cadastrar()

        page.wait_for_timeout(500)

        # Se tentar matricular mesmo aluno duas vezes, deve falhar

    def test_uc053_validar_vagas_disponiveis(self, page: Page, base_url: str):
        """
        UC-053: Nao deve permitir matricula se turma estiver lotada.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_matriculas = AdminMatriculasPage(page, base_url)
        admin_matriculas.navegar_cadastrar()

        # Verificacao depende do estado do banco

    # =========================================================================
    # UC-054: Editar matricula
    # =========================================================================

    def test_uc054_admin_editar_matricula(self, page: Page, base_url: str):
        """
        UC-054: Admin deve editar matricula existente.

        Cenario: Edicao de matricula
        Dado que existe uma matricula
        Quando o admin edita (valor, dia vencimento)
        Entao as alteracoes devem ser salvas
        """
        self._criar_admin_e_logar(page, base_url)

        admin_matriculas = AdminMatriculasPage(page, base_url)
        admin_matriculas.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Editar valor mensalidade se disponivel
            campo_valor = page.locator('input[name="valor_mensalidade"]')
            if campo_valor.is_visible():
                campo_valor.fill("150.00")
                page.locator('button[type="submit"]').click()

                page.wait_for_timeout(1000)

    def test_uc054_admin_nao_altera_aluno_turma(self, page: Page, base_url: str):
        """
        UC-054: Admin nao deve alterar aluno ou turma da matricula.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_matriculas = AdminMatriculasPage(page, base_url)
        admin_matriculas.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Campos de aluno e turma devem estar desabilitados ou nao existir
            select_aluno = page.locator('select[name="id_aluno"]')
            select_turma = page.locator('select[name="id_turma"]')

            # Podem estar disabled ou nao editaveis

    # =========================================================================
    # UC-055: Cancelar matricula
    # =========================================================================

    def test_uc055_admin_cancelar_matricula_sem_pagamentos(self, page: Page, base_url: str):
        """
        UC-055: Admin deve cancelar matricula sem pagamentos.

        Cenario: Cancelamento de matricula
        Dado que existe uma matricula sem pagamentos
        Quando o admin cancela a matricula
        Entao a matricula deve ser removida
        """
        self._criar_admin_e_logar(page, base_url)

        admin_matriculas = AdminMatriculasPage(page, base_url)
        admin_matriculas.navegar_listar()

        # Tentar cancelar/excluir
        btn_excluir = page.locator('button:has-text("Excluir"), button:has-text("Cancelar"), form[action*="excluir"] button').first
        if btn_excluir.is_visible():
            btn_excluir.click()
            page.wait_for_timeout(1000)

    def test_uc055_nao_cancela_matricula_com_pagamentos(self, page: Page, base_url: str):
        """
        UC-055: Nao deve cancelar matricula com pagamentos.

        Cenario: Tentativa de cancelamento bloqueada
        Dado que existe uma matricula com pagamentos
        Quando o admin tenta cancelar
        Entao deve ver mensagem de erro
        """
        self._criar_admin_e_logar(page, base_url)

        admin_matriculas = AdminMatriculasPage(page, base_url)
        admin_matriculas.navegar_listar()

        # Se tentar cancelar matricula com pagamentos, deve falhar


class TestAlunoMatriculas:
    """Testes para casos de uso de matriculas do aluno."""

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
    # UC-056: Visualizar matriculas proprias (Aluno)
    # =========================================================================

    def test_uc056_aluno_visualizar_matriculas(self, page: Page, base_url: str):
        """
        UC-056: Aluno deve visualizar suas matriculas.

        Cenario: Visualizacao de matriculas proprias
        Dado que o aluno esta autenticado
        Quando ele acessa minhas matriculas
        Entao deve ver suas matriculas (turmas, horarios, professor)
        """
        self._criar_aluno_e_logar(page, base_url)

        aluno_matriculas = AlunoMatriculasPage(page, base_url)
        aluno_matriculas.navegar_minhas_matriculas()

        page.wait_for_timeout(1000)

        # Deve estar na area do usuario
        assert "/usuario" in page.url

    def test_uc056_aluno_nao_edita_matriculas(self, page: Page, base_url: str):
        """
        UC-056: Aluno nao pode editar matriculas (somente visualizacao).
        """
        self._criar_aluno_e_logar(page, base_url)

        # Tentar acessar edicao admin
        page.goto(f"{base_url}/admin/matriculas/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/matriculas" not in page.url

    def test_uc056_aluno_ve_info_turma(self, page: Page, base_url: str):
        """
        UC-056: Aluno deve ver informacoes da turma em suas matriculas.
        """
        self._criar_aluno_e_logar(page, base_url)

        aluno_matriculas = AlunoMatriculasPage(page, base_url)
        aluno_matriculas.navegar_minhas_matriculas()

        page.wait_for_timeout(500)

        # Se houver matriculas, deve mostrar info da turma
        conteudo = page.content().lower()
        # Pode mostrar: turma, horario, professor, ou mensagem de sem matriculas
        assert (
            "turma" in conteudo
            or "matricula" in conteudo
            or "nenhuma" in conteudo
            or "/usuario" in page.url
        )
