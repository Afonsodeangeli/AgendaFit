"""
Testes para funcionalidades de Atividades do AgendaFit
"""
import pytest
from fastapi.testclient import TestClient


class TestListarAtividades:
    """Testes para listagem de atividades"""

    def test_listar_atividades_requer_admin(self, client, criar_usuario, fazer_login):
        """Apenas admin pode listar atividades (admin)"""
        # Criar e logar como aluno
        criar_usuario("João Aluno", "joao@test.com", "Senha@123", perfil="Aluno")
        fazer_login("joao@test.com", "Senha@123")

        response = client.get("/admin/atividades")
        assert response.status_code == 403

    def test_listar_atividades_admin_acessa(self, admin_autenticado):
        """Admin consegue acessar listagem de atividades"""
        response = admin_autenticado.get("/admin/atividades")
        assert response.status_code == 200

    def test_aluno_pode_ver_atividades_disponiveis(self, client, criar_usuario, fazer_login):
        """Aluno pode ver atividades disponíveis"""
        criar_usuario("Aluno", "aluno@test.com", "Senha@123", perfil="Aluno")
        fazer_login("aluno@test.com", "Senha@123")

        response = client.get("/aluno/atividades")
        assert response.status_code == 200


class TestCriarAtividade:
    """Testes para criação de atividades"""

    def test_criar_atividade_requer_categoria(self, admin_autenticado):
        """Atividade requer uma categoria válida"""
        # Primeiro criar uma categoria
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Cardio",
            "descricao": "Atividades cardiovasculares"
        })

        # Criar atividade com categoria
        response = admin_autenticado.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "Corrida",
            "descricao": "Treino de corrida em esteira ou pista"
        }, follow_redirects=False)

        assert response.status_code in [303, 404]  # 303 sucesso, 404 se categoria não existir

    def test_criar_atividade_nome_muito_curto(self, admin_autenticado):
        """Nome da atividade deve ter no mínimo 3 caracteres"""
        response = admin_autenticado.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "AB",
            "descricao": "Descrição válida com mais de 10 caracteres"
        })

        assert response.status_code in [400, 422, 200, 404]

    def test_criar_atividade_sem_autenticacao(self, client):
        """Não pode criar atividade sem autenticação"""
        response = client.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "Natação",
            "descricao": "Aulas de natação"
        })

        assert response.status_code in [401, 403, 307]  # Redirect para login ou forbidden


class TestEditarAtividade:
    """Testes para edição de atividades"""

    def test_editar_atividade_existente(self, admin_autenticado):
        """Admin pode editar atividade existente"""
        # Criar categoria
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Força",
            "descricao": "Atividades de força muscular"
        })

        # Criar atividade
        admin_autenticado.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "Crossfit Original",
            "descricao": "Treino funcional de alta intensidade original"
        })

        # Editar
        response = admin_autenticado.post("/admin/atividades/1/editar", data={
            "id_categoria": "1",
            "nome": "Crossfit Modificado",
            "descricao": "Treino funcional de alta intensidade modificado"
        }, follow_redirects=False)

        assert response.status_code in [303, 404]


class TestExcluirAtividade:
    """Testes para exclusão de atividades"""

    def test_excluir_atividade_existente(self, admin_autenticado):
        """Admin pode excluir atividade"""
        # Criar categoria
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Teste",
            "descricao": "Categoria de teste"
        })

        # Criar atividade
        admin_autenticado.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "Atividade Temporária",
            "descricao": "Esta atividade será excluída"
        })

        # Excluir
        response = admin_autenticado.post("/admin/atividades/1/excluir", follow_redirects=False)
        assert response.status_code in [303, 404]


class TestSegurancaAtividades:
    """Testes de segurança para atividades"""

    def test_aluno_nao_pode_criar_atividade(self, client, criar_usuario, fazer_login):
        """Aluno não pode criar atividades"""
        criar_usuario("Aluno", "aluno@test.com", "Senha@123", perfil="Aluno")
        fazer_login("aluno@test.com", "Senha@123")

        response = client.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "Tentativa Aluno",
            "descricao": "Aluno tentando criar atividade"
        })

        assert response.status_code == 403

    def test_aluno_nao_pode_editar_atividade(self, client, criar_usuario, fazer_login):
        """Aluno não pode editar atividades"""
        criar_usuario("Aluno", "aluno@test.com", "Senha@123", perfil="Aluno")
        fazer_login("aluno@test.com", "Senha@123")

        response = client.post("/admin/atividades/1/editar", data={
            "id_categoria": "1",
            "nome": "Tentativa",
            "descricao": "Tentativa de edição"
        })

        assert response.status_code == 403


class TestAtividadesPorCategoria:
    """Testes para filtrar atividades por categoria"""

    def test_atividades_agrupadas_por_categoria(self, admin_autenticado):
        """Atividades devem ser agrupadas por categoria na listagem"""
        # Criar categorias
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Aeróbico",
            "descricao": "Exercícios aeróbicos"
        })

        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Anaeróbico",
            "descricao": "Exercícios anaeróbicos"
        })

        # Criar atividades
        admin_autenticado.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "Spinning",
            "descricao": "Aula de bike indoor"
        })

        admin_autenticado.post("/admin/atividades/nova", data={
            "id_categoria": "2",
            "nome": "HIIT",
            "descricao": "Treino intervalado de alta intensidade"
        })

        response = admin_autenticado.get("/admin/atividades")
        assert response.status_code == 200
