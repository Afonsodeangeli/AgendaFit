"""
Rotas administrativas para gerenciamento de turmas.

Fornece CRUD completo de turmas para administradores.
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

from repo import turma_repo, atividade_repo, usuario_repo
from model.turma_model import Turma
from dtos.turma_dto import CriarTurmaDTO, AlterarTurmaDTO

router = APIRouter(prefix="/admin/turmas")

# Rate limiter para operações administrativas
admin_turmas_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)

# Templates
templates = criar_templates()


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as turmas cadastradas"""
    turmas = turma_repo.obter_todos()

    return templates.TemplateResponse(
        "admin/turmas/listar.html",
        {
            "request": request,
            "turmas": turmas
        }
    )


@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    id_atividade: int = Form(...),
    id_professor: int = Form(...),
    horario_inicio: str = Form(...),
    horario_fim: str = Form(...),
    dias_semana: str = Form(...),
    vagas: int = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Cadastra uma nova turma"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_turmas_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {
        "nome": nome,
        "id_atividade": id_atividade,
        "id_professor": id_professor,
        "horario_inicio": horario_inicio,
        "horario_fim": horario_fim,
        "dias_semana": dias_semana,
        "vagas": vagas
    }

    try:
        # Validar com DTO
        dto = CriarTurmaDTO(
            nome=nome,
            id_atividade=id_atividade,
            id_professor=id_professor,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim,
            dias_semana=dias_semana,
            vagas=vagas
        )

        # Verificar se atividade existe
        atividade = atividade_repo.obter_por_id(dto.id_atividade)
        if not atividade:
            informar_erro(request, "Atividade selecionada não existe.")
            dados_formulario["atividades"] = atividade_repo.obter_todas()
            dados_formulario["professores"] = usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value)
            return templates.TemplateResponse(
                "admin/turmas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se professor existe
        professor = usuario_repo.obter_por_id(dto.id_professor)
        if not professor or professor.perfil != Perfil.PROFESSOR.value:
            informar_erro(request, "Professor selecionado não existe.")
            dados_formulario["atividades"] = atividade_repo.obter_todas()
            dados_formulario["professores"] = usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value)
            return templates.TemplateResponse(
                "admin/turmas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Criar turma
        turma = Turma(
            id_turma=0,
            nome=dto.nome,
            id_atividade=dto.id_atividade,
            id_professor=dto.id_professor,
            horario_inicio=dto.horario_inicio,
            horario_fim=dto.horario_fim,
            dias_semana=dto.dias_semana,
            vagas=dto.vagas,
            data_cadastro=None
        )

        turma_repo.inserir(turma)
        logger.info(f"Turma '{dto.nome}' cadastrada por admin {usuario_logado.id}")

        informar_sucesso(request, "Turma cadastrada com sucesso!")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["atividades"] = atividade_repo.obter_todas()
        dados_formulario["professores"] = usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value)
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/turmas/cadastrar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de edição de turma"""
    turma = turma_repo.obter_por_id(id)

    if not turma:
        informar_erro(request, "Turma não encontrada")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    atividades = atividade_repo.obter_todas()
    professores = usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value)
    dados_turma = turma.__dict__.copy()

    # Converter horários para string formato HH:MM
    if hasattr(turma.horario_inicio, 'strftime'):
        dados_turma['horario_inicio'] = turma.horario_inicio.strftime('%H:%M')
    if hasattr(turma.horario_fim, 'strftime'):
        dados_turma['horario_fim'] = turma.horario_fim.strftime('%H:%M')

    return templates.TemplateResponse(
        "admin/turmas/editar.html",
        {
            "request": request,
            "turma": turma,
            "dados": dados_turma,
            "atividades": atividades,
            "professores": professores
        }
    )


@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de turma"""
    atividades = atividade_repo.obter_todas()
    professores = usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value)

    if not atividades:
        informar_erro(request, "É necessário cadastrar pelo menos uma atividade antes de criar turmas.")
        return RedirectResponse("/admin/atividades/listar", status_code=status.HTTP_303_SEE_OTHER)

    if not professores:
        informar_erro(request, "É necessário cadastrar pelo menos um professor antes de criar turmas.")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse(
        "admin/turmas/cadastrar.html",
        {
            "request": request,
            "atividades": atividades,
            "professores": professores
        }
    )


@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    nome: str = Form(...),
    id_atividade: int = Form(...),
    id_professor: int = Form(...),
    horario_inicio: str = Form(...),
    horario_fim: str = Form(...),
    dias_semana: str = Form(...),
    vagas: int = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Edita uma turma existente"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_turmas_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se turma existe
    turma_atual = turma_repo.obter_por_id(id)
    if not turma_atual:
        informar_erro(request, "Turma não encontrada")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {
        "id_turma": id,
        "nome": nome,
        "id_atividade": id_atividade,
        "id_professor": id_professor,
        "horario_inicio": horario_inicio,
        "horario_fim": horario_fim,
        "dias_semana": dias_semana,
        "vagas": vagas
    }

    try:
        # Validar com DTO
        dto = AlterarTurmaDTO(
            id=id,
            nome=nome,
            id_atividade=id_atividade,
            id_professor=id_professor,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim,
            dias_semana=dias_semana,
            vagas=vagas
        )

        # Verificar se atividade existe
        atividade = atividade_repo.obter_por_id(dto.id_atividade)
        if not atividade:
            informar_erro(request, "Atividade selecionada não existe.")
            dados_formulario["turma"] = turma_atual
            dados_formulario["atividades"] = atividade_repo.obter_todas()
            dados_formulario["professores"] = usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value)
            return templates.TemplateResponse(
                "admin/turmas/editar.html",
                {"request": request, "dados": dados_formulario, **dados_formulario}
            )

        # Verificar se professor existe
        professor = usuario_repo.obter_por_id(dto.id_professor)
        if not professor or professor.perfil != Perfil.PROFESSOR.value:
            informar_erro(request, "Professor selecionado não existe.")
            dados_formulario["turma"] = turma_atual
            dados_formulario["atividades"] = atividade_repo.obter_todas()
            dados_formulario["professores"] = usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value)
            return templates.TemplateResponse(
                "admin/turmas/editar.html",
                {"request": request, "dados": dados_formulario, **dados_formulario}
            )

        # Atualizar turma
        turma_atualizada = Turma(
            id_turma=id,
            nome=dto.nome,
            id_atividade=dto.id_atividade,
            id_professor=dto.id_professor,
            horario_inicio=dto.horario_inicio,
            horario_fim=dto.horario_fim,
            dias_semana=dto.dias_semana,
            vagas=dto.vagas,
            data_cadastro=turma_atual.data_cadastro
        )

        turma_repo.alterar(turma_atualizada)
        logger.info(f"Turma {id} alterada por admin {usuario_logado.id}")

        informar_sucesso(request, "Turma alterada com sucesso!")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["turma"] = turma_repo.obter_por_id(id)
        dados_formulario["atividades"] = atividade_repo.obter_todas()
        dados_formulario["professores"] = usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value)
        raise ErroValidacaoFormulario(
            validation_error=e,
            template_path="admin/turmas/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.get("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma turma"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_turmas_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    turma = turma_repo.obter_por_id(id)

    if not turma:
        informar_erro(request, "Turma não encontrada")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há matrículas associadas a esta turma
    from repo import matricula_repo
    matriculas = matricula_repo.obter_por_turma(id)
    if matriculas:
        informar_erro(
            request,
            f"Não é possível excluir esta turma pois há {len(matriculas)} matrícula(s) de aluno(s)."
        )
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    turma_repo.excluir(id)
    logger.info(f"Turma {id} excluída por admin {usuario_logado.id}")

    informar_sucesso(request, "Turma excluída com sucesso!")
    return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui uma turma"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_turmas_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    turma = turma_repo.obter_por_id(id)

    if not turma:
        informar_erro(request, "Turma não encontrada")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há matrículas associadas a esta turma
    from repo import matricula_repo
    matriculas = matricula_repo.obter_por_turma(id)
    if matriculas:
        informar_erro(
            request,
            f"Não é possível excluir esta turma pois há {len(matriculas)} matrícula(s) de aluno(s)."
        )
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    turma_repo.excluir(id)
    logger.info(f"Turma {id} excluída por admin {usuario_logado.id}")

    informar_sucesso(request, "Turma excluída com sucesso!")
    return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)
