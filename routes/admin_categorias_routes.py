"""
Rotas administrativas para gerenciamento de categorias.

Fornece CRUD completo de categorias para administradores.
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

from repo import categoria_repo
from model.categoria_model import Categoria
from dtos.categoria_dto import CriarCategoriaDTO, AlterarCategoriaDTO

router = APIRouter(prefix="/admin/categorias")

# Criar instância de templates configurada
templates = criar_templates("templates")

# Rate limiter para operações administrativas
admin_categorias_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as categorias cadastradas"""
    categorias = categoria_repo.obter_todos()

    return templates.TemplateResponse(
        "admin/categorias/listar.html",
        {
            "request": request,
            "categorias": categorias
        }
    )
