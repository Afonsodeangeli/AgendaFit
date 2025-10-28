from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Tarefa:
    """
    Model de tarefa do AgendaFit.

    Representa uma tarefa/to-do de um usuário.

    Attributes:
        id: Identificador único da tarefa
        titulo: Título da tarefa
        descricao: Descrição detalhada da tarefa
        concluida: Indica se a tarefa foi concluída
        usuario_id: ID do usuário dono da tarefa
        data_cadastro: Data de criação da tarefa
        data_atualizacao: Data da última atualização da tarefa
        data_conclusao: Data de conclusão da tarefa
        usuario_nome: Nome do usuário (campo do JOIN)
        usuario_email: Email do usuário (campo do JOIN)
    """
    id: int
    titulo: str
    descricao: str
    concluida: bool
    usuario_id: int
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None
    # Campos do JOIN (para exibição)
    usuario_nome: Optional[str] = None
    usuario_email: Optional[str] = None
