"""
Rotas administrativas para gerenciamento de alunos.

Fornece CRUD completo de alunos para administradores.
"""
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates
from util.logger_config import logger
from util.rate_limiter import RateLimiter, obter_identificador_cliente
from util.exceptions import FormValidationError
from util.security import criar_hash_senha

from repo import usuario_repo
from model.usuario_model import Usuario
from dtos.aluno_dto import CriarAlunoDTO, AlterarAlunoDTO

router = APIRouter(prefix="/admin/alunos")

# Criar instancia de templates
templates = criar_templates("templates")

# Rate limiter para operações administrativas
admin_alunos_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)


def verificar_email_disponivel_aluno(email: str, id_excluir: Optional[int] = None) -> tuple[bool, str]:
    """Verifica se email está disponível para uso"""
    usuario_existente = usuario_repo.obter_por_email(email)

    if usuario_existente:
        # Se está editando, permitir o mesmo email
        if id_excluir and usuario_existente.id == id_excluir:
            return True, ""
        return False, "Este email já está cadastrado no sistema."

    return True, ""


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todos os alunos cadastrados"""
    alunos = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)

    return templates.TemplateResponse(
        "admin/alunos/listar.html",
        {
            "request": request,
            "alunos": alunos
        }
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de aluno"""
    return templates.TemplateResponse(
        "admin/alunos/cadastrar.html",
        {
            "request": request,
        }
    )
