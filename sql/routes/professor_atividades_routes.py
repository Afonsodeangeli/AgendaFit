from fastapi import APIRouter, Request
from util.auth_decorator import requer_professor
from util.template_util import criar_templates
from repo import atividade_repo

router = APIRouter(prefix="/professor/atividades")
templates = criar_templates("templates/professor/atividades")

@router.get("")
@requer_professor
async def listar_atividades(request: Request):
    """Lista atividades disponíveis para criar turmas"""
    atividades = atividade_repo.obter_todas()
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "atividades": atividades
    })

# Professor também pode ter endpoints para criar atividades se permitido