# Checklist de Conformidade - Novo CRUD

**Versão:** 1.0
**Data:** 2025-10-28

Use este checklist ao criar um novo CRUD para garantir conformidade com os padrões da aplicação.

---

## ANTES DE COMEÇAR

- [ ] Li o documento `PADROES_ARQUITETURAIS.md`
- [ ] Identifiquei qual padrão usar (CRUD Completo, Facade, Child Entity, Subsistema, Key-Value)
- [ ] Revisei a implementação de referência (Categoria para CRUD completo)

---

## 1. CAMADA SQL (`sql/<entidade>_sql.py`)

### Estrutura da Tabela

- [ ] **Nome da tabela** em minúsculo e singular
- [ ] **Campo ID** usa `id` simples (não `id_entidade`)
- [ ] **Primary Key:** `id INTEGER PRIMARY KEY AUTOINCREMENT`
- [ ] **Campos obrigatórios** têm `NOT NULL`
- [ ] **Campos únicos** têm `UNIQUE` constraint

### Timestamps

- [ ] **data_cadastro:** `DATETIME DEFAULT CURRENT_TIMESTAMP`
- [ ] **data_atualizacao:** `DATETIME DEFAULT CURRENT_TIMESTAMP` (se entidade for mutável)
- [ ] Outros timestamps específicos conforme necessário (ex: data_conclusao, data_fechamento)

### Foreign Keys

- [ ] Todas as FKs declaradas com `FOREIGN KEY (campo) REFERENCES tabela(id)`
- [ ] FKs têm `ON DELETE RESTRICT` (para relacionamentos importantes) ou
- [ ] FKs têm `ON DELETE CASCADE` (para entidades filhas/dependentes)
- [ ] Exemplo: `FOREIGN KEY (id_categoria) REFERENCES categoria(id) ON DELETE RESTRICT`

### Queries

- [ ] **CRIAR_TABELA** definido
- [ ] **INSERIR** com placeholders `?` (nunca concatenação)
- [ ] **ALTERAR** atualiza `data_atualizacao = CURRENT_TIMESTAMP`
- [ ] **EXCLUIR** definido
- [ ] **OBTER_POR_ID** definido
- [ ] **OBTER_TODOS** com `ORDER BY` lógico
- [ ] **OBTER_QUANTIDADE** (opcional mas recomendado)
- [ ] Queries adicionais conforme necessário (OBTER_POR_*)

### Exemplo Completo:
```python
CRIAR_TABELA = """CREATE TABLE IF NOT EXISTS minha_entidade (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    id_categoria INTEGER NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id) ON DELETE RESTRICT
)"""

INSERIR = "INSERT INTO minha_entidade (nome, descricao, id_categoria) VALUES (?, ?, ?)"
ALTERAR = "UPDATE minha_entidade SET nome = ?, descricao = ?, id_categoria = ?, data_atualizacao = CURRENT_TIMESTAMP WHERE id = ?"
EXCLUIR = "DELETE FROM minha_entidade WHERE id = ?"
OBTER_POR_ID = "SELECT * FROM minha_entidade WHERE id = ?"
OBTER_TODOS = "SELECT * FROM minha_entidade ORDER BY nome"
```

---

## 2. CAMADA MODEL (`model/<entidade>_model.py`)

### Estrutura Básica

- [ ] Usa `from dataclasses import dataclass`
- [ ] Usa `@dataclass` decorator
- [ ] Imports necessários: `from datetime import datetime`, `from typing import Optional`

### Campos

- [ ] **Todos os campos** têm type hints
- [ ] Campo `id: int`
- [ ] Campos obrigatórios sem default
- [ ] Campos opcionais com `Optional[T] = None`
- [ ] `data_cadastro: Optional[datetime] = None`
- [ ] `data_atualizacao: Optional[datetime] = None` (se aplicável)
- [ ] Campos de JOIN opcionais ao final (ex: `categoria: Optional[Categoria] = None`)

### Documentação

- [ ] **Docstring da classe** descrevendo a entidade
- [ ] **Seção Attributes** na docstring listando todos os campos
- [ ] Se for padrão especial (Facade, Child, etc), documentar na docstring

### Exemplo Completo:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MinhaEntidade:
    """
    Model de <descrição da entidade>.

    Attributes:
        id: Identificador único
        nome: Nome da entidade
        descricao: Descrição detalhada
        id_categoria: ID da categoria relacionada
        data_cadastro: Data de criação
        data_atualizacao: Data da última modificação
        categoria: Objeto Categoria relacionado (campo do JOIN)
    """
    id: int
    nome: str
    descricao: str
    id_categoria: int
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    categoria: Optional[Categoria] = None
```

---

## 3. CAMADA REPOSITORY (`repo/<entidade>_repo.py`)

### Imports

- [ ] `from typing import Optional`
- [ ] `from datetime import datetime`
- [ ] `from model.<entidade>_model import <Entidade>`
- [ ] `from sql.<entidade>_sql import *`
- [ ] `from util.db_util import get_connection`

### Função de Conversão Privada

- [ ] Tem função `_row_to_<entidade>(row) -> <Entidade>`
- [ ] Função é **privada** (começa com `_`)
- [ ] Tem docstring descrevendo sua função
- [ ] Mapeia TODOS os campos do model
- [ ] Usa `_converter_data()` para timestamps (se necessário)
- [ ] Trata campos de JOIN opcionais

### Funções Helper (Opcional mas Recomendado)

- [ ] `_converter_data(data_str) -> Optional[datetime]` para timestamps
- [ ] `_row_get(row, key, default)` para acesso seguro

### Funções CRUD

- [ ] **criar_tabela() -> bool**
- [ ] **inserir(entidade: Entidade) -> Optional[int]** (retorna lastrowid)
- [ ] **alterar(entidade: Entidade) -> bool** (retorna rowcount > 0)
- [ ] **excluir(id: int) -> bool** (retorna rowcount > 0)
- [ ] **obter_por_id(id: int) -> Optional[Entidade]**
- [ ] **obter_todos() -> list[Entidade]**
- [ ] **obter_quantidade() -> int** (opcional)

### Padrões de Implementação

- [ ] Todas as funções usam `with get_connection() as conn:`
- [ ] Todas as funções têm **docstrings**
- [ ] Todas as funções têm **type hints**
- [ ] Queries usam **parâmetros** `(valor1, valor2, ...)`

### Exemplo Completo:
```python
from typing import Optional
from datetime import datetime
from model.minha_entidade_model import MinhaEntidade
from sql.minha_entidade_sql import *
from util.db_util import get_connection

def _row_to_minha_entidade(row) -> MinhaEntidade:
    """Converte linha do BD em objeto MinhaEntidade."""
    return MinhaEntidade(
        id=row["id"],
        nome=row["nome"],
        descricao=row["descricao"],
        id_categoria=row["id_categoria"],
        data_cadastro=row["data_cadastro"],
        data_atualizacao=row.get("data_atualizacao"),
        categoria=None
    )

def inserir(entidade: MinhaEntidade) -> Optional[int]:
    """Insere nova entidade no banco."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (entidade.nome, entidade.descricao, entidade.id_categoria))
        return cursor.lastrowid

def obter_por_id(id: int) -> Optional[MinhaEntidade]:
    """Obtém entidade por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        return _row_to_minha_entidade(row) if row else None
```

---

## 4. CAMADA DTO (`dtos/<entidade>_dto.py`)

### Imports

- [ ] `from pydantic import BaseModel, field_validator`
- [ ] `from dtos.validators import ...` (validadores necessários)

### DTOs Separados

- [ ] **Criar<Entidade>DTO** (sem campo id)
- [ ] **Alterar<Entidade>DTO** (com campo id)

### Validação

- [ ] Todos os campos obrigatórios declarados
- [ ] Campos opcionais com default (ex: `descricao: str = ""`)
- [ ] **Validadores** usando `field_validator`
- [ ] Usa **validadores reutilizáveis** de `dtos/validators.py`:
  - `validar_string_obrigatoria()` para strings obrigatórias
  - `validar_comprimento()` para strings opcionais
  - `validar_id_positivo()` para IDs
  - `validar_email()`, `validar_senha_forte()`, etc conforme necessário

### Documentação

- [ ] Docstring em cada DTO descrevendo seu propósito
- [ ] Se for padrão especial, documentar no início do arquivo

### Exemplo Completo:
```python
from pydantic import BaseModel, field_validator
from dtos.validators import validar_string_obrigatoria, validar_comprimento, validar_id_positivo

class CriarMinhaEntidadeDTO(BaseModel):
    """DTO para criação de nova entidade."""
    nome: str
    descricao: str = ""
    id_categoria: int

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=500)
    )
    _validar_id_categoria = field_validator("id_categoria")(
        validar_id_positivo("Categoria")
    )

class AlterarMinhaEntidadeDTO(BaseModel):
    """DTO para alteração de entidade existente."""
    id: int
    nome: str
    descricao: str = ""
    id_categoria: int

    _validar_id = field_validator("id")(validar_id_positivo("ID"))
    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=100)
    )
    _validar_descricao = field_validator("descricao")(
        validar_comprimento(tamanho_maximo=500)
    )
    _validar_id_categoria = field_validator("id_categoria")(
        validar_id_positivo("Categoria")
    )
```

---

## 5. CAMADA ROUTES (`routes/admin_<entidades>_routes.py`)

### Configuração do Router

- [ ] `from fastapi import APIRouter, Request`
- [ ] `router = APIRouter(prefix="/admin/<entidades>")`
- [ ] `templates = criar_templates("templates")`
- [ ] `limiter = RateLimiter(max_tentativas=10, janela_minutos=1)`

### Endpoints Obrigatórios

#### GET /listar
- [ ] Endpoint definido
- [ ] `@requer_autenticacao([Perfil.ADMIN.value])`
- [ ] Chama `obter_todos()` do repo
- [ ] Renderiza template `admin/<entidades>/listar.html`

#### GET /cadastrar
- [ ] Endpoint definido
- [ ] `@requer_autenticacao([Perfil.ADMIN.value])`
- [ ] Carrega dados necessários (ex: categorias para select)
- [ ] Renderiza template `admin/<entidades>/cadastrar.html`

#### POST /cadastrar
- [ ] Endpoint definido
- [ ] `@requer_autenticacao([Perfil.ADMIN.value])`
- [ ] Valida com DTO (`CriarEntidadeDTO`)
- [ ] Trata `FormValidationError`
- [ ] Chama `inserir()` do repo
- [ ] Flash message de sucesso/erro
- [ ] Logging da ação
- [ ] Redirect (PRG pattern) com status_code=303

#### GET /editar/{id}
- [ ] Endpoint definido
- [ ] `@requer_autenticacao([Perfil.ADMIN.value])`
- [ ] Chama `obter_por_id(id)`
- [ ] Verifica se existe (404 se não)
- [ ] Carrega dados necessários
- [ ] Renderiza template `admin/<entidades>/editar.html`

#### POST /editar/{id}
- [ ] Endpoint definido
- [ ] `@requer_autenticacao([Perfil.ADMIN.value])`
- [ ] Valida com DTO (`AlterarEntidadeDTO`)
- [ ] Trata `FormValidationError`
- [ ] Chama `alterar()` do repo
- [ ] Flash message de sucesso/erro
- [ ] Logging da ação
- [ ] Redirect (PRG pattern)

#### POST /{id}/excluir
- [ ] Endpoint definido
- [ ] `@requer_autenticacao([Perfil.ADMIN.value])`
- [ ] **Verifica integridade referencial** antes de excluir
- [ ] Chama `excluir(id)` do repo
- [ ] Flash message de sucesso/erro
- [ ] Logging da ação
- [ ] Redirect para listar

### Padrões de Implementação

- [ ] Todas as rotas autenticadas
- [ ] Rate limiting em rotas de mutação (POST)
- [ ] Flash messages (`informar_sucesso`, `informar_erro`)
- [ ] Logging de ações admin (`logger.info`)
- [ ] Padrão PRG (Post/Redirect/Get)
- [ ] Status code 303 nos redirects POST
- [ ] Try/except para tratamento de erros

### Exemplo Completo:
```python
from fastapi import APIRouter, Request, Form
from util.auth_utils import requer_autenticacao, Perfil
from util.rate_limiter import RateLimiter
from util.mensagens import informar_sucesso, informar_erro
import logging

router = APIRouter(prefix="/admin/minhas_entidades")
templates = criar_templates("templates")
limiter = RateLimiter(max_tentativas=10, janela_minutos=1)
logger = logging.getLogger(__name__)

@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    """Lista todas as entidades."""
    entidades = obter_todos()
    return templates.TemplateResponse(
        "admin/minhas_entidades/listar.html",
        {"request": request, "entidades": entidades, "usuario_logado": usuario_logado}
    )

@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(
    request: Request,
    usuario_logado: Optional[dict] = None,
    nome: str = Form(...),
    descricao: str = Form(""),
    id_categoria: int = Form(...)
):
    """Cadastra nova entidade."""
    try:
        # Validação
        dto = CriarMinhaEntidadeDTO(nome=nome, descricao=descricao, id_categoria=id_categoria)

        # Criação do model
        entidade = MinhaEntidade(id=0, nome=dto.nome, descricao=dto.descricao, id_categoria=dto.id_categoria)

        # Persistência
        entidade_id = inserir(entidade)

        if entidade_id:
            informar_sucesso(request, "Entidade cadastrada com sucesso!")
            logger.info(f"Admin {usuario_logado['nome']} cadastrou entidade ID {entidade_id}")
            return RedirectResponse(url="/admin/minhas_entidades/listar", status_code=303)
        else:
            informar_erro(request, "Erro ao cadastrar entidade.")

    except FormValidationError as e:
        informar_erro(request, str(e))

    return RedirectResponse(url="/admin/minhas_entidades/cadastrar", status_code=303)

@router.post("/{id}/excluir")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_excluir(id: int, request: Request, usuario_logado: Optional[dict] = None):
    """Exclui entidade."""
    # Verificar integridade referencial
    # dependentes = verificar_dependentes(id)
    # if dependentes:
    #     informar_erro(request, "Não é possível excluir: existem registros dependentes.")
    #     return RedirectResponse(...)

    if excluir(id):
        informar_sucesso(request, "Entidade excluída com sucesso!")
        logger.info(f"Admin {usuario_logado['nome']} excluiu entidade ID {id}")
    else:
        informar_erro(request, "Erro ao excluir entidade.")

    return RedirectResponse(url="/admin/minhas_entidades/listar", status_code=303)
```

---

## 6. TEMPLATES (Opcional - se usando interface web)

### Estrutura de Arquivos

- [ ] `templates/admin/<entidades>/listar.html`
- [ ] `templates/admin/<entidades>/cadastrar.html`
- [ ] `templates/admin/<entidades>/editar.html`

### Padrões

- [ ] Extends template base
- [ ] Flash messages exibidas
- [ ] CSRF token nos formulários
- [ ] Confirmação de exclusão (JavaScript)
- [ ] Responsivo

---

## 7. TESTES

### Repositório

- [ ] Teste de `inserir()`
- [ ] Teste de `obter_por_id()`
- [ ] Teste de `obter_todos()`
- [ ] Teste de `alterar()`
- [ ] Teste de `excluir()`

### DTOs

- [ ] Teste de validação com dados válidos
- [ ] Teste de validação com dados inválidos
- [ ] Teste de cada validador

### Rotas

- [ ] Teste de autenticação (401 sem login)
- [ ] Teste de autorização (403 sem perfil)
- [ ] Teste de CRUD completo via HTTP

---

## 8. DOCUMENTAÇÃO

- [ ] Docstrings em todas as funções
- [ ] Type hints em todos os parâmetros e retornos
- [ ] Comentários em lógica complexa
- [ ] Se for padrão não-óbvio, documentar decisão de design

---

## 9. INTEGRIDADE E SEGURANÇA

### Integridade Referencial

- [ ] FKs declaradas no SQL
- [ ] ON DELETE adequado (RESTRICT ou CASCADE)
- [ ] Verificação de dependentes antes de exclusão nas rotas

### Segurança

- [ ] Queries parametrizadas (NUNCA concatenação)
- [ ] Autenticação em todas as rotas
- [ ] Rate limiting em rotas de mutação
- [ ] Validação de entrada via DTOs
- [ ] Logging de ações críticas

---

## 10. REVISÃO FINAL

Antes de considerar completo, verifique:

- [ ] Rodei os testes e todos passaram
- [ ] Testei manualmente cada operação CRUD
- [ ] Verifiquei que as constraints FK funcionam
- [ ] Testei integridade referencial (não permite exclusão se tem dependentes)
- [ ] Código segue convenções de nomenclatura
- [ ] Sem código duplicado (usei validadores reutilizáveis)
- [ ] Flash messages funcionando
- [ ] Logging funcionando
- [ ] Templates renderizando corretamente
- [ ] Documentação completa

---

## REFERÊNCIAS

- **Exemplo completo:** Categoria (sql/categoria_sql.py, model/categoria_model.py, etc.)
- **Padrões arquiteturais:** `docs/PADROES_ARQUITETURAIS.md`
- **Parecer técnico:** `docs/PARECER.md`
- **Mudanças implementadas:** `docs/MUDANCAS_IMPLEMENTADAS.md`

---

**Data de criação:** 2025-10-28
**Última atualização:** 2025-10-28
