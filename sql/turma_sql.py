# IMPORTANTE: Turma representa uma classe de atividade ministrada por um professor
# id_atividade é FOREIGN KEY - deve existir em atividade
# id_professor é FOREIGN KEY - deve existir em usuario com perfil Professor
# data_cadastro é preenchida automaticamente pelo banco via CURRENT_TIMESTAMP
# Queries com JOIN retornam campos prefixados: atividade_nome, professor_nome, etc
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS turma (
    id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    id_atividade INTEGER NOT NULL,
    id_professor INTEGER NOT NULL,
    horario_inicio TEXT NOT NULL,
    horario_fim TEXT NOT NULL,
    dias_semana TEXT NOT NULL,
    vagas INTEGER NOT NULL DEFAULT 20,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade) ON DELETE RESTRICT,
    FOREIGN KEY (id_professor) REFERENCES usuario(id) ON DELETE RESTRICT
)
"""

INSERIR = """
INSERT INTO turma (nome, id_atividade, id_professor, horario_inicio, horario_fim, dias_semana, vagas)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""

ALTERAR = """
UPDATE turma SET
    nome = ?,
    id_atividade = ?,
    id_professor = ?,
    horario_inicio = ?,
    horario_fim = ?,
    dias_semana = ?,
    vagas = ?,
    data_atualizacao = CURRENT_TIMESTAMP
WHERE id_turma = ?
"""

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
ORDER BY t.nome
"""

OBTER_POR_PROFESSOR = """
SELECT t.*,
       a.nome as atividade_nome, a.descricao as atividade_descricao
FROM turma t
JOIN atividade a ON t.id_atividade = a.id_atividade
WHERE t.id_professor = ?
ORDER BY t.nome
"""

OBTER_QUANTIDADE = "SELECT COUNT(*) as total FROM turma"