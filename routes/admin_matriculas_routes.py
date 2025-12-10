"""
Rotas administrativas para gerenciamento de matrículas.

Fornece CRUD completo de matrículas para administradores.
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

from repo import matricula_repo, usuario_repo, turma_repo
from model.matricula_model import Matricula
from dtos.matricula_dto import CriarMatriculaDTO, AlterarMatriculaDTO

router = APIRouter(prefix="/admin/matriculas")

# Rate limiter para operações administrativas
admin_matriculas_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)

# Templates
templates = criar_templates()


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as matrículas cadastradas"""
    matriculas = matricula_repo.obter_todos()

    return templates.TemplateResponse(
        "admin/matriculas/listar.html",
        {
            "request": request,
            "matriculas": matriculas
        }
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de matrícula"""
    alunos = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
    turmas = turma_repo.obter_todos()

    if not alunos:
        informar_erro(request, "É necessário cadastrar pelo menos um aluno antes de criar matrículas.")
        return RedirectResponse("/admin/alunos/listar", status_code=status.HTTP_303_SEE_OTHER)

    if not turmas:
        informar_erro(request, "É necessário cadastrar pelo menos uma turma antes de criar matrículas.")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/matriculas/cadastrar.html",
        {
            "request": request,
            "alunos": alunos,
            "turmas": turmas
        }
    )


@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    id_aluno: int = Form(...),
    id_turma: int = Form(...),
    valor_mensalidade: float = Form(...),
    dia_vencimento: int = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Cadastra uma nova matrícula"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_matriculas_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {
        "id_aluno": id_aluno,
        "id_turma": id_turma,
        "valor_mensalidade": valor_mensalidade,
        "dia_vencimento": dia_vencimento
    }

    try:
        # Validar com DTO
        dto = CriarMatriculaDTO(
            id_aluno=id_aluno,
            id_turma=id_turma,
            valor_mensalidade=valor_mensalidade,
            dia_vencimento=dia_vencimento
        )

        # Verificar se aluno existe
        aluno = usuario_repo.obter_por_id(dto.id_aluno)
        if not aluno or aluno.perfil != Perfil.ALUNO.value:
            informar_erro(request, "Aluno selecionado não existe.")
            dados_formulario["alunos"] = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se turma existe
        turma = turma_repo.obter_por_id(dto.id_turma)
        if not turma:
            informar_erro(request, "Turma selecionada não existe.")
            dados_formulario["alunos"] = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se aluno já está matriculado nesta turma
        matricula_existente = matricula_repo.obter_por_aluno_e_turma(dto.id_aluno, dto.id_turma)
        if matricula_existente:
            informar_erro(request, "Este aluno já está matriculado nesta turma.")
            dados_formulario["alunos"] = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se há vagas disponíveis
        total_matriculas = len(matricula_repo.obter_por_turma(dto.id_turma))
        if total_matriculas >= turma.vagas:
            informar_erro(request, "Esta turma não possui vagas disponíveis.")
            dados_formulario["alunos"] = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Criar data de vencimento (usando o dia informado no mês atual)
        hoje = datetime.now()
        data_vencimento = datetime(hoje.year, hoje.month, dto.dia_vencimento)

        # Criar matrícula
        matricula = Matricula(
            id_matricula=0,
            id_aluno=dto.id_aluno,
            id_turma=dto.id_turma,
            data_matricula=datetime.now(),
            valor_mensalidade=dto.valor_mensalidade,
            data_vencimento=data_vencimento,
            turma=None,
            aluno=None
        )

        matricula_repo.inserir(matricula)
        logger.info(f"Matrícula criada: aluno {dto.id_aluno} na turma {dto.id_turma} por admin {usuario_logado.id}")

        informar_sucesso(request, "Matrícula cadastrada com sucesso!")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["alunos"] = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
        dados_formulario["turmas"] = turma_repo.obter_todos()
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/matriculas/cadastrar.html",
            dados_formulario=dados_formulario,
            campo_padrao="id_aluno",
        )


@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de edição de matrícula"""
    matricula = matricula_repo.obter_por_id(id)

    if not matricula:
        informar_erro(request, "Matrícula não encontrada")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    alunos = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
    turmas = turma_repo.obter_todos()

    # Preparar dados para o template
    dados_matricula = {
        "id_matricula": matricula.id_matricula,
        "id_aluno": matricula.id_aluno,
        "id_turma": matricula.id_turma,
        "valor_mensalidade": matricula.valor_mensalidade,
        "dia_vencimento": matricula.data_vencimento.day if matricula.data_vencimento else 5
    }

    return templates.TemplateResponse(
        "admin/matriculas/editar.html",
        {
            "request": request,
            "matricula": matricula,
            "dados": dados_matricula,
            "alunos": alunos,
            "turmas": turmas
        }
    )


@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    id_aluno: int = Form(...),
    id_turma: int = Form(...),
    valor_mensalidade: float = Form(...),
    dia_vencimento: int = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Edita uma matrícula existente"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_matriculas_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se matrícula existe
    matricula_atual = matricula_repo.obter_por_id(id)
    if not matricula_atual:
        informar_erro(request, "Matrícula não encontrada")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {
        "id_matricula": id,
        "id_aluno": id_aluno,
        "id_turma": id_turma,
        "valor_mensalidade": valor_mensalidade,
        "dia_vencimento": dia_vencimento
    }

    try:
        # Validar com DTO
        dto = AlterarMatriculaDTO(
            id=id,
            id_aluno=id_aluno,
            id_turma=id_turma,
            valor_mensalidade=valor_mensalidade,
            dia_vencimento=dia_vencimento
        )

        # Verificar se aluno existe
        aluno = usuario_repo.obter_por_id(dto.id_aluno)
        if not aluno or aluno.perfil != Perfil.ALUNO.value:
            informar_erro(request, "Aluno selecionado não existe.")
            dados_formulario["matricula"] = matricula_atual
            dados_formulario["alunos"] = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/editar.html",
                {"request": request, "dados": dados_formulario, **dados_formulario}
            )

        # Verificar se turma existe
        turma = turma_repo.obter_por_id(dto.id_turma)
        if not turma:
            informar_erro(request, "Turma selecionada não existe.")
            dados_formulario["matricula"] = matricula_atual
            dados_formulario["alunos"] = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/editar.html",
                {"request": request, "dados": dados_formulario, **dados_formulario}
            )

        # Criar data de vencimento
        hoje = datetime.now()
        data_vencimento = datetime(hoje.year, hoje.month, dto.dia_vencimento)

        # Atualizar matrícula
        matricula_atualizada = Matricula(
            id_matricula=id,
            id_aluno=dto.id_aluno,
            id_turma=dto.id_turma,
            data_matricula=matricula_atual.data_matricula,
            valor_mensalidade=dto.valor_mensalidade,
            data_vencimento=data_vencimento,
            turma=None,
            aluno=None
        )

        matricula_repo.alterar(matricula_atualizada)
        logger.info(f"Matrícula {id} alterada por admin {usuario_logado.id}")

        informar_sucesso(request, "Matrícula alterada com sucesso!")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["matricula"] = matricula_repo.obter_por_id(id)
        dados_formulario["alunos"] = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
        dados_formulario["turmas"] = turma_repo.obter_todos()
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/matriculas/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="id_aluno",
        )


@router.get("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma matrícula (cancela matrícula do aluno)"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_matriculas_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    matricula = matricula_repo.obter_por_id(id)

    if not matricula:
        informar_erro(request, "Matrícula não encontrada")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há pagamentos associados a esta matrícula
    from repo import pagamento_repo
    pagamentos = pagamento_repo.obter_por_matricula(id)
    if pagamentos:
        informar_erro(
            request,
            f"Não é possível excluir esta matrícula pois há {len(pagamentos)} pagamento(s) associado(s)."
        )
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    matricula_repo.excluir(id)
    logger.info(f"Matrícula {id} excluída por admin {usuario_logado.id}")

    informar_sucesso(request, "Matrícula cancelada com sucesso!")
    return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma matrícula (cancela matrícula do aluno)"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_matriculas_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    matricula = matricula_repo.obter_por_id(id)

    if not matricula:
        informar_erro(request, "Matrícula não encontrada")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há pagamentos associados a esta matrícula
    from repo import pagamento_repo
    pagamentos = pagamento_repo.obter_por_matricula(id)
    if pagamentos:
        informar_erro(
            request,
            f"Não é possível excluir esta matrícula pois há {len(pagamentos)} pagamento(s) associado(s)."
        )
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    matricula_repo.excluir(id)
    logger.info(f"Matrícula {id} excluída por admin {usuario_logado.id}")

    informar_sucesso(request, "Matrícula cancelada com sucesso!")
    return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)
