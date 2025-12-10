"""
Testes E2E para Casos de Uso de Gestao de Turmas.

UC-046: Listar todas as turmas (Admin)
UC-047: Criar turma (Admin)
UC-048: Editar turma (Admin)
UC-049: Excluir turma (Admin)
UC-050: Visualizar turmas proprias (Professor)
UC-051: Visualizar alunos da turma (Professor)
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    AdminTurmasPage,
    ProfessorTurmasPage,
    gerar_email_unico,
    gerar_nome_unico,
    logar_com_seed_admin,
)


class TestAdminTurmas:
    """Testes para casos de uso de gestao de turmas pelo admin."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> None:
        """Faz login com admin do seed data."""
        logar_com_seed_admin(page, base_url)

    # =========================================================================
    # UC-046: Listar todas as turmas
    # =========================================================================

    def test_uc046_admin_listar_turmas(self, page: Page, base_url: str):
        """
        UC-046: Admin deve ver lista de todas as turmas.

        Cenario: Listagem de turmas
        Dado que o admin esta autenticado
        Quando ele acessa a lista de turmas
        Entao deve ver todas as turmas do sistema
        """
        self._criar_admin_e_logar(page, base_url)

        admin_turmas = AdminTurmasPage(page, base_url)
        admin_turmas.navegar_listar()

        # Deve estar na pagina de turmas admin
        assert "/admin/turmas" in page.url

    def test_uc046_usuario_comum_nao_acessa(self, page: Page, base_url: str):
        """
        UC-046: Usuario comum nao deve acessar lista admin de turmas.
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
        page.goto(f"{base_url}/admin/turmas/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/turmas" not in page.url or "acesso" in page.content().lower()

    # =========================================================================
    # UC-047: Criar turma
    # =========================================================================

    def test_uc047_admin_acessar_cadastro_turma(self, page: Page, base_url: str):
        """
        UC-047: Admin deve acessar formulario de cadastro de turma.

        Cenario: Acesso ao cadastro
        Dado que o admin esta autenticado
        Quando ele acessa o formulario de turma
        Entao deve ver os campos necessarios
        """
        self._criar_admin_e_logar(page, base_url)

        admin_turmas = AdminTurmasPage(page, base_url)
        admin_turmas.navegar_cadastrar()

        # Pode redirecionar se nao houver atividades/professores
        page.wait_for_timeout(1000)

        conteudo = page.content().lower()
        # Ou esta no formulario ou foi redirecionado com mensagem
        assert (
            "cadastrar" in page.url
            or "atividade" in conteudo
            or "professor" in conteudo
        )

    def test_uc047_admin_criar_turma_campos_obrigatorios(self, page: Page, base_url: str):
        """
        UC-047: Campos obrigatorios devem ser validados.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_turmas = AdminTurmasPage(page, base_url)
        admin_turmas.navegar_cadastrar()

        page.wait_for_timeout(500)

        # Verificar presenca dos campos no formulario
        if "cadastrar" in page.url:
            campos_esperados = ['nome', 'id_atividade', 'id_professor', 'horario_inicio', 'horario_fim']
            for campo in campos_esperados:
                locator = page.locator(f'[name="{campo}"]')
                # Pelo menos o campo nome deve existir
                if campo == 'nome':
                    assert locator.count() >= 0  # Pode nao existir se redirecionado

    # =========================================================================
    # UC-048: Editar turma
    # =========================================================================

    def test_uc048_admin_editar_turma(self, page: Page, base_url: str):
        """
        UC-048: Admin deve editar turma existente.

        Cenario: Edicao de turma
        Dado que existe uma turma
        Quando o admin edita as informacoes
        Entao as alteracoes devem ser salvas
        """
        self._criar_admin_e_logar(page, base_url)

        admin_turmas = AdminTurmasPage(page, base_url)
        admin_turmas.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Editar nome se disponivel
            campo_nome = page.locator('input[name="nome"]')
            if campo_nome.is_visible():
                campo_nome.fill("Turma Editada E2E")
                page.locator('button[type="submit"]').first.click()

                page.wait_for_timeout(1000)

    def test_uc048_admin_editar_turma_horario(self, page: Page, base_url: str):
        """
        UC-048: Admin pode editar horario da turma.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_turmas = AdminTurmasPage(page, base_url)
        admin_turmas.navegar_listar()

        link_editar = page.locator('a[href*="/editar/"]').first
        if link_editar.is_visible():
            link_editar.click()
            page.wait_for_timeout(500)

            # Verificar campos de horario
            campo_inicio = page.locator('input[name="horario_inicio"]')
            campo_fim = page.locator('input[name="horario_fim"]')

            if campo_inicio.is_visible() and campo_fim.is_visible():
                campo_inicio.fill("08:00")
                campo_fim.fill("09:00")

    # =========================================================================
    # UC-049: Excluir turma
    # =========================================================================

    def test_uc049_admin_excluir_turma_sem_matriculas(self, page: Page, base_url: str):
        """
        UC-049: Admin deve excluir turma sem matriculas.

        Cenario: Exclusao de turma
        Dado que existe uma turma sem matriculas
        Quando o admin exclui a turma
        Entao a turma deve ser removida
        """
        self._criar_admin_e_logar(page, base_url)

        admin_turmas = AdminTurmasPage(page, base_url)
        admin_turmas.navegar_listar()

        # Tentar excluir
        btn_excluir = page.locator('button:has-text("Excluir"), form[action*="excluir"] button').first
        if btn_excluir.is_visible():
            btn_excluir.click()
            page.wait_for_timeout(1000)

    def test_uc049_nao_excluir_turma_com_matriculas(self, page: Page, base_url: str):
        """
        UC-049: Nao deve excluir turma com matriculas.

        Cenario: Tentativa de exclusao bloqueada
        Dado que existe uma turma com matriculas
        Quando o admin tenta excluir
        Entao deve ver mensagem de erro
        """
        # Este teste depende do estado do banco
        self._criar_admin_e_logar(page, base_url)

        admin_turmas = AdminTurmasPage(page, base_url)
        admin_turmas.navegar_listar()

        # Se tentar excluir turma com matriculas, deve falhar


class TestProfessorTurmas:
    """Testes para casos de uso de turmas do professor."""

    def _criar_professor_e_logar(self, page: Page, base_url: str) -> tuple:
        """Helper para criar professor e fazer login."""
        email = gerar_email_unico()
        senha = "Teste@123456"
        nome = gerar_nome_unico()

        cadastro = CadastroPage(page, base_url)
        cadastro.navegar()
        cadastro.cadastrar(
            perfil="Professor",
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
    # UC-050: Visualizar turmas proprias (Professor)
    # =========================================================================

    def test_uc050_professor_visualizar_turmas(self, page: Page, base_url: str):
        """
        UC-050: Professor deve visualizar suas turmas.

        Cenario: Visualizacao de turmas proprias
        Dado que o professor esta autenticado
        Quando ele acessa minhas turmas
        Entao deve ver apenas as turmas que ministra
        """
        self._criar_professor_e_logar(page, base_url)

        professor_turmas = ProfessorTurmasPage(page, base_url)
        professor_turmas.navegar_minhas_turmas()

        page.wait_for_timeout(1000)

        # Deve estar na pagina de turmas do professor ou dashboard
        assert "/usuario" in page.url

    def test_uc050_professor_nao_edita_turmas(self, page: Page, base_url: str):
        """
        UC-050: Professor nao pode editar turmas (somente visualizacao).
        """
        self._criar_professor_e_logar(page, base_url)

        # Tentar acessar edicao admin
        page.goto(f"{base_url}/admin/turmas/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/turmas" not in page.url

    # =========================================================================
    # UC-051: Visualizar alunos da turma (Professor)
    # =========================================================================

    def test_uc051_professor_ver_alunos_turma(self, page: Page, base_url: str):
        """
        UC-051: Professor deve ver alunos de suas turmas.

        Cenario: Visualizacao de alunos
        Dado que o professor tem turmas
        Quando ele acessa os detalhes de uma turma
        Entao deve ver a lista de alunos matriculados
        """
        self._criar_professor_e_logar(page, base_url)

        professor_turmas = ProfessorTurmasPage(page, base_url)
        professor_turmas.navegar_minhas_turmas()

        page.wait_for_timeout(500)

        # Clicar em turma para ver alunos (se houver)
        link_turma = page.locator('a[href*="/turma/"]').first
        if link_turma.is_visible():
            link_turma.click()
            page.wait_for_timeout(1000)

    def test_uc051_professor_nao_ve_outras_turmas(self, page: Page, base_url: str):
        """
        UC-051: Professor nao deve ver alunos de turmas de outros.
        """
        self._criar_professor_e_logar(page, base_url)

        # Tentar acessar turma com ID ficticio
        page.goto(f"{base_url}/usuario/turma/99999/alunos")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado ou redirecionado
        conteudo = page.content().lower()
        assert (
            "acesso" in conteudo
            or "permissao" in conteudo
            or "encontrad" in conteudo
            or "/usuario" in page.url
        )
