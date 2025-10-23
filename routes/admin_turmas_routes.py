"""
Rotas administrativas para gerenciamento de turmas.

Fornece CRUD completo de turmas para administradores.
"""
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from datetime import time

from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates
from util.logger_config import logger
from util.rate_limiter import RateLimiter, obter_identificador_cliente
from util.exceptions import FormValidationError

from repo import turma_repo, atividade_repo, usuario_repo
from model.turma_model import Turma
from dtos.turma_dto import CriarTurmaDTO, AlterarTurmaDTO

router = APIRouter(prefix="/admin/turmas")

# Rate limiter para operações administrativas
admin_turmas_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)

# Templates
templates = criar_templates("templates/admin/turmas")


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as turmas cadastradas"""
    turmas = turma_repo.obter_todos()
    atividades = atividade_repo.obter_todos()
    professores = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)

    # Criar dicionários para lookup
    atividades_dict = {ativ.id: ativ.nome for ativ in atividades}
    professores_dict = {prof.id: prof.nome for prof in professores}

    return templates.TemplateResponse(
        "admin/turmas/listar.html",
        {
            "request": request,
            "turmas": turmas,
            "atividades_dict": atividades_dict,
            "professores_dict": professores_dict
        }
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de turma"""
    atividades = atividade_repo.obter_todos()
    professores = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)

    if not atividades:
        informar_erro(request, "É necessário cadastrar pelo menos uma atividade antes de criar turmas.")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    if not professores:
        informar_erro(request, "É necessário cadastrar pelo menos um professor antes de criar turmas.")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/turmas/cadastrar.html",
        {
            "request": request,
            "atividades": atividades,
            "professores": professores
        }
    )
