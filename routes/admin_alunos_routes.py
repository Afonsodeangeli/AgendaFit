"""
Rotas administrativas para gerenciamento de alunos.

Fornece CRUD completo de alunos para administradores.
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
from util.rate_limiter import RateLimiter, obter_identificador_cliente
from util.exceptions import ErroValidacaoFormulario
from util.security import criar_hash_senha

from repo import usuario_repo
from model.usuario_model import Usuario
from dtos.aluno_dto import CriarAlunoDTO, AlterarAlunoDTO

router = APIRouter(prefix="/admin/alunos")

# Criar instancia de templates
templates = criar_templates("templates")

# Rate limiter para operações administrativas
admin_alunos_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)


def verificar_email_disponivel_aluno(email: str, id_excluir: Optional[int] = None) -> tuple[bool, str]:
    """Verifica se email está disponível para uso"""
    usuario_existente = usuario_repo.obter_por_email(email)

    if usuario_existente:
        # Se está editando, permitir o mesmo email
        if id_excluir and usuario_existente.id == id_excluir:
            return True, ""
        return False, "Este email já está cadastrado no sistema."

    return True, ""


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todos os alunos cadastrados"""
    alunos = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)

    return templates.TemplateResponse(
        "admin/alunos/listar.html",
        {
            "request": request,
            "alunos": alunos
        }
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de aluno"""
    return templates.TemplateResponse(
        "admin/alunos/cadastrar.html",
        {
            "request": request,
        }
    )


@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Cadastra um novo aluno"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_alunos_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {"nome": nome, "email": email}

    try:
        # Validar com DTO
        dto = CriarAlunoDTO(nome=nome, email=email, senha=senha)

        # Verificar se email já existe
        disponivel, mensagem_erro = verificar_email_disponivel_aluno(dto.email)
        if not disponivel:
            informar_erro(request, mensagem_erro)
            return templates.TemplateResponse(
                "admin/alunos/cadastrar.html",
                {
                    "request": request,
                    "dados": dados_formulario
                }
            )

        # Criar hash da senha
        senha_hash = criar_hash_senha(dto.senha)

        # Criar aluno
        aluno = Usuario(
            id=0,
            nome=dto.nome,
            email=dto.email,
            senha=senha_hash,
            perfil=Perfil.ALUNO.value
        )

        usuario_repo.inserir(aluno)
        logger.info(f"Aluno '{dto.email}' cadastrado por admin {usuario_logado['id']}")

        informar_sucesso(request, "Aluno cadastrado com sucesso!")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/alunos/cadastrar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de edição de aluno"""
    aluno = usuario_repo.obter_por_id(id)

    if not aluno or aluno.perfil != Perfil.ALUNO.value:
        informar_erro(request, "Aluno não encontrado")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Criar cópia dos dados sem senha
    dados_aluno = aluno.__dict__.copy()
    dados_aluno.pop('senha', None)

    return templates.TemplateResponse(
        "admin/alunos/editar.html",
        {
            "request": request,
            "aluno": aluno,
            "dados": dados_aluno
        }
    )


@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    nome: str = Form(...),
    email: str = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Edita um aluno existente"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_alunos_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se aluno existe
    aluno_atual = usuario_repo.obter_por_id(id)
    if not aluno_atual or aluno_atual.perfil != Perfil.ALUNO.value:
        informar_erro(request, "Aluno não encontrado")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {"id": id, "nome": nome, "email": email}

    try:
        # Validar com DTO
        dto = AlterarAlunoDTO(id=id, nome=nome, email=email)

        # Verificar se email já existe em outro usuário
        disponivel, mensagem_erro = verificar_email_disponivel_aluno(dto.email, id)
        if not disponivel:
            informar_erro(request, mensagem_erro)
            return templates.TemplateResponse(
                "admin/alunos/editar.html",
                {
                    "request": request,
                    "aluno": aluno_atual,
                    "dados": dados_formulario
                }
            )

        # Atualizar aluno
        aluno_atualizado = Usuario(
            id=id,
            nome=dto.nome,
            email=dto.email,
            senha=aluno_atual.senha,  # Mantém senha existente
            perfil=Perfil.ALUNO.value
        )

        usuario_repo.alterar(aluno_atualizado)
        logger.info(f"Aluno {id} alterado por admin {usuario_logado['id']}")

        informar_sucesso(request, "Aluno alterado com sucesso!")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["aluno"] = usuario_repo.obter_por_id(id)
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/alunos/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui um aluno"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_alunos_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    aluno = usuario_repo.obter_por_id(id)

    if not aluno or aluno.perfil != Perfil.ALUNO.value:
        informar_erro(request, "Aluno não encontrado")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há matrículas associadas a este aluno
    from repo import matricula_repo
    matriculas = matricula_repo.obter_por_aluno(id)
    if matriculas:
        informar_erro(
            request,
            f"Não é possível excluir este aluno pois há {len(matriculas)} matrícula(s) ativa(s)."
        )
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    usuario_repo.excluir(id)
    logger.info(f"Aluno {id} excluído por admin {usuario_logado['id']}")

    informar_sucesso(request, "Aluno excluído com sucesso!")
    return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de aluno"""
    return templates.TemplateResponse(
        "admin/alunos/cadastrar.html",
        {
            "request": request,
        }
    )
