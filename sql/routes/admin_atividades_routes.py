from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from datetime import datetime

from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.exceptions import FormValidationError
from sql.dtos.atividade_dto import AtividadeCreateDTO, AtividadeUpdateDTO
from model.Atividade_model import Atividade
from sql.repo import atividade_repo, categoria_repo

router = APIRouter(prefix="/admin/atividades")
templates = criar_templates("templates/admin/atividades")

@router.get("")
@requer_autenticacao([Perfil.ADMIN.value])
async def listar_atividades(request: Request):
    atividades = atividade_repo.obter_todas()
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "atividades": atividades
    })

@router.get("/nova")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_nova_atividade(request: Request):
    categorias = categoria_repo.obter_todas()
    return templates.TemplateResponse("form.html", {
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
    descricao: str = Form()
):
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

        raise FormValidationError({"geral": "Erro ao criar atividade"})

    except ValidationError as e:
        erros = {err['loc'][0]: err['msg'] for err in e.errors()}
        raise FormValidationError(erros)

# Demais métodos (editar, excluir) seguem o mesmo padrão das categorias