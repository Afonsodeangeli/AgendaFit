from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from model.matricula_model import Matricula
from model.usuario_model import Usuario

@dataclass
class Pagamento:
    """
    Model de pagamento do AgendaFit.

    Representa pagamentos de mensalidades efetuados por alunos.

    Attributes:
        id_pagamento: Identificador único do pagamento
        id_matricula: FK para matricula
        id_aluno: FK para usuario (perfil 'aluno')
        data_pagamento: Data/hora do pagamento (auto)
        valor_pago: Valor efetivamente pago
        matricula: Objeto Matricula relacionado (opcional, depende da query)
        aluno: Objeto Usuario relacionado (opcional, depende da query)

    Características:
        - ON DELETE RESTRICT em ambos FKs: Não pode excluir matricula/aluno com pagamentos
        - data_pagamento automático via DEFAULT CURRENT_TIMESTAMP
        - Registro imutável: pagamentos não são editados após criação
        - Sem timestamps de auditoria: data_pagamento é suficiente
        - Sem CRUD completo: Apenas inserção e consulta

    Padrão:
        Tabela append-only (histórico financeiro)
    """
    id_pagamento: int
    id_matricula: int
    id_aluno: int
    data_pagamento: datetime
    valor_pago: float
    matricula: Optional[Matricula]
    aluno: Optional[Usuario]