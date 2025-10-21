from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_decorator import requer_admin
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.exceptions import FormValidationError
from dtos.categoria_dto import CategoriaCreateDTO, CategoriaUpdateDTO
from model.categoria_model import Categoria
from repo import categoria_repo

router = APIRouter(prefix="/admin/categorias")
templates = criar_templates("templates/admin/categorias")

@router.get("")
@requer_admin
async def listar_categorias(request: Request):
    """Lista todas as categorias"""
    categorias = categoria_repo.obter_todas()
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "categorias": categorias
    })

@router.get("/nova")
@requer_admin
async def get_nova_categoria(request: Request):
    """Formulário de nova categoria"""
    return templates.TemplateResponse("form.html", {
        "request": request,
        "titulo": "Nova Categoria"
    })

@router.post("/nova")
@requer_admin
async def post_nova_categoria(
    request: Request,
    nome: str = Form(),
    descricao: str = Form()
):
    """Cria nova categoria"""
    try:
        dto = CategoriaCreateDTO(nome=nome, descricao=descricao)
        categoria = Categoria(id_categoria=0, nome=dto.nome, descricao=dto.descricao)

        id_categoria = categoria_repo.inserir(categoria)
        if id_categoria:
            informar_sucesso(request, "Categoria criada com sucesso!")
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

        raise FormValidationError({"geral": "Erro ao criar categoria"})

    except ValidationError as e:
        erros = {err['loc'][0]: err['msg'] for err in e.errors()}
        raise FormValidationError(erros)

@router.get("/{id}/editar")
@requer_admin
async def get_editar_categoria(request: Request, id: int):
    """Formulário de edição"""
    categoria = categoria_repo.obter_por_id(id)
    if not categoria:
        informar_erro(request, "Categoria não encontrada")
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("form.html", {
        "request": request,
        "categoria": categoria,
        "titulo": "Editar Categoria"
    })

@router.post("/{id}/editar")
@requer_admin
async def post_editar_categoria(
    request: Request,
    id: int,
    nome: str = Form(),
    descricao: str = Form()
):
    """Atualiza categoria"""
    try:
        dto = CategoriaUpdateDTO(nome=nome, descricao=descricao)
        categoria = Categoria(id_categoria=id, nome=dto.nome, descricao=dto.descricao)

        if categoria_repo.alterar(categoria):
            informar_sucesso(request, "Categoria atualizada com sucesso!")
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

        raise FormValidationError({"geral": "Erro ao atualizar categoria"})

    except ValidationError as e:
        erros = {err['loc'][0]: err['msg'] for err in e.errors()}
        raise FormValidationError(erros)

@router.post("/{id}/excluir")
@requer_admin
async def excluir_categoria(request: Request, id: int):
    """Exclui categoria"""
    if categoria_repo.excluir(id):
        informar_sucesso(request, "Categoria excluída com sucesso!")
    else:
        informar_erro(request, "Erro ao excluir categoria")

    return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)