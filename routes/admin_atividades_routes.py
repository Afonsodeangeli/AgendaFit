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

# Instância global de templates para este conjunto de rotas
templates = criar_templates("templates/admin/atividades")

@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as atividades cadastradas"""
    atividades = atividade_repo.obter_todas()
    categorias = categoria_repo.obter_todas()

    # Criar dicionário de categorias para lookup rápido
    # mapear nomes - alguns models usam id_categoria / id, ajustar defensivamente
    categorias_dict = {getattr(cat, 'id_categoria', getattr(cat, 'id', None)): getattr(cat, 'nome', '') for cat in categorias}

    return templates.TemplateResponse(
        "admin/atividades/listar.html",
        {
            "request": request,
            "atividades": atividades,
            "categorias_dict": categorias_dict
        }
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de atividade"""
    categorias = categoria_repo.obter_todas()

    if not categorias:
        informar_erro(request, "É necessário cadastrar pelo menos uma categoria antes de criar atividades.")
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/atividades/cadastrar.html",
        {
            "request": request,
            "categorias": categorias
        }
    )


@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(""),
    id_categoria: int = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Cadastra uma nova atividade"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_atividades_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {
        "nome": nome,
        "descricao": descricao,
        "id_categoria": id_categoria
    }

    try:
        # Validar com DTO
        dto = CriarAtividadeDTO(nome=nome, descricao=descricao, id_categoria=id_categoria)

        # Verificar se categoria existe
        categoria = categoria_repo.obter_por_id(dto.id_categoria)
        if not categoria:
            informar_erro(request, "Categoria selecionada não existe.")
            categorias = categoria_repo.obter_todas()
            return templates.TemplateResponse(
                "admin/atividades/cadastrar.html",
                {
                    "request": request,
                    "categorias": categorias,
                    "dados": dados_formulario
                }
            )

        # Criar atividade
        atividade = Atividade(
            id=0,
            nome=dto.nome,
            descricao=dto.descricao,
            id_categoria=dto.id_categoria
        )

        atividade_repo.inserir(atividade)
        logger.info(f"Atividade '{dto.nome}' cadastrada por admin {usuario_logado['id']}")

        informar_sucesso(request, "Atividade cadastrada com sucesso!")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["categorias"] = categoria_repo.obter_todas()
        raise FormValidationError(
            validation_error=e,
            template_path="admin/atividades/cadastrar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(""),
    id_categoria: int = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Edita uma atividade existente"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_atividades_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se atividade existe
    atividade_atual = atividade_repo.obter_por_id(id)
    if not atividade_atual:
        informar_erro(request, "Atividade não encontrada")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {
        "id": id,
        "nome": nome,
        "descricao": descricao,
        "id_categoria": id_categoria
    }

    try:
        # Validar com DTO
        dto = AlterarAtividadeDTO(
            id=id,
            nome=nome,
            descricao=descricao,
            id_categoria=id_categoria
        )

        # Verificar se categoria existe
        categoria = categoria_repo.obter_por_id(dto.id_categoria)
        if not categoria:
            informar_erro(request, "Categoria selecionada não existe.")
            categorias = categoria_repo.obter_todas()
            return templates.TemplateResponse(
                "admin/atividades/editar.html",
                {
                    "request": request,
                    "atividade": atividade_atual,
                    "categorias": categorias,
                    "dados": dados_formulario
                }
            )

        # Atualizar atividade
        atividade_atualizada = Atividade(
            id=id,
            nome=dto.nome,
            descricao=dto.descricao,
            id_categoria=dto.id_categoria
        )

        atividade_repo.alterar(atividade_atualizada)
        logger.info(f"Atividade {id} alterada por admin {usuario_logado['id']}")

        informar_sucesso(request, "Atividade alterada com sucesso!")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["atividade"] = atividade_repo.obter_por_id(id)
        dados_formulario["categorias"] = categoria_repo.obter_todas()
        raise FormValidationError(
            validation_error=e,
            template_path="admin/atividades/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma atividade"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_atividades_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    atividade = atividade_repo.obter_por_id(id)

    if not atividade:
        informar_erro(request, "Atividade não encontrada")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há turmas associadas a esta atividade
    from repo import turma_repo
    turmas = turma_repo.obter_por_atividade(id)
    if turmas:
        informar_erro(
            request,
            f"Não é possível excluir esta atividade pois há {len(turmas)} turma(s) associada(s) a ela."
        )
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    atividade_repo.excluir(id)
    logger.info(f"Atividade {id} excluída por admin {usuario_logado['id']}")

    informar_sucesso(request, "Atividade excluída com sucesso!")
    return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)
