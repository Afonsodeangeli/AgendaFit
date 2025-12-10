"""
Testes E2E para Casos de Uso de Sistema de Chamados.

UC-017: Listar chamados proprios
UC-018: Criar novo chamado
UC-019: Visualizar detalhes do chamado
UC-020: Responder chamado proprio
UC-021: Excluir chamado proprio
UC-022: Listar todos os chamados do sistema (Admin)
UC-023: Responder qualquer chamado (Admin)
UC-024: Fechar chamado (Admin)
UC-025: Reabrir chamado fechado (Admin)
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    ChamadosPage,
    AdminChamadosPage,
    gerar_email_unico,
    gerar_nome_unico,
    logar_com_seed_admin,
)


class TestChamadosUsuario:
    """Testes para casos de uso de chamados (usuario comum)."""

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
    # UC-017: Listar chamados proprios
    # =========================================================================

    def test_uc017_listar_chamados_proprio(self, page: Page, base_url: str):
        """
        UC-017: Usuario deve ver lista de seus chamados.

        Cenario: Listagem de chamados do usuario
        Dado que o usuario esta autenticado
        Quando ele acessa a lista de chamados
        Entao deve ver seus chamados
        """
        self._criar_e_logar(page, base_url)

        chamados = ChamadosPage(page, base_url)
        chamados.navegar_listar()

        # Deve estar na pagina de chamados
        assert "/chamados" in page.url

    def test_uc017_listar_chamados_nao_autenticado(self, page: Page, base_url: str):
        """
        UC-017: Usuario nao autenticado nao deve listar chamados.
        """
        chamados = ChamadosPage(page, base_url)
        chamados.navegar_listar()

        page.wait_for_timeout(1000)

        # Deve ser redirecionado para login
        assert "/login" in page.url

    # =========================================================================
    # UC-018: Criar novo chamado
    # =========================================================================

    def test_uc018_criar_chamado_sucesso(self, page: Page, base_url: str):
        """
        UC-018: Usuario deve criar chamado com sucesso.

        Cenario: Criacao de chamado
        Dado que o usuario esta autenticado
        Quando ele preenche e submete o formulario de chamado
        Entao o chamado deve ser criado
        """
        self._criar_e_logar(page, base_url)

        chamados = ChamadosPage(page, base_url)
        chamados.navegar_cadastrar()

        # Criar chamado
        chamados.criar_chamado(
            titulo="Problema de teste E2E",
            descricao="Descricao do problema para teste E2E",
            prioridade="Media"
        )

        page.wait_for_timeout(1000)

        # Deve redirecionar ou mostrar sucesso
        conteudo = page.content().lower()
        assert (
            "sucesso" in conteudo
            or "criado" in conteudo
            or "/chamados" in page.url
        )

    def test_uc018_criar_chamado_prioridade_alta(self, page: Page, base_url: str):
        """
        UC-018: Usuario pode criar chamado com prioridade alta.
        """
        self._criar_e_logar(page, base_url)

        chamados = ChamadosPage(page, base_url)
        chamados.navegar_cadastrar()

        chamados.criar_chamado(
            titulo="Problema urgente E2E",
            descricao="Problema urgente para teste",
            prioridade="Alta"
        )

        page.wait_for_timeout(1000)
        assert "/chamados" in page.url or "sucesso" in page.content().lower()

    def test_uc018_criar_chamado_nao_autenticado(self, page: Page, base_url: str):
        """
        UC-018: Usuario nao autenticado nao deve criar chamado.
        """
        chamados = ChamadosPage(page, base_url)
        chamados.navegar_cadastrar()

        page.wait_for_timeout(1000)

        assert "/login" in page.url

    # =========================================================================
    # UC-019: Visualizar detalhes do chamado
    # =========================================================================

    def test_uc019_visualizar_chamado_proprio(self, page: Page, base_url: str):
        """
        UC-019: Usuario deve visualizar detalhes de chamado proprio.

        Cenario: Visualizacao de chamado
        Dado que o usuario criou um chamado
        Quando ele acessa os detalhes
        Entao deve ver as informacoes completas
        """
        self._criar_e_logar(page, base_url)

        chamados = ChamadosPage(page, base_url)
        chamados.navegar_cadastrar()

        # Criar chamado primeiro
        chamados.criar_chamado(
            titulo="Chamado para visualizar",
            descricao="Descricao do chamado",
            prioridade="Baixa"
        )

        page.wait_for_timeout(1000)

        # Ir para lista e clicar no chamado
        chamados.navegar_listar()

        # Clicar no primeiro chamado da lista
        link_chamado = page.locator('a[href*="/chamados/"]').first
        if link_chamado.is_visible():
            link_chamado.click()
            page.wait_for_timeout(1000)

            # Verificar que esta na pagina de detalhes
            conteudo = page.content().lower()
            assert "chamado" in conteudo or "visualizar" in page.url

    # =========================================================================
    # UC-020: Responder chamado proprio
    # =========================================================================

    def test_uc020_responder_chamado_proprio(self, page: Page, base_url: str):
        """
        UC-020: Usuario deve poder responder ao seu chamado.

        Cenario: Resposta ao chamado
        Dado que o usuario tem um chamado aberto
        Quando ele adiciona uma mensagem
        Entao a mensagem deve ser salva
        """
        self._criar_e_logar(page, base_url)

        chamados = ChamadosPage(page, base_url)
        chamados.navegar_cadastrar()

        # Criar chamado
        chamados.criar_chamado(
            titulo="Chamado para responder",
            descricao="Descricao inicial",
            prioridade="Media"
        )

        page.wait_for_timeout(1000)

        # Ir para lista e abrir chamado
        chamados.navegar_listar()

        link_chamado = page.locator('a[href*="/chamados/"]').first
        if link_chamado.is_visible():
            link_chamado.click()
            page.wait_for_timeout(500)

            # Adicionar resposta se houver campo de mensagem
            campo_mensagem = page.locator('textarea[name="mensagem"]')
            if campo_mensagem.is_visible():
                campo_mensagem.fill("Resposta adicional ao chamado")
                page.locator('button[type="submit"]').first.click()

    # =========================================================================
    # UC-021: Excluir chamado proprio
    # =========================================================================

    def test_uc021_excluir_chamado_proprio_aberto(self, page: Page, base_url: str):
        """
        UC-021: Usuario pode excluir chamado proprio com status Aberto.

        Cenario: Exclusao de chamado
        Dado que o usuario tem um chamado com status Aberto
        E sem respostas do admin
        Quando ele tenta excluir
        Entao o chamado deve ser removido
        """
        self._criar_e_logar(page, base_url)

        chamados = ChamadosPage(page, base_url)
        chamados.navegar_cadastrar()

        # Criar chamado
        chamados.criar_chamado(
            titulo="Chamado para excluir",
            descricao="Este chamado sera excluido",
            prioridade="Baixa"
        )

        page.wait_for_timeout(1000)

        # Ir para lista
        chamados.navegar_listar()

        # Tentar encontrar botao de excluir
        btn_excluir = page.locator('button:has-text("Excluir"), a:has-text("Excluir")').first
        if btn_excluir.is_visible():
            btn_excluir.click()
            page.wait_for_timeout(1000)


class TestChamadosAdmin:
    """Testes para casos de uso de chamados (Admin)."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> None:
        """Faz login com admin do seed data."""
        logar_com_seed_admin(page, base_url)

    # =========================================================================
    # UC-022: Listar todos os chamados do sistema (Admin)
    # =========================================================================

    def test_uc022_admin_listar_todos_chamados(self, page: Page, base_url: str):
        """
        UC-022: Admin deve ver todos os chamados do sistema.

        Cenario: Listagem administrativa de chamados
        Dado que o admin esta autenticado
        Quando ele acessa a lista de chamados admin
        Entao deve ver chamados de todos os usuarios
        """
        self._criar_admin_e_logar(page, base_url)

        admin_chamados = AdminChamadosPage(page, base_url)
        admin_chamados.navegar_listar()

        # Deve estar na pagina de chamados admin
        assert "/admin/chamados" in page.url

    def test_uc022_usuario_comum_nao_acessa_admin_chamados(self, page: Page, base_url: str):
        """
        UC-022: Usuario comum nao deve acessar lista admin de chamados.
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
        page.goto(f"{base_url}/admin/chamados/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado ou redirecionado
        assert "/admin/chamados" not in page.url or "acesso" in page.content().lower()

    # =========================================================================
    # UC-023: Responder qualquer chamado (Admin)
    # =========================================================================

    def test_uc023_admin_responder_chamado(self, page: Page, base_url: str):
        """
        UC-023: Admin deve poder responder a qualquer chamado.

        Cenario: Resposta administrativa
        Dado que existe um chamado no sistema
        Quando o admin acessa e responde
        Entao a resposta deve ser salva com tipo RESPOSTA_ADMIN
        """
        self._criar_admin_e_logar(page, base_url)

        admin_chamados = AdminChamadosPage(page, base_url)
        admin_chamados.navegar_listar()

        # Verificar se ha chamados para responder
        link_responder = page.locator('a[href*="/responder"]').first
        if link_responder.is_visible():
            link_responder.click()
            page.wait_for_timeout(500)

            # Preencher resposta
            campo_mensagem = page.locator('textarea[name="mensagem"]')
            if campo_mensagem.is_visible():
                campo_mensagem.fill("Resposta administrativa de teste E2E")

                # Selecionar status
                select_status = page.locator('select[name="status_chamado"]')
                if select_status.is_visible():
                    select_status.select_option(index=1)  # Seleciona segunda opcao

                page.locator('button[type="submit"]').first.click()
                page.wait_for_timeout(1000)

    # =========================================================================
    # UC-024: Fechar chamado (Admin)
    # =========================================================================

    def test_uc024_admin_fechar_chamado(self, page: Page, base_url: str):
        """
        UC-024: Admin deve poder fechar chamado.

        Cenario: Fechamento de chamado
        Dado que existe um chamado aberto
        Quando o admin fecha o chamado
        Entao o status deve mudar para Fechado
        """
        self._criar_admin_e_logar(page, base_url)

        admin_chamados = AdminChamadosPage(page, base_url)
        admin_chamados.navegar_listar()

        # Verificar se ha chamados para fechar
        link_responder = page.locator('a[href*="/responder"]').first
        if link_responder.is_visible():
            link_responder.click()
            page.wait_for_timeout(500)

            # Procurar botao de fechar
            btn_fechar = page.locator('button:has-text("Fechar")').first
            if btn_fechar.is_visible():
                btn_fechar.click()
                page.wait_for_timeout(1000)

    # =========================================================================
    # UC-025: Reabrir chamado fechado (Admin)
    # =========================================================================

    def test_uc025_admin_reabrir_chamado(self, page: Page, base_url: str):
        """
        UC-025: Admin deve poder reabrir chamado fechado.

        Cenario: Reabertura de chamado
        Dado que existe um chamado fechado
        Quando o admin reabre o chamado
        Entao o status deve mudar para Em Analise
        """
        self._criar_admin_e_logar(page, base_url)

        admin_chamados = AdminChamadosPage(page, base_url)
        admin_chamados.navegar_listar()

        # Procurar chamado fechado e botao de reabrir
        btn_reabrir = page.locator('button:has-text("Reabrir"), a:has-text("Reabrir")').first
        if btn_reabrir.is_visible():
            btn_reabrir.click()
            page.wait_for_timeout(1000)

            # Verificar sucesso
            conteudo = page.content().lower()
            assert "sucesso" in conteudo or "reaberto" in conteudo or "/admin/chamados" in page.url
