# data_cadastro é preenchida automaticamente pelo banco via CURRENT_TIMESTAMP
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS atividade (
    id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

INSERIR = """
INSERT INTO atividade (nome, descricao)
VALUES (?, ?)
"""

ALTERAR = """
UPDATE atividade
SET nome = ?, descricao = ?, data_atualizacao = CURRENT_TIMESTAMP
WHERE id_atividade = ?
"""

EXCLUIR = "DELETE FROM atividade WHERE id_atividade = ?"

OBTER_POR_ID = """
SELECT *
FROM atividade
WHERE id_atividade = ?
"""

OBTER_TODAS = """
SELECT *
FROM atividade
ORDER BY nome
"""

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM atividade"