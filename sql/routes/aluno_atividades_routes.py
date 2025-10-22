from fastapi import APIRouter, Request
from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.template_util import criar_templates
from repo import atividade_repo

router = APIRouter(prefix="/aluno/atividades")
templates = criar_templates("templates/aluno/atividades")

@router.get("")
@requer_autenticacao([Perfil.ALUNO.value])
async def listar_atividades(request: Request):
    """Lista atividades disponíveis"""
    atividades = atividade_repo.obter_todas()
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "atividades": atividades
    })

@router.get("/{id}")
@requer_autenticacao([Perfil.ALUNO.value])
async def ver_atividade(request: Request, id: int):
    """Detalhes de uma atividade"""
    atividade = atividade_repo.obter_por_id(id)
    return templates.TemplateResponse("detalhes.html", {
        "request": request,
        "atividade": atividade
    })