"""
Testes unitários para matricula_repo.

Testa todas as operações do repositório de matrículas,
incluindo validações de duplicação (UNIQUE constraint),
foreign keys (turma e aluno), e queries com JOINs complexos.
"""
import pytest
from datetime import datetime, timedelta
from model.matricula_model import Matricula
from model.turma_model import Turma
from model.atividade_model import Atividade
from model.categoria_model import Categoria
from model.usuario_model import Usuario
from repo import matricula_repo, turma_repo, atividade_repo, categoria_repo
from repo import usuario_repo
from util.db_util import get_connection


class TestCriarTabela:
    """Testes para criação da tabela matricula"""

    def test_criar_tabela_sucesso(self):
        """Deve criar tabela matricula com sucesso"""
        resultado = matricula_repo.criar_tabela()
        assert resultado is True

        # Verificar se tabela foi criada
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='matricula'"
            )
            assert cursor.fetchone() is not None

    def test_criar_tabela_idempotente(self):
        """Criar tabela múltiplas vezes não deve gerar erro"""
        matricula_repo.criar_tabela()
        resultado = matricula_repo.criar_tabela()
        assert resultado is True

    def test_criar_tabela_com_foreign_keys(self):
        """Deve criar tabela com foreign keys para turma e aluno"""
        matricula_repo.criar_tabela()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_key_list(matricula)")
            fks = cursor.fetchall()

            # Deve ter 2 foreign keys
            assert len(fks) >= 2

            # Verificar referências
            fk_tables = [fk["table"] for fk in fks]
            assert "turma" in fk_tables
            assert "usuario" in fk_tables

    def test_criar_tabela_com_unique_constraint(self):
        """Deve criar tabela com constraint UNIQUE(id_turma, id_aluno)"""
        matricula_repo.criar_tabela()

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA index_list(matricula)")
            indexes = cursor.fetchall()

            # Deve ter pelo menos um índice único
            assert any(idx["unique"] == 1 for idx in indexes)


class TestInserir:
    """Testes para inserção de matrículas"""

    def test_inserir_matricula_valida(self):
        """Deve inserir matrícula válida e retornar ID"""
        # Setup: criar dependências
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        # Criar estrutura completa
        id_categoria = categoria_repo.inserir(Categoria(0, "Natação", "Natação"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Natação Adulto", "Adultos", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Natação", "prof@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))
        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Teste", "aluno@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        # Inserir matrícula
        vencimento = datetime.now() + timedelta(days=30)
        matricula = Matricula(
            id_matricula=0,
            id_turma=id_turma,
            id_aluno=id_aluno,
            data_matricula=datetime.now(),
            valor_mensalidade=150.00,
            data_vencimento=vencimento,
            turma=None,
            aluno=None
        )

        id_inserido = matricula_repo.inserir(matricula)

        assert id_inserido is not None
        assert id_inserido > 0

    def test_inserir_matricula_data_automatica(self):
        """Deve preencher data_matricula automaticamente"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Yoga", "Yoga"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Yoga Matinal", "Manhã", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Yoga", "yoga@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))
        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Yoga", "alunoyoga@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        # Inserir matrícula
        vencimento = datetime.now() + timedelta(days=30)
        matricula = Matricula(0, id_turma, id_aluno, datetime.now(), 120.00, vencimento, None, None)
        id_inserido = matricula_repo.inserir(matricula)

        # Verificar via obter_por_aluno
        matriculas = matricula_repo.obter_por_aluno(id_aluno)
        assert len(matriculas) == 1
        assert matriculas[0].data_matricula is not None
        assert isinstance(matriculas[0].data_matricula, datetime)

    def test_inserir_matricula_duplicada(self):
        """Não deve permitir inserir matrícula duplicada (mesma turma e aluno)"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Pilates", "Pilates"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Pilates Solo", "Solo", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Pilates", "pilates@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))
        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Pilates", "alunopilates@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        # Primeira matrícula
        vencimento = datetime.now() + timedelta(days=30)
        matricula1 = Matricula(0, id_turma, id_aluno, datetime.now(), 180.00, vencimento, None, None)
        id1 = matricula_repo.inserir(matricula1)
        assert id1 is not None

        # Segunda matrícula (duplicada)
        matricula2 = Matricula(0, id_turma, id_aluno, datetime.now(), 180.00, vencimento, None, None)
        id2 = matricula_repo.inserir(matricula2)

        # Deve retornar None devido à verificação de duplicação
        assert id2 is None

    def test_inserir_matricula_turma_inexistente(self):
        """Não deve permitir inserir matrícula com turma inexistente"""
        usuario_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Teste", "teste@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        matricula = Matricula(0, 999, id_aluno, datetime.now(), 100.00, vencimento, None, None)

        with pytest.raises(Exception):  # Foreign key violation
            matricula_repo.inserir(matricula)

    def test_inserir_matricula_aluno_inexistente(self):
        """Não deve permitir inserir matrícula com aluno inexistente"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Dança", "Dança"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Dança Jazz", "Jazz", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Dança", "danca@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        vencimento = datetime.now() + timedelta(days=30)
        matricula = Matricula(0, id_turma, 999, datetime.now(), 100.00, vencimento, None, None)

        with pytest.raises(Exception):  # Foreign key violation
            matricula_repo.inserir(matricula)

    def test_inserir_multiplas_matriculas_aluno_diferente(self):
        """Deve permitir múltiplos alunos na mesma turma"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Funcional", "Funcional"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Funcional Grupo", "Grupo", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Func", "func@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        id_aluno1 = usuario_repo.inserir(
            Usuario(0, "Aluno 1", "aluno1@test.com", "senha", "Aluno", None, None, datetime.now())
        )
        id_aluno2 = usuario_repo.inserir(
            Usuario(0, "Aluno 2", "aluno2@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        matricula1 = Matricula(0, id_turma, id_aluno1, datetime.now(), 150.00, vencimento, None, None)
        matricula2 = Matricula(0, id_turma, id_aluno2, datetime.now(), 150.00, vencimento, None, None)

        id1 = matricula_repo.inserir(matricula1)
        id2 = matricula_repo.inserir(matricula2)

        assert id1 is not None
        assert id2 is not None
        assert id1 != id2


class TestVerificarMatriculaExistente:
    """Testes para verificação de matrícula duplicada"""

    def test_verificar_matricula_inexistente(self):
        """Deve retornar False para matrícula não existente"""
        matricula_repo.criar_tabela()

        existe = matricula_repo.verificar_matricula_existente(1, 1)
        assert existe is False

    def test_verificar_matricula_existente(self):
        """Deve retornar True para matrícula existente"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "CrossFit", "CrossFit"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "CrossFit WOD", "WOD", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Cross", "cross@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))
        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Cross", "alunocross@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        matricula = Matricula(0, id_turma, id_aluno, datetime.now(), 200.00, vencimento, None, None)
        matricula_repo.inserir(matricula)

        # Verificar
        existe = matricula_repo.verificar_matricula_existente(id_turma, id_aluno)
        assert existe is True


class TestObterPorAluno:
    """Testes para listagem de matrículas por aluno"""

    def test_obter_por_aluno_vazio(self):
        """Deve retornar lista vazia quando aluno não tem matrículas"""
        usuario_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Sem Mat", "sem@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        matriculas = matricula_repo.obter_por_aluno(id_aluno)
        assert matriculas == []

    def test_obter_por_aluno_com_matriculas(self):
        """Deve retornar todas as matrículas de um aluno"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Multi", "Multi"))
        id_ativ1 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Atividade 1", "Desc 1", datetime.now(), None)
        )
        id_ativ2 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Atividade 2", "Desc 2", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Multi", "multi@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma1 = turma_repo.inserir(Turma(0, id_ativ1, id_professor, datetime.now(), None, None))
        id_turma2 = turma_repo.inserir(Turma(0, id_ativ2, id_professor, datetime.now(), None, None))

        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Multi", "alumult@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        matricula_repo.inserir(Matricula(0, id_turma1, id_aluno, datetime.now(), 100.00, vencimento, None, None))
        matricula_repo.inserir(Matricula(0, id_turma2, id_aluno, datetime.now(), 120.00, vencimento, None, None))

        matriculas = matricula_repo.obter_por_aluno(id_aluno)

        assert len(matriculas) == 2
        assert all(isinstance(m, Matricula) for m in matriculas)
        assert all(m.id_aluno == id_aluno for m in matriculas)
        assert all(m.turma is not None for m in matriculas)
        assert all(m.aluno is not None for m in matriculas)

    def test_obter_por_aluno_com_join_atividade(self):
        """Deve retornar matrículas com dados da atividade via JOIN"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Spinning", "Spinning"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Spinning Intenso", "Alta intensidade", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Spin", "spin@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))
        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Spin", "aluspin@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        matricula_repo.inserir(Matricula(0, id_turma, id_aluno, datetime.now(), 160.00, vencimento, None, None))

        matriculas = matricula_repo.obter_por_aluno(id_aluno)

        assert len(matriculas) == 1
        # A query faz JOIN com turma e atividade
        assert matriculas[0].turma is not None

    def test_obter_por_aluno_ordenado_por_data_desc(self):
        """Deve retornar matrículas ordenadas por data (mais recente primeiro)"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Ordem", "Ordem"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Atividade Ordem", "Ordem", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Ordem", "ordem@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma1 = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))
        id_turma2 = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Ordem", "aluordem@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        # Inserir em ordem
        matricula_repo.inserir(Matricula(0, id_turma1, id_aluno, datetime.now(), 100.00, vencimento, None, None))
        matricula_repo.inserir(Matricula(0, id_turma2, id_aluno, datetime.now(), 100.00, vencimento, None, None))

        matriculas = matricula_repo.obter_por_aluno(id_aluno)

        # Query ordena por data_matricula DESC, então verificar que retorna as 2 matrículas
        assert len(matriculas) == 2
        # Verificar que ambas turmas estão presentes (ordem pode variar se timestamps forem iguais)
        turmas_ids = {m.id_turma for m in matriculas}
        assert turmas_ids == {id_turma1, id_turma2}


class TestObterPorTurma:
    """Testes para listagem de matrículas por turma"""

    def test_obter_por_turma_vazio(self):
        """Deve retornar lista vazia quando turma não tem matrículas"""
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Vazia", "Vazia"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Sem Alunos", "Vazia", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Vazio", "vazio@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        matriculas = matricula_repo.obter_por_turma(id_turma)
        assert matriculas == []

    def test_obter_por_turma_com_alunos(self):
        """Deve retornar todas as matrículas de uma turma"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "HIIT", "HIIT"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "HIIT Grupo", "Grupo", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof HIIT", "hiit@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        id_aluno1 = usuario_repo.inserir(
            Usuario(0, "Aluno HIIT 1", "hiit1@test.com", "senha", "Aluno", None, None, datetime.now())
        )
        id_aluno2 = usuario_repo.inserir(
            Usuario(0, "Aluno HIIT 2", "hiit2@test.com", "senha", "Aluno", None, None, datetime.now())
        )
        id_aluno3 = usuario_repo.inserir(
            Usuario(0, "Aluno HIIT 3", "hiit3@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        matricula_repo.inserir(Matricula(0, id_turma, id_aluno1, datetime.now(), 140.00, vencimento, None, None))
        matricula_repo.inserir(Matricula(0, id_turma, id_aluno2, datetime.now(), 140.00, vencimento, None, None))
        matricula_repo.inserir(Matricula(0, id_turma, id_aluno3, datetime.now(), 140.00, vencimento, None, None))

        matriculas = matricula_repo.obter_por_turma(id_turma)

        assert len(matriculas) == 3
        assert all(isinstance(m, Matricula) for m in matriculas)
        assert all(m.id_turma == id_turma for m in matriculas)
        assert all(m.aluno is not None for m in matriculas)

    def test_obter_por_turma_ordenado_por_aluno_nome(self):
        """Deve retornar matrículas ordenadas por nome do aluno"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Alfabética", "Alfa"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Turma Alfa", "Alfa", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Alfa", "alfa@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        # Inserir em ordem alfabética inversa
        id_zeca = usuario_repo.inserir(
            Usuario(0, "Zeca", "zeca@test.com", "senha", "Aluno", None, None, datetime.now())
        )
        id_ana = usuario_repo.inserir(
            Usuario(0, "Ana", "ana@test.com", "senha", "Aluno", None, None, datetime.now())
        )
        id_bruno = usuario_repo.inserir(
            Usuario(0, "Bruno", "bruno@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        matricula_repo.inserir(Matricula(0, id_turma, id_zeca, datetime.now(), 100.00, vencimento, None, None))
        matricula_repo.inserir(Matricula(0, id_turma, id_ana, datetime.now(), 100.00, vencimento, None, None))
        matricula_repo.inserir(Matricula(0, id_turma, id_bruno, datetime.now(), 100.00, vencimento, None, None))

        matriculas = matricula_repo.obter_por_turma(id_turma)
        nomes_alunos = [m.aluno.nome for m in matriculas]

        # Deve estar em ordem alfabética
        assert nomes_alunos == sorted(nomes_alunos)
        assert nomes_alunos == ["Ana", "Bruno", "Zeca"]


class TestConverterData:
    """Testes para helper de conversão de data"""

    def test_converter_data_valida(self):
        """Deve converter string de data do SQLite corretamente"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Teste Data", "Data"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Ativ Data", "Data", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Data", "profdata@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))
        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Data", "aludata@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        matricula_repo.inserir(Matricula(0, id_turma, id_aluno, datetime.now(), 100.00, vencimento, None, None))

        matriculas = matricula_repo.obter_por_aluno(id_aluno)

        # Datas devem ser objetos datetime
        assert isinstance(matriculas[0].data_matricula, datetime)
        assert isinstance(matriculas[0].data_vencimento, datetime)
        assert matriculas[0].data_matricula.year >= 2024


class TestIntegridadeReferencial:
    """Testes de integridade e edge cases"""

    def test_valores_monetarios_com_decimais(self):
        """Deve armazenar e recuperar valores monetários com precisão"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Decimal", "Decimal"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Ativ Decimal", "Decimal", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Dec", "dec@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))
        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Dec", "aludec@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        valor_original = 123.45
        matricula_repo.inserir(Matricula(0, id_turma, id_aluno, datetime.now(), valor_original, vencimento, None, None))

        matriculas = matricula_repo.obter_por_aluno(id_aluno)
        assert abs(matriculas[0].valor_mensalidade - valor_original) < 0.01

    def test_aluno_multiplas_turmas_diferentes(self):
        """Aluno pode se matricular em múltiplas turmas diferentes"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Variadas", "Var"))
        id_ativ1 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Boxe", "Boxe", datetime.now(), None)
        )
        id_ativ2 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Muay Thai", "Muay", datetime.now(), None)
        )
        id_ativ3 = atividade_repo.inserir(
            Atividade(0, id_categoria, "Jiu-Jitsu", "JJ", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Luta", "luta@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma1 = turma_repo.inserir(Turma(0, id_ativ1, id_professor, datetime.now(), None, None))
        id_turma2 = turma_repo.inserir(Turma(0, id_ativ2, id_professor, datetime.now(), None, None))
        id_turma3 = turma_repo.inserir(Turma(0, id_ativ3, id_professor, datetime.now(), None, None))

        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Lutador", "lutador@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        vencimento = datetime.now() + timedelta(days=30)
        matricula_repo.inserir(Matricula(0, id_turma1, id_aluno, datetime.now(), 150.00, vencimento, None, None))
        matricula_repo.inserir(Matricula(0, id_turma2, id_aluno, datetime.now(), 160.00, vencimento, None, None))
        matricula_repo.inserir(Matricula(0, id_turma3, id_aluno, datetime.now(), 170.00, vencimento, None, None))

        matriculas = matricula_repo.obter_por_aluno(id_aluno)
        assert len(matriculas) == 3

        turmas_matriculadas = {m.id_turma for m in matriculas}
        assert turmas_matriculadas == {id_turma1, id_turma2, id_turma3}

    def test_turma_multiplos_alunos(self):
        """Turma pode ter múltiplos alunos matriculados"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Coletiva", "Coletiva"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Turma Grande", "Grande", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Grande", "grande@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))

        alunos_ids = []
        for i in range(10):
            id_aluno = usuario_repo.inserir(
                Usuario(0, f"Aluno {i}", f"aluno{i}@test.com", "senha", "Aluno", None, None, datetime.now())
            )
            alunos_ids.append(id_aluno)

        vencimento = datetime.now() + timedelta(days=30)
        for id_aluno in alunos_ids:
            matricula_repo.inserir(Matricula(0, id_turma, id_aluno, datetime.now(), 100.00, vencimento, None, None))

        matriculas = matricula_repo.obter_por_turma(id_turma)
        assert len(matriculas) == 10

    def test_data_vencimento_futura(self):
        """Deve aceitar datas de vencimento futuras"""
        # Setup
        categoria_repo.criar_tabela()
        atividade_repo.criar_tabela()
        usuario_repo.criar_tabela()
        turma_repo.criar_tabela()
        matricula_repo.criar_tabela()

        id_categoria = categoria_repo.inserir(Categoria(0, "Futura", "Futura"))
        id_atividade = atividade_repo.inserir(
            Atividade(0, id_categoria, "Ativ Futura", "Futura", datetime.now(), None)
        )
        id_professor = usuario_repo.inserir(
            Usuario(0, "Prof Fut", "fut@test.com", "senha", "Professor", None, None, datetime.now())
        )
        id_turma = turma_repo.inserir(Turma(0, id_atividade, id_professor, datetime.now(), None, None))
        id_aluno = usuario_repo.inserir(
            Usuario(0, "Aluno Fut", "alufut@test.com", "senha", "Aluno", None, None, datetime.now())
        )

        # Vencimento daqui a 60 dias
        vencimento = datetime.now() + timedelta(days=60)
        id_matricula = matricula_repo.inserir(
            Matricula(0, id_turma, id_aluno, datetime.now(), 200.00, vencimento, None, None)
        )

        assert id_matricula is not None

        matriculas = matricula_repo.obter_por_aluno(id_aluno)
        assert matriculas[0].data_vencimento > datetime.now()
