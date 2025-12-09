"""
Rotas administrativas para visualização de estatísticas.

Fornece dashboard com métricas e indicadores do sistema.
"""
from typing import Optional
from fastapi import APIRouter, Request
from util.auth_decorator import requer_autenticacao
from util.perfis import Perfil
from util.template_util import criar_templates

from repo import (
    usuario_repo,
    categoria_repo,
    atividade_repo,
    turma_repo,
    matricula_repo
)

router = APIRouter(prefix="/admin/estatisticas")

# Templates
templates = criar_templates()


@router.get("/dashboard")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_dashboard(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe dashboard com estatísticas do sistema"""

    # Contadores gerais
    total_alunos = len(usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value))
    total_professores = len(usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value))
    total_categorias = len(categoria_repo.obter_todas())
    total_atividades = len(atividade_repo.obter_todas())
    total_turmas = len(turma_repo.obter_todos())
    total_matriculas = len(matricula_repo.obter_todos())

    # Turmas com mais matrículas
    turmas = turma_repo.obter_todos()
    turmas_com_contagem = []
    for turma in turmas:
        num_matriculas = len(matricula_repo.obter_por_turma(turma.id))
        turmas_com_contagem.append({
            "turma": turma,
            "num_matriculas": num_matriculas,
            "percentual_ocupacao": round((num_matriculas / turma.vagas * 100) if turma.vagas > 0 else 0, 1)
        })

    # Ordenar por número de matrículas (top 5)
    turmas_com_contagem.sort(key=lambda x: x["num_matriculas"], reverse=True)
    top_turmas = turmas_com_contagem[:5]

    # Atividades mais populares
    atividades = atividade_repo.obter_todas()
    atividades_com_contagem = []
    for atividade in atividades:
        turmas_atividade = turma_repo.obter_por_atividade(atividade.id)
        total_alunos_atividade = 0
        for turma in turmas_atividade:
            total_alunos_atividade += len(matricula_repo.obter_por_turma(turma.id))

        atividades_com_contagem.append({
            "atividade": atividade,
            "num_turmas": len(turmas_atividade),
            "num_alunos": total_alunos_atividade
        })

    # Ordenar por número de alunos (top 5)
    atividades_com_contagem.sort(key=lambda x: x["num_alunos"], reverse=True)
    top_atividades = atividades_com_contagem[:5]

    # Professores e suas turmas
    professores = usuario_repo.obter_todos_por_perfil(Perfil.PROFESSOR.value)
    professores_com_turmas = []
    for professor in professores:
        turmas_professor = turma_repo.obter_por_professor(professor.id)
        total_alunos_professor = 0
        for turma in turmas_professor:
            total_alunos_professor += len(matricula_repo.obter_por_turma(turma.id))

        professores_com_turmas.append({
            "professor": professor,
            "num_turmas": len(turmas_professor),
            "num_alunos": total_alunos_professor
        })

    # Ordenar por número de alunos
    professores_com_turmas.sort(key=lambda x: x["num_alunos"], reverse=True)

    return templates.TemplateResponse(
        "admin/estatisticas/dashboard.html",
        {
            "request": request,
            "total_alunos": total_alunos,
            "total_professores": total_professores,
            "total_categorias": total_categorias,
            "total_atividades": total_atividades,
            "total_turmas": total_turmas,
            "total_matriculas": total_matriculas,
            "top_turmas": top_turmas,
            "top_atividades": top_atividades,
            "professores_com_turmas": professores_com_turmas
        }
    )
