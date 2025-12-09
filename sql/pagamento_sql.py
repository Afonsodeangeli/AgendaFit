CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS pagamento (
    id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_matricula INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_pago REAL NOT NULL,
    FOREIGN KEY (id_matricula) REFERENCES matricula(id_matricula) ON DELETE RESTRICT,
    FOREIGN KEY (id_aluno) REFERENCES usuario(id) ON DELETE RESTRICT
)
"""

INSERIR = "INSERT INTO pagamento (id_matricula, id_aluno, valor_pago) VALUES (?, ?, ?)"

OBTER_TODOS = """
SELECT p.*,
       m.id_turma, m.valor_mensalidade,
       t.nome as turma_nome,
       u.nome as aluno_nome, u.email as aluno_email
FROM pagamento p
JOIN matricula m ON p.id_matricula = m.id_matricula
JOIN turma t ON m.id_turma = t.id_turma
JOIN usuario u ON p.id_aluno = u.id
ORDER BY p.data_pagamento DESC
"""

OBTER_POR_ID = """
SELECT p.*,
       m.id_turma, m.valor_mensalidade,
       t.nome as turma_nome,
       u.nome as aluno_nome, u.email as aluno_email
FROM pagamento p
JOIN matricula m ON p.id_matricula = m.id_matricula
JOIN turma t ON m.id_turma = t.id_turma
JOIN usuario u ON p.id_aluno = u.id
WHERE p.id_pagamento = ?
"""

OBTER_POR_ALUNO = """
SELECT p.*,
       m.id_turma, m.valor_mensalidade,
       t.nome as turma_nome,
       u.nome as aluno_nome, u.email as aluno_email
FROM pagamento p
JOIN matricula m ON p.id_matricula = m.id_matricula
JOIN turma t ON m.id_turma = t.id_turma
JOIN usuario u ON p.id_aluno = u.id
WHERE p.id_aluno = ?
ORDER BY p.data_pagamento DESC
"""

OBTER_POR_MATRICULA = """
SELECT p.*,
       m.id_turma, m.valor_mensalidade,
       t.nome as turma_nome,
       u.nome as aluno_nome, u.email as aluno_email
FROM pagamento p
JOIN matricula m ON p.id_matricula = m.id_matricula
JOIN turma t ON m.id_turma = t.id_turma
JOIN usuario u ON p.id_aluno = u.id
WHERE p.id_matricula = ?
ORDER BY p.data_pagamento DESC
"""

ALTERAR = """
UPDATE pagamento SET valor_pago = ? WHERE id_pagamento = ?
"""

EXCLUIR = "DELETE FROM pagamento WHERE id_pagamento = ?"

OBTER_QUANTIDADE = "SELECT COUNT(*) as total FROM pagamento"