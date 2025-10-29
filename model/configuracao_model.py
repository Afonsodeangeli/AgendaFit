from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Configuracao:
    """
    Model de configuração do AgendaFit.

    Segue padrão Key-Value Store para configurações dinâmicas do sistema.

    Attributes:
        id: Identificador único (autoincrement)
        chave: Chave única identificadora (ex: 'theme', 'nome_sistema')
        valor: Valor da configuração (string)
        descricao: Descrição opcional explicando uso da configuração
        data_atualizacao: Data da última modificação do valor

    Características:
        - Chave UNIQUE: Identificador principal da configuração
        - Query principal: obter_por_chave() (não obter_por_id)
        - Operação comum: inserir_ou_atualizar() (upsert pattern)
        - data_atualizacao: Rastreia quando valor foi alterado
        - Sem data_cadastro: chave é imutável, apenas valor muda
        - Sem ON DELETE: tabela independente

    Exemplo:
        >>> # Buscar sempre por chave
        >>> config = obter_por_chave("theme")
        >>> print(config.valor)  # "original"
    """
    id: int
    chave: str
    valor: str
    descricao: Optional[str] = None
    data_atualizacao: Optional[datetime] = None
