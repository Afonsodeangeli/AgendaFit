"""
Rotas administrativas para gerenciamento de matrículas.

Fornece CRUD completo de matrículas para administradores.
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
from util.rate_limiter import RateLimiter
from util.exceptions import FormValidationError
from util.rate_limiter import obter_identificador_cliente

from repo import matricula_repo, usuario_repo, turma_repo
from model.matricula_model import Matricula
from dtos.matricula_dto import CriarMatriculaDTO, AlterarMatriculaDTO

router = APIRouter(prefix="/admin/matriculas")

# Rate limiter para operações administrativas
admin_matriculas_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)

# Templates
templates = criar_templates("templates/admin/matriculas")


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as matrículas cadastradas"""
    matriculas = matricula_repo.obter_todos()
    alunos = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
    turmas = turma_repo.obter_todos()

    # Criar dicionários para lookup
    alunos_dict = {aluno.id: aluno.nome for aluno in alunos}
    # turmas may not have 'nome' attribute if model differs; use defensively
    turmas_dict = {getattr(turma, 'id_turma', getattr(turma, 'id', None)): getattr(turma, 'nome', '') for turma in turmas}

    return templates.TemplateResponse(
        "admin/matriculas/listar.html",
        {
            "request": request,
            "matriculas": matriculas,
            "alunos_dict": alunos_dict,
            "turmas_dict": turmas_dict
        }
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de matrícula"""
    alunos = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
    turmas = turma_repo.obter_todos()

    if not alunos:
        informar_erro(request, "É necessário cadastrar pelo menos um aluno antes de criar matrículas.")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    if not turmas:
        informar_erro(request, "É necessário cadastrar pelo menos uma turma antes de criar matrículas.")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/matriculas/cadastrar.html",
        {
            "request": request,
            "alunos": alunos,
            "turmas": turmas
        }
    )
