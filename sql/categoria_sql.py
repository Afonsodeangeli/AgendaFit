# IMPORTANTE: nome é UNIQUE - não permite categorias duplicadas
# data_cadastro é preenchida automaticamente pelo banco via CURRENT_TIMESTAMP
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

INSERIR = """
INSERT INTO categoria (nome, descricao)
VALUES (?, ?)
"""

ALTERAR = """
UPDATE categoria
SET nome = ?, descricao = ?
WHERE id_categoria = ?
"""

EXCLUIR = "DELETE FROM categoria WHERE id_categoria = ?"

OBTER_POR_ID = "SELECT * FROM categoria WHERE id_categoria = ?"

OBTER_TODAS = "SELECT * FROM categoria ORDER BY nome"

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM categoria"