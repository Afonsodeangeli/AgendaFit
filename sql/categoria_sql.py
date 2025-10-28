# IMPORTANTE: nome é UNIQUE - não permite categorias duplicadas
# data_cadastro e data_atualizacao são preenchidos automaticamente pelo banco
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

INSERIR = """
INSERT INTO categoria (nome, descricao)
VALUES (?, ?)
"""

ALTERAR = """
UPDATE categoria
SET nome = ?,
    descricao = ?,
    data_atualizacao = CURRENT_TIMESTAMP
WHERE id = ?
"""

EXCLUIR = "DELETE FROM categoria WHERE id = ?"

OBTER_POR_ID = "SELECT * FROM categoria WHERE id = ?"

OBTER_TODOS = "SELECT * FROM categoria ORDER BY nome"

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM categoria"