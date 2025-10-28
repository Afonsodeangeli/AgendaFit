"""
DTOs para validação de dados do sistema de chat.

IMPORTANTE - PADRÃO SUBSISTEMA COESO:
O sistema de Chat é implementado como um SUBSISTEMA COESO composto por 3 tabelas
interdependentes que funcionam como uma unidade:

1. chat_sala: Salas de conversação
2. chat_participante: Usuários em cada sala (many-to-many)
3. chat_mensagem: Mensagens trocadas nas salas

CARACTERÍSTICAS DESTE PADRÃO:

✅ DTOs CONSOLIDADOS:
   - Um único arquivo de DTOs para todo o subsistema (este arquivo)
   - Evita fragmentação de validações relacionadas

✅ ROTAS CONSOLIDADAS:
   - Um único arquivo de rotas: chat_routes.py
   - Todas as operações de chat em um lugar
   - Ex: criar_sala(), enviar_mensagem(), listar_mensagens()

✅ FORTE COESÃO:
   - As 3 tabelas sempre são usadas juntas
   - Raramente se acessa uma sem as outras
   - Formam um "módulo" lógico completo

✅ INTEGRIDADE REFERENCIAL:
   - ON DELETE CASCADE: Excluir sala → exclui participantes e mensagens
   - UNIQUE constraints: Um usuário não pode estar 2x na mesma sala

QUANDO USAR ESTE PADRÃO:
- Sistemas multi-tabela que formam uma funcionalidade completa
- Tabelas que raramente são acessadas isoladamente
- Exemplos: Carrinho de compras, Sistema de pedidos, Fórum (tópico+post+resposta)

QUANDO NÃO USAR:
- Entidades independentes (mesmo que relacionadas)
- CRUDs que podem ser acessados separadamente
"""
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

from dtos.validators import validar_string_obrigatoria, validar_comprimento


class CriarSalaDTO(BaseModel):
    """DTO para criar ou obter uma sala de chat."""
    outro_usuario_id: int

    @field_validator('outro_usuario_id')
    @classmethod
    def validar_outro_usuario_id(cls, v):
        if v <= 0:
            raise ValueError('ID do usuário deve ser um número positivo.')
        return v


class EnviarMensagemDTO(BaseModel):
    """DTO para enviar uma mensagem em uma sala."""
    sala_id: str
    mensagem: str

    _validar_sala_id = field_validator('sala_id')(validar_string_obrigatoria())
    _validar_mensagem = field_validator('mensagem')(validar_string_obrigatoria())
    _validar_comprimento = field_validator('mensagem')(validar_comprimento(tamanho_minimo=1, tamanho_maximo=5000))


class ConversaResumoDTO(BaseModel):
    """DTO para resumo de uma conversa na lista."""
    sala_id: str
    outro_usuario: dict  # {id, nome, email, foto_url}
    ultima_mensagem: Optional[dict] = None  # {mensagem, data_envio, usuario_id}
    nao_lidas: int = 0
    ultima_atividade: datetime


class UsuarioBuscaDTO(BaseModel):
    """DTO para resultado de busca de usuários."""
    id: int
    nome: str
    email: str
    foto_url: str
