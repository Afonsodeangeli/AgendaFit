from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from model.usuario_model import Usuario

@dataclass
class Endereco:
    """
    Model de endereço do AgendaFit.

    Representa endereços vinculados a usuários. Um usuário pode ter múltiplos endereços.

    Attributes:
        id_endereco: Identificador único do endereço
        id_usuario: FK para usuario
        titulo: Nome/descrição do endereço (ex: "Casa", "Trabalho")
        logradouro: Nome da rua/avenida
        numero: Número do imóvel
        complemento: Complemento (apto, bloco, etc)
        bairro: Bairro
        cidade: Cidade
        uf: Estado (sigla - 2 letras)
        cep: CEP (inteiro, sem formatação)
        usuario: Objeto Usuario relacionado (opcional, depende da query)

    Características:
        - ON DELETE CASCADE: Endereços são excluídos com o usuário
        - Sem timestamps: endereços não precisam auditoria temporal
        - Sem DTOs: Acessado apenas por rotas de usuario
        - Sem CRUD completo: Gerenciado como sub-recurso de usuario

    Padrão Child Entity:
        Acessado via /usuario/{id}/enderecos (não tem rotas próprias)
    """
    id_endereco: int
    id_usuario: int
    titulo: str
    logradouro: str
    numero: int
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: int

    usuario: Optional[Usuario]
    