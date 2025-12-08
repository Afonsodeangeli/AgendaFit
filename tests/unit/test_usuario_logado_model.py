"""
Testes para o modelo UsuarioLogado (model/usuario_logado_model.py)

Testa todos os métodos do dataclass UsuarioLogado incluindo
verificação de perfis, serialização e desserialização.
"""

import pytest
from unittest.mock import MagicMock

from model.usuario_logado_model import UsuarioLogado
from util.perfis import Perfil


class TestUsuarioLogadoInstanciacao:
    """Testes de criação de instâncias"""

    def test_criar_usuario_logado(self):
        """Deve criar instância com todos os campos"""
        usuario = UsuarioLogado(
            id=1,
            nome="João Silva",
            email="joao@teste.com",
            perfil=Perfil.ALUNO.value
        )

        assert usuario.id == 1
        assert usuario.nome == "João Silva"
        assert usuario.email == "joao@teste.com"
        assert usuario.perfil == "Aluno"

    def test_usuario_logado_imutavel(self):
        """UsuarioLogado deve ser imutável (frozen=True)"""
        usuario = UsuarioLogado(
            id=1,
            nome="João",
            email="joao@teste.com",
            perfil=Perfil.ALUNO.value
        )

        with pytest.raises(AttributeError):
            usuario.nome = "Novo Nome"


class TestIsAdmin:
    """Testes para o método is_admin()"""

    def test_admin_retorna_true(self):
        """Admin deve retornar True"""
        admin = UsuarioLogado(
            id=1,
            nome="Admin",
            email="admin@teste.com",
            perfil=Perfil.ADMIN.value
        )

        assert admin.is_admin() is True

    def test_aluno_retorna_false(self):
        """Aluno não deve ser admin"""
        aluno = UsuarioLogado(
            id=1,
            nome="Aluno",
            email="aluno@teste.com",
            perfil=Perfil.ALUNO.value
        )

        assert aluno.is_admin() is False

    def test_professor_retorna_false(self):
        """Professor não deve ser admin"""
        professor = UsuarioLogado(
            id=1,
            nome="Professor",
            email="professor@teste.com",
            perfil=Perfil.PROFESSOR.value
        )

        assert professor.is_admin() is False


class TestIsAluno:
    """Testes para o método is_aluno()"""

    def test_aluno_retorna_true(self):
        """Aluno deve retornar True"""
        aluno = UsuarioLogado(
            id=1,
            nome="Aluno",
            email="aluno@teste.com",
            perfil=Perfil.ALUNO.value
        )

        assert aluno.is_aluno() is True

    def test_admin_retorna_false(self):
        """Admin não deve ser aluno"""
        admin = UsuarioLogado(
            id=1,
            nome="Admin",
            email="admin@teste.com",
            perfil=Perfil.ADMIN.value
        )

        assert admin.is_aluno() is False

    def test_professor_retorna_false(self):
        """Professor não deve ser aluno"""
        professor = UsuarioLogado(
            id=1,
            nome="Professor",
            email="professor@teste.com",
            perfil=Perfil.PROFESSOR.value
        )

        assert professor.is_aluno() is False


class TestIsProfessor:
    """Testes para o método is_professor()"""

    def test_professor_retorna_true(self):
        """Professor deve retornar True"""
        professor = UsuarioLogado(
            id=1,
            nome="Professor",
            email="professor@teste.com",
            perfil=Perfil.PROFESSOR.value
        )

        assert professor.is_professor() is True

    def test_admin_retorna_false(self):
        """Admin não deve ser professor"""
        admin = UsuarioLogado(
            id=1,
            nome="Admin",
            email="admin@teste.com",
            perfil=Perfil.ADMIN.value
        )

        assert admin.is_professor() is False

    def test_aluno_retorna_false(self):
        """Aluno não deve ser professor"""
        aluno = UsuarioLogado(
            id=1,
            nome="Aluno",
            email="aluno@teste.com",
            perfil=Perfil.ALUNO.value
        )

        assert aluno.is_professor() is False


class TestTemPerfil:
    """Testes para o método tem_perfil()"""

    def test_tem_perfil_unico(self):
        """Deve retornar True quando tem o perfil"""
        admin = UsuarioLogado(
            id=1,
            nome="Admin",
            email="admin@teste.com",
            perfil=Perfil.ADMIN.value
        )

        assert admin.tem_perfil(Perfil.ADMIN.value) is True

    def test_nao_tem_perfil(self):
        """Deve retornar False quando não tem o perfil"""
        aluno = UsuarioLogado(
            id=1,
            nome="Aluno",
            email="aluno@teste.com",
            perfil=Perfil.ALUNO.value
        )

        assert aluno.tem_perfil(Perfil.ADMIN.value) is False

    def test_tem_perfil_multiplos(self):
        """Deve retornar True quando tem um dos perfis"""
        professor = UsuarioLogado(
            id=1,
            nome="Professor",
            email="professor@teste.com",
            perfil=Perfil.PROFESSOR.value
        )

        # Professor está na lista
        assert professor.tem_perfil(
            Perfil.ADMIN.value,
            Perfil.PROFESSOR.value
        ) is True

    def test_nao_tem_nenhum_perfil(self):
        """Deve retornar False quando não tem nenhum dos perfis"""
        aluno = UsuarioLogado(
            id=1,
            nome="Aluno",
            email="aluno@teste.com",
            perfil=Perfil.ALUNO.value
        )

        # Aluno não é admin nem professor
        assert aluno.tem_perfil(
            Perfil.ADMIN.value,
            Perfil.PROFESSOR.value
        ) is False


class TestToDict:
    """Testes para o método to_dict()"""

    def test_converte_para_dict(self):
        """Deve converter para dicionário"""
        usuario = UsuarioLogado(
            id=42,
            nome="Teste",
            email="teste@email.com",
            perfil="Aluno"
        )

        resultado = usuario.to_dict()

        assert resultado == {
            "id": 42,
            "nome": "Teste",
            "email": "teste@email.com",
            "perfil": "Aluno"
        }


class TestFromDict:
    """Testes para o método from_dict()"""

    def test_cria_de_dict_completo(self):
        """Deve criar instância de dicionário completo"""
        dados = {
            "id": 1,
            "nome": "João",
            "email": "joao@email.com",
            "perfil": "Aluno"
        }

        usuario = UsuarioLogado.from_dict(dados)

        assert usuario is not None
        assert usuario.id == 1
        assert usuario.nome == "João"
        assert usuario.email == "joao@email.com"
        assert usuario.perfil == "Aluno"

    def test_retorna_none_para_none(self):
        """Deve retornar None quando data é None"""
        resultado = UsuarioLogado.from_dict(None)

        assert resultado is None

    def test_levanta_erro_campo_faltando(self):
        """Deve levantar ValueError quando campo está faltando"""
        dados_incompletos = {
            "id": 1,
            "nome": "João",
            # falta email e perfil
        }

        with pytest.raises(ValueError) as exc_info:
            UsuarioLogado.from_dict(dados_incompletos)

        assert "Campos obrigatórios ausentes" in str(exc_info.value)

    def test_levanta_erro_mostra_campos_faltantes(self):
        """Mensagem de erro deve mostrar quais campos faltam"""
        dados_incompletos = {
            "id": 1,
            "nome": "João",
            "email": "joao@email.com"
            # falta perfil
        }

        with pytest.raises(ValueError) as exc_info:
            UsuarioLogado.from_dict(dados_incompletos)

        assert "perfil" in str(exc_info.value)


class TestFromUsuario:
    """Testes para o método from_usuario()"""

    def test_cria_de_usuario(self):
        """Deve criar UsuarioLogado de objeto Usuario"""
        # Mock do objeto Usuario
        usuario_mock = MagicMock()
        usuario_mock.id = 123
        usuario_mock.nome = "Maria"
        usuario_mock.email = "maria@email.com"
        usuario_mock.perfil = "Professor"

        usuario_logado = UsuarioLogado.from_usuario(usuario_mock)

        assert usuario_logado.id == 123
        assert usuario_logado.nome == "Maria"
        assert usuario_logado.email == "maria@email.com"
        assert usuario_logado.perfil == "Professor"
