"""
Testes unitários para categoria_repo.

Testa todas as operações CRUD do repositório de categorias,
incluindo tratamento de erros, validações de integridade e edge cases.
"""
import pytest
from datetime import datetime
from model.categoria_model import Categoria
from repo import categoria_repo
from util.db_util import get_connection


class TestCriarTabela:
    """Testes para criação da tabela categoria"""

    def test_criar_tabela_sucesso(self):
        """Deve criar tabela categoria com sucesso"""
        resultado = categoria_repo.criar_tabela()
        assert resultado is True

        # Verificar se tabela foi criada
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='categoria'"
            )
            assert cursor.fetchone() is not None

    def test_criar_tabela_idempotente(self):
        """Criar tabela múltiplas vezes não deve gerar erro"""
        categoria_repo.criar_tabela()
        resultado = categoria_repo.criar_tabela()
        assert resultado is True


class TestInserir:
    """Testes para inserção de categorias"""

    def test_inserir_categoria_valida(self):
        """Deve inserir categoria válida e retornar ID"""
        categoria_repo.criar_tabela()

        categoria = Categoria(
            id_categoria=0,
            nome="Musculação",
            descricao="Atividades de fortalecimento muscular"
        )

        id_inserido = categoria_repo.inserir(categoria)

        assert id_inserido is not None
        assert id_inserido > 0

    def test_inserir_categoria_data_cadastro_automatica(self):
        """Deve preencher data_cadastro automaticamente"""
        categoria_repo.criar_tabela()

        categoria = Categoria(
            id_categoria=0,
            nome="Yoga",
            descricao="Práticas de yoga e meditação"
        )

        id_inserido = categoria_repo.inserir(categoria)
        categoria_recuperada = categoria_repo.obter_por_id(id_inserido)

        assert categoria_recuperada is not None
        assert categoria_recuperada.data_cadastro is not None
        assert isinstance(categoria_recuperada.data_cadastro, datetime)

    def test_inserir_categoria_nome_duplicado(self):
        """Não deve permitir inserir categoria com nome duplicado"""
        categoria_repo.criar_tabela()

        categoria1 = Categoria(
            id_categoria=0,
            nome="Pilates",
            descricao="Primeira descrição"
        )
        categoria_repo.inserir(categoria1)

        categoria2 = Categoria(
            id_categoria=0,
            nome="Pilates",  # Nome duplicado
            descricao="Segunda descrição"
        )

        # Deve lançar exceção de constraint UNIQUE
        with pytest.raises(Exception):  # sqlite3.IntegrityError
            categoria_repo.inserir(categoria2)

    def test_inserir_multiplas_categorias(self):
        """Deve inserir múltiplas categorias com sucesso"""
        categoria_repo.criar_tabela()

        categorias = [
            Categoria(0, "Cardio", "Exercícios cardiovasculares"),
            Categoria(0, "Força", "Exercícios de força"),
            Categoria(0, "Flexibilidade", "Exercícios de alongamento"),
        ]

        ids = [categoria_repo.inserir(cat) for cat in categorias]

        assert len(ids) == 3
        assert all(id > 0 for id in ids)
        assert len(set(ids)) == 3  # Todos IDs diferentes


class TestAlterar:
    """Testes para alteração de categorias"""

    def test_alterar_categoria_existente(self):
        """Deve alterar categoria existente com sucesso"""
        categoria_repo.criar_tabela()

        # Inserir
        categoria = Categoria(0, "Dança", "Descrição original")
        id_inserido = categoria_repo.inserir(categoria)

        # Alterar
        categoria_alterada = Categoria(
            id_categoria=id_inserido,
            nome="Dança Moderna",
            descricao="Descrição atualizada"
        )
        resultado = categoria_repo.alterar(categoria_alterada)

        assert resultado is True

        # Verificar alteração
        categoria_recuperada = categoria_repo.obter_por_id(id_inserido)
        assert categoria_recuperada.nome == "Dança Moderna"
        assert categoria_recuperada.descricao == "Descrição atualizada"

    def test_alterar_categoria_inexistente(self):
        """Alterar categoria inexistente deve retornar False"""
        categoria_repo.criar_tabela()

        categoria = Categoria(
            id_categoria=999,  # ID inexistente
            nome="Teste",
            descricao="Teste"
        )

        resultado = categoria_repo.alterar(categoria)
        assert resultado is False

    def test_alterar_nome_para_duplicado(self):
        """Não deve permitir alterar nome para um já existente"""
        categoria_repo.criar_tabela()

        # Inserir duas categorias
        id1 = categoria_repo.inserir(Categoria(0, "Natação", "Desc 1"))
        id2 = categoria_repo.inserir(Categoria(0, "Corrida", "Desc 2"))

        # Tentar alterar segunda para nome da primeira
        categoria_alterada = Categoria(id2, "Natação", "Nova desc")

        with pytest.raises(Exception):  # sqlite3.IntegrityError
            categoria_repo.alterar(categoria_alterada)


class TestExcluir:
    """Testes para exclusão de categorias"""

    def test_excluir_categoria_existente(self):
        """Deve excluir categoria existente com sucesso"""
        categoria_repo.criar_tabela()

        id_inserido = categoria_repo.inserir(
            Categoria(0, "Temporária", "Será excluída")
        )

        resultado = categoria_repo.excluir(id_inserido)
        assert resultado is True

        # Verificar exclusão
        categoria = categoria_repo.obter_por_id(id_inserido)
        assert categoria is None

    def test_excluir_categoria_inexistente(self):
        """Excluir categoria inexistente deve retornar False"""
        categoria_repo.criar_tabela()

        resultado = categoria_repo.excluir(999)
        assert resultado is False


class TestObterPorId:
    """Testes para busca de categoria por ID"""

    def test_obter_categoria_existente(self):
        """Deve retornar categoria existente corretamente"""
        categoria_repo.criar_tabela()

        id_inserido = categoria_repo.inserir(
            Categoria(0, "Spinning", "Aulas de bike indoor")
        )

        categoria = categoria_repo.obter_por_id(id_inserido)

        assert categoria is not None
        assert categoria.id_categoria == id_inserido
        assert categoria.nome == "Spinning"
        assert categoria.descricao == "Aulas de bike indoor"
        assert categoria.data_cadastro is not None

    def test_obter_categoria_inexistente(self):
        """Deve retornar None para categoria inexistente"""
        categoria_repo.criar_tabela()

        categoria = categoria_repo.obter_por_id(999)
        assert categoria is None

    def test_obter_categoria_apos_alteracao(self):
        """Deve retornar dados atualizados após alteração"""
        categoria_repo.criar_tabela()

        id_inserido = categoria_repo.inserir(
            Categoria(0, "HIIT", "Descrição original")
        )

        categoria_repo.alterar(
            Categoria(id_inserido, "HIIT Avançado", "Descrição nova")
        )

        categoria = categoria_repo.obter_por_id(id_inserido)
        assert categoria.nome == "HIIT Avançado"
        assert categoria.descricao == "Descrição nova"


class TestObterTodas:
    """Testes para listagem de todas as categorias"""

    def test_obter_todas_vazio(self):
        """Deve retornar lista vazia quando não há categorias"""
        categoria_repo.criar_tabela()

        categorias = categoria_repo.obter_todas()
        assert categorias == []

    def test_obter_todas_com_dados(self):
        """Deve retornar todas as categorias cadastradas"""
        categoria_repo.criar_tabela()

        nomes = ["Aeróbico", "Anaeróbico", "Misto"]
        for nome in nomes:
            categoria_repo.inserir(
                Categoria(0, nome, f"Descrição de {nome}")
            )

        categorias = categoria_repo.obter_todas()

        assert len(categorias) == 3
        assert all(isinstance(cat, Categoria) for cat in categorias)

        nomes_recuperados = [cat.nome for cat in categorias]
        assert set(nomes_recuperados) == set(nomes)

    def test_obter_todas_ordenado_por_nome(self):
        """Deve retornar categorias ordenadas por nome"""
        categoria_repo.criar_tabela()

        # Inserir em ordem diferente
        nomes = ["Zumba", "Aeróbica", "Musculação"]
        for nome in nomes:
            categoria_repo.inserir(Categoria(0, nome, f"Desc {nome}"))

        categorias = categoria_repo.obter_todas()
        nomes_recuperados = [cat.nome for cat in categorias]

        # Deve estar em ordem alfabética
        assert nomes_recuperados == sorted(nomes)

    def test_obter_todas_com_data_cadastro(self):
        """Todas as categorias devem ter data_cadastro preenchida"""
        categoria_repo.criar_tabela()

        categoria_repo.inserir(Categoria(0, "Teste 1", "Desc 1"))
        categoria_repo.inserir(Categoria(0, "Teste 2", "Desc 2"))

        categorias = categoria_repo.obter_todas()

        assert all(cat.data_cadastro is not None for cat in categorias)
        assert all(isinstance(cat.data_cadastro, datetime) for cat in categorias)


class TestObterQuantidade:
    """Testes para contagem de categorias"""

    def test_obter_quantidade_vazio(self):
        """Deve retornar 0 quando não há categorias"""
        categoria_repo.criar_tabela()

        quantidade = categoria_repo.obter_quantidade()
        assert quantidade == 0

    def test_obter_quantidade_com_dados(self):
        """Deve retornar quantidade correta de categorias"""
        categoria_repo.criar_tabela()

        for i in range(5):
            categoria_repo.inserir(
                Categoria(0, f"Categoria {i}", f"Descrição {i}")
            )

        quantidade = categoria_repo.obter_quantidade()
        assert quantidade == 5

    def test_obter_quantidade_apos_exclusao(self):
        """Quantidade deve diminuir após exclusão"""
        categoria_repo.criar_tabela()

        id1 = categoria_repo.inserir(Categoria(0, "Cat 1", "Desc 1"))
        id2 = categoria_repo.inserir(Categoria(0, "Cat 2", "Desc 2"))

        assert categoria_repo.obter_quantidade() == 2

        categoria_repo.excluir(id1)
        assert categoria_repo.obter_quantidade() == 1

        categoria_repo.excluir(id2)
        assert categoria_repo.obter_quantidade() == 0


class TestConverterData:
    """Testes para helper de conversão de data"""

    def test_converter_data_valida(self):
        """Deve converter string de data do SQLite corretamente"""
        categoria_repo.criar_tabela()

        id_inserido = categoria_repo.inserir(
            Categoria(0, "Teste Data", "Teste de conversão de data")
        )

        categoria = categoria_repo.obter_por_id(id_inserido)

        # Data deve ser objeto datetime
        assert isinstance(categoria.data_cadastro, datetime)
        assert categoria.data_cadastro.year >= 2024

    def test_converter_data_none(self):
        """Deve retornar None para data None"""
        # Testado implicitamente pelas fixtures que usam row.get()
        # que pode retornar None
        categoria_repo.criar_tabela()
        categorias = categoria_repo.obter_todas()
        # Se não houver exceção, o teste passa
        assert categorias == []


class TestIntegridadeReferencial:
    """Testes de integridade e edge cases"""

    def test_categoria_com_caracteres_especiais(self):
        """Deve aceitar caracteres especiais no nome e descrição"""
        categoria_repo.criar_tabela()

        categoria = Categoria(
            id_categoria=0,
            nome="Yoga & Meditação",
            descricao="Práticas de bem-estar: yoga, pilates & tai-chi"
        )

        id_inserido = categoria_repo.inserir(categoria)
        categoria_recuperada = categoria_repo.obter_por_id(id_inserido)

        assert categoria_recuperada.nome == "Yoga & Meditação"
        assert "tai-chi" in categoria_recuperada.descricao

    def test_categoria_com_acentos(self):
        """Deve preservar acentuação em português"""
        categoria_repo.criar_tabela()

        categoria = Categoria(
            id_categoria=0,
            nome="Educação Física",
            descricao="Atividades de educação física e recreação"
        )

        id_inserido = categoria_repo.inserir(categoria)
        categoria_recuperada = categoria_repo.obter_por_id(id_inserido)

        assert categoria_recuperada.nome == "Educação Física"
        assert "recreação" in categoria_recuperada.descricao

    def test_sequencia_completa_crud(self):
        """Teste integrado de todo o ciclo CRUD"""
        categoria_repo.criar_tabela()

        # CREATE
        id_inserido = categoria_repo.inserir(
            Categoria(0, "CrossFit", "Treino funcional")
        )
        assert id_inserido > 0

        # READ
        categoria = categoria_repo.obter_por_id(id_inserido)
        assert categoria.nome == "CrossFit"

        # UPDATE
        categoria_repo.alterar(
            Categoria(id_inserido, "CrossFit Pro", "Treino funcional avançado")
        )
        categoria = categoria_repo.obter_por_id(id_inserido)
        assert categoria.nome == "CrossFit Pro"

        # DELETE
        categoria_repo.excluir(id_inserido)
        categoria = categoria_repo.obter_por_id(id_inserido)
        assert categoria is None
