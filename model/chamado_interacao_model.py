from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from model.chamado_model import StatusChamado


class TipoInteracao(Enum):
    ABERTURA = "Abertura"
    RESPOSTA_USUARIO = "Resposta do Usuário"
    RESPOSTA_ADMIN = "Resposta do Administrador"


@dataclass
class ChamadoInteracao:
    """
    Model de interação/mensagem em um chamado de suporte.

    IMPORTANTE - PADRÃO CHILD ENTITY (Entidade Filha/Dependente):
    ChamadoInteracao é uma entidade FILHA de Chamado. Características deste padrão:

    1. SEMPRE VINCULADA AO PAI: Não existe sem um Chamado associado (chamado_id NOT NULL)
    2. CASCADE DELETE: Quando Chamado é excluído, suas interações são excluídas automaticamente
    3. SEM ROTAS PRÓPRIAS: Não possui admin_chamado_interacao_routes.py
       - Acessada sempre através das rotas de Chamado
       - Ex: /chamados/{id}/adicionar_mensagem
    4. OPERAÇÕES LIMITADAS: Geralmente apenas INSERT e SELECT
       - Mensagens são imutáveis (não há UPDATE/DELETE individual)
       - Exclusão só via cascade do pai

    Este padrão deve ser seguido para outras entidades filhas, como:
    - Itens de pedido (pedido → item_pedido)
    - Respostas de avaliação (avaliacao → resposta)
    - Histórico de alterações (entidade → historico_alteracao)

    Attributes:
        id: Identificador único da interação
        chamado_id: ID do chamado pai (FOREIGN KEY obrigatória)
        usuario_id: ID do usuário que criou a interação
        mensagem: Conteúdo da mensagem
        tipo: Tipo da interação (Enum TipoInteracao)
        data_interacao: Data/hora da interação
        status_resultante: Status do chamado após esta interação
        data_leitura: Data/hora em que a mensagem foi lida
        usuario_nome: Nome do usuário (campo do JOIN)
        usuario_email: Email do usuário (campo do JOIN)
    """
    id: int
    chamado_id: int
    usuario_id: int
    mensagem: str
    tipo: TipoInteracao
    data_interacao: datetime
    status_resultante: Optional[StatusChamado] = None
    data_leitura: Optional[datetime] = None
    # Campos do JOIN (para exibição)
    usuario_nome: Optional[str] = None
    usuario_email: Optional[str] = None
