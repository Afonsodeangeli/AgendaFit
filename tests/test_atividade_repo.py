"""
Testes unitários para atividade_repo.

Testa todas as operações CRUD do repositório de atividades,
incluindo relacionamentos com categorias e tratamento de foreign keys.
"""
import pytest
from datetime import datetime
from model.atividade_model import Atividade
from model.categoria_model import Categoria
from repo import atividade_repo, categoria_repo
from util.db_util import get_connection


class TestCriarTabela:
    """Testes para criação da tabela atividade"""

    def test_criar_tabela_sucesso(self):
        """Deve criar tabela atividade com sucesso"""
        resultado = atividade_repo.criar_tabela()
        assert resultado is True

        # Verificar se tabela foi criada
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='atividade'"
            )
            assert cursor.fetchone() is not None

    def test_criar_tabela_com_foreign_key(self):
        """Tabela atividade deve ter foreign key para categoria"""
        atividade_repo.criar_tabela()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_key_list(atividade)")
            fks = cursor.fetchall()

            # Deve ter FK para categoria
            assert len(fks) > 0
            assert any(fk[2] == 'categoria' for fk in fks)


class TestInserir:
    """Testes para inserção de atividades"""

    def test_inserir_atividade_valida(self):
        """Deve inserir atividade válida e retornar ID"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        # Criar categoria primeiro
        id_categoria = categoria_repo.inserir(
            Categoria(0, "Cardio", "Exercícios cardiovasculares")
        )

        atividade = Atividade(
            id_atividade=0,
            id_categoria=id_categoria,
            nome="Corrida",
            descricao="Treino de corrida em esteira ou pista",
            data_cadastro=datetime.now(),
            categoria=None
        )

        id_inserido = atividade_repo.inserir(atividade)

        assert id_inserido is not None
        assert id_inserido > 0

    def test_inserir_atividade_data_cadastro_automatica(self):
        """Deve preencher data_cadastro automaticamente"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(
            Categoria(0, "Força", "Exercícios de força")
        )

        atividade = Atividade(
            id_atividade=0,
            id_categoria=id_categoria,
            nome="Musculação",
            descricao="Treino de musculação",
            data_cadastro=datetime.now(),
            categoria=None
        )

        id_inserido = atividade_repo.inserir(atividade)
        atividade_recuperada = atividade_repo.obter_por_id(id_inserido)

        assert atividade_recuperada is not None
        assert atividade_recuperada.data_cadastro is not None
        assert isinstance(atividade_recuperada.data_cadastro, datetime)

    def test_inserir_atividade_categoria_inexistente(self):
        """Não deve permitir inserir atividade com categoria inexistente"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        atividade = Atividade(
            id_atividade=0,
            id_categoria=999,  # Categoria inexistente
            nome="Teste",
            descricao="Teste FK",
            data_cadastro=datetime.now(),
            categoria=None
        )

        # Deve lançar exceção de foreign key
        with pytest.raises(Exception):  # sqlite3.IntegrityError
            atividade_repo.inserir(atividade)

    def test_inserir_multiplas_atividades_mesma_categoria(self):
        """Deve inserir múltiplas atividades para mesma categoria"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(
            Categoria(0, "Dança", "Atividades de dança")
        )

        atividades = ["Zumba", "Ballet", "Jazz"]
        ids = []

        for nome in atividades:
            atividade = Atividade(
                id_atividade=0,
                id_categoria=id_categoria,
                nome=nome,
                descricao=f"Aula de {nome}",
                data_cadastro=datetime.now(),
                categoria=None
            )
            ids.append(atividade_repo.inserir(atividade))

        assert len(ids) == 3
        assert all(id > 0 for id in ids)


class TestAlterar:
    """Testes para alteração de atividades"""

    def test_alterar_atividade_existente(self):
        """Deve alterar atividade existente com sucesso"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(
            Categoria(0, "Aquático", "Atividades aquáticas")
        )

        atividade = Atividade(
            id_atividade=0,
            id_categoria=id_categoria,
            nome="Natação",
            descricao="Descrição original",
            data_cadastro=datetime.now(),
            categoria=None
        )
        id_inserido = atividade_repo.inserir(atividade)

        # Alterar
        atividade_alterada = Atividade(
            id_atividade=id_inserido,
            id_categoria=id_categoria,
            nome="Natação Avançada",
            descricao="Descrição atualizada",
            data_cadastro=datetime.now(),
            categoria=None
        )
        resultado = atividade_repo.alterar(atividade_alterada)

        assert resultado is True

        # Verificar alteração
        atividade_recuperada = atividade_repo.obter_por_id(id_inserido)
        assert atividade_recuperada.nome == "Natação Avançada"
        assert atividade_recuperada.descricao == "Descrição atualizada"

    def test_alterar_categoria_atividade(self):
        """Deve permitir alterar categoria de uma atividade"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_cat1 = categoria_repo.inserir(Categoria(0, "Cat 1", "Desc 1"))
        id_cat2 = categoria_repo.inserir(Categoria(0, "Cat 2", "Desc 2"))

        atividade = Atividade(
            id_atividade=0,
            id_categoria=id_cat1,
            nome="Atividade Móvel",
            descricao="Teste de mudança de categoria",
            data_cadastro=datetime.now(),
            categoria=None
        )
        id_inserido = atividade_repo.inserir(atividade)

        # Mudar para outra categoria
        atividade_alterada = Atividade(
            id_atividade=id_inserido,
            id_categoria=id_cat2,
            nome="Atividade Móvel",
            descricao="Teste de mudança de categoria",
            data_cadastro=datetime.now(),
            categoria=None
        )
        resultado = atividade_repo.alterar(atividade_alterada)

        assert resultado is True

        atividade_recuperada = atividade_repo.obter_por_id(id_inserido)
        assert atividade_recuperada.id_categoria == id_cat2

    def test_alterar_atividade_inexistente(self):
        """Alterar atividade inexistente deve retornar False"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Cat", "Desc"))

        atividade = Atividade(
            id_atividade=999,  # ID inexistente
            id_categoria=id_categoria,
            nome="Teste",
            descricao="Teste",
            data_cadastro=datetime.now(),
            categoria=None
        )

        resultado = atividade_repo.alterar(atividade)
        assert resultado is False


class TestExcluir:
    """Testes para exclusão de atividades"""

    def test_excluir_atividade_existente(self):
        """Deve excluir atividade existente com sucesso"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Cat", "Desc"))

        atividade = Atividade(
            id_atividade=0,
            id_categoria=id_categoria,
            nome="Temporária",
            descricao="Será excluída",
            data_cadastro=datetime.now(),
            categoria=None
        )
        id_inserido = atividade_repo.inserir(atividade)

        resultado = atividade_repo.excluir(id_inserido)
        assert resultado is True

        # Verificar exclusão
        atividade = atividade_repo.obter_por_id(id_inserido)
        assert atividade is None

    def test_excluir_atividade_inexistente(self):
        """Excluir atividade inexistente deve retornar False"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        resultado = atividade_repo.excluir(999)
        assert resultado is False


class TestObterPorId:
    """Testes para busca de atividade por ID"""

    def test_obter_atividade_existente(self):
        """Deve retornar atividade existente com categoria preenchida"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(
            Categoria(0, "Aeróbico", "Exercícios aeróbicos")
        )

        atividade = Atividade(
            id_atividade=0,
            id_categoria=id_categoria,
            nome="Spinning",
            descricao="Aula de bike indoor",
            data_cadastro=datetime.now(),
            categoria=None
        )
        id_inserido = atividade_repo.inserir(atividade)

        atividade_recuperada = atividade_repo.obter_por_id(id_inserido)

        assert atividade_recuperada is not None
        assert atividade_recuperada.id_atividade == id_inserido
        assert atividade_recuperada.nome == "Spinning"
        assert atividade_recuperada.categoria is not None
        assert atividade_recuperada.categoria.nome == "Aeróbico"

    def test_obter_atividade_inexistente(self):
        """Deve retornar None para atividade inexistente"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        atividade = atividade_repo.obter_por_id(999)
        assert atividade is None


class TestObterTodas:
    """Testes para listagem de todas as atividades"""

    def test_obter_todas_vazio(self):
        """Deve retornar lista vazia quando não há atividades"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        atividades = atividade_repo.obter_todas()
        assert atividades == []

    def test_obter_todas_com_dados(self):
        """Deve retornar todas as atividades com categorias preenchidas"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(
            Categoria(0, "Esporte", "Atividades esportivas")
        )

        nomes = ["Futebol", "Vôlei", "Basquete"]
        for nome in nomes:
            atividade = Atividade(
                id_atividade=0,
                id_categoria=id_categoria,
                nome=nome,
                descricao=f"Jogo de {nome}",
                data_cadastro=datetime.now(),
                categoria=None
            )
            atividade_repo.inserir(atividade)

        atividades = atividade_repo.obter_todas()

        assert len(atividades) == 3
        assert all(isinstance(at, Atividade) for at in atividades)
        assert all(at.categoria is not None for at in atividades)
        assert all(at.categoria.nome == "Esporte" for at in atividades)

    def test_obter_todas_ordenado_por_categoria_e_nome(self):
        """Deve retornar atividades ordenadas por categoria e nome"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        # Criar duas categorias
        id_cat_b = categoria_repo.inserir(Categoria(0, "B - Segunda", "Desc B"))
        id_cat_a = categoria_repo.inserir(Categoria(0, "A - Primeira", "Desc A"))

        # Inserir atividades em ordem inversa
        atividades_inserir = [
            (id_cat_b, "Z - Última"),
            (id_cat_a, "B - Segunda"),
            (id_cat_a, "A - Primeira"),
        ]

        for id_cat, nome in atividades_inserir:
            atividade_repo.inserir(Atividade(
                0, id_cat, nome, f"Desc {nome}",
                datetime.now(), None
            ))

        atividades = atividade_repo.obter_todas()

        # Ordem esperada: categoria A primeiro, depois B
        # Dentro de cada categoria, ordem alfabética de atividade
        assert atividades[0].categoria.nome == "A - Primeira"
        assert atividades[0].nome == "A - Primeira"
        assert atividades[1].categoria.nome == "A - Primeira"
        assert atividades[1].nome == "B - Segunda"
        assert atividades[2].categoria.nome == "B - Segunda"


class TestObterPorCategoria:
    """Testes para busca de atividades por categoria"""

    def test_obter_por_categoria_vazio(self):
        """Deve retornar lista vazia para categoria sem atividades"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Vazia", "Sem atividades"))

        atividades = atividade_repo.obter_por_categoria(id_categoria)
        assert atividades == []

    def test_obter_por_categoria_com_dados(self):
        """Deve retornar apenas atividades da categoria especificada"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_cat1 = categoria_repo.inserir(Categoria(0, "Cat 1", "Desc 1"))
        id_cat2 = categoria_repo.inserir(Categoria(0, "Cat 2", "Desc 2"))

        # Adicionar atividades em cat1
        for i in range(3):
            atividade_repo.inserir(Atividade(
                0, id_cat1, f"At Cat1 {i}", f"Desc {i}",
                datetime.now(), None
            ))

        # Adicionar atividades em cat2
        for i in range(2):
            atividade_repo.inserir(Atividade(
                0, id_cat2, f"At Cat2 {i}", f"Desc {i}",
                datetime.now(), None
            ))

        atividades_cat1 = atividade_repo.obter_por_categoria(id_cat1)
        atividades_cat2 = atividade_repo.obter_por_categoria(id_cat2)

        assert len(atividades_cat1) == 3
        assert len(atividades_cat2) == 2
        assert all(at.id_categoria == id_cat1 for at in atividades_cat1)
        assert all(at.id_categoria == id_cat2 for at in atividades_cat2)

    def test_obter_por_categoria_ordenado_por_nome(self):
        """Deve retornar atividades ordenadas por nome"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Cat", "Desc"))

        nomes = ["Zumba", "Aeróbica", "Musculação"]
        for nome in nomes:
            atividade_repo.inserir(Atividade(
                0, id_categoria, nome, f"Desc {nome}",
                datetime.now(), None
            ))

        atividades = atividade_repo.obter_por_categoria(id_categoria)
        nomes_recuperados = [at.nome for at in atividades]

        assert nomes_recuperados == sorted(nomes)


class TestObterQuantidade:
    """Testes para contagem de atividades"""

    def test_obter_quantidade_vazio(self):
        """Deve retornar 0 quando não há atividades"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        quantidade = atividade_repo.obter_quantidade()
        assert quantidade == 0

    def test_obter_quantidade_com_dados(self):
        """Deve retornar quantidade correta de atividades"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Cat", "Desc"))

        for i in range(7):
            atividade_repo.inserir(Atividade(
                0, id_categoria, f"At {i}", f"Desc {i}",
                datetime.now(), None
            ))

        quantidade = atividade_repo.obter_quantidade()
        assert quantidade == 7

    def test_obter_quantidade_multiplascategorias(self):
        """Quantidade deve contar atividades de todas as categorias"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_cat1 = categoria_repo.inserir(Categoria(0, "Cat 1", "Desc 1"))
        id_cat2 = categoria_repo.inserir(Categoria(0, "Cat 2", "Desc 2"))

        atividade_repo.inserir(Atividade(0, id_cat1, "At 1", "D1", datetime.now(), None))
        atividade_repo.inserir(Atividade(0, id_cat2, "At 2", "D2", datetime.now(), None))

        assert atividade_repo.obter_quantidade() == 2


class TestIntegridadeReferencial:
    """Testes de integridade referencial e edge cases"""

    def test_categoria_vinculada_nao_pode_ser_excluida(self):
        """Não deve permitir excluir categoria que tem atividades"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Cat", "Desc"))

        atividade_repo.inserir(Atividade(
            0, id_categoria, "Atividade", "Desc",
            datetime.now(), None
        ))

        # Tentar excluir categoria com atividades vinculadas
        # Depende de como o SQLite está configurado (RESTRICT ou CASCADE)
        # Por padrão, deve dar erro de foreign key
        with pytest.raises(Exception):
            categoria_repo.excluir(id_categoria)

    def test_sequencia_completa_crud(self):
        """Teste integrado de todo o ciclo CRUD"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()

        # Setup
        id_categoria = categoria_repo.inserir(Categoria(0, "Cat", "Desc"))

        # CREATE
        atividade = Atividade(
            0, id_categoria, "CrossFit", "Treino funcional",
            datetime.now(), None
        )
        id_inserido = atividade_repo.inserir(atividade)
        assert id_inserido > 0

        # READ
        atividade = atividade_repo.obter_por_id(id_inserido)
        assert atividade.nome == "CrossFit"
        assert atividade.categoria.nome == "Cat"

        # UPDATE
        atividade_repo.alterar(Atividade(
            id_inserido, id_categoria, "CrossFit Pro",
            "Treino funcional avançado", datetime.now(), None
        ))
        atividade = atividade_repo.obter_por_id(id_inserido)
        assert atividade.nome == "CrossFit Pro"

        # DELETE
        atividade_repo.excluir(id_inserido)
        atividade = atividade_repo.obter_por_id(id_inserido)
        assert atividade is None
