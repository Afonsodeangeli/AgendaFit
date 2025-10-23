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
from util.rate_limiter import obter_identificador_cliente

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


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de categoria"""
    return templates.TemplateResponse(
        "admin/categorias/cadastrar.html",
        {
            "request": request,
        }
    )

@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(""),
    usuario_logado: Optional[dict] = None
):
    """Edita uma categoria existente"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_categorias_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se categoria existe
    categoria_atual = categoria_repo.obter_por_id(id)
    if not categoria_atual:
        informar_erro(request, "Categoria não encontrada")
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {"id": id, "nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = AlterarCategoriaDTO(id=id, nome=nome, descricao=descricao)

        # Atualizar categoria
        categoria_atualizada = Categoria(
            id=id,
            nome=dto.nome,
            descricao=dto.descricao
        )

        categoria_repo.alterar(categoria_atualizada)
        logger.info(f"Categoria {id} alterada por admin {usuario_logado['id']}")

        informar_sucesso(request, "Categoria alterada com sucesso!")
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["categoria"] = categoria_repo.obter_por_id(id)
        raise FormValidationError(
            validation_error=e,
            template_path="admin/categorias/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma categoria"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_categorias_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    categoria = categoria_repo.obter_por_id(id)

    if not categoria:
        informar_erro(request, "Categoria não encontrada")
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há atividades associadas a esta categoria
    from repo import atividade_repo
    atividades = atividade_repo.obter_por_categoria(id)
    if atividades:
        informar_erro(
            request,
            f"Não é possível excluir esta categoria pois há {len(atividades)} atividade(s) associada(s) a ela."
        )
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    categoria_repo.excluir(id)
    logger.info(f"Categoria {id} excluída por admin {usuario_logado['id']}")

    informar_sucesso(request, "Categoria excluída com sucesso!")
    return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(""),
    usuario_logado: Optional[dict] = None
):
    """Cadastra uma nova categoria"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_categorias_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário para reexibição em caso de erro
    dados_formulario: dict = {"nome": nome, "descricao": descricao}

    try:
        # Validar com DTO
        dto = CriarCategoriaDTO(nome=nome, descricao=descricao)

        # Criar categoria
        categoria = Categoria(
            id=0,
            nome=dto.nome,
            descricao=dto.descricao
        )

        categoria_repo.inserir(categoria)
        logger.info(f"Categoria '{dto.nome}' cadastrada por admin {usuario_logado['id']}")

        informar_sucesso(request, "Categoria cadastrada com sucesso!")
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="admin/categorias/cadastrar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )
