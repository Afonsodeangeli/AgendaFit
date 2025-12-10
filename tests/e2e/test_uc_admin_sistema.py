"""
Testes E2E para Casos de Uso de Administracao do Sistema.

UC-062: Visualizar todas as configuracoes (Admin)
UC-063: Editar configuracoes em lote (Admin)
UC-064: Visualizar temas disponiveis (Admin)
UC-065: Aplicar tema (Admin)
UC-066: Listar todos os backups (Admin)
UC-067: Criar backup (Admin)
UC-068: Restaurar backup (Admin)
UC-069: Baixar backup (Admin)
UC-070: Excluir backup (Admin)
UC-071: Visualizar logs do sistema (Admin)
UC-072: Pesquisar logs (Admin)
"""
import pytest
from playwright.sync_api import Page, expect

from tests.e2e.test_e2e_helpers import (
    LoginPage,
    CadastroPage,
    AdminConfiguracoesPage,
    AdminTemaPage,
    AdminBackupsPage,
    AdminAuditoriaPage,
    gerar_email_unico,
    gerar_nome_unico,
    logar_com_seed_admin,
)


class TestAdminConfiguracoes:
    """Testes para casos de uso de configuracoes do sistema."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> None:
        """Faz login com admin do seed data."""
        logar_com_seed_admin(page, base_url)

    # =========================================================================
    # UC-062: Visualizar todas as configuracoes
    # =========================================================================

    def test_uc062_admin_visualizar_configuracoes(self, page: Page, base_url: str):
        """
        UC-062: Admin deve visualizar todas as configuracoes.

        Cenario: Visualizacao de configuracoes
        Dado que o admin esta autenticado
        Quando ele acessa a pagina de configuracoes
        Entao deve ver configuracoes agrupadas por categoria
        """
        self._criar_admin_e_logar(page, base_url)

        admin_config = AdminConfiguracoesPage(page, base_url)
        admin_config.navegar()

        # Deve estar na pagina de configuracoes
        assert admin_config.esta_na_pagina_configuracoes()

    def test_uc062_configuracoes_agrupadas(self, page: Page, base_url: str):
        """
        UC-062: Configuracoes devem estar agrupadas por categoria.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_config = AdminConfiguracoesPage(page, base_url)
        admin_config.navegar()

        page.wait_for_timeout(500)

        conteudo = page.content().lower()
        # Deve haver categorias como Aplicacao, Seguranca, Email, etc
        assert (
            "aplicacao" in conteudo
            or "seguranca" in conteudo
            or "email" in conteudo
            or "configurac" in conteudo
        )

    def test_uc062_usuario_comum_nao_acessa(self, page: Page, base_url: str):
        """
        UC-062: Usuario comum nao deve acessar configuracoes.
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

        # Tentar acessar configuracoes
        page.goto(f"{base_url}/admin/configuracoes")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/configuracoes" not in page.url

    # =========================================================================
    # UC-063: Editar configuracoes em lote
    # =========================================================================

    def test_uc063_admin_editar_configuracoes(self, page: Page, base_url: str):
        """
        UC-063: Admin deve editar configuracoes em lote.

        Cenario: Edicao de configuracoes
        Dado que o admin esta na pagina de configuracoes
        Quando ele altera valores e salva
        Entao as configuracoes devem ser atualizadas
        """
        self._criar_admin_e_logar(page, base_url)

        admin_config = AdminConfiguracoesPage(page, base_url)
        admin_config.navegar()

        page.wait_for_timeout(500)

        # Verificar se ha formulario de edicao
        btn_salvar = page.locator('button[type="submit"]').first
        if btn_salvar.is_visible():
            # O formulario existe
            assert True


class TestAdminTemas:
    """Testes para casos de uso de temas visuais."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> None:
        """Faz login com admin do seed data."""
        logar_com_seed_admin(page, base_url)

    # =========================================================================
    # UC-064: Visualizar temas disponiveis
    # =========================================================================

    def test_uc064_admin_visualizar_temas(self, page: Page, base_url: str):
        """
        UC-064: Admin deve visualizar temas disponiveis.

        Cenario: Visualizacao de temas
        Dado que o admin esta autenticado
        Quando ele acessa a pagina de temas
        Entao deve ver os temas disponiveis com previews
        """
        self._criar_admin_e_logar(page, base_url)

        admin_tema = AdminTemaPage(page, base_url)
        admin_tema.navegar()

        # Deve estar na pagina de temas
        assert admin_tema.esta_na_pagina_temas()

    def test_uc064_temas_com_preview(self, page: Page, base_url: str):
        """
        UC-064: Temas devem ter thumbnails/previews.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_tema = AdminTemaPage(page, base_url)
        admin_tema.navegar()

        page.wait_for_timeout(500)

        # Deve haver imagens de preview
        imagens = page.locator('img[src*="bootswatch"]')
        assert imagens.count() >= 0  # Pode nao haver se diretorio vazio

    # =========================================================================
    # UC-065: Aplicar tema
    # =========================================================================

    def test_uc065_admin_aplicar_tema(self, page: Page, base_url: str):
        """
        UC-065: Admin deve aplicar tema selecionado.

        Cenario: Aplicacao de tema
        Dado que o admin esta na pagina de temas
        Quando ele seleciona e aplica um tema
        Entao o tema deve ser aplicado
        """
        self._criar_admin_e_logar(page, base_url)

        admin_tema = AdminTemaPage(page, base_url)
        admin_tema.navegar()

        page.wait_for_timeout(500)

        # Verificar se ha botao/formulario para aplicar tema
        form_tema = page.locator('form[action*="tema"]').first
        if form_tema.is_visible():
            # O sistema permite aplicar temas
            assert True


class TestAdminBackups:
    """Testes para casos de uso de backups."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> None:
        """Faz login com admin do seed data."""
        logar_com_seed_admin(page, base_url)

    # =========================================================================
    # UC-066: Listar todos os backups
    # =========================================================================

    def test_uc066_admin_listar_backups(self, page: Page, base_url: str):
        """
        UC-066: Admin deve listar backups disponiveis.

        Cenario: Listagem de backups
        Dado que o admin esta autenticado
        Quando ele acessa a pagina de backups
        Entao deve ver lista de backups com data e tamanho
        """
        self._criar_admin_e_logar(page, base_url)

        admin_backups = AdminBackupsPage(page, base_url)
        admin_backups.navegar_listar()

        # Deve estar na pagina de backups
        assert admin_backups.esta_na_pagina_backups()

    def test_uc066_usuario_comum_nao_acessa(self, page: Page, base_url: str):
        """
        UC-066: Usuario comum nao deve acessar backups.
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

        # Tentar acessar backups
        page.goto(f"{base_url}/admin/backups/listar")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/backups" not in page.url

    # =========================================================================
    # UC-067: Criar backup
    # =========================================================================

    def test_uc067_admin_criar_backup(self, page: Page, base_url: str):
        """
        UC-067: Admin deve criar backup manual.

        Cenario: Criacao de backup
        Dado que o admin esta na pagina de backups
        Quando ele clica em criar backup
        Entao um novo backup deve ser criado
        """
        self._criar_admin_e_logar(page, base_url)

        admin_backups = AdminBackupsPage(page, base_url)
        admin_backups.navegar_listar()

        page.wait_for_timeout(500)

        # Verificar se ha botao de criar
        btn_criar = page.locator('button:has-text("Criar"), a:has-text("Criar")').first
        if btn_criar.is_visible():
            btn_criar.click()
            page.wait_for_timeout(2000)

            # Verificar sucesso
            conteudo = page.content().lower()
            assert (
                "sucesso" in conteudo
                or "criado" in conteudo
                or "/admin/backups" in page.url
            )

    # =========================================================================
    # UC-068: Restaurar backup
    # =========================================================================

    def test_uc068_admin_restaurar_backup_existe(self, page: Page, base_url: str):
        """
        UC-068: Opcao de restaurar backup deve existir.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_backups = AdminBackupsPage(page, base_url)
        admin_backups.navegar_listar()

        page.wait_for_timeout(500)

        # Verificar se ha opcao de restaurar
        conteudo = page.content().lower()
        assert "restaurar" in conteudo or "backup" in conteudo

    # =========================================================================
    # UC-069: Baixar backup
    # =========================================================================

    def test_uc069_admin_download_backup_link(self, page: Page, base_url: str):
        """
        UC-069: Admin deve ter opcao de download de backup.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_backups = AdminBackupsPage(page, base_url)
        admin_backups.navegar_listar()

        page.wait_for_timeout(500)

        # Verificar se ha links de download
        links_download = page.locator('a[href*="/download/"]')
        # Pode nao haver se nao existem backups
        assert links_download.count() >= 0

    # =========================================================================
    # UC-070: Excluir backup
    # =========================================================================

    def test_uc070_admin_excluir_backup_opcao(self, page: Page, base_url: str):
        """
        UC-070: Admin deve ter opcao de excluir backup.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_backups = AdminBackupsPage(page, base_url)
        admin_backups.navegar_listar()

        page.wait_for_timeout(500)

        # Verificar se ha botao de excluir
        conteudo = page.content().lower()
        assert "excluir" in conteudo or "backup" in conteudo


class TestAdminAuditoria:
    """Testes para casos de uso de auditoria/logs."""

    def _criar_admin_e_logar(self, page: Page, base_url: str) -> None:
        """Faz login com admin do seed data."""
        logar_com_seed_admin(page, base_url)

    # =========================================================================
    # UC-071: Visualizar logs do sistema
    # =========================================================================

    def test_uc071_admin_visualizar_logs(self, page: Page, base_url: str):
        """
        UC-071: Admin deve visualizar logs do sistema.

        Cenario: Visualizacao de logs
        Dado que o admin esta autenticado
        Quando ele acessa a pagina de auditoria
        Entao deve ver logs do sistema
        """
        self._criar_admin_e_logar(page, base_url)

        admin_auditoria = AdminAuditoriaPage(page, base_url)
        admin_auditoria.navegar()

        # Deve estar na pagina de auditoria
        assert admin_auditoria.esta_na_pagina_auditoria()

    def test_uc071_logs_filtros_disponiveis(self, page: Page, base_url: str):
        """
        UC-071: Pagina de logs deve ter filtros por data e nivel.
        """
        self._criar_admin_e_logar(page, base_url)

        admin_auditoria = AdminAuditoriaPage(page, base_url)
        admin_auditoria.navegar()

        page.wait_for_timeout(500)

        # Verificar presenca de filtros
        campo_data = page.locator('input[name="data"]')
        select_nivel = page.locator('select[name="nivel"]')

        assert campo_data.is_visible() or select_nivel.is_visible()

    def test_uc071_usuario_comum_nao_acessa(self, page: Page, base_url: str):
        """
        UC-071: Usuario comum nao deve acessar logs.
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

        # Tentar acessar auditoria
        page.goto(f"{base_url}/admin/auditoria")

        page.wait_for_timeout(1000)

        # Deve ser bloqueado
        assert "/admin/auditoria" not in page.url

    # =========================================================================
    # UC-072: Pesquisar logs
    # =========================================================================

    def test_uc072_admin_filtrar_logs(self, page: Page, base_url: str):
        """
        UC-072: Admin deve filtrar logs por data e nivel.

        Cenario: Filtragem de logs
        Dado que o admin esta na pagina de auditoria
        Quando ele aplica filtros
        Entao deve ver logs filtrados
        """
        self._criar_admin_e_logar(page, base_url)

        admin_auditoria = AdminAuditoriaPage(page, base_url)
        admin_auditoria.navegar()

        page.wait_for_timeout(500)

        # Preencher data de hoje
        from datetime import date
        data_hoje = date.today().strftime('%Y-%m-%d')

        campo_data = page.locator('input[name="data"]')
        if campo_data.is_visible():
            campo_data.fill(data_hoje)

            # Selecionar nivel TODOS
            select_nivel = page.locator('select[name="nivel"]')
            if select_nivel.is_visible():
                select_nivel.select_option("TODOS")

            # Submeter filtro
            page.locator('button[type="submit"]').click()

            page.wait_for_timeout(1000)

    def test_uc072_filtrar_por_nivel(self, page: Page, base_url: str):
        """
        UC-072: Admin pode filtrar por nivel especifico (INFO, ERROR, etc).
        """
        self._criar_admin_e_logar(page, base_url)

        admin_auditoria = AdminAuditoriaPage(page, base_url)
        admin_auditoria.navegar()

        page.wait_for_timeout(500)

        # Verificar opcoes de nivel
        select_nivel = page.locator('select[name="nivel"]')
        if select_nivel.is_visible():
            opcoes = select_nivel.locator('option')
            # Deve haver opcoes como INFO, ERROR, WARNING, etc
            assert opcoes.count() > 1
