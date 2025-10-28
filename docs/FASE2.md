# FASE 2 - Plano de Implementação - Rotas Administrativas do AgendaFit

**Versão:** 1.0
**Data:** 2025-10-22
**Objetivo:** Implementar todas as rotas administrativas necessárias para o perfil Administrador gerenciar o sistema AgendaFit, seguindo rigorosamente os padrões do projeto DefaultWebApp.

---

## Índice

1. [Introdução](#introdução)
2. [Padrões e Convenções](#padrões-e-convenções)
3. [Módulo 1: Categorias](#módulo-1-categorias)
4. [Módulo 2: Atividades](#módulo-2-atividades)
5. [Módulo 3: Turmas](#módulo-3-turmas)
6. [Módulo 4: Professores](#módulo-4-professores)
7. [Módulo 5: Alunos](#módulo-5-alunos)
8. [Módulo 6: Matrículas](#módulo-6-matrículas)
9. [Módulo 7: Dashboard de Estatísticas](#módulo-7-dashboard-de-estatísticas)
10. [Checklist de Implementação](#checklist-de-implementação)

---

## Introdução

Este documento detalha o plano de implementação completo para todas as rotas administrativas do AgendaFit. Cada seção contém código pronto para uso, seguindo exatamente os mesmos padrões arquiteturais, de validação, segurança e UX do projeto original DefaultWebApp.

### Princípios Fundamentais

- **Reutilização de Componentes:** Utilizar macros existentes (`form_fields.html`) e componentes (`alerta_erro.html`, `modal_confirmacao.html`)
- **Validação Consistente:** DTOs com Pydantic 2.0+ e validadores reutilizáveis
- **Segurança:** Decorador `@requer_autenticacao([Perfil.ADMIN.value])` em todas as rotas administrativas
- **Rate Limiting:** Proteção contra abuso em operações de escrita
- **Feedback ao Usuário:** Mensagens flash para sucesso/erro
- **UX Consistente:** Bootstrap 5.3.8, ícones Bootstrap Icons, modal de confirmação para exclusões

---

## Padrões e Convenções

### Estrutura de Arquivos

```
routes/
  └── admin_categorias_routes.py
  └── admin_atividades_routes.py
  └── admin_turmas_routes.py
  └── admin_professores_routes.py
  └── admin_alunos_routes.py
  └── admin_matriculas_routes.py
  └── admin_estatisticas_routes.py

dtos/
  └── categoria_dto.py
  └── atividade_dto.py
  └── turma_dto.py
  └── professor_dto.py
  └── aluno_dto.py
  └── matricula_dto.py

templates/
  └── admin/
      ├── categorias/
      │   ├── listar.html
      │   ├── cadastrar.html
      │   └── editar.html
      ├── atividades/
      │   ├── listar.html
      │   ├── cadastrar.html
      │   └── editar.html
      ├── turmas/
      │   ├── listar.html
      │   ├── cadastrar.html
      │   └── editar.html
      ├── professores/
      │   ├── listar.html
      │   ├── cadastrar.html
      │   └── editar.html
      ├── alunos/
      │   ├── listar.html
      │   ├── cadastrar.html
      │   └── editar.html
      ├── matriculas/
      │   ├── listar.html
      │   ├── cadastrar.html
      │   └── editar.html
      └── estatisticas/
          └── dashboard.html
```

### Padrão de Rotas CRUD

Cada módulo CRUD segue este padrão:

- **GET `/admin/<recurso>/listar`** - Lista todos os registros
- **GET `/admin/<recurso>/cadastrar`** - Exibe formulário de cadastro
- **POST `/admin/<recurso>/cadastrar`** - Processa cadastro
- **GET `/admin/<recurso>/editar/{id}`** - Exibe formulário de edição
- **POST `/admin/<recurso>/editar/{id}`** - Processa edição
- **POST `/admin/<recurso>/excluir/{id}`** - Exclui registro

### Padrão de DTO

```python
from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_string_obrigatoria,
    validar_id_positivo,
    # outros validadores conforme necessário
)

class CriarRecursoDTO(BaseModel):
    """DTO para criação de recurso"""
    campo1: str
    campo2: str

    _validar_campo1 = field_validator("campo1")(
        validar_string_obrigatoria("Campo 1", tamanho_minimo=3, tamanho_maximo=100)
    )

class AlterarRecursoDTO(BaseModel):
    """DTO para alteração de recurso"""
    id: int
    campo1: str
    campo2: str

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_campo1 = field_validator("campo1")(
        validar_string_obrigatoria("Campo 1", tamanho_minimo=3, tamanho_maximo=100)
    )
```

### Padrão de Template de Listagem

```html
{% extends "base_privada.html" %}

{% block titulo %}Lista de Recursos{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-icon"></i> Recursos</h2>
            <a href="/admin/recursos/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Novo Recurso
            </a>
        </div>

        {% if recursos %}
        <div class="card shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th>Coluna 1</th>
                                <th>Coluna 2</th>
                                <th class="text-end">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for recurso in recursos %}
                            <tr>
                                <td>{{ recurso.campo1 }}</td>
                                <td>{{ recurso.campo2 }}</td>
                                <td class="text-end">
                                    <div class="btn-group">
                                        <a href="/admin/recursos/editar/{{ recurso.id }}"
                                           class="btn btn-sm btn-outline-primary">
                                            <i class="bi bi-pencil"></i> Editar
                                        </a>
                                        <button type="button" class="btn btn-sm btn-outline-danger"
                                                onclick="excluirRecurso({{ recurso.id }}, '{{ recurso.campo1|replace(\"'\", \"\\\\'\") }}')">
                                            <i class="bi bi-trash"></i> Excluir
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info">
            <i class="bi bi-info-circle"></i> Nenhum recurso cadastrado.
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function excluirRecurso(id, nome) {
    const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <p class="mb-0"><strong>${nome}</strong></p>
            </div>
        </div>
    `;

    abrirModalConfirmacao({
        url: `/admin/recursos/${id}/excluir`,
        mensagem: 'Tem certeza que deseja excluir este recurso?',
        detalhes: detalhes
    });
}
</script>
{% endblock %}
```

---

## Módulo 1: Categorias

Gerenciamento completo de categorias de atividades físicas (ex: Musculação, Yoga, Natação).

### 1.1 - DTO: Criar Categoria

**Arquivo:** `dtos/categoria_dto.py`

```python
"""
DTOs para validação de dados de Categoria.

Fornece validação de campos para operações CRUD de categorias.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_string_obrigatoria,
    validar_comprimento,
    validar_id_positivo,
)


class CriarCategoriaDTO(BaseModel):
    """DTO para criação de categoria"""

    nome: str
    descricao: str = ""

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=500)
    )


class AlterarCategoriaDTO(BaseModel):
    """DTO para alteração de categoria"""

    id: int
    nome: str
    descricao: str = ""

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=500)
    )
```

### 1.2 - Rota GET: Listar Categorias

**Arquivo:** `routes/admin_categorias_routes.py` (parte 1/4)

```python
"""
Rotas administrativas para gerenciamento de categorias.

Fornece CRUD completo de categorias para administradores.
"""
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_utils import requer_autenticacao
from util.perfis import Perfil
from util.mensagens import informar_sucesso, informar_erro
from util.templates import templates
from util.logger_config import logger
from util.rate_limiter import RateLimiter
from util.exceptions import FormValidationError
from util.request_utils import obter_identificador_cliente

from repo import categoria_repo
from model.categoria_model import Categoria
from dtos.categoria_dto import CriarCategoriaDTO, AlterarCategoriaDTO

router = APIRouter(prefix="/admin/categorias")

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
```

### 1.3 - Template: Listar Categorias

**Arquivo:** `templates/admin/categorias/listar.html`

```html
{% extends "base_privada.html" %}

{% block titulo %}Categorias{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-tags"></i> Categorias de Atividades</h2>
            <a href="/admin/categorias/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Nova Categoria
            </a>
        </div>

        {% if categorias %}
        <div class="card shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th style="width: 30%">Nome</th>
                                <th style="width: 50%">Descrição</th>
                                <th class="text-end" style="width: 20%">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for categoria in categorias %}
                            <tr>
                                <td>
                                    <strong>{{ categoria.nome }}</strong>
                                </td>
                                <td>
                                    {% if categoria.descricao %}
                                    {{ categoria.descricao }}
                                    {% else %}
                                    <em class="text-muted">Sem descrição</em>
                                    {% endif %}
                                </td>
                                <td class="text-end">
                                    <div class="btn-group btn-group-sm">
                                        <a href="/admin/categorias/editar/{{ categoria.id }}"
                                           class="btn btn-outline-primary"
                                           title="Editar categoria">
                                            <i class="bi bi-pencil"></i> Editar
                                        </a>
                                        <button type="button"
                                                class="btn btn-outline-danger"
                                                title="Excluir categoria"
                                                onclick="excluirCategoria({{ categoria.id }}, '{{ categoria.nome|replace(\"'\", \"\\\\'\") }}')">
                                            <i class="bi bi-trash"></i> Excluir
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card-footer text-muted">
                <small><i class="bi bi-info-circle"></i> Total: {{ categorias|length }} categoria(s)</small>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info" role="alert">
            <h4 class="alert-heading"><i class="bi bi-info-circle"></i> Nenhuma categoria cadastrada</h4>
            <p>Não há categorias cadastradas no sistema. Clique em "Nova Categoria" para começar.</p>
            <hr>
            <a href="/admin/categorias/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Cadastrar Primeira Categoria
            </a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
/**
 * Abre modal de confirmação para excluir categoria
 */
function excluirCategoria(categoriaId, categoriaNome) {
    const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <h6 class="card-title mb-2">
                    <i class="bi bi-tag"></i> Categoria:
                </h6>
                <p class="mb-0"><strong>${categoriaNome}</strong></p>
            </div>
        </div>
        <div class="alert alert-warning mt-3 mb-0">
            <i class="bi bi-exclamation-triangle"></i>
            <strong>Atenção:</strong> Esta ação não pode ser desfeita.
            Todas as atividades associadas a esta categoria poderão ser afetadas.
        </div>
    `;

    abrirModalConfirmacao({
        url: `/admin/categorias/${categoriaId}/excluir`,
        mensagem: 'Tem certeza que deseja excluir esta categoria?',
        detalhes: detalhes
    });
}
</script>
{% endblock %}
```

### 1.4 - Rota GET: Cadastrar Categoria

**Arquivo:** `routes/admin_categorias_routes.py` (parte 2/4)

```python
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
```

### 1.5 - Template: Cadastrar Categoria

**Arquivo:** `templates/admin/categorias/cadastrar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Cadastrar Categoria{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-tag-fill"></i> Cadastrar Nova Categoria</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/categorias/cadastrar">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome da Categoria', type='text', required=true,
                                   attributes={'maxlength': 100, 'placeholder': 'Ex: Musculação, Yoga, Natação'}) }}
                        </div>

                        <div class="col-12">
                            {{ field(name='descricao', label='Descrição', type='textarea', rows=3,
                                   attributes={'maxlength': 500, 'placeholder': 'Descrição opcional da categoria'},
                                   wrapper_class='mb-0') }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Cadastrar
                        </button>
                        <a href="/admin/categorias/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 1.6 - Rota POST: Cadastrar Categoria

**Arquivo:** `routes/admin_categorias_routes.py` (parte 3/4)

```python
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


@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de edição de categoria"""
    categoria = categoria_repo.obter_por_id(id)

    if not categoria:
        informar_erro(request, "Categoria não encontrada")
        return RedirectResponse("/admin/categorias/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Criar cópia dos dados da categoria para o formulário
    dados_categoria = categoria.__dict__.copy()

    return templates.TemplateResponse(
        "admin/categorias/editar.html",
        {
            "request": request,
            "categoria": categoria,
            "dados": dados_categoria
        }
    )
```

### 1.7 - Template: Editar Categoria

**Arquivo:** `templates/admin/categorias/editar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Editar Categoria{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-tag"></i> Editar Categoria</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/categorias/editar/{{ dados.id if dados.id is defined else categoria.id }}">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome da Categoria', type='text', required=true,
                                   value=dados.nome, attributes={'maxlength': 100}) }}
                        </div>

                        <div class="col-12">
                            {{ field(name='descricao', label='Descrição', type='textarea', rows=3,
                                   value=dados.descricao, attributes={'maxlength': 500}, wrapper_class='mb-0') }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Salvar Alterações
                        </button>
                        <a href="/admin/categorias/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 1.8 - Rota POST: Editar e Excluir Categoria

**Arquivo:** `routes/admin_categorias_routes.py` (parte 4/4)

```python
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
```

---

## Módulo 2: Atividades

Gerenciamento completo de atividades físicas oferecidas (ex: Musculação Básica, Yoga Avançado).

### 2.1 - DTO: Criar Atividade

**Arquivo:** `dtos/atividade_dto.py`

```python
"""
DTOs para validação de dados de Atividade.

Fornece validação de campos para operações CRUD de atividades.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_string_obrigatoria,
    validar_comprimento,
    validar_id_positivo,
)


class CriarAtividadeDTO(BaseModel):
    """DTO para criação de atividade"""

    nome: str
    descricao: str = ""
    id_categoria: int

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=1000)
    )
    _validar_id_categoria = field_validator("id_categoria")(validar_id_positivo())


class AlterarAtividadeDTO(BaseModel):
    """DTO para alteração de atividade"""

    id: int
    nome: str
    descricao: str = ""
    id_categoria: int

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=1000)
    )
    _validar_id_categoria = field_validator("id_categoria")(validar_id_positivo())
```

### 2.2 - Rota GET: Listar Atividades

**Arquivo:** `routes/admin_atividades_routes.py` (parte 1/4)

```python
"""
Rotas administrativas para gerenciamento de atividades.

Fornece CRUD completo de atividades para administradores.
"""
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_utils import requer_autenticacao
from util.perfis import Perfil
from util.mensagens import informar_sucesso, informar_erro
from util.templates import templates
from util.logger_config import logger
from util.rate_limiter import RateLimiter
from util.exceptions import FormValidationError
from util.request_utils import obter_identificador_cliente

from repo import atividade_repo, categoria_repo
from model.atividade_model import Atividade
from dtos.atividade_dto import CriarAtividadeDTO, AlterarAtividadeDTO

router = APIRouter(prefix="/admin/atividades")

# Rate limiter para operações administrativas
admin_atividades_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as atividades cadastradas"""
    atividades = atividade_repo.obter_todos()
    categorias = categoria_repo.obter_todos()

    # Criar dicionário de categorias para lookup rápido
    categorias_dict = {cat.id: cat.nome for cat in categorias}

    return templates.TemplateResponse(
        "admin/atividades/listar.html",
        {
            "request": request,
            "atividades": atividades,
            "categorias_dict": categorias_dict
        }
    )
```

### 2.3 - Template: Listar Atividades

**Arquivo:** `templates/admin/atividades/listar.html`

```html
{% extends "base_privada.html" %}

{% block titulo %}Atividades{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-activity"></i> Atividades Físicas</h2>
            <a href="/admin/atividades/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Nova Atividade
            </a>
        </div>

        {% if atividades %}
        <div class="card shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th style="width: 25%">Nome</th>
                                <th style="width: 15%">Categoria</th>
                                <th style="width: 40%">Descrição</th>
                                <th class="text-end" style="width: 20%">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for atividade in atividades %}
                            <tr>
                                <td>
                                    <strong>{{ atividade.nome }}</strong>
                                </td>
                                <td>
                                    <span class="badge bg-primary">
                                        {{ categorias_dict.get(atividade.id_categoria, 'Sem categoria') }}
                                    </span>
                                </td>
                                <td>
                                    {% if atividade.descricao %}
                                    {{ atividade.descricao[:100] }}{% if atividade.descricao|length > 100 %}...{% endif %}
                                    {% else %}
                                    <em class="text-muted">Sem descrição</em>
                                    {% endif %}
                                </td>
                                <td class="text-end">
                                    <div class="btn-group btn-group-sm">
                                        <a href="/admin/atividades/editar/{{ atividade.id }}"
                                           class="btn btn-outline-primary"
                                           title="Editar atividade">
                                            <i class="bi bi-pencil"></i> Editar
                                        </a>
                                        <button type="button"
                                                class="btn btn-outline-danger"
                                                title="Excluir atividade"
                                                onclick="excluirAtividade({{ atividade.id }}, '{{ atividade.nome|replace(\"'\", \"\\\\'\") }}')">
                                            <i class="bi bi-trash"></i> Excluir
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card-footer text-muted">
                <small><i class="bi bi-info-circle"></i> Total: {{ atividades|length }} atividade(s)</small>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info" role="alert">
            <h4 class="alert-heading"><i class="bi bi-info-circle"></i> Nenhuma atividade cadastrada</h4>
            <p>Não há atividades cadastradas no sistema. Clique em "Nova Atividade" para começar.</p>
            <hr>
            <a href="/admin/atividades/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Cadastrar Primeira Atividade
            </a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
/**
 * Abre modal de confirmação para excluir atividade
 */
function excluirAtividade(atividadeId, atividadeNome) {
    const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <h6 class="card-title mb-2">
                    <i class="bi bi-activity"></i> Atividade:
                </h6>
                <p class="mb-0"><strong>${atividadeNome}</strong></p>
            </div>
        </div>
        <div class="alert alert-warning mt-3 mb-0">
            <i class="bi bi-exclamation-triangle"></i>
            <strong>Atenção:</strong> Esta ação não pode ser desfeita.
            Todas as turmas associadas a esta atividade poderão ser afetadas.
        </div>
    `;

    abrirModalConfirmacao({
        url: `/admin/atividades/${atividadeId}/excluir`,
        mensagem: 'Tem certeza que deseja excluir esta atividade?',
        detalhes: detalhes
    });
}
</script>
{% endblock %}
```

### 2.4 - Rota GET: Cadastrar Atividade

**Arquivo:** `routes/admin_atividades_routes.py` (parte 2/4)

```python
@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de atividade"""
    categorias = categoria_repo.obter_todos()

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
```

### 2.5 - Template: Cadastrar Atividade

**Arquivo:** `templates/admin/atividades/cadastrar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Cadastrar Atividade{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-plus-circle"></i> Cadastrar Nova Atividade</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/atividades/cadastrar">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome da Atividade', type='text', required=true,
                                   attributes={'maxlength': 100, 'placeholder': 'Ex: Musculação Básica, Yoga Avançado'}) }}
                        </div>

                        <div class="col-12 mb-3">
                            {% set categorias_dict = {} %}
                            {% for cat in categorias %}
                            {% set _ = categorias_dict.update({cat.id|string: cat.nome}) %}
                            {% endfor %}
                            {{ field(name='id_categoria', label='Categoria', type='select', required=true,
                                   options=categorias_dict) }}
                        </div>

                        <div class="col-12">
                            {{ field(name='descricao', label='Descrição', type='textarea', rows=4,
                                   attributes={'maxlength': 1000, 'placeholder': 'Descrição detalhada da atividade'},
                                   wrapper_class='mb-0') }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Cadastrar
                        </button>
                        <a href="/admin/atividades/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 2.6 - Rota POST: Cadastrar Atividade

**Arquivo:** `routes/admin_atividades_routes.py` (parte 3/4)

```python
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
            categorias = categoria_repo.obter_todos()
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
        dados_formulario["categorias"] = categoria_repo.obter_todos()
        raise FormValidationError(
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

    categorias = categoria_repo.obter_todos()
    dados_atividade = atividade.__dict__.copy()

    return templates.TemplateResponse(
        "admin/atividades/editar.html",
        {
            "request": request,
            "atividade": atividade,
            "dados": dados_atividade,
            "categorias": categorias
        }
    )
```

### 2.7 - Template: Editar Atividade

**Arquivo:** `templates/admin/atividades/editar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Editar Atividade{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-activity"></i> Editar Atividade</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/atividades/editar/{{ dados.id if dados.id is defined else atividade.id }}">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome da Atividade', type='text', required=true,
                                   value=dados.nome, attributes={'maxlength': 100}) }}
                        </div>

                        <div class="col-12 mb-3">
                            {% set categorias_dict = {} %}
                            {% for cat in categorias %}
                            {% set _ = categorias_dict.update({cat.id|string: cat.nome}) %}
                            {% endfor %}
                            {{ field(name='id_categoria', label='Categoria', type='select', required=true,
                                   options=categorias_dict, value=dados.id_categoria) }}
                        </div>

                        <div class="col-12">
                            {{ field(name='descricao', label='Descrição', type='textarea', rows=4,
                                   value=dados.descricao, attributes={'maxlength': 1000}, wrapper_class='mb-0') }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Salvar Alterações
                        </button>
                        <a href="/admin/atividades/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 2.8 - Rota POST: Editar e Excluir Atividade

**Arquivo:** `routes/admin_atividades_routes.py` (parte 4/4)

```python
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
            categorias = categoria_repo.obter_todos()
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
        dados_formulario["categorias"] = categoria_repo.obter_todos()
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
```

---

## Módulo 3: Turmas

Gerenciamento completo de turmas (grupos de alunos para uma atividade específica em horários definidos).

### 3.1 - DTO: Criar Turma

**Arquivo:** `dtos/turma_dto.py`

```python
"""
DTOs para validação de dados de Turma.

Fornece validação de campos para operações CRUD de turmas.
"""
from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import time
from dtos.validators import (
    validar_string_obrigatoria,
    validar_id_positivo,
)


def validar_horario(nome_campo: str = "Horário"):
    """Validador para horários em formato HH:MM"""
    def validator(cls, v):
        if not v:
            raise ValueError(f"{nome_campo} é obrigatório")

        # Se já é objeto time, retornar
        if isinstance(v, time):
            return v

        # Se é string, tentar converter
        if isinstance(v, str):
            try:
                partes = v.split(":")
                if len(partes) != 2:
                    raise ValueError(f"{nome_campo} deve estar no formato HH:MM")
                hora, minuto = int(partes[0]), int(partes[1])
                if not (0 <= hora <= 23 and 0 <= minuto <= 59):
                    raise ValueError(f"{nome_campo} inválido")
                return time(hour=hora, minute=minuto)
            except Exception:
                raise ValueError(f"{nome_campo} deve estar no formato HH:MM")

        raise ValueError(f"{nome_campo} inválido")

    return validator


class CriarTurmaDTO(BaseModel):
    """DTO para criação de turma"""

    nome: str
    id_atividade: int
    id_professor: int
    horario_inicio: time
    horario_fim: time
    dias_semana: str
    vagas: int

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_id_atividade = field_validator("id_atividade")(validar_id_positivo())
    _validar_id_professor = field_validator("id_professor")(validar_id_positivo())
    _validar_horario_inicio = field_validator("horario_inicio")(validar_horario("Horário de início"))
    _validar_horario_fim = field_validator("horario_fim")(validar_horario("Horário de fim"))
    _validar_dias_semana = field_validator("dias_semana")(
        validar_string_obrigatoria("Dias da semana", tamanho_minimo=1, tamanho_maximo=50)
    )

    @field_validator("vagas")
    def validar_vagas(cls, v):
        """Valida número de vagas"""
        if not isinstance(v, int) or v < 1:
            raise ValueError("Número de vagas deve ser maior que zero")
        if v > 100:
            raise ValueError("Número de vagas não pode ser maior que 100")
        return v

    @model_validator(mode='after')
    def validar_horarios(self):
        """Valida se horário de fim é posterior ao de início"""
        if self.horario_fim <= self.horario_inicio:
            raise ValueError("Horário de fim deve ser posterior ao horário de início")
        return self


class AlterarTurmaDTO(BaseModel):
    """DTO para alteração de turma"""

    id: int
    nome: str
    id_atividade: int
    id_professor: int
    horario_inicio: time
    horario_fim: time
    dias_semana: str
    vagas: int

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_id_atividade = field_validator("id_atividade")(validar_id_positivo())
    _validar_id_professor = field_validator("id_professor")(validar_id_positivo())
    _validar_horario_inicio = field_validator("horario_inicio")(validar_horario("Horário de início"))
    _validar_horario_fim = field_validator("horario_fim")(validar_horario("Horário de fim"))
    _validar_dias_semana = field_validator("dias_semana")(
        validar_string_obrigatoria("Dias da semana", tamanho_minimo=1, tamanho_maximo=50)
    )

    @field_validator("vagas")
    def validar_vagas(cls, v):
        """Valida número de vagas"""
        if not isinstance(v, int) or v < 1:
            raise ValueError("Número de vagas deve ser maior que zero")
        if v > 100:
            raise ValueError("Número de vagas não pode ser maior que 100")
        return v

    @model_validator(mode='after')
    def validar_horarios(self):
        """Valida se horário de fim é posterior ao de início"""
        if self.horario_fim <= self.horario_inicio:
            raise ValueError("Horário de fim deve ser posterior ao horário de início")
        return self
```

### 3.2 - Rota GET: Listar Turmas

**Arquivo:** `routes/admin_turmas_routes.py` (parte 1/4)

```python
"""
Rotas administrativas para gerenciamento de turmas.

Fornece CRUD completo de turmas para administradores.
"""
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from datetime import time

from util.auth_utils import requer_autenticacao
from util.perfis import Perfil
from util.mensagens import informar_sucesso, informar_erro
from util.templates import templates
from util.logger_config import logger
from util.rate_limiter import RateLimiter
from util.exceptions import FormValidationError
from util.request_utils import obter_identificador_cliente

from repo import turma_repo, atividade_repo, usuario_repo
from model.turma_model import Turma
from dtos.turma_dto import CriarTurmaDTO, AlterarTurmaDTO

router = APIRouter(prefix="/admin/turmas")

# Rate limiter para operações administrativas
admin_turmas_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as turmas cadastradas"""
    turmas = turma_repo.obter_todos()
    atividades = atividade_repo.obter_todos()
    professores = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)

    # Criar dicionários para lookup
    atividades_dict = {ativ.id: ativ.nome for ativ in atividades}
    professores_dict = {prof.id: prof.nome for prof in professores}

    return templates.TemplateResponse(
        "admin/turmas/listar.html",
        {
            "request": request,
            "turmas": turmas,
            "atividades_dict": atividades_dict,
            "professores_dict": professores_dict
        }
    )
```

### 3.3 - Template: Listar Turmas

**Arquivo:** `templates/admin/turmas/listar.html`

```html
{% extends "base_privada.html" %}

{% block titulo %}Turmas{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-people-fill"></i> Turmas</h2>
            <a href="/admin/turmas/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Nova Turma
            </a>
        </div>

        {% if turmas %}
        <div class="card shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th style="width: 20%">Nome</th>
                                <th style="width: 15%">Atividade</th>
                                <th style="width: 15%">Professor</th>
                                <th style="width: 15%">Horário</th>
                                <th style="width: 15%">Dias</th>
                                <th style="width: 10%" class="text-center">Vagas</th>
                                <th class="text-end" style="width: 10%">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for turma in turmas %}
                            <tr>
                                <td>
                                    <strong>{{ turma.nome }}</strong>
                                </td>
                                <td>
                                    <span class="badge bg-primary">
                                        {{ atividades_dict.get(turma.id_atividade, 'N/A') }}
                                    </span>
                                </td>
                                <td>
                                    {{ professores_dict.get(turma.id_professor, 'N/A') }}
                                </td>
                                <td>
                                    <small>
                                        {{ turma.horario_inicio.strftime('%H:%M') }} -
                                        {{ turma.horario_fim.strftime('%H:%M') }}
                                    </small>
                                </td>
                                <td>
                                    <small>{{ turma.dias_semana }}</small>
                                </td>
                                <td class="text-center">
                                    <span class="badge bg-secondary">{{ turma.vagas }}</span>
                                </td>
                                <td class="text-end">
                                    <div class="btn-group btn-group-sm">
                                        <a href="/admin/turmas/editar/{{ turma.id }}"
                                           class="btn btn-outline-primary"
                                           title="Editar turma">
                                            <i class="bi bi-pencil"></i>
                                        </a>
                                        <button type="button"
                                                class="btn btn-outline-danger"
                                                title="Excluir turma"
                                                onclick="excluirTurma({{ turma.id }}, '{{ turma.nome|replace(\"'\", \"\\\\'\") }}')">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card-footer text-muted">
                <small><i class="bi bi-info-circle"></i> Total: {{ turmas|length }} turma(s)</small>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info" role="alert">
            <h4 class="alert-heading"><i class="bi bi-info-circle"></i> Nenhuma turma cadastrada</h4>
            <p>Não há turmas cadastradas no sistema. Clique em "Nova Turma" para começar.</p>
            <hr>
            <a href="/admin/turmas/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Cadastrar Primeira Turma
            </a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
/**
 * Abre modal de confirmação para excluir turma
 */
function excluirTurma(turmaId, turmaNome) {
    const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <h6 class="card-title mb-2">
                    <i class="bi bi-people-fill"></i> Turma:
                </h6>
                <p class="mb-0"><strong>${turmaNome}</strong></p>
            </div>
        </div>
        <div class="alert alert-warning mt-3 mb-0">
            <i class="bi bi-exclamation-triangle"></i>
            <strong>Atenção:</strong> Esta ação não pode ser desfeita.
            Todas as matrículas de alunos nesta turma serão excluídas.
        </div>
    `;

    abrirModalConfirmacao({
        url: `/admin/turmas/${turmaId}/excluir`,
        mensagem: 'Tem certeza que deseja excluir esta turma?',
        detalhes: detalhes
    });
}
</script>
{% endblock %}
```

### 3.4 - Rota GET: Cadastrar Turma

**Arquivo:** `routes/admin_turmas_routes.py` (parte 2/4)

```python
@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de turma"""
    atividades = atividade_repo.obter_todos()
    professores = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)

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
```

### 3.5 - Template: Cadastrar Turma

**Arquivo:** `templates/admin/turmas/cadastrar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Cadastrar Turma{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-10">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-plus-circle"></i> Cadastrar Nova Turma</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/turmas/cadastrar">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-md-6 mb-3">
                            {{ field(name='nome', label='Nome da Turma', type='text', required=true,
                                   attributes={'maxlength': 100, 'placeholder': 'Ex: Turma A - Manhã'}) }}
                        </div>

                        <div class="col-md-6 mb-3">
                            {% set atividades_dict = {} %}
                            {% for ativ in atividades %}
                            {% set _ = atividades_dict.update({ativ.id|string: ativ.nome}) %}
                            {% endfor %}
                            {{ field(name='id_atividade', label='Atividade', type='select', required=true,
                                   options=atividades_dict) }}
                        </div>

                        <div class="col-md-6 mb-3">
                            {% set professores_dict = {} %}
                            {% for prof in professores %}
                            {% set _ = professores_dict.update({prof.id|string: prof.nome}) %}
                            {% endfor %}
                            {{ field(name='id_professor', label='Professor', type='select', required=true,
                                   options=professores_dict) }}
                        </div>

                        <div class="col-md-6 mb-3">
                            {{ field(name='vagas', label='Número de Vagas', type='number', required=true,
                                   attributes={'min': '1', 'max': '100', 'placeholder': 'Ex: 20'}) }}
                        </div>

                        <div class="col-md-4 mb-3">
                            {{ field(name='horario_inicio', label='Horário Início', type='time', required=true) }}
                        </div>

                        <div class="col-md-4 mb-3">
                            {{ field(name='horario_fim', label='Horário Fim', type='time', required=true) }}
                        </div>

                        <div class="col-md-4 mb-3">
                            {{ field(name='dias_semana', label='Dias da Semana', type='text', required=true,
                                   attributes={'maxlength': 50, 'placeholder': 'Ex: Seg, Qua, Sex'}) }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Cadastrar
                        </button>
                        <a href="/admin/turmas/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 3.6 - Rota POST: Cadastrar Turma

**Arquivo:** `routes/admin_turmas_routes.py` (parte 3/4)

```python
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
            dados_formulario["atividades"] = atividade_repo.obter_todos()
            dados_formulario["professores"] = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)
            return templates.TemplateResponse(
                "admin/turmas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se professor existe
        professor = usuario_repo.obter_por_id(dto.id_professor)
        if not professor or professor.perfil != Perfil.PROFESSOR.value:
            informar_erro(request, "Professor selecionado não existe.")
            dados_formulario["atividades"] = atividade_repo.obter_todos()
            dados_formulario["professores"] = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)
            return templates.TemplateResponse(
                "admin/turmas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Criar turma
        turma = Turma(
            id=0,
            nome=dto.nome,
            id_atividade=dto.id_atividade,
            id_professor=dto.id_professor,
            horario_inicio=dto.horario_inicio,
            horario_fim=dto.horario_fim,
            dias_semana=dto.dias_semana,
            vagas=dto.vagas
        )

        turma_repo.inserir(turma)
        logger.info(f"Turma '{dto.nome}' cadastrada por admin {usuario_logado['id']}")

        informar_sucesso(request, "Turma cadastrada com sucesso!")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["atividades"] = atividade_repo.obter_todos()
        dados_formulario["professores"] = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)
        raise FormValidationError(
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

    atividades = atividade_repo.obter_todos()
    professores = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)
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
```

### 3.7 - Template: Editar Turma

**Arquivo:** `templates/admin/turmas/editar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Editar Turma{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-10">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-people-fill"></i> Editar Turma</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/turmas/editar/{{ dados.id if dados.id is defined else turma.id }}">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-md-6 mb-3">
                            {{ field(name='nome', label='Nome da Turma', type='text', required=true,
                                   value=dados.nome, attributes={'maxlength': 100}) }}
                        </div>

                        <div class="col-md-6 mb-3">
                            {% set atividades_dict = {} %}
                            {% for ativ in atividades %}
                            {% set _ = atividades_dict.update({ativ.id|string: ativ.nome}) %}
                            {% endfor %}
                            {{ field(name='id_atividade', label='Atividade', type='select', required=true,
                                   options=atividades_dict, value=dados.id_atividade) }}
                        </div>

                        <div class="col-md-6 mb-3">
                            {% set professores_dict = {} %}
                            {% for prof in professores %}
                            {% set _ = professores_dict.update({prof.id|string: prof.nome}) %}
                            {% endfor %}
                            {{ field(name='id_professor', label='Professor', type='select', required=true,
                                   options=professores_dict, value=dados.id_professor) }}
                        </div>

                        <div class="col-md-6 mb-3">
                            {{ field(name='vagas', label='Número de Vagas', type='number', required=true,
                                   value=dados.vagas, attributes={'min': '1', 'max': '100'}) }}
                        </div>

                        <div class="col-md-4 mb-3">
                            {{ field(name='horario_inicio', label='Horário Início', type='time', required=true,
                                   value=dados.horario_inicio) }}
                        </div>

                        <div class="col-md-4 mb-3">
                            {{ field(name='horario_fim', label='Horário Fim', type='time', required=true,
                                   value=dados.horario_fim) }}
                        </div>

                        <div class="col-md-4 mb-3">
                            {{ field(name='dias_semana', label='Dias da Semana', type='text', required=true,
                                   value=dados.dias_semana, attributes={'maxlength': 50}) }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Salvar Alterações
                        </button>
                        <a href="/admin/turmas/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 3.8 - Rota POST: Editar e Excluir Turma

**Arquivo:** `routes/admin_turmas_routes.py` (parte 4/4)

```python
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
        "id": id,
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
            dados_formulario["atividades"] = atividade_repo.obter_todos()
            dados_formulario["professores"] = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)
            return templates.TemplateResponse(
                "admin/turmas/editar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se professor existe
        professor = usuario_repo.obter_por_id(dto.id_professor)
        if not professor or professor.perfil != Perfil.PROFESSOR.value:
            informar_erro(request, "Professor selecionado não existe.")
            dados_formulario["turma"] = turma_atual
            dados_formulario["atividades"] = atividade_repo.obter_todos()
            dados_formulario["professores"] = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)
            return templates.TemplateResponse(
                "admin/turmas/editar.html",
                {"request": request, **dados_formulario}
            )

        # Atualizar turma
        turma_atualizada = Turma(
            id=id,
            nome=dto.nome,
            id_atividade=dto.id_atividade,
            id_professor=dto.id_professor,
            horario_inicio=dto.horario_inicio,
            horario_fim=dto.horario_fim,
            dias_semana=dto.dias_semana,
            vagas=dto.vagas
        )

        turma_repo.alterar(turma_atualizada)
        logger.info(f"Turma {id} alterada por admin {usuario_logado['id']}")

        informar_sucesso(request, "Turma alterada com sucesso!")
        return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["turma"] = turma_repo.obter_por_id(id)
        dados_formulario["atividades"] = atividade_repo.obter_todos()
        dados_formulario["professores"] = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)
        raise FormValidationError(
            validation_error=e,
            template_path="admin/turmas/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


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
    logger.info(f"Turma {id} excluída por admin {usuario_logado['id']}")

    informar_sucesso(request, "Turma excluída com sucesso!")
    return RedirectResponse("/admin/turmas/listar", status_code=status.HTTP_303_SEE_OTHER)
```

---

## Módulo 4: Professores

Gerenciamento de usuários com perfil Professor (cadastro, edição, exclusão).

### 4.1 - DTO: Criar Professor

**Arquivo:** `dtos/professor_dto.py`

```python
"""
DTOs para validação de dados de Professor.

Fornece validação de campos para operações CRUD de professores.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_nome_pessoa,
    validar_email,
    validar_senha_forte,
    validar_id_positivo,
)


class CriarProfessorDTO(BaseModel):
    """DTO para criação de professor"""

    nome: str
    email: str
    senha: str

    _validar_nome = field_validator("nome")(validar_nome_pessoa())
    _validar_email = field_validator("email")(validar_email())
    _validar_senha = field_validator("senha")(validar_senha_forte())


class AlterarProfessorDTO(BaseModel):
    """DTO para alteração de professor"""

    id: int
    nome: str
    email: str

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(validar_nome_pessoa())
    _validar_email = field_validator("email")(validar_email())
```

### 4.2 - Rota GET: Listar Professores

**Arquivo:** `routes/admin_professores_routes.py` (parte 1/4)

```python
"""
Rotas administrativas para gerenciamento de professores.

Fornece CRUD completo de professores para administradores.
"""
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_utils import requer_autenticacao
from util.perfis import Perfil
from util.mensagens import informar_sucesso, informar_erro
from util.templates import templates
from util.logger_config import logger
from util.rate_limiter import RateLimiter
from util.exceptions import FormValidationError
from util.request_utils import obter_identificador_cliente
from util.security import criar_hash_senha

from repo import usuario_repo
from model.usuario_model import Usuario
from dtos.professor_dto import CriarProfessorDTO, AlterarProfessorDTO

router = APIRouter(prefix="/admin/professores")

# Rate limiter para operações administrativas
admin_professores_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)


def verificar_email_disponivel_professor(email: str, id_excluir: Optional[int] = None) -> tuple[bool, str]:
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
    """Lista todos os professores cadastrados"""
    professores = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)

    return templates.TemplateResponse(
        "admin/professores/listar.html",
        {
            "request": request,
            "professores": professores
        }
    )
```

### 4.3 - Template: Listar Professores

**Arquivo:** `templates/admin/professores/listar.html`

```html
{% extends "base_privada.html" %}

{% block titulo %}Professores{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-person-badge"></i> Professores</h2>
            <a href="/admin/professores/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Novo Professor
            </a>
        </div>

        {% if professores %}
        <div class="card shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th style="width: 5%">#</th>
                                <th style="width: 35%">Nome</th>
                                <th style="width: 40%">Email</th>
                                <th class="text-end" style="width: 20%">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for professor in professores %}
                            <tr>
                                <td>{{ professor.id }}</td>
                                <td>
                                    <strong>{{ professor.nome }}</strong>
                                </td>
                                <td>
                                    <small>{{ professor.email }}</small>
                                </td>
                                <td class="text-end">
                                    <div class="btn-group btn-group-sm">
                                        <a href="/admin/professores/editar/{{ professor.id }}"
                                           class="btn btn-outline-primary"
                                           title="Editar professor">
                                            <i class="bi bi-pencil"></i> Editar
                                        </a>
                                        <button type="button"
                                                class="btn btn-outline-danger"
                                                title="Excluir professor"
                                                onclick="excluirProfessor({{ professor.id }}, '{{ professor.nome|replace(\"'\", \"\\\\'\") }}')">
                                            <i class="bi bi-trash"></i> Excluir
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card-footer text-muted">
                <small><i class="bi bi-info-circle"></i> Total: {{ professores|length }} professor(es)</small>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info" role="alert">
            <h4 class="alert-heading"><i class="bi bi-info-circle"></i> Nenhum professor cadastrado</h4>
            <p>Não há professores cadastrados no sistema. Clique em "Novo Professor" para começar.</p>
            <hr>
            <a href="/admin/professores/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Cadastrar Primeiro Professor
            </a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
/**
 * Abre modal de confirmação para excluir professor
 */
function excluirProfessor(professorId, professorNome) {
    const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <h6 class="card-title mb-2">
                    <i class="bi bi-person-badge"></i> Professor:
                </h6>
                <p class="mb-0"><strong>${professorNome}</strong></p>
            </div>
        </div>
        <div class="alert alert-warning mt-3 mb-0">
            <i class="bi bi-exclamation-triangle"></i>
            <strong>Atenção:</strong> Esta ação não pode ser desfeita.
            Todas as turmas deste professor poderão ser afetadas.
        </div>
    `;

    abrirModalConfirmacao({
        url: `/admin/professores/${professorId}/excluir`,
        mensagem: 'Tem certeza que deseja excluir este professor?',
        detalhes: detalhes
    });
}
</script>
{% endblock %}
```

### 4.4 - Rota GET: Cadastrar Professor

**Arquivo:** `routes/admin_professores_routes.py` (parte 2/4)

```python
@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de professor"""
    return templates.TemplateResponse(
        "admin/professores/cadastrar.html",
        {
            "request": request,
        }
    )
```

### 4.5 - Template: Cadastrar Professor

**Arquivo:** `templates/admin/professores/cadastrar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Cadastrar Professor{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-person-plus"></i> Cadastrar Novo Professor</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/professores/cadastrar">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome Completo', type='text', required=true,
                                   attributes={'maxlength': 256, 'placeholder': 'Nome completo do professor'}) }}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='email', label='Email', type='email', required=true,
                                   attributes={'maxlength': 256, 'placeholder': 'email@exemplo.com'}) }}
                        </div>

                        <div class="col-md-6 mb-3 mb-md-0">
                            {{ field(name='senha', label='Senha', type='password', required=true) }}
                        </div>

                        <div class="col-md-6 mb-3 mb-md-0">
                            {{ field(name='confirma_senha', label='Confirmar Senha', type='password', required=true) }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Cadastrar
                        </button>
                        <a href="/admin/professores/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
// Inicializar validador de senha
const passwordValidator = new PasswordValidator({
    passwordFieldId: 'senha',
    confirmPasswordFieldId: 'confirma_senha',
    minLength: 6
});

// Validação do formulário
document.querySelector('form').addEventListener('submit', function (e) {
    if (!passwordValidator.validateForm()) {
        e.preventDefault();
        return false;
    }
});
</script>
{% endblock %}
```

### 4.6 - Rota POST: Cadastrar Professor

**Arquivo:** `routes/admin_professores_routes.py` (parte 3/4)

```python
@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Cadastra um novo professor"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_professores_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {"nome": nome, "email": email}

    try:
        # Validar com DTO
        dto = CriarProfessorDTO(nome=nome, email=email, senha=senha)

        # Verificar se email já existe
        disponivel, mensagem_erro = verificar_email_disponivel_professor(dto.email)
        if not disponivel:
            informar_erro(request, mensagem_erro)
            return templates.TemplateResponse(
                "admin/professores/cadastrar.html",
                {
                    "request": request,
                    "dados": dados_formulario
                }
            )

        # Criar hash da senha
        senha_hash = criar_hash_senha(dto.senha)

        # Criar professor
        professor = Usuario(
            id=0,
            nome=dto.nome,
            email=dto.email,
            senha=senha_hash,
            perfil=Perfil.PROFESSOR.value
        )

        usuario_repo.inserir(professor)
        logger.info(f"Professor '{dto.email}' cadastrado por admin {usuario_logado['id']}")

        informar_sucesso(request, "Professor cadastrado com sucesso!")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        raise FormValidationError(
            validation_error=e,
            template_path="admin/professores/cadastrar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.get("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_editar(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exibe formulário de edição de professor"""
    professor = usuario_repo.obter_por_id(id)

    if not professor or professor.perfil != Perfil.PROFESSOR.value:
        informar_erro(request, "Professor não encontrado")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Criar cópia dos dados sem senha
    dados_professor = professor.__dict__.copy()
    dados_professor.pop('senha', None)

    return templates.TemplateResponse(
        "admin/professores/editar.html",
        {
            "request": request,
            "professor": professor,
            "dados": dados_professor
        }
    )
```

### 4.7 - Template: Editar Professor

**Arquivo:** `templates/admin/professores/editar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Editar Professor{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-person-gear"></i> Editar Professor</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/professores/editar/{{ dados.id if dados.id is defined else professor.id }}">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome Completo', type='text', required=true,
                                   value=dados.nome, attributes={'maxlength': 256}) }}
                        </div>

                        <div class="col-12">
                            {{ field(name='email', label='Email', type='email', required=true,
                                   value=dados.email, attributes={'maxlength': 256}, wrapper_class='mb-0') }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Salvar Alterações
                        </button>
                        <a href="/admin/professores/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 4.8 - Rota POST: Editar e Excluir Professor

**Arquivo:** `routes/admin_professores_routes.py` (parte 4/4)

```python
@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    nome: str = Form(...),
    email: str = Form(...),
    usuario_logado: Optional[dict] = None
):
    """Edita um professor existente"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_professores_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se professor existe
    professor_atual = usuario_repo.obter_por_id(id)
    if not professor_atual or professor_atual.perfil != Perfil.PROFESSOR.value:
        informar_erro(request, "Professor não encontrado")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Armazena dados do formulário
    dados_formulario: dict = {"id": id, "nome": nome, "email": email}

    try:
        # Validar com DTO
        dto = AlterarProfessorDTO(id=id, nome=nome, email=email)

        # Verificar se email já existe em outro usuário
        disponivel, mensagem_erro = verificar_email_disponivel_professor(dto.email, id)
        if not disponivel:
            informar_erro(request, mensagem_erro)
            return templates.TemplateResponse(
                "admin/professores/editar.html",
                {
                    "request": request,
                    "professor": professor_atual,
                    "dados": dados_formulario
                }
            )

        # Atualizar professor
        professor_atualizado = Usuario(
            id=id,
            nome=dto.nome,
            email=dto.email,
            senha=professor_atual.senha,  # Mantém senha existente
            perfil=Perfil.PROFESSOR.value
        )

        usuario_repo.alterar(professor_atualizado)
        logger.info(f"Professor {id} alterado por admin {usuario_logado['id']}")

        informar_sucesso(request, "Professor alterado com sucesso!")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["professor"] = usuario_repo.obter_por_id(id)
        raise FormValidationError(
            validation_error=e,
            template_path="admin/professores/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="nome",
        )


@router.post("/excluir/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(request: Request, id: int, usuario_logado: Optional[dict] = None):
    """Exclui um professor"""
    assert usuario_logado is not None

    # Rate limiting
    ip = obter_identificador_cliente(request)
    if not admin_professores_limiter.verificar(ip):
        informar_erro(request, "Muitas operações. Aguarde um momento e tente novamente.")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    professor = usuario_repo.obter_por_id(id)

    if not professor or professor.perfil != Perfil.PROFESSOR.value:
        informar_erro(request, "Professor não encontrado")
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    # Verificar se há turmas associadas a este professor
    from repo import turma_repo
    turmas = turma_repo.obter_por_professor(id)
    if turmas:
        informar_erro(
            request,
            f"Não é possível excluir este professor pois há {len(turmas)} turma(s) sob sua responsabilidade."
        )
        return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)

    usuario_repo.excluir(id)
    logger.info(f"Professor {id} excluído por admin {usuario_logado['id']}")

    informar_sucesso(request, "Professor excluído com sucesso!")
    return RedirectResponse("/admin/professores/listar", status_code=status.HTTP_303_SEE_OTHER)
```

---

## Módulo 5: Alunos

Gerenciamento de usuários com perfil Aluno (cadastro, edição, exclusão).

### 5.1 - DTO: Criar Aluno

**Arquivo:** `dtos/aluno_dto.py`

```python
"""
DTOs para validação de dados de Aluno.

Fornece validação de campos para operações CRUD de alunos.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import (
    validar_nome_pessoa,
    validar_email,
    validar_senha_forte,
    validar_id_positivo,
)


class CriarAlunoDTO(BaseModel):
    """DTO para criação de aluno"""

    nome: str
    email: str
    senha: str

    _validar_nome = field_validator("nome")(validar_nome_pessoa())
    _validar_email = field_validator("email")(validar_email())
    _validar_senha = field_validator("senha")(validar_senha_forte())


class AlterarAlunoDTO(BaseModel):
    """DTO para alteração de aluno"""

    id: int
    nome: str
    email: str

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_nome = field_validator("nome")(validar_nome_pessoa())
    _validar_email = field_validator("email")(validar_email())
```

### 5.2 - Rota GET: Listar Alunos

**Arquivo:** `routes/admin_alunos_routes.py` (parte 1/4)

```python
"""
Rotas administrativas para gerenciamento de alunos.

Fornece CRUD completo de alunos para administradores.
"""
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_utils import requer_autenticacao
from util.perfis import Perfil
from util.mensagens import informar_sucesso, informar_erro
from util.templates import templates
from util.logger_config import logger
from util.rate_limiter import RateLimiter
from util.exceptions import FormValidationError
from util.request_utils import obter_identificador_cliente
from util.security import criar_hash_senha

from repo import usuario_repo
from model.usuario_model import Usuario
from dtos.aluno_dto import CriarAlunoDTO, AlterarAlunoDTO

router = APIRouter(prefix="/admin/alunos")

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
```

### 5.3 - Template: Listar Alunos

**Arquivo:** `templates/admin/alunos/listar.html`

```html
{% extends "base_privada.html" %}

{% block titulo %}Alunos{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-person-circle"></i> Alunos</h2>
            <a href="/admin/alunos/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Novo Aluno
            </a>
        </div>

        {% if alunos %}
        <div class="card shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th style="width: 5%">#</th>
                                <th style="width: 35%">Nome</th>
                                <th style="width: 40%">Email</th>
                                <th class="text-end" style="width: 20%">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for aluno in alunos %}
                            <tr>
                                <td>{{ aluno.id }}</td>
                                <td>
                                    <strong>{{ aluno.nome }}</strong>
                                </td>
                                <td>
                                    <small>{{ aluno.email }}</small>
                                </td>
                                <td class="text-end">
                                    <div class="btn-group btn-group-sm">
                                        <a href="/admin/alunos/editar/{{ aluno.id }}"
                                           class="btn btn-outline-primary"
                                           title="Editar aluno">
                                            <i class="bi bi-pencil"></i> Editar
                                        </a>
                                        <button type="button"
                                                class="btn btn-outline-danger"
                                                title="Excluir aluno"
                                                onclick="excluirAluno({{ aluno.id }}, '{{ aluno.nome|replace(\"'\", \"\\\\'\") }}')">
                                            <i class="bi bi-trash"></i> Excluir
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card-footer text-muted">
                <small><i class="bi bi-info-circle"></i> Total: {{ alunos|length }} aluno(s)</small>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info" role="alert">
            <h4 class="alert-heading"><i class="bi bi-info-circle"></i> Nenhum aluno cadastrado</h4>
            <p>Não há alunos cadastrados no sistema. Clique em "Novo Aluno" para começar.</p>
            <hr>
            <a href="/admin/alunos/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Cadastrar Primeiro Aluno
            </a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
/**
 * Abre modal de confirmação para excluir aluno
 */
function excluirAluno(alunoId, alunoNome) {
    const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <h6 class="card-title mb-2">
                    <i class="bi bi-person-circle"></i> Aluno:
                </h6>
                <p class="mb-0"><strong>${alunoNome}</strong></p>
            </div>
        </div>
        <div class="alert alert-warning mt-3 mb-0">
            <i class="bi bi-exclamation-triangle"></i>
            <strong>Atenção:</strong> Esta ação não pode ser desfeita.
            Todas as matrículas deste aluno serão excluídas.
        </div>
    `;

    abrirModalConfirmacao({
        url: `/admin/alunos/${alunoId}/excluir`,
        mensagem: 'Tem certeza que deseja excluir este aluno?',
        detalhes: detalhes
    });
}
</script>
{% endblock %}
```

### 5.4 - Rota GET: Cadastrar Aluno

**Arquivo:** `routes/admin_alunos_routes.py` (parte 2/4)

```python
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
```

### 5.5 - Template: Cadastrar Aluno

**Arquivo:** `templates/admin/alunos/cadastrar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Cadastrar Aluno{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-person-plus"></i> Cadastrar Novo Aluno</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/alunos/cadastrar">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome Completo', type='text', required=true,
                                   attributes={'maxlength': 256, 'placeholder': 'Nome completo do aluno'}) }}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='email', label='Email', type='email', required=true,
                                   attributes={'maxlength': 256, 'placeholder': 'email@exemplo.com'}) }}
                        </div>

                        <div class="col-md-6 mb-3 mb-md-0">
                            {{ field(name='senha', label='Senha', type='password', required=true) }}
                        </div>

                        <div class="col-md-6 mb-3 mb-md-0">
                            {{ field(name='confirma_senha', label='Confirmar Senha', type='password', required=true) }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Cadastrar
                        </button>
                        <a href="/admin/alunos/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
// Inicializar validador de senha
const passwordValidator = new PasswordValidator({
    passwordFieldId: 'senha',
    confirmPasswordFieldId: 'confirma_senha',
    minLength: 6
});

// Validação do formulário
document.querySelector('form').addEventListener('submit', function (e) {
    if (!passwordValidator.validateForm()) {
        e.preventDefault();
        return false;
    }
});
</script>
{% endblock %}
```

### 5.6 - Rota POST: Cadastrar Aluno

**Arquivo:** `routes/admin_alunos_routes.py` (parte 3/4)

```python
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
        raise FormValidationError(
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
```

### 5.7 - Template: Editar Aluno

**Arquivo:** `templates/admin/alunos/editar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Editar Aluno{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-person-gear"></i> Editar Aluno</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/alunos/editar/{{ dados.id if dados.id is defined else aluno.id }}">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {{ field(name='nome', label='Nome Completo', type='text', required=true,
                                   value=dados.nome, attributes={'maxlength': 256}) }}
                        </div>

                        <div class="col-12">
                            {{ field(name='email', label='Email', type='email', required=true,
                                   value=dados.email, attributes={'maxlength': 256}, wrapper_class='mb-0') }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Salvar Alterações
                        </button>
                        <a href="/admin/alunos/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.8 - Rota POST: Editar e Excluir Aluno

**Arquivo:** `routes/admin_alunos_routes.py` (parte 4/4)

```python
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
        raise FormValidationError(
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
```

---

## Módulo 6: Matrículas

Gerenciamento de matrículas de alunos em turmas.

### 6.1 - DTO: Criar Matrícula

**Arquivo:** `dtos/matricula_dto.py`

```python
"""
DTOs para validação de dados de Matrícula.

Fornece validação de campos para operações CRUD de matrículas.
"""
from pydantic import BaseModel, field_validator
from dtos.validators import validar_id_positivo


class CriarMatriculaDTO(BaseModel):
    """DTO para criação de matrícula"""

    id_aluno: int
    id_turma: int

    _validar_id_aluno = field_validator("id_aluno")(validar_id_positivo())
    _validar_id_turma = field_validator("id_turma")(validar_id_positivo())


class AlterarMatriculaDTO(BaseModel):
    """DTO para alteração de matrícula"""

    id: int
    id_aluno: int
    id_turma: int

    _validar_id = field_validator("id")(validar_id_positivo())
    _validar_id_aluno = field_validator("id_aluno")(validar_id_positivo())
    _validar_id_turma = field_validator("id_turma")(validar_id_positivo())
```

### 6.2 - Rota GET: Listar Matrículas

**Arquivo:** `routes/admin_matriculas_routes.py` (parte 1/4)

```python
"""
Rotas administrativas para gerenciamento de matrículas.

Fornece CRUD completo de matrículas para administradores.
"""
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_utils import requer_autenticacao
from util.perfis import Perfil
from util.mensagens import informar_sucesso, informar_erro
from util.templates import templates
from util.logger_config import logger
from util.rate_limiter import RateLimiter
from util.exceptions import FormValidationError
from util.request_utils import obter_identificador_cliente

from repo import matricula_repo, usuario_repo, turma_repo
from model.matricula_model import Matricula
from dtos.matricula_dto import CriarMatriculaDTO, AlterarMatriculaDTO

router = APIRouter(prefix="/admin/matriculas")

# Rate limiter para operações administrativas
admin_matriculas_limiter = RateLimiter(max_tentativas=10, janela_minutos=1)


@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as matrículas cadastradas"""
    matriculas = matricula_repo.obter_todos()
    alunos = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
    turmas = turma_repo.obter_todos()

    # Criar dicionários para lookup
    alunos_dict = {aluno.id: aluno.nome for aluno in alunos}
    turmas_dict = {turma.id: turma.nome for turma in turmas}

    return templates.TemplateResponse(
        "admin/matriculas/listar.html",
        {
            "request": request,
            "matriculas": matriculas,
            "alunos_dict": alunos_dict,
            "turmas_dict": turmas_dict
        }
    )
```

### 6.3 - Template: Listar Matrículas

**Arquivo:** `templates/admin/matriculas/listar.html`

```html
{% extends "base_privada.html" %}

{% block titulo %}Matrículas{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-card-checklist"></i> Matrículas</h2>
            <a href="/admin/matriculas/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Nova Matrícula
            </a>
        </div>

        {% if matriculas %}
        <div class="card shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover mb-0">
                        <thead>
                            <tr>
                                <th style="width: 5%">#</th>
                                <th style="width: 35%">Aluno</th>
                                <th style="width: 35%">Turma</th>
                                <th style="width: 15%">Data Matrícula</th>
                                <th class="text-end" style="width: 10%">Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for matricula in matriculas %}
                            <tr>
                                <td>{{ matricula.id }}</td>
                                <td>
                                    <strong>{{ alunos_dict.get(matricula.id_aluno, 'N/A') }}</strong>
                                </td>
                                <td>
                                    <span class="badge bg-primary">
                                        {{ turmas_dict.get(matricula.id_turma, 'N/A') }}
                                    </span>
                                </td>
                                <td>
                                    <small>{{ matricula.data_matricula.strftime('%d/%m/%Y') }}</small>
                                </td>
                                <td class="text-end">
                                    <div class="btn-group btn-group-sm">
                                        <a href="/admin/matriculas/editar/{{ matricula.id }}"
                                           class="btn btn-outline-primary"
                                           title="Editar matrícula">
                                            <i class="bi bi-pencil"></i>
                                        </a>
                                        <button type="button"
                                                class="btn btn-outline-danger"
                                                title="Cancelar matrícula"
                                                onclick="excluirMatricula({{ matricula.id }}, '{{ alunos_dict.get(matricula.id_aluno, \"\")|replace(\"'\", \"\\\\'\") }}', '{{ turmas_dict.get(matricula.id_turma, \"\")|replace(\"'\", \"\\\\'\") }}')">
                                            <i class="bi bi-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="card-footer text-muted">
                <small><i class="bi bi-info-circle"></i> Total: {{ matriculas|length }} matrícula(s)</small>
            </div>
        </div>
        {% else %}
        <div class="alert alert-info" role="alert">
            <h4 class="alert-heading"><i class="bi bi-info-circle"></i> Nenhuma matrícula cadastrada</h4>
            <p>Não há matrículas cadastradas no sistema. Clique em "Nova Matrícula" para começar.</p>
            <hr>
            <a href="/admin/matriculas/cadastrar" class="btn btn-success">
                <i class="bi bi-plus-circle"></i> Cadastrar Primeira Matrícula
            </a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
/**
 * Abre modal de confirmação para excluir matrícula
 */
function excluirMatricula(matriculaId, alunoNome, turmaNome) {
    const detalhes = `
        <div class="card bg-light">
            <div class="card-body">
                <h6 class="card-title mb-2">
                    <i class="bi bi-person-circle"></i> Aluno:
                </h6>
                <p class="mb-2"><strong>${alunoNome}</strong></p>
                <h6 class="card-title mb-2">
                    <i class="bi bi-people-fill"></i> Turma:
                </h6>
                <p class="mb-0"><strong>${turmaNome}</strong></p>
            </div>
        </div>
        <div class="alert alert-warning mt-3 mb-0">
            <i class="bi bi-exclamation-triangle"></i>
            <strong>Atenção:</strong> Esta ação cancelará a matrícula do aluno nesta turma.
        </div>
    `;

    abrirModalConfirmacao({
        url: `/admin/matriculas/${matriculaId}/excluir`,
        mensagem: 'Tem certeza que deseja cancelar esta matrícula?',
        detalhes: detalhes
    });
}
</script>
{% endblock %}
```

### 6.4 - Rota GET: Cadastrar Matrícula

**Arquivo:** `routes/admin_matriculas_routes.py` (parte 2/4)

```python
@router.get("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_cadastrar(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário de cadastro de matrícula"""
    alunos = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
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
```

### 6.5 - Template: Cadastrar Matrícula

**Arquivo:** `templates/admin/matriculas/cadastrar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Cadastrar Matrícula{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-plus-circle"></i> Cadastrar Nova Matrícula</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/matriculas/cadastrar">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {% set alunos_dict = {} %}
                            {% for aluno in alunos %}
                            {% set _ = alunos_dict.update({aluno.id|string: aluno.nome ~ ' (' ~ aluno.email ~ ')'}) %}
                            {% endfor %}
                            {{ field(name='id_aluno', label='Aluno', type='select', required=true,
                                   options=alunos_dict) }}
                        </div>

                        <div class="col-12">
                            {% set turmas_dict = {} %}
                            {% for turma in turmas %}
                            {% set _ = turmas_dict.update({turma.id|string: turma.nome}) %}
                            {% endfor %}
                            {{ field(name='id_turma', label='Turma', type='select', required=true,
                                   options=turmas_dict, wrapper_class='mb-0') }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Cadastrar
                        </button>
                        <a href="/admin/matriculas/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 6.6 - Rota POST: Cadastrar Matrícula

**Arquivo:** `routes/admin_matriculas_routes.py` (parte 3/4)

```python
@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    id_aluno: int = Form(...),
    id_turma: int = Form(...),
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
        "id_turma": id_turma
    }

    try:
        # Validar com DTO
        dto = CriarMatriculaDTO(id_aluno=id_aluno, id_turma=id_turma)

        # Verificar se aluno existe
        aluno = usuario_repo.obter_por_id(dto.id_aluno)
        if not aluno or aluno.perfil != Perfil.ALUNO.value:
            informar_erro(request, "Aluno selecionado não existe.")
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se turma existe
        turma = turma_repo.obter_por_id(dto.id_turma)
        if not turma:
            informar_erro(request, "Turma selecionada não existe.")
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se aluno já está matriculado nesta turma
        matricula_existente = matricula_repo.obter_por_aluno_e_turma(dto.id_aluno, dto.id_turma)
        if matricula_existente:
            informar_erro(request, "Este aluno já está matriculado nesta turma.")
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se há vagas disponíveis
        total_matriculas = len(matricula_repo.obter_por_turma(dto.id_turma))
        if total_matriculas >= turma.vagas:
            informar_erro(request, "Esta turma não possui vagas disponíveis.")
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/cadastrar.html",
                {"request": request, **dados_formulario}
            )

        # Criar matrícula
        from datetime import datetime
        matricula = Matricula(
            id=0,
            id_aluno=dto.id_aluno,
            id_turma=dto.id_turma,
            data_matricula=datetime.now()
        )

        matricula_repo.inserir(matricula)
        logger.info(f"Matrícula criada: aluno {dto.id_aluno} na turma {dto.id_turma} por admin {usuario_logado['id']}")

        informar_sucesso(request, "Matrícula cadastrada com sucesso!")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
        dados_formulario["turmas"] = turma_repo.obter_todos()
        raise FormValidationError(
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

    alunos = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
    turmas = turma_repo.obter_todos()
    dados_matricula = matricula.__dict__.copy()

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
```

### 6.7 - Template: Editar Matrícula

**Arquivo:** `templates/admin/matriculas/editar.html`

```html
{% extends "base_privada.html" %}
{% from "macros/form_fields.html" import field with context %}

{% block titulo %}Editar Matrícula{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="d-flex align-items-center mb-4">
            <h2 class="mb-0"><i class="bi bi-card-checklist"></i> Editar Matrícula</h2>
        </div>

        <div class="card shadow-sm">
            <form method="POST" action="/admin/matriculas/editar/{{ dados.id if dados.id is defined else matricula.id }}">
                <div class="card-body p-4">
                    <div class="row">
                        <div class="col-12">
                            {% include "components/alerta_erro.html" %}
                        </div>

                        <div class="col-12 mb-3">
                            {% set alunos_dict = {} %}
                            {% for aluno in alunos %}
                            {% set _ = alunos_dict.update({aluno.id|string: aluno.nome ~ ' (' ~ aluno.email ~ ')'}) %}
                            {% endfor %}
                            {{ field(name='id_aluno', label='Aluno', type='select', required=true,
                                   options=alunos_dict, value=dados.id_aluno) }}
                        </div>

                        <div class="col-12">
                            {% set turmas_dict = {} %}
                            {% for turma in turmas %}
                            {% set _ = turmas_dict.update({turma.id|string: turma.nome}) %}
                            {% endfor %}
                            {{ field(name='id_turma', label='Turma', type='select', required=true,
                                   options=turmas_dict, value=dados.id_turma, wrapper_class='mb-0') }}
                        </div>
                    </div>
                </div>
                <div class="card-footer p-4">
                    <div class="d-flex gap-3">
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-check-circle"></i> Salvar Alterações
                        </button>
                        <a href="/admin/matriculas/listar" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancelar
                        </a>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 6.8 - Rota POST: Editar e Excluir Matrícula

**Arquivo:** `routes/admin_matriculas_routes.py` (parte 4/4)

```python
@router.post("/editar/{id}")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_editar(
    request: Request,
    id: int,
    id_aluno: int = Form(...),
    id_turma: int = Form(...),
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
        "id": id,
        "id_aluno": id_aluno,
        "id_turma": id_turma
    }

    try:
        # Validar com DTO
        dto = AlterarMatriculaDTO(id=id, id_aluno=id_aluno, id_turma=id_turma)

        # Verificar se aluno existe
        aluno = usuario_repo.obter_por_id(dto.id_aluno)
        if not aluno or aluno.perfil != Perfil.ALUNO.value:
            informar_erro(request, "Aluno selecionado não existe.")
            dados_formulario["matricula"] = matricula_atual
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/editar.html",
                {"request": request, **dados_formulario}
            )

        # Verificar se turma existe
        turma = turma_repo.obter_por_id(dto.id_turma)
        if not turma:
            informar_erro(request, "Turma selecionada não existe.")
            dados_formulario["matricula"] = matricula_atual
            dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
            dados_formulario["turmas"] = turma_repo.obter_todos()
            return templates.TemplateResponse(
                "admin/matriculas/editar.html",
                {"request": request, **dados_formulario}
            )

        # Atualizar matrícula
        matricula_atualizada = Matricula(
            id=id,
            id_aluno=dto.id_aluno,
            id_turma=dto.id_turma,
            data_matricula=matricula_atual.data_matricula
        )

        matricula_repo.alterar(matricula_atualizada)
        logger.info(f"Matrícula {id} alterada por admin {usuario_logado['id']}")

        informar_sucesso(request, "Matrícula alterada com sucesso!")
        return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        dados_formulario["matricula"] = matricula_repo.obter_por_id(id)
        dados_formulario["alunos"] = usuario_repo.obter_por_perfil(Perfil.ALUNO.value)
        dados_formulario["turmas"] = turma_repo.obter_todos()
        raise FormValidationError(
            validation_error=e,
            template_path="admin/matriculas/editar.html",
            dados_formulario=dados_formulario,
            campo_padrao="id_aluno",
        )


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

    matricula_repo.excluir(id)
    logger.info(f"Matrícula {id} excluída por admin {usuario_logado['id']}")

    informar_sucesso(request, "Matrícula cancelada com sucesso!")
    return RedirectResponse("/admin/matriculas/listar", status_code=status.HTTP_303_SEE_OTHER)
```

---

## Módulo 7: Dashboard de Estatísticas

Dashboard administrativo com estatísticas e métricas do sistema.

### 7.1 - Rota GET: Dashboard de Estatísticas

**Arquivo:** `routes/admin_estatisticas_routes.py`

```python
"""
Rotas administrativas para visualização de estatísticas.

Fornece dashboard com métricas e indicadores do sistema.
"""
from typing import Optional
from fastapi import APIRouter, Request
from util.auth_utils import requer_autenticacao
from util.perfis import Perfil
from util.templates import templates

from repo import (
    usuario_repo,
    categoria_repo,
    atividade_repo,
    turma_repo,
    matricula_repo
)

router = APIRouter(prefix="/admin/estatisticas")


@router.get("/dashboard")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_dashboard(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe dashboard com estatísticas do sistema"""

    # Contadores gerais
    total_alunos = len(usuario_repo.obter_por_perfil(Perfil.ALUNO.value))
    total_professores = len(usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value))
    total_categorias = len(categoria_repo.obter_todos())
    total_atividades = len(atividade_repo.obter_todos())
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
    atividades = atividade_repo.obter_todos()
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
    professores = usuario_repo.obter_por_perfil(Perfil.PROFESSOR.value)
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
```

### 7.2 - Template: Dashboard de Estatísticas

**Arquivo:** `templates/admin/estatisticas/dashboard.html`

```html
{% extends "base_privada.html" %}

{% block titulo %}Dashboard{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2><i class="bi bi-bar-chart-fill"></i> Dashboard de Estatísticas</h2>
        </div>

        <!-- Cards de Resumo -->
        <div class="row g-3 mb-4">
            <div class="col-md-4">
                <div class="card bg-primary text-white shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2 opacity-75">Total de Alunos</h6>
                                <h2 class="card-title mb-0">{{ total_alunos }}</h2>
                            </div>
                            <div>
                                <i class="bi bi-person-circle" style="font-size: 3rem; opacity: 0.5;"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-success text-white shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2 opacity-75">Total de Professores</h6>
                                <h2 class="card-title mb-0">{{ total_professores }}</h2>
                            </div>
                            <div>
                                <i class="bi bi-person-badge" style="font-size: 3rem; opacity: 0.5;"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-info text-white shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2 opacity-75">Total de Turmas</h6>
                                <h2 class="card-title mb-0">{{ total_turmas }}</h2>
                            </div>
                            <div>
                                <i class="bi bi-people-fill" style="font-size: 3rem; opacity: 0.5;"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-warning text-dark shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2 opacity-75">Total de Categorias</h6>
                                <h2 class="card-title mb-0">{{ total_categorias }}</h2>
                            </div>
                            <div>
                                <i class="bi bi-tags" style="font-size: 3rem; opacity: 0.3;"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-secondary text-white shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2 opacity-75">Total de Atividades</h6>
                                <h2 class="card-title mb-0">{{ total_atividades }}</h2>
                            </div>
                            <div>
                                <i class="bi bi-activity" style="font-size: 3rem; opacity: 0.5;"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card bg-dark text-white shadow-sm">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="card-subtitle mb-2 opacity-75">Total de Matrículas</h6>
                                <h2 class="card-title mb-0">{{ total_matriculas }}</h2>
                            </div>
                            <div>
                                <i class="bi bi-card-checklist" style="font-size: 3rem; opacity: 0.5;"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Turmas Mais Populares -->
        <div class="row mb-4">
            <div class="col-lg-6 mb-4 mb-lg-0">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0"><i class="bi bi-trophy"></i> Top 5 Turmas (Mais Matriculadas)</h5>
                    </div>
                    <div class="card-body">
                        {% if top_turmas %}
                        <div class="list-group list-group-flush">
                            {% for item in top_turmas %}
                            <div class="list-group-item">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div class="flex-grow-1">
                                        <h6 class="mb-1">{{ item.turma.nome }}</h6>
                                        <small class="text-muted">
                                            {{ item.num_matriculas }} / {{ item.turma.vagas }} alunos
                                            ({{ item.percentual_ocupacao }}% ocupação)
                                        </small>
                                    </div>
                                    <div>
                                        <span class="badge bg-primary rounded-pill">{{ item.num_matriculas }}</span>
                                    </div>
                                </div>
                                <div class="progress mt-2" style="height: 8px;">
                                    <div class="progress-bar bg-primary" role="progressbar"
                                         style="width: {{ item.percentual_ocupacao }}%"
                                         aria-valuenow="{{ item.percentual_ocupacao }}"
                                         aria-valuemin="0" aria-valuemax="100"></div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                        {% else %}
                        <p class="text-muted mb-0">Nenhuma turma cadastrada.</p>
                        {% endif %}
                    </div>
                </div>
            </div>

            <!-- Atividades Mais Populares -->
            <div class="col-lg-6">
                <div class="card shadow-sm">
                    <div class="card-header bg-success text-white">
                        <h5 class="mb-0"><i class="bi bi-fire"></i> Top 5 Atividades (Mais Alunos)</h5>
                    </div>
                    <div class="card-body">
                        {% if top_atividades %}
                        <div class="list-group list-group-flush">
                            {% for item in top_atividades %}
                            <div class="list-group-item">
                                <div class="d-flex justify-content-between align-items-center">
                                    <div>
                                        <h6 class="mb-1">{{ item.atividade.nome }}</h6>
                                        <small class="text-muted">
                                            {{ item.num_turmas }} turma(s) | {{ item.num_alunos }} aluno(s)
                                        </small>
                                    </div>
                                    <div>
                                        <span class="badge bg-success rounded-pill">{{ item.num_alunos }}</span>
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
                        {% else %}
                        <p class="text-muted mb-0">Nenhuma atividade cadastrada.</p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>

        <!-- Professores e Cargas -->
        <div class="row">
            <div class="col-12">
                <div class="card shadow-sm">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0"><i class="bi bi-person-workspace"></i> Professores e Cargas Horárias</h5>
                    </div>
                    <div class="card-body">
                        {% if professores_com_turmas %}
                        <div class="table-responsive">
                            <table class="table table-hover mb-0">
                                <thead>
                                    <tr>
                                        <th>Professor</th>
                                        <th class="text-center">Turmas</th>
                                        <th class="text-center">Total de Alunos</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for item in professores_com_turmas %}
                                    <tr>
                                        <td>
                                            <strong>{{ item.professor.nome }}</strong>
                                            <br>
                                            <small class="text-muted">{{ item.professor.email }}</small>
                                        </td>
                                        <td class="text-center">
                                            <span class="badge bg-info">{{ item.num_turmas }}</span>
                                        </td>
                                        <td class="text-center">
                                            <span class="badge bg-primary">{{ item.num_alunos }}</span>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                        {% else %}
                        <p class="text-muted mb-0">Nenhum professor cadastrado.</p>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Checklist de Implementação

### Ordem Recomendada de Implementação

1. **Módulo 1: Categorias** ✓
   - [ ] Criar `dtos/categoria_dto.py`
   - [ ] Criar `routes/admin_categorias_routes.py`
   - [ ] Criar templates em `templates/admin/categorias/`
   - [ ] Registrar router em `main.py`
   - [ ] Testar CRUD completo

2. **Módulo 2: Atividades** ✓
   - [ ] Criar `dtos/atividade_dto.py`
   - [ ] Criar `routes/admin_atividades_routes.py`
   - [ ] Criar templates em `templates/admin/atividades/`
   - [ ] Registrar router em `main.py`
   - [ ] Testar CRUD completo

3. **Módulo 3: Turmas** ✓ (parcial - continua com mesmo padrão)
   - [ ] Criar `dtos/turma_dto.py`
   - [ ] Criar `routes/admin_turmas_routes.py`
   - [ ] Criar templates em `templates/admin/turmas/`
   - [ ] Registrar router em `main.py`
   - [ ] Testar CRUD completo

4. **Módulo 4: Professores**
   - [ ] Criar `dtos/professor_dto.py`
   - [ ] Criar `routes/admin_professores_routes.py`
   - [ ] Criar templates em `templates/admin/professores/`
   - [ ] Registrar router em `main.py`
   - [ ] Testar CRUD completo

5. **Módulo 5: Alunos**
   - [ ] Criar `dtos/aluno_dto.py`
   - [ ] Criar `routes/admin_alunos_routes.py`
   - [ ] Criar templates em `templates/admin/alunos/`
   - [ ] Registrar router em `main.py`
   - [ ] Testar CRUD completo

6. **Módulo 6: Matrículas**
   - [ ] Criar `dtos/matricula_dto.py`
   - [ ] Criar `routes/admin_matriculas_routes.py`
   - [ ] Criar templates em `templates/admin/matriculas/`
   - [ ] Registrar router em `main.py`
   - [ ] Testar CRUD completo

7. **Módulo 7: Dashboard de Estatísticas**
   - [ ] Criar `routes/admin_estatisticas_routes.py`
   - [ ] Criar template em `templates/admin/estatisticas/dashboard.html`
   - [ ] Registrar router em `main.py`
   - [ ] Testar visualização de dados

### Registro de Routers em main.py

```python
# Adicionar imports
from routes.admin_categorias_routes import router as admin_categorias_router
from routes.admin_atividades_routes import router as admin_atividades_router
from routes.admin_turmas_routes import router as admin_turmas_router
from routes.admin_professores_routes import router as admin_professores_router
from routes.admin_alunos_routes import router as admin_alunos_router
from routes.admin_matriculas_routes import router as admin_matriculas_router
from routes.admin_estatisticas_routes import router as admin_estatisticas_router

# Registrar routers (após admin_backups_router)
app.include_router(admin_categorias_router, tags=["Admin - Categorias"])
logger.info("Router admin de categorias incluído")

app.include_router(admin_atividades_router, tags=["Admin - Atividades"])
logger.info("Router admin de atividades incluído")

app.include_router(admin_turmas_router, tags=["Admin - Turmas"])
logger.info("Router admin de turmas incluído")

app.include_router(admin_professores_router, tags=["Admin - Professores"])
logger.info("Router admin de professores incluído")

app.include_router(admin_alunos_router, tags=["Admin - Alunos"])
logger.info("Router admin de alunos incluído")

app.include_router(admin_matriculas_router, tags=["Admin - Matrículas"])
logger.info("Router admin de matrículas incluído")

app.include_router(admin_estatisticas_router, tags=["Admin - Estatísticas"])
logger.info("Router admin de estatísticas incluído")
```

### Testes

Para cada módulo, criar arquivo de teste seguindo padrão existente:
- `tests/test_admin_categorias.py`
- `tests/test_admin_atividades.py`
- `tests/test_admin_turmas.py`
- `tests/test_admin_professores.py`
- `tests/test_admin_alunos.py`
- `tests/test_admin_matriculas.py`
- `tests/test_admin_estatisticas.py`

---

**FIM DO DOCUMENTO - FASE 2**

Este plano fornece a base completa para implementação de todos os módulos administrativos do AgendaFit, seguindo rigorosamente os padrões estabelecidos no projeto DefaultWebApp.
