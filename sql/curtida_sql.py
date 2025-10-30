CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS curtida (
    id_usuario INTEGER NOT NULL,
    id_atividade INTEGER NOT NULL,
    data_curtida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario, id_atividade),
    FOREIGN KEY (id_usuario) REFERENCES usuario (id),
    FOREIGN KEY (id_atividade) REFERENCES atividade (id)
)
"""

INSERIR = "INSERT INTO curtida (id_usuario, id_atividade) VALUES (?, ?)"
EXCLUIR = "DELETE FROM curtida WHERE id_usuario = ? AND id_atividade = ?"
OBTER_POR_ID = "SELECT * FROM curtida WHERE id_usuario = ? AND id_atividade = ?"
OBTER_QUANTIDADE_POR_ATIVIDADE = "SELECT COUNT(*) AS quantidade FROM curtida WHERE id_atividade = ?"