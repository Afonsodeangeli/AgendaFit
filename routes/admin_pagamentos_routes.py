"""
Rotas administrativas para gerenciamento de pagamentos.

Fornece CRUD completo de pagamentos para administradores.
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
from util.rate_limiter import RateLimiter, obter_identificador_cliente
from util.exceptions import ErroValidacaoFormulario

from repo import pagamento_repo, matricula_repo
from model.pagamento_model import Pagamento
from dtos.pagamento_dto import CriarPagamentoDTO, AlterarPagamentoDTO

router = APIRouter(prefix="/admin/pagamentos")

# Rate limiter para operações administrativas
admin_pagamentos_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)

# Templates
templates = criar_templates()


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todos os pagamentos cadastrados"""
    pagamentos = pagamento_repo.obter_todos()

    return templates.TemplateResponse(
        "admin/pagamentos/listar.html",
        {
            "request": request,
            "pagamentos": pagamentos
        }
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de pagamento"""
    matriculas = matricula_repo.obter_todos()

    if not matriculas:
        informar_erro(request, "É necessário ter pelo menos uma matrícula cadastrada antes de registrar pagamentos.")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/pagamentos/cadastrar.html",
        {
            "request": request,
            "matriculas": matriculas
        }
    )


@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    id_matricula: int = Form(...),
    valor_pago: float = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Cadastra um novo pagamento"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_pagamentos_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/pagamentos/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {
        "id_matricula": id_matricula,
        "valor_pago": valor_pago
    }

    try:
        # Validar com DTO
        dto = CriarPagamentoDTO(
            id_matricula=id_matricula,
            valor_pago=valor_pago
        )

        # Verificar se matrícula existe
        matricula = matricula_repo.obter_por_id(dto.id_matricula)
        if not matricula:
            informar_erro(request, "Matrícula selecionada não existe.")
            dados_formulario["matriculas"] = matricula_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/pagamentos/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Criar pagamento
        pagamento = Pagamento(
            id_pagamento=0,
            id_matricula=dto.id_matricula,
            id_aluno=matricula.id_aluno,
            data_pagamento=datetime.now(),
            valor_pago=dto.valor_pago,
            matricula=None,
            aluno=None
        )

        pagamento_repo.inserir(pagamento)
        logger.info(f"Pagamento criado: matrícula {dto.id_matricula}, valor R$ {dto.valor_pago} por admin {usuario_logado['id']}")

        informar_sucesso(request, "Pagamento registrado com sucesso!")
        return RedirectResponse("/admin/pagamentos/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["matriculas"] = matricula_repo.obter_todos()
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/pagamentos/cadastrar.html",
            dados_formulario=dados_formulario,
            campo_padrao="id_matricula",
        )


@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de edição de pagamento"""
    pagamento = pagamento_repo.obter_por_id(id)

    if not pagamento:
        informar_erro(request, "Pagamento não encontrado")
        return RedirectResponse("/admin/pagamentos/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Preparar dados para o template
    dados_pagamento = {
        "id_pagamento": pagamento.id_pagamento,
        "id_matricula": pagamento.id_matricula,
        "id_aluno": pagamento.id_aluno,
        "valor_pago": pagamento.valor_pago,
        "data_pagamento": pagamento.data_pagamento
    }

    return templates.TemplateResponse(
        "admin/pagamentos/editar.html",
        {
            "request": request,
            "pagamento": pagamento,
            "dados": dados_pagamento
        }
    )


@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    valor_pago: float = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Edita um pagamento existente (apenas o valor)"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_pagamentos_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/pagamentos/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se pagamento existe
    pagamento_atual = pagamento_repo.obter_por_id(id)
    if not pagamento_atual:
        informar_erro(request, "Pagamento não encontrado")
        return RedirectResponse("/admin/pagamentos/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {
        "id_pagamento": id,
        "valor_pago": valor_pago
    }

    try:
        # Validar com DTO
        dto = AlterarPagamentoDTO(
            id=id,
            valor_pago=valor_pago
        )

        # Atualizar pagamento
        pagamento_atualizado = Pagamento(
            id_pagamento=id,
            id_matricula=pagamento_atual.id_matricula,
            id_aluno=pagamento_atual.id_aluno,
            data_pagamento=pagamento_atual.data_pagamento,
            valor_pago=dto.valor_pago,
            matricula=None,
            aluno=None
        )

        pagamento_repo.alterar(pagamento_atualizado)
        logger.info(f"Pagamento {id} alterado por admin {usuario_logado['id']}")

        informar_sucesso(request, "Pagamento alterado com sucesso!")
        return RedirectResponse("/admin/pagamentos/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["pagamento"] = pagamento_repo.obter_por_id(id)
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/pagamentos/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="valor_pago",
        )


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui um pagamento"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_pagamentos_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/pagamentos/listar", status_code=status.HTTP_303_SEE_OTHER)

    pagamento = pagamento_repo.obter_por_id(id)

    if not pagamento:
        informar_erro(request, "Pagamento não encontrado")
        return RedirectResponse("/admin/pagamentos/listar", status_code=status.HTTP_303_SEE_OTHER)

    pagamento_repo.excluir(id)
    logger.info(f"Pagamento {id} excluído por admin {usuario_logado['id']}")

    informar_sucesso(request, "Pagamento excluído com sucesso!")
    return RedirectResponse("/admin/pagamentos/listar", status_code=status.HTTP_303_SEE_OTHER)
