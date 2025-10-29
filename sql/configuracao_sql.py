CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS configuracao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave TEXT UNIQUE NOT NULL,
    valor TEXT NOT NULL,
    descricao TEXT,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

INSERIR = "INSERT INTO configuracao (chave, valor, descricao) VALUES (?, ?, ?)"

OBTER_POR_CHAVE = "SELECT * FROM configuracao WHERE chave = ?"

OBTER_TODOS = "SELECT * FROM configuracao ORDER BY chave"

ATUALIZAR = """
UPDATE configuracao
SET valor = ?,
    data_atualizacao = CURRENT_TIMESTAMP
WHERE chave = ?
"""
