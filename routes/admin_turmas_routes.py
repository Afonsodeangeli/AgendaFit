from typing import Optional
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.exceptions import FormValidationError
from dtos.turma_dto import TurmaCreateDTO
from model.turma_model import Turma
from repo import turma_repo, atividade_repo, usuario_repo

router = APIRouter(prefix="/admin/turmas")
templates = criar_templates("templates/admin/turmas")


@router.get("")
@requer_autenticacao([Perfil.ADMIN.value])
async def listar_turmas(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as turmas"""
    turmas = turma_repo.obter_todas()
    return templates.TemplateResponse("admin/turmas/lista.html", {"request": request, "turmas": turmas})


@router.get("/nova")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_nova_turma(request: Request, usuario_logado: Optional[dict] = None):
    """Formulário de nova turma"""
    atividades = atividade_repo.obter_todas()
    # tentar obter apenas professores, se existir função específica
    try:
        professores = usuario_repo.obter_todos_por_perfil("PROFESSOR")
    except Exception:
        professores = usuario_repo.obter_todos()

    return templates.TemplateResponse("admin/turmas/form.html", {
        "request": request,
        "atividades": atividades,
        "professores": professores,
        "titulo": "Nova Turma"
    })


@router.post("/nova")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_nova_turma(
    request: Request,
    id_atividade: int = Form(),
    id_professor: int = Form(),
    usuario_logado: Optional[dict] = None
):
    """Cria nova turma"""
    try:
        dto = TurmaCreateDTO(id_atividade=id_atividade, id_professor=id_professor)
        turma = Turma(
            id_turma=0,
            id_atividade=dto.id_atividade,
            id_professor=dto.id_professor,
            data_cadastro=None,
            atividade=None,
            professor=None
        )

        if turma_repo.inserir(turma):
            informar_sucesso(request, "Turma criada com sucesso!")
            return RedirectResponse("/admin/turmas", status_code=status.HTTP_303_SEE_OTHER)

        informar_erro(request, "Erro ao criar turma")
        return RedirectResponse("/admin/turmas/nova", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = e.errors()
        mensagem = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in erros])
        informar_erro(request, f"Erro de validação: {mensagem}")
        return RedirectResponse("/admin/turmas/nova", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{id}/editar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar_turma(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Formulário de edição"""
    turma = turma_repo.obter_por_id(id)
    if not turma:
        informar_erro(request, "Turma não encontrada")
        return RedirectResponse("/admin/turmas", status_code=status.HTTP_303_SEE_OTHER)

    atividades = atividade_repo.obter_todas()
    try:
        professores = usuario_repo.obter_todos_por_perfil("PROFESSOR")
    except Exception:
        professores = usuario_repo.obter_todos()

    return templates.TemplateResponse("admin/turmas/form.html", {
        "request": request,
        "turma": turma,
        "atividades": atividades,
        "professores": professores,
        "titulo": "Editar Turma"
    })


@router.post("/{id}/editar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar_turma(
    request: Request,
    id: int,
    id_atividade: int = Form(),
    id_professor: int = Form(),
    usuario_logado: Optional[dict] = None
):
    """Atualiza turma"""
    try:
        dto = TurmaCreateDTO(id_atividade=id_atividade, id_professor=id_professor)
        turma = Turma(
            id_turma=id,
            id_atividade=dto.id_atividade,
            id_professor=dto.id_professor,
            data_cadastro=None,
            atividade=None,
            professor=None
        )

        if turma_repo.alterar(turma):
            informar_sucesso(request, "Turma atualizada com sucesso!")
            return RedirectResponse("/admin/turmas", status_code=status.HTTP_303_SEE_OTHER)

        informar_erro(request, "Erro ao atualizar turma")
        return RedirectResponse(f"/admin/turmas/{id}/editar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = e.errors()
        mensagem = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in erros])
        informar_erro(request, f"Erro de validação: {mensagem}")
        return RedirectResponse("/admin/turmas/nova", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{id}/excluir")
@requer_autenticacao([Perfil.ADMIN.value])
async def excluir_turma(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui turma"""
    if turma_repo.excluir(id):
        informar_sucesso(request, "Turma excluída com sucesso!")
    else:
        informar_erro(request, "Erro ao excluir turma")

    return RedirectResponse("/admin/turmas", status_code=status.HTTP_303_SEE_OTHER)
