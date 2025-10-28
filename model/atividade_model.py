from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.categoria_model import Categoria


@dataclass
class Atividade:
    """
    Model de atividade física/esportiva do AgendaFit.

    Attributes:
        id_atividade: Identificador único da atividade
        id_categoria: ID da categoria à qual pertence esta atividade
        nome: Nome da atividade
        descricao: Descrição detalhada da atividade
        data_cadastro: Data de cadastro da atividade
        data_atualizacao: Data da última atualização da atividade
        categoria: Objeto Categoria relacionado (opcional, carregado via JOIN)
    """
    id_atividade: int
    id_categoria: int
    nome: str
    descricao: str
    data_cadastro: datetime
    data_atualizacao: Optional[datetime] = None

    categoria: Optional[Categoria] = None
