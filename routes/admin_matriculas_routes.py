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


@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    id_aluno: int = Form(...),
    id_turma: int = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Cadastra uma nova matrícula"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_matriculas_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {
        "id_aluno": id_aluno,
        "id_turma": id_turma
    }

    try:
        # Validar com DTO
        dto = CriarMatriculaDTO(id_aluno=id_aluno, id_turma=id_turma)

        # Verificar se aluno existe
        aluno = usuario_repo.obter_por_id(dto.id_aluno)
        if not aluno or aluno.perfil != Perfil.ALUNO.value:
            informar_erro(request, "Aluno selecionado não existe.")
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se turma existe
        turma = turma_repo.obter_por_id(dto.id_turma)
        if not turma:
            informar_erro(request, "Turma selecionada não existe.")
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se aluno já está matriculado nesta turma
        matricula_existente = matricula_repo.obter_por_aluno_e_turma(dto.id_aluno, dto.id_turma)
        if matricula_existente:
            informar_erro(request, "Este aluno já está matriculado nesta turma.")
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se há vagas disponíveis
        total_matriculas = len(matricula_repo.obter_por_turma(dto.id_turma))
        if total_matriculas >= turma.vagas:
            informar_erro(request, "Esta turma não possui vagas disponíveis.")
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Criar matrícula
        from datetime import datetime
        matricula = Matricula(
            id=0,
            id_aluno=dto.id_aluno,
            id_turma=dto.id_turma,
            data_matricula=datetime.now()
        )

        matricula_repo.inserir(matricula)
        logger.info(f"Matrícula criada: aluno {dto.id_aluno} na turma {dto.id_turma} por admin {usuario_logado['id']}")

        informar_sucesso(request, "Matrícula cadastrada com sucesso!")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
        dados_formulario["turmas"] = turma_repo.obter_todos()
        raise FormValidationError(
            validation_error=e,
            template_path="admin/matriculas/cadastrar.html",
            dados_formulario=dados_formulario,
            campo_padrao="id_aluno",
        )


@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de edição de matrícula"""
    matricula = matricula_repo.obter_por_id(id)

    if not matricula:
        informar_erro(request, "Matrícula não encontrada")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    alunos = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
    turmas = turma_repo.obter_todos()
    dados_matricula = matricula.__dict__.copy()

    return templates.TemplateResponse(
        "admin/matriculas/editar.html",
        {
            "request": request,
            "matricula": matricula,
            "dados": dados_matricula,
            "alunos": alunos,
            "turmas": turmas
        }
    )
