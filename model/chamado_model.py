from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class StatusChamado(Enum):
    ABERTO = "Aberto"
    EM_ANALISE = "Em Análise"
    RESOLVIDO = "Resolvido"
    FECHADO = "Fechado"

class PrioridadeChamado(Enum):
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"
    URGENTE = "Urgente"


@dataclass
class Chamado:
    """
    Model de chamado/ticket de suporte do AgendaFit.

    Representa um chamado aberto por um usuário para suporte.

    Attributes:
        id: Identificador único do chamado
        titulo: Título do chamado
        status: Status atual do chamado (Enum StatusChamado)
        prioridade: Prioridade do chamado (Enum PrioridadeChamado)
        usuario_id: ID do usuário que abriu o chamado
        data_cadastro: Data de abertura do chamado
        data_atualizacao: Data da última atualização do chamado
        data_fechamento: Data de fechamento do chamado
        usuario_nome: Nome do usuário (campo do JOIN)
        usuario_email: Email do usuário (campo do JOIN)
        mensagens_nao_lidas: Contador de mensagens não lidas
        tem_resposta_admin: Indica se há resposta de administrador
    """
    id: int
    titulo: str
    status: StatusChamado
    prioridade: PrioridadeChamado
    usuario_id: int
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    data_fechamento: Optional[datetime] = None
    # Campos do JOIN (para exibição)
    usuario_nome: Optional[str] = None
    usuario_email: Optional[str] = None
    mensagens_nao_lidas: int = 0
    tem_resposta_admin: bool = False
