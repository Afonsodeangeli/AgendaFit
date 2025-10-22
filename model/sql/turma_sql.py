CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS turma (
    id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
    id_atividade INTEGER NOT NULL,
    id_professor INTEGER NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade),
    FOREIGN KEY (id_professor) REFERENCES usuario(id)
)
"""

INSERIR = "INSERT INTO turma (id_atividade, id_professor) VALUES (?, ?)"
ALTERAR = "UPDATE turma SET id_atividade = ?, id_professor = ? WHERE id_turma = ?"
EXCLUIR = "DELETE FROM turma WHERE id_turma = ?"

OBTER_POR_ID = """
SELECT t.*,
       a.nome as atividade_nome, a.descricao as atividade_descricao,
       u.nome as professor_nome, u.email as professor_email
FROM turma t
JOIN atividade a ON t.id_atividade = a.id_atividade
JOIN usuario u ON t.id_professor = u.id
WHERE t.id_turma = ?
"""

OBTER_TODAS = """
SELECT t.*,
       a.nome as atividade_nome, a.descricao as atividade_descricao,
       u.nome as professor_nome
FROM turma t
JOIN atividade a ON t.id_atividade = a.id_atividade
JOIN usuario u ON t.id_professor = u.id
ORDER BY a.nome
"""

OBTER_POR_PROFESSOR = "SELECT * FROM turma WHERE id_professor = ?"