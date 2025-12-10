"""
Rotas administrativas para gerenciamento de atividades.

Fornece CRUD completo de atividades para administradores.
"""
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.flash_messages import informar_sucesso, informar_erro
from util.template_util import criar_templates
from util.logger_config import logger
from util.rate_limiter import RateLimiter
from util.exceptions import ErroValidacaoFormulario
from util.rate_limiter import obter_identificador_cliente

from repo import atividade_repo, categoria_repo
from model.atividade_model import Atividade
from dtos.atividade_dto import CriarAtividadeDTO, AlterarAtividadeDTO

router = APIRouter(prefix="/admin/atividades")

# Rate limiter para operações administrativas
admin_atividades_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)

# Instância global de templates para este conjunto de rotas
templates = criar_templates()

@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as atividades cadastradas"""
    atividades = atividade_repo.obter_todas()

    return templates.TemplateResponse(
        "admin/atividades/listar.html",
        {
            "request": request,
            "atividades": atividades
        }
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de atividade"""
    categorias = categoria_repo.obter_todas()
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
    id_categoria: Optional[int] = Form(None),
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

        # Criar atividade
        atividade = Atividade(
            id_atividade=0,
            id_categoria=dto.id_categoria,
            nome=dto.nome,
            descricao=dto.descricao,
            data_cadastro=datetime.now()
        )

        atividade_repo.inserir(atividade)
        logger.info(f"Atividade '{dto.nome}' cadastrada por admin {usuario_logado.id}")

        informar_sucesso(request, "Atividade cadastrada com sucesso!")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["categorias"] = categoria_repo.obter_todas()
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/atividades/cadastrar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de edição de atividade"""
    atividade = atividade_repo.obter_por_id(id)

    if not atividade:
        informar_erro(request, "Atividade não encontrada")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    categorias = categoria_repo.obter_todas()

    return templates.TemplateResponse(
        "admin/atividades/editar.html",
        {
            "request": request,
            "atividade": atividade,
            "categorias": categorias,
            "dados": {
                "id": atividade.id_atividade,
                "id_categoria": atividade.id_categoria,
                "nome": atividade.nome,
                "descricao": atividade.descricao
            }
        }
    )


@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(""),
    id_categoria: Optional[int] = Form(None),
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
        "id_categoria": id_categoria,
        "nome": nome,
        "descricao": descricao
    }

    try:
        # Validar com DTO
        dto = AlterarAtividadeDTO(
            id=id,
            id_categoria=id_categoria,
            nome=nome,
            descricao=descricao
        )

        # Atualizar atividade
        atividade_atualizada = Atividade(
            id_atividade=id,
            id_categoria=dto.id_categoria,
            nome=dto.nome,
            descricao=dto.descricao,
            data_cadastro=atividade_atual.data_cadastro
        )

        atividade_repo.alterar(atividade_atualizada)
        logger.info(f"Atividade {id} alterada por admin {usuario_logado.id}")

        informar_sucesso(request, "Atividade alterada com sucesso!")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["atividade"] = atividade_atual
        dados_formulario["categorias"] = categoria_repo.obter_todas()
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/atividades/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.get("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe página de confirmação de exclusão (fallback)"""
    atividade = atividade_repo.obter_por_id(id)

    if not atividade:
        informar_erro(request, "Atividade não encontrada")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há turmas associadas
    from repo import turma_repo
    todas_turmas = turma_repo.obter_todas()
    turmas_atividade = [t for t in todas_turmas if t.id_atividade == id]
    if turmas_atividade:
        informar_erro(
            request,
            f"Não é possível excluir esta atividade pois há {len(turmas_atividade)} turma(s) associada(s) a ela."
        )
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Se chegar aqui, proceeder com exclusão (fallback para GET)
    atividade_repo.excluir(id)
    logger.info(f"Atividade {id} excluída por admin {usuario_logado.id} (via GET fallback)")

    informar_sucesso(request, "Atividade excluída com sucesso!")
    return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)


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
    todas_turmas = turma_repo.obter_todas()
    turmas_atividade = [t for t in todas_turmas if t.id_atividade == id]
    if turmas_atividade:
        informar_erro(
            request,
            f"Não é possível excluir esta atividade pois há {len(turmas_atividade)} turma(s) associada(s) a ela."
        )
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    atividade_repo.excluir(id)
    logger.info(f"Atividade {id} excluída por admin {usuario_logado.id}")

    informar_sucesso(request, "Atividade excluída com sucesso!")
    return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)
