"""
Rotas administrativas para gerenciamento de atividades.

Fornece CRUD completo de atividades para administradores.
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

from repo import atividade_repo, categoria_repo
from model.atividade_model import Atividade
from dtos.atividade_dto import CriarAtividadeDTO, AlterarAtividadeDTO

router = APIRouter(prefix="/admin/atividades")

# Rate limiter para operações administrativas
admin_atividades_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as atividades cadastradas"""
    atividades = atividade_repo.obter_todas()
    categorias = categoria_repo.obter_todas()

    # Criar dicionário de categorias para lookup rápido
    # mapear nomes - alguns models usam id_categoria / id, ajustar defensivamente
    categorias_dict = {getattr(cat, 'id_categoria', getattr(cat, 'id', None)): getattr(cat, 'nome', '') for cat in categorias}
    templates = criar_templates("templates/admin/atividades")

    return templates.TemplateResponse(
        "admin/atividades/listar.html",
        {
            "request": request,
            "atividades": atividades,
            "categorias_dict": categorias_dict
        }
    )
