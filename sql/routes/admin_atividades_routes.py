from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from datetime import datetime

from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.exceptions import FormValidationError
from dtos.atividade_dto import AtividadeCreateDTO, AtividadeUpdateDTO
from model.atividade_model import Atividade
from repo import atividade_repo, categoria_repo

router = APIRouter(prefix="/admin/atividades")
templates = criar_templates("templates/admin/atividades")

@router.get("")
@requer_autenticacao([Perfil.ADMIN.value])
async def listar_atividades(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as atividades"""
    atividades = atividade_repo.obter_todas()
    return templates.TemplateResponse("admin/atividades/lista.html", {
        "request": request,
        "atividades": atividades
    })

@router.get("/nova")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_nova_atividade(request: Request, usuario_logado: Optional[dict] = None):
    """Formulário de nova atividade"""
    categorias = categoria_repo.obter_todas()
    return templates.TemplateResponse("admin/atividades/form.html", {
        "request": request,
        "categorias": categorias,
        "titulo": "Nova Atividade"
    })

@router.post("/nova")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_nova_atividade(
    request: Request,
    id_categoria: int = Form(),
    nome: str = Form(),
    descricao: str = Form(),
    usuario_logado: Optional[dict] = None
):
    """Cria nova atividade"""
    try:
        dto = AtividadeCreateDTO(id_categoria=id_categoria, nome=nome, descricao=descricao)
        atividade = Atividade(
            id_atividade=0,
            id_categoria=dto.id_categoria,
            nome=dto.nome,
            descricao=dto.descricao,
            data_cadastro=datetime.now(),
            categoria=None
        )

        if atividade_repo.inserir(atividade):
            informar_sucesso(request, "Atividade criada com sucesso!")
            return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)

        informar_erro(request, "Erro ao criar atividade")
        return RedirectResponse("/admin/atividades/nova", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = e.errors()
        mensagem = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in erros])
        informar_erro(request, f"Erro de validação: {mensagem}")
        return RedirectResponse("/admin/atividades/nova", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/{id}/editar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar_atividade(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Formulário de edição"""
    atividade = atividade_repo.obter_por_id(id)
    if not atividade:
        informar_erro(request, "Atividade não encontrada")
        return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)

    categorias = categoria_repo.obter_todas()
    return templates.TemplateResponse("admin/atividades/form.html", {
        "request": request,
        "atividade": atividade,
        "categorias": categorias,
        "titulo": "Editar Atividade"
    })

@router.post("/{id}/editar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar_atividade(
    request: Request,
    id: int,
    id_categoria: int = Form(),
    nome: str = Form(),
    descricao: str = Form(),
    usuario_logado: Optional[dict] = None
):
    """Atualiza atividade"""
    try:
        dto = AtividadeUpdateDTO(id_categoria=id_categoria, nome=nome, descricao=descricao)
        atividade_existente = atividade_repo.obter_por_id(id)
        if not atividade_existente:
            raise FormValidationError({"geral": "Atividade não encontrada"})

        atividade = Atividade(
            id_atividade=id,
            id_categoria=dto.id_categoria,
            nome=dto.nome,
            descricao=dto.descricao,
            data_cadastro=atividade_existente.data_cadastro,
            categoria=None
        )

        if atividade_repo.alterar(atividade):
            informar_sucesso(request, "Atividade atualizada com sucesso!")
            return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)

        informar_erro(request, "Erro ao atualizar atividade")
        return RedirectResponse(f"/admin/atividades/{id}/editar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = e.errors()
        mensagem = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in erros])
        informar_erro(request, f"Erro de validação: {mensagem}")
        return RedirectResponse("/admin/atividades/nova", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/{id}/excluir")
@requer_autenticacao([Perfil.ADMIN.value])
async def excluir_atividade(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui atividade"""
    if atividade_repo.excluir(id):
        informar_sucesso(request, "Atividade excluída com sucesso!")
    else:
        informar_erro(request, "Erro ao excluir atividade")

    return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)