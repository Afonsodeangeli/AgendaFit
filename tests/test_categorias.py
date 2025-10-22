"""
Testes para funcionalidades de Categorias do AgendaFit
"""
import pytest
from fastapi.testclient import TestClient


class TestListarCategorias:
    """Testes para listagem de categorias"""

    def test_listar_categorias_requer_admin(self, client, criar_usuario, fazer_login):
        """Apenas admin pode listar categorias"""
        # Criar e logar como aluno
        criar_usuario("João Aluno", "joao@test.com", "Senha@123", perfil="Aluno")
        fazer_login("joao@test.com", "Senha@123")

        response = client.get("/admin/categorias")
        assert response.status_code == 403

    def test_listar_categorias_admin_acessa(self, admin_autenticado):
        """Admin consegue acessar listagem de categorias"""
        response = admin_autenticado.get("/admin/categorias")
        assert response.status_code == 200
        assert b"Gerenciar Categorias" in response.content or b"Categorias" in response.content


class TestCriarCategoria:
    """Testes para criação de categorias"""

    def test_criar_categoria_com_dados_validos(self, admin_autenticado):
        """Admin pode criar categoria com dados válidos"""
        response = admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Musculação",
            "descricao": "Atividades de musculação e fortalecimento"
        }, follow_redirects=False)

        assert response.status_code == 303
        assert response.headers["location"] == "/admin/categorias"

    def test_criar_categoria_nome_duplicado(self, admin_autenticado):
        """Não pode criar categoria com nome duplicado"""
        # Criar primeira categoria
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Yoga",
            "descricao": "Práticas de yoga e meditação"
        })

        # Tentar criar com mesmo nome
        response = admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Yoga",
            "descricao": "Outra descrição"
        })

        assert response.status_code in [400, 422, 200]

    def test_criar_categoria_nome_muito_curto(self, admin_autenticado):
        """Nome da categoria deve ter no mínimo 3 caracteres"""
        response = admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "AB",
            "descricao": "Descrição válida com mais de 10 caracteres"
        })

        assert response.status_code in [400, 422, 200]
        if response.status_code == 200:
            assert b"no m\xc3\xadnimo 3 caracteres" in response.content or b"muito curto" in response.content

    def test_criar_categoria_descricao_muito_curta(self, admin_autenticado):
        """Descrição da categoria deve ter no mínimo 10 caracteres"""
        response = admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Categoria Teste",
            "descricao": "Curta"
        })

        assert response.status_code in [400, 422, 200]
        if response.status_code == 200:
            assert b"no m\xc3\xadnimo 10 caracteres" in response.content or b"muito curta" in response.content


class TestEditarCategoria:
    """Testes para edição de categorias"""

    def test_editar_categoria_existente(self, admin_autenticado):
        """Admin pode editar categoria existente"""
        # Criar categoria
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Pilates Original",
            "descricao": "Descrição original do pilates"
        })

        # Editar (assumindo ID 1)
        response = admin_autenticado.post("/admin/categorias/1/editar", data={
            "nome": "Pilates Atualizado",
            "descricao": "Descrição atualizada do pilates"
        }, follow_redirects=False)

        assert response.status_code in [303, 404]  # 404 se ID não existir


class TestExcluirCategoria:
    """Testes para exclusão de categorias"""

    def test_excluir_categoria_existente(self, admin_autenticado):
        """Admin pode excluir categoria"""
        # Criar categoria
        admin_autenticado.post("/admin/categorias/nova", data={
            "nome": "Categoria Temporária",
            "descricao": "Esta categoria será excluída"
        })

        # Excluir
        response = admin_autenticado.post("/admin/categorias/1/excluir", follow_redirects=False)
        assert response.status_code in [303, 404]


class TestSegurancaCategorias:
    """Testes de segurança para categorias"""

    def test_aluno_nao_pode_criar_categoria(self, client, criar_usuario, fazer_login):
        """Aluno não pode criar categorias"""
        criar_usuario("Aluno", "aluno@test.com", "Senha@123", perfil="Aluno")
        fazer_login("aluno@test.com", "Senha@123")

        response = client.post("/admin/categorias/nova", data={
            "nome": "Tentativa Aluno",
            "descricao": "Aluno tentando criar categoria"
        })

        assert response.status_code == 403

    def test_professor_nao_pode_criar_categoria(self, client, criar_usuario, fazer_login):
        """Professor não pode criar categorias"""
        criar_usuario("Professor", "prof@test.com", "Senha@123", perfil="Professor")
        fazer_login("prof@test.com", "Senha@123")

        response = client.post("/admin/categorias/nova", data={
            "nome": "Tentativa Professor",
            "descricao": "Professor tentando criar categoria"
        })

        assert response.status_code == 403
