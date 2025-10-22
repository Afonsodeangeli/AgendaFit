CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS pagamento (
    id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_matricula INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_pago REAL NOT NULL,
    FOREIGN KEY (id_matricula) REFERENCES matricula(id_matricula),
    FOREIGN KEY (id_aluno) REFERENCES usuario(id)
)
"""

INSERIR = "INSERT INTO pagamento (id_matricula, id_aluno, valor_pago) VALUES (?, ?, ?)"

OBTER_POR_ALUNO = """
SELECT p.*, m.valor_mensalidade, u.nome as aluno_nome
FROM pagamento p
JOIN matricula m ON p.id_matricula = m.id_matricula
JOIN usuario u ON p.id_aluno = u.id
WHERE p.id_aluno = ?
ORDER BY p.data_pagamento DESC
"""

OBTER_POR_MATRICULA = "SELECT * FROM pagamento WHERE id_matricula = ?"
