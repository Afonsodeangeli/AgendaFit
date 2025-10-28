"""
DTOs para validação de dados de Aluno.

IMPORTANTE - PADRÃO FACADE:
Aluno NÃO é uma entidade separada no banco de dados. É um "facade" (fachada)
sobre a entidade Usuario com perfil=ALUNO. Esta decisão de design:

1. EVITA DUPLICAÇÃO: Não duplica a estrutura de tabelas/models para cada tipo de usuário
2. CENTRALIZA USUÁRIOS: Todos os usuários (admin, professor, aluno) estão na mesma tabela
3. ESPECIALIZA COMPORTAMENTO: DTOs e rotas específicas para alunos, mas reutilizam
   a infraestrutura de Usuario (repo, model, SQL)
4. SIMPLIFICA MANUTENÇÃO: Mudanças em Usuario automaticamente afetam Aluno

Este padrão deve ser seguido para outros "tipos especializados" de entidades base.
Por exemplo, se houver necessidade de "Administrador", use o mesmo padrão facade.

Arquivos relacionados:
- SQL/Model/Repo: Usa usuario_* (não existe aluno_*)
- DTOs: Este arquivo (aluno_dto.py) - especializado
- Routes: admin_alunos_routes.py - filtra por perfil=ALUNO
"""
from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_nome_pessoa,
    validar_email,
    validar_senha_forte,
    validar_id_positivo,
)


class CriarAlunoDTO(BaseModel):
    """DTO para criação de aluno"""

    nome: str
    email: str
    senha: str

    @field_validator("nome")
    @classmethod
    def _validar_nome(cls, v: str) -> str:
        return validar_nome_pessoa()(v)

    @field_validator("email")
    @classmethod
    def _validar_email(cls, v: str) -> str:
        return validar_email()(v)

    @field_validator("senha")
    @classmethod
    def _validar_senha(cls, v: str) -> str:
        return validar_senha_forte()(v)


class AlterarAlunoDTO(BaseModel):
    """DTO para alteração de aluno"""

    id: int
    nome: str
    email: str

    @field_validator("id")
    @classmethod
    def _validar_id(cls, v: int) -> int:
        return validar_id_positivo()(v)

    @field_validator("nome")
    @classmethod
    def _validar_nome(cls, v: str) -> str:
        return validar_nome_pessoa()(v)

    @field_validator("email")
    @classmethod
    def _validar_email(cls, v: str) -> str:
        return validar_email()(v)
