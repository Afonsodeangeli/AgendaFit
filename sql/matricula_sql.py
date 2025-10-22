CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS matricula (
    id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
    id_turma INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    data_matricula DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_mensalidade REAL NOT NULL,
    data_vencimento DATETIME NOT NULL,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma),
    FOREIGN KEY (id_aluno) REFERENCES usuario(id),
    UNIQUE(id_turma, id_aluno)
)
"""

INSERIR = """
INSERT INTO matricula (id_turma, id_aluno, valor_mensalidade, data_vencimento)
VALUES (?, ?, ?, ?)
"""

OBTER_POR_ALUNO = """
SELECT m.*,
       t.id_atividade, t.id_professor,
       a.nome as atividade_nome,
       u.nome as aluno_nome
FROM matricula m
JOIN turma t ON m.id_turma = t.id_turma
JOIN atividade a ON t.id_atividade = a.id_atividade
JOIN usuario u ON m.id_aluno = u.id
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
