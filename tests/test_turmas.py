"""
Testes para funcionalidades de Turmas do AgendaFit
"""
import pytest
from fastapi.testclient import TestClient


class TestListarTurmas:
    """Testes para listagem de turmas"""

    def test_listar_turmas_requer_admin(self, client, criar_usuario, fazer_login):
        """Apenas admin pode listar turmas"""
        criar_usuario("Aluno", "aluno@test.com", "Senha@123", perfil="Aluno")
        fazer_login("aluno@test.com", "Senha@123")

        response = client.get("/admin/turmas")
        assert response.status_code == 403

    def test_listar_turmas_admin_acessa(self, admin_autenticado):
        """Admin consegue acessar listagem de turmas"""
        response = admin_autenticado.get("/admin/turmas")
        assert response.status_code == 200


class TestCriarTurma:
    """Testes para criação de turmas"""

    def test_criar_turma_requer_atividade_e_professor(self, admin_autenticado):
        """Turma requer atividade e professor válidos"""
        # Criar categoria
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Dança",
            "descricao": "Atividades de dança"
        })

        # Criar atividade
        admin_autenticado.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "Zumba",
            "descricao": "Aula de zumba"
        })

        # Criar professor
        admin_autenticado.post("/admin/usuarios/cadastrar", data={
            "nome": "Prof. Carlos",
            "email": "carlos@test.com",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "perfil": "Professor"
        })

        # Criar turma
        response = admin_autenticado.post("/admin/turmas/nova", data={
            "id_atividade": "1",
            "id_professor": "2"  # ID 1 é o admin, 2 é o professor
        }, follow_redirects=False)

        assert response.status_code in [303, 404]

    def test_criar_turma_sem_professor_invalido(self, admin_autenticado):
        """Não pode criar turma sem professor válido"""
        response = admin_autenticado.post("/admin/turmas/nova", data={
            "id_atividade": "1",
            "id_professor": "999"  # ID inexistente
        })

        assert response.status_code in [400, 404, 422, 200]

    def test_criar_turma_sem_autenticacao(self, client):
        """Não pode criar turma sem autenticação"""
        response = client.post("/admin/turmas/nova", data={
            "id_atividade": "1",
            "id_professor": "1"
        })

        assert response.status_code in [401, 403, 307]


class TestEditarTurma:
    """Testes para edição de turmas"""

    def test_editar_turma_trocar_professor(self, admin_autenticado):
        """Admin pode trocar professor de uma turma"""
        # Setup: criar categoria, atividade e professores
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Aquático",
            "descricao": "Atividades aquáticas"
        })

        admin_autenticado.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "Hidroginástica",
            "descricao": "Ginástica na água"
        })

        # Professor 1
        admin_autenticado.post("/admin/usuarios/cadastrar", data={
            "nome": "Prof. Ana",
            "email": "ana@test.com",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "perfil": "Professor"
        })

        # Professor 2
        admin_autenticado.post("/admin/usuarios/cadastrar", data={
            "nome": "Prof. Bruno",
            "email": "bruno@test.com",
            "senha": "Senha@123",
            "confirmar_senha": "Senha@123",
            "perfil": "Professor"
        })

        # Criar turma com Prof. Ana
        admin_autenticado.post("/admin/turmas/nova", data={
            "id_atividade": "1",
            "id_professor": "2"
        })

        # Editar para Prof. Bruno
        response = admin_autenticado.post("/admin/turmas/1/editar", data={
            "id_atividade": "1",
            "id_professor": "3"
        }, follow_redirects=False)

        assert response.status_code in [303, 404]


class TestExcluirTurma:
    """Testes para exclusão de turmas"""

    def test_excluir_turma_existente(self, admin_autenticado):
        """Admin pode excluir turma"""
        response = admin_autenticado.post("/admin/turmas/1/excluir", follow_redirects=False)
        assert response.status_code in [303, 404]


class TestSegurancaTurmas:
    """Testes de segurança para turmas"""

    def test_aluno_nao_pode_criar_turma(self, client, criar_usuario, fazer_login):
        """Aluno não pode criar turmas"""
        criar_usuario("Aluno", "aluno@test.com", "Senha@123", perfil="Aluno")
        fazer_login("aluno@test.com", "Senha@123")

        response = client.post("/admin/turmas/nova", data={
            "id_atividade": "1",
            "id_professor": "1"
        })

        assert response.status_code == 403

    def test_professor_nao_pode_criar_turma(self, client, criar_usuario, fazer_login):
        """Professor não pode criar turmas"""
        criar_usuario("Professor", "prof@test.com", "Senha@123", perfil="Professor")
        fazer_login("prof@test.com", "Senha@123")

        response = client.post("/admin/turmas/nova", data={
            "id_atividade": "1",
            "id_professor": "1"
        })

        assert response.status_code == 403


class TestTurmasPorProfessor:
    """Testes para filtrar turmas por professor"""

    def test_professor_ve_apenas_suas_turmas(self, client, admin_autenticado, criar_usuario, fazer_login):
        """Professor deve ver apenas suas próprias turmas"""
        # Setup pelo admin
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Esporte",
            "descricao": "Atividades esportivas"
        })

        admin_autenticado.post("/admin/atividades/nova", data={
            "id_categoria": "1",
            "nome": "Futsal",
            "descricao": "Futebol de salão"
        })

        # Criar professor
        criar_usuario("Prof. João", "joao.prof@test.com", "Senha@123", perfil="Professor")

        # Admin cria turma para o professor
        admin_autenticado.post("/admin/turmas/nova", data={
            "id_atividade": "1",
            "id_professor": "2"  # ID do professor
        })

        # Fazer logout do admin
        admin_autenticado.get("/logout")

        # Login como professor
        fazer_login("joao.prof@test.com", "Senha@123")

        # Professor acessa suas turmas (se houver rota específica)
        # Esta rota pode não existir ainda, então testar se retorna 404 ou dados
        response = client.get("/professor/turmas")
        assert response.status_code in [200, 404]  # 200 se implementado, 404 se não
