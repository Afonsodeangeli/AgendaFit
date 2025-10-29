from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from util.perfis import Perfil

@dataclass
class Usuario:
    """
    Model de usuário do AgendaFit.

    Representa qualquer usuário do sistema (admin, professor, aluno).
    O campo 'perfil' determina as permissões e funcionalidades disponíveis.

    Attributes:
        id: Identificador único do usuário
        nome: Nome completo do usuário
        email: Email único (usado para login)
        senha: Senha hasheada (nunca plaintext)
        perfil: Tipo de usuário ('admin', 'professor', 'aluno')
        token_redefinicao: Token para redefinição de senha (temporário)
        data_token: Data de expiração do token de redefinição
        data_cadastro: Data de criação do registro
        data_atualizacao: Data da última modificação

    Relacionamentos:
        - Turma (professor): ON DELETE RESTRICT
        - Matricula (aluno): ON DELETE RESTRICT
        - Tarefa: ON DELETE CASCADE
        - Chamado: ON DELETE CASCADE
        - Endereco: ON DELETE CASCADE
    """
    id: int
    nome: str
    email: str
    senha: str
    perfil: str
    token_redefinicao: Optional[str] = None
    data_token: Optional[datetime] = None
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
