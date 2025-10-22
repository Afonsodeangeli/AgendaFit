from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse

from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from dtos.matricula_dto import MatriculaCreateDTO
from model.matricula_model import Matricula
from repo import matricula_repo

router = APIRouter(prefix="/aluno/matriculas")
templates = criar_templates("templates/aluno/matriculas")


@router.get("")
@requer_autenticacao([Perfil.ALUNO.value])
async def listar_matriculas(request: Request):
    usuario_logado = request.session.get("usuario_logado")
    id_aluno = usuario_logado["id"]
    matriculas = matricula_repo.obter_por_aluno(id_aluno)
    return templates.TemplateResponse("lista.html", {"request": request, "matriculas": matriculas})


@router.post("/nova")
@requer_autenticacao([Perfil.ALUNO.value])
async def matricular(request: Request, id_turma: int = Form(), valor_mensalidade: float = Form(), data_vencimento: str = Form()):
    """Aluno se matricula em uma turma"""
    usuario_logado = request.session.get("usuario_logado")
    id_aluno = usuario_logado["id"]

    # Validar entrada com DTO
    try:
        dto = MatriculaCreateDTO(
            id_turma=id_turma,
            id_aluno=id_aluno,
            valor_mensalidade=valor_mensalidade,
            data_vencimento=data_vencimento
        )
    except Exception as e:
        informar_erro(request, str(e))
        return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar duplicação (ordem: id_turma, id_aluno)
    if matricula_repo.verificar_matricula_existente(dto.id_turma, dto.id_aluno):
        informar_erro(request, "Você já está matriculado nesta turma")
        return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)

    # Construir objeto Matricula
    try:
        data_venc = datetime.fromisoformat(dto.data_vencimento)
    except Exception:
        informar_erro(request, "Data de vencimento inválida")
        return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)

    matricula = Matricula(
        id_matricula=0,
        id_turma=dto.id_turma,
        id_aluno=dto.id_aluno,
        data_matricula=None,
        valor_mensalidade=dto.valor_mensalidade,
        data_vencimento=data_venc,
        turma=None,
        aluno=None
    )

    if matricula_repo.inserir(matricula):
        informar_sucesso(request, "Matrícula realizada com sucesso!")

    return RedirectResponse("/aluno/matriculas", status_code=status.HTTP_303_SEE_OTHER)
