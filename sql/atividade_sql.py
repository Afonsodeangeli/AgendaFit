# IMPORTANTE: id_categoria é FOREIGN KEY - deve existir em categoria
# data_cadastro é preenchida automaticamente pelo banco via CURRENT_TIMESTAMP
# Queries com JOIN retornam campos prefixados: categoria_nome, categoria_descricao
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS atividade (
    id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria) ON DELETE RESTRICT
)
"""

INSERIR = """
INSERT INTO atividade (id_categoria, nome, descricao)
VALUES (?, ?, ?)
"""

ALTERAR = """
UPDATE atividade
SET id_categoria = ?, nome = ?, descricao = ?, data_atualizacao = CURRENT_TIMESTAMP
WHERE id_atividade = ?
"""

EXCLUIR = "DELETE FROM atividade WHERE id_atividade = ?"

OBTER_POR_ID = """
SELECT a.*, c.nome as categoria_nome, c.descricao as categoria_descricao
FROM atividade a
JOIN categoria c ON a.id_categoria = c.id_categoria
WHERE a.id_atividade = ?
"""

OBTER_TODAS = """
SELECT a.*, c.nome as categoria_nome, c.descricao as categoria_descricao
FROM atividade a
JOIN categoria c ON a.id_categoria = c.id_categoria
ORDER BY c.nome, a.nome
"""

OBTER_POR_CATEGORIA = """
SELECT a.*, c.nome as categoria_nome, c.descricao as categoria_descricao
FROM atividade a
JOIN categoria c ON a.id_categoria = c.id_categoria
WHERE a.id_categoria = ?
ORDER BY a.nome
"""

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM atividade"