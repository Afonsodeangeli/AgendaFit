"""
Testes unitários para turma_repo.

Testa todas as operações CRUD do repositório de turmas,
incluindo tratamento de erros, validações de integridade referencial
com duas foreign keys (atividade e professor), e edge cases.
"""
import pytest
from datetime import datetime
from model.turma_model import Turma
from model.atividade_model import Atividade
from model.categoria_model import Categoria
from model.usuario_model import Usuario
from repo import turma_repo, atividade_repo, categoria_repo
from repo import usuario_repo
from util.db_util import get_connection


class TestCriarTabela:
    """Testes para criação da tabela turma"""

    def test_criar_tabela_sucesso(self):
        """Deve criar tabela turma com sucesso"""
        resultado = turma_repo.criar_tabela()
        assert resultado is True

        # Verificar se tabela foi criada
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='turma'"
            )
            assert cursor.fetchone() is not None

    def test_criar_tabela_idempotente(self):
        """Criar tabela múltiplas vezes não deve gerar erro"""
        turma_repo.criar_tabela()
        resultado = turma_repo.criar_tabela()
        assert resultado is True

    def test_criar_tabela_com_foreign_keys(self):
        """Deve criar tabela com foreign keys para atividade e professor"""
        turma_repo.criar_tabela()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_key_list(turma)")
            fks = cursor.fetchall()

            # Deve ter 2 foreign keys
            assert len(fks) >= 2

            # Verificar referências
            fk_tables = [fk["table"] for fk in fks]
            assert "atividade" in fk_tables
            assert "usuario" in fk_tables


class TestInserir:
    """Testes para inserção de turmas"""

    def test_inserir_turma_valida(self):
        """Deve inserir turma válida e retornar ID"""
        # Setup: criar dependências
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        # Criar categoria
        id_categoria = categoria_repo.inserir(
            Categoria(0, "Musculação", "Treino de força")
        )

        # Criar atividade
        atividade = Atividade(
            id_atividade=0,
            id_categoria=id_categoria,
            nome="Musculação Avançada",
            descricao="Treino avançado",
            data_cadastro=datetime.now(),
            categoria=None
        )
        id_atividade = atividade_repo.inserir(atividade)

        # Criar professor
        professor = Usuario(
            id=0,
            nome="João Silva",
            email="joao@test.com",
            senha="senha123",
            perfil="Professor",
            token_redefinicao=None,
            data_token=None,
            data_cadastro=datetime.now()
        )
        id_professor = usuario_repo.inserir(professor)

        # Inserir turma
        turma = Turma(
            id_turma=0,
            id_atividade=id_atividade,
            id_professor=id_professor,
            data_cadastro=datetime.now(),
            atividade=None,
            professor=None
        )

        id_inserido = turma_repo.inserir(turma)

        assert id_inserido is not None
        assert id_inserido > 0

    def test_inserir_turma_data_cadastro_automatica(self):
        """Deve preencher data_cadastro automaticamente"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Yoga", "Yoga básico"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Yoga Matinal", "Aula matinal", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Maria", "maria@test.com", "senha", "Professor", None, None, datetime.now())
        )

        # Inserir turma
        turma = Turma(0, id_atividade, id_professor, datetime.now(), None, None)
        id_inserido = turma_repo.inserir(turma)

        # Verificar data_cadastro
        turma_recuperada = turma_repo.obter_por_id(id_inserido)
        assert turma_recuperada is not None
        assert turma_recuperada.data_cadastro is not None
        assert isinstance(turma_recuperada.data_cadastro, datetime)

    def test_inserir_turma_atividade_inexistente(self):
        """Não deve permitir inserir turma com atividade inexistente"""
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        # Criar professor válido
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Teste", "prof@test.com", "senha", "Professor", None, None, datetime.now())
        )

        # Tentar inserir com atividade inexistente
        turma = Turma(0, 999, id_professor, datetime.now(), None, None)

        with pytest.raises(Exception):  # Foreign key violation
            turma_repo.inserir(turma)

    def test_inserir_turma_professor_inexistente(self):
        """Não deve permitir inserir turma com professor inexistente"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        turma_repo.criar_tabela()

        # Criar atividade válida
        id_categoria = categoria_repo.inserir(Categoria(0, "Dança", "Aulas de dança"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Dança Jazz", "Jazz moderno", datetime.now(), None)
        )

        # Tentar inserir com professor inexistente
        turma = Turma(0, id_atividade, 999, datetime.now(), None, None)

        with pytest.raises(Exception):  # Foreign key violation
            turma_repo.inserir(turma)

    def test_inserir_multiplas_turmas_mesma_atividade(self):
        """Deve permitir múltiplas turmas da mesma atividade"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        # Setup
        id_categoria = categoria_repo.inserir(Categoria(0, "Pilates", "Pilates"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Pilates Solo", "Solo", datetime.now(), None)
        )
        id_prof1 = usuario_repo.inserir(
            Usuario(0, "Prof 1", "prof1@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_prof2 = usuario_repo.inserir(
            Usuario(0, "Prof 2", "prof2@test.com", "senha", "Professor", None, None, datetime.now())
        )

        # Inserir duas turmas da mesma atividade
        turma1 = Turma(0, id_atividade, id_prof1, datetime.now(), None, None)
        turma2 = Turma(0, id_atividade, id_prof2, datetime.now(), None, None)

        id1 = turma_repo.inserir(turma1)
        id2 = turma_repo.inserir(turma2)

        assert id1 > 0
        assert id2 > 0
        assert id1 != id2


class TestAlterar:
    """Testes para alteração de turmas"""

    def test_alterar_turma_existente(self):
        """Deve alterar turma existente com sucesso"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Natação", "Natação"))
        id_ativ1 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Natação Iniciante", "Iniciante", datetime.now(), None)
        )
        id_ativ2 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Natação Avançada", "Avançada", datetime.now(), None)
        )
        id_prof1 = usuario_repo.inserir(
            Usuario(0, "Prof A", "profa@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_prof2 = usuario_repo.inserir(
            Usuario(0, "Prof B", "profb@test.com", "senha", "Professor", None, None, datetime.now())
        )

        # Inserir turma
        turma = Turma(0, id_ativ1, id_prof1, datetime.now(), None, None)
        id_turma = turma_repo.inserir(turma)

        # Alterar turma
        turma_alterada = Turma(id_turma, id_ativ2, id_prof2, datetime.now(), None, None)
        resultado = turma_repo.alterar(turma_alterada)

        assert resultado is True

        # Verificar alteração
        turma_recuperada = turma_repo.obter_por_id(id_turma)
        assert turma_recuperada.id_atividade == id_ativ2
        assert turma_recuperada.id_professor == id_prof2

    def test_alterar_turma_inexistente(self):
        """Alterar turma inexistente deve retornar False"""
        turma_repo.criar_tabela()

        turma = Turma(999, 1, 1, datetime.now(), None, None)
        resultado = turma_repo.alterar(turma)

        assert resultado is False

    def test_alterar_turma_atividade_inexistente(self):
        """Não deve permitir alterar para atividade inexistente"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        # Criar turma válida
        id_categoria = categoria_repo.inserir(Categoria(0, "HIIT", "HIIT"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "HIIT Básico", "Básico", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof HIIT", "hiit@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        # Tentar alterar para atividade inexistente
        turma_alterada = Turma(id_turma, 999, id_professor, datetime.now(), None, None)

        with pytest.raises(Exception):  # Foreign key violation
            turma_repo.alterar(turma_alterada)


class TestExcluir:
    """Testes para exclusão de turmas"""

    def test_excluir_turma_existente(self):
        """Deve excluir turma existente com sucesso"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "CrossFit", "CrossFit"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "CrossFit WOD", "WOD", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Cross", "cross@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        # Excluir
        resultado = turma_repo.excluir(id_turma)
        assert resultado is True

        # Verificar exclusão
        turma = turma_repo.obter_por_id(id_turma)
        assert turma is None

    def test_excluir_turma_inexistente(self):
        """Excluir turma inexistente deve retornar False"""
        turma_repo.criar_tabela()

        resultado = turma_repo.excluir(999)
        assert resultado is False


class TestObterPorId:
    """Testes para busca de turma por ID"""

    def test_obter_turma_existente_com_join(self):
        """Deve retornar turma com dados de atividade e professor via JOIN"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Spinning", "Aulas de bike"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Spinning Intenso", "Alta intensidade", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Spin", "spin@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        # Obter turma
        turma = turma_repo.obter_por_id(id_turma)

        assert turma is not None
        assert turma.id_turma == id_turma
        assert turma.id_atividade == id_atividade
        assert turma.id_professor == id_professor
        assert turma.data_cadastro is not None

        # Verificar JOIN com atividade
        assert turma.atividade is not None
        assert turma.atividade.nome == "Spinning Intenso"

        # Verificar JOIN com professor
        assert turma.professor is not None
        assert turma.professor.nome == "Prof Spin"
        assert turma.professor.email == "spin@test.com"

    def test_obter_turma_inexistente(self):
        """Deve retornar None para turma inexistente"""
        turma_repo.criar_tabela()

        turma = turma_repo.obter_por_id(999)
        assert turma is None


class TestObterTodas:
    """Testes para listagem de todas as turmas"""

    def test_obter_todas_vazio(self):
        """Deve retornar lista vazia quando não há turmas"""
        turma_repo.criar_tabela()

        turmas = turma_repo.obter_todas()
        assert turmas == []

    def test_obter_todas_com_dados(self):
        """Deve retornar todas as turmas cadastradas"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Aeróbica", "Aeróbica"))
        id_ativ1 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Aeróbica 1", "Manhã", datetime.now(), None)
        )
        id_ativ2 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Aeróbica 2", "Tarde", datetime.now(), None)
        )
        id_prof = usuario_repo.inserir(
            Usuario(0, "Prof Aero", "aero@test.com", "senha", "Professor", None, None, datetime.now())
        )

        turma_repo.inserir(Turma(0, id_ativ1, id_prof, datetime.now(), None, None))
        turma_repo.inserir(Turma(0, id_ativ2, id_prof, datetime.now(), None, None))

        turmas = turma_repo.obter_todas()

        assert len(turmas) == 2
        assert all(isinstance(t, Turma) for t in turmas)
        assert all(t.atividade is not None for t in turmas)
        assert all(t.professor is not None for t in turmas)

    def test_obter_todas_ordenado_por_atividade_nome(self):
        """Deve retornar turmas ordenadas por nome da atividade"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Variadas", "Variadas"))
        id_ativ_z = atividade_repo.inserir(
            Atividade(0, id_categoria, "Zumba", "Dança", datetime.now(), None)
        )
        id_ativ_a = atividade_repo.inserir(
            Atividade(0, id_categoria, "Aeróbica", "Cardio", datetime.now(), None)
        )
        id_prof = usuario_repo.inserir(
            Usuario(0, "Prof Multi", "multi@test.com", "senha", "Professor", None, None, datetime.now())
        )

        # Inserir em ordem diferente
        turma_repo.inserir(Turma(0, id_ativ_z, id_prof, datetime.now(), None, None))
        turma_repo.inserir(Turma(0, id_ativ_a, id_prof, datetime.now(), None, None))

        turmas = turma_repo.obter_todas()
        nomes_atividades = [t.atividade.nome for t in turmas]

        # Deve estar em ordem alfabética
        assert nomes_atividades == sorted(nomes_atividades)


class TestObterPorProfessor:
    """Testes para listagem de turmas por professor"""

    def test_obter_por_professor_vazio(self):
        """Deve retornar lista vazia quando professor não tem turmas"""
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Sem Turma", "sem@test.com", "senha", "Professor", None, None, datetime.now())
        )

        turmas = turma_repo.obter_por_professor(id_professor)
        assert turmas == []

    def test_obter_por_professor_com_turmas(self):
        """Deve retornar todas as turmas de um professor"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Funcional", "Funcional"))
        id_ativ1 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Funcional 1", "Manhã", datetime.now(), None)
        )
        id_ativ2 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Funcional 2", "Tarde", datetime.now(), None)
        )
        id_prof1 = usuario_repo.inserir(
            Usuario(0, "Prof Func", "func@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_prof2 = usuario_repo.inserir(
            Usuario(0, "Prof Outro", "outro@test.com", "senha", "Professor", None, None, datetime.now())
        )

        # Prof 1 tem 2 turmas
        turma_repo.inserir(Turma(0, id_ativ1, id_prof1, datetime.now(), None, None))
        turma_repo.inserir(Turma(0, id_ativ2, id_prof1, datetime.now(), None, None))
        # Prof 2 tem 1 turma
        turma_repo.inserir(Turma(0, id_ativ1, id_prof2, datetime.now(), None, None))

        turmas_prof1 = turma_repo.obter_por_professor(id_prof1)
        turmas_prof2 = turma_repo.obter_por_professor(id_prof2)

        assert len(turmas_prof1) == 2
        assert len(turmas_prof2) == 1
        assert all(t.id_professor == id_prof1 for t in turmas_prof1)
        assert all(t.id_professor == id_prof2 for t in turmas_prof2)

    def test_obter_por_professor_inexistente(self):
        """Deve retornar lista vazia para professor inexistente"""
        turma_repo.criar_tabela()

        turmas = turma_repo.obter_por_professor(999)
        assert turmas == []


class TestConverterData:
    """Testes para helper de conversão de data"""

    def test_converter_data_valida(self):
        """Deve converter string de data do SQLite corretamente"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Teste Data", "Teste"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Ativ Data", "Teste", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Data", "data@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        turma = turma_repo.obter_por_id(id_turma)

        # Data deve ser objeto datetime
        assert isinstance(turma.data_cadastro, datetime)
        assert turma.data_cadastro.year >= 2024


class TestIntegridadeReferencial:
    """Testes de integridade e edge cases"""

    def test_sequencia_completa_crud(self):
        """Teste integrado de todo o ciclo CRUD"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Boxe", "Boxe"))
        id_ativ1 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Boxe Básico", "Básico", datetime.now(), None)
        )
        id_ativ2 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Boxe Avançado", "Avançado", datetime.now(), None)
        )
        id_prof = usuario_repo.inserir(
            Usuario(0, "Prof Boxe", "boxe@test.com", "senha", "Professor", None, None, datetime.now())
        )

        # CREATE
        id_turma = turma_repo.inserir(Turma(0, id_ativ1, id_prof, datetime.now(), None, None))
        assert id_turma > 0

        # READ
        turma = turma_repo.obter_por_id(id_turma)
        assert turma.id_atividade == id_ativ1

        # UPDATE
        turma_repo.alterar(Turma(id_turma, id_ativ2, id_prof, datetime.now(), None, None))
        turma = turma_repo.obter_por_id(id_turma)
        assert turma.id_atividade == id_ativ2

        # DELETE
        turma_repo.excluir(id_turma)
        turma = turma_repo.obter_por_id(id_turma)
        assert turma is None

    def test_turma_persiste_apos_alteracao_atividade(self):
        """Turma deve persistir mesmo se a atividade for alterada"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "TRX", "TRX"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "TRX Original", "Original", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof TRX", "trx@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        # Alterar nome da atividade
        atividade_repo.alterar(
            Atividade(id_atividade, id_categoria, "TRX Modificado", "Modificado", datetime.now(), None)
        )

        # Turma deve ainda existir e refletir mudança
        turma = turma_repo.obter_por_id(id_turma)
        assert turma is not None
        assert turma.atividade.nome == "TRX Modificado"
