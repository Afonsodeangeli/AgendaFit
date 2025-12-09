CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS matricula (
    id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
    id_turma INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    data_matricula DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_mensalidade REAL NOT NULL,
    data_vencimento DATETIME NOT NULL,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma) ON DELETE RESTRICT,
    FOREIGN KEY (id_aluno) REFERENCES usuario(id) ON DELETE RESTRICT,
    UNIQUE(id_turma, id_aluno)
)
"""

INSERIR = """
INSERT INTO matricula (id_turma, id_aluno, valor_mensalidade, data_vencimento)
VALUES (?, ?, ?, ?)
"""

OBTER_POR_ALUNO = """
SELECT m.*,
       t.nome as turma_nome, t.id_atividade, t.id_professor, t.horario_inicio, t.horario_fim, t.dias_semana, t.vagas,
       a.nome as atividade_nome,
       u.nome as aluno_nome, u.email as aluno_email,
       p.nome as professor_nome, p.email as professor_email
FROM matricula m
JOIN turma t ON m.id_turma = t.id_turma
JOIN atividade a ON t.id_atividade = a.id_atividade
JOIN usuario u ON m.id_aluno = u.id
LEFT JOIN usuario p ON t.id_professor = p.id
WHERE m.id_aluno = ?
ORDER BY m.data_matricula DESC
"""

OBTER_POR_TURMA = """
SELECT m.*, u.nome as aluno_nome, u.email as aluno_email
FROM matricula m
JOIN usuario u ON m.id_aluno = u.id
WHERE m.id_turma = ?
ORDER BY u.nome
"""

VERIFICAR_MATRICULA_EXISTENTE = """
SELECT COUNT(*) as qtd FROM matricula
WHERE id_turma = ? AND id_aluno = ?
"""

OBTER_TODAS = """
SELECT m.*,
       t.nome as turma_nome, t.id_atividade, t.id_professor, t.horario_inicio, t.horario_fim, t.dias_semana, t.vagas,
       a.nome as atividade_nome,
       u.nome as aluno_nome, u.email as aluno_email
FROM matricula m
JOIN turma t ON m.id_turma = t.id_turma
JOIN atividade a ON t.id_atividade = a.id_atividade
JOIN usuario u ON m.id_aluno = u.id
ORDER BY m.data_matricula DESC
"""

OBTER_POR_ID = """
SELECT m.*,
       t.nome as turma_nome, t.id_atividade, t.id_professor, t.horario_inicio, t.horario_fim, t.dias_semana, t.vagas,
       a.nome as atividade_nome,
       u.nome as aluno_nome, u.email as aluno_email
FROM matricula m
JOIN turma t ON m.id_turma = t.id_turma
JOIN atividade a ON t.id_atividade = a.id_atividade
JOIN usuario u ON m.id_aluno = u.id
WHERE m.id_matricula = ?
"""

OBTER_POR_ALUNO_E_TURMA = """
SELECT m.*,
       t.nome as turma_nome,
       u.nome as aluno_nome
FROM matricula m
JOIN turma t ON m.id_turma = t.id_turma
JOIN usuario u ON m.id_aluno = u.id
WHERE m.id_aluno = ? AND m.id_turma = ?
"""

ALTERAR = """
UPDATE matricula
SET id_turma = ?, id_aluno = ?, valor_mensalidade = ?, data_vencimento = ?
WHERE id_matricula = ?
"""

EXCLUIR = """
DELETE FROM matricula WHERE id_matricula = ?
"""

OBTER_QUANTIDADE = """
SELECT COUNT(*) as total FROM matricula
"""
