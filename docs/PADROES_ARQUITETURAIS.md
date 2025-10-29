# Padrões Arquiteturais - AgendaFit

**Data:** 2025-10-28
**Versão:** 1.0
**Propósito:** Documentação dos padrões de design usados na aplicação

---

## SUMÁRIO

1. [Arquitetura em Camadas](#1-arquitetura-em-camadas)
2. [Padrão CRUD Completo](#2-padrão-crud-completo)
3. [Padrão Facade](#3-padrão-facade)
4. [Padrão Child Entity](#4-padrão-child-entity)
5. [Padrão Subsistema Coeso](#5-padrão-subsistema-coeso)
6. [Padrão Key-Value Store](#6-padrão-key-value-store)
7. [Validação e Segurança](#7-validação-e-segurança)
8. [Quando Usar Cada Padrão](#8-quando-usar-cada-padrão)

---

## 1. ARQUITETURA EM CAMADAS

A aplicação AgendaFit segue uma **arquitetura em 5 camadas** bem definida:

```
┌──────────────────────────────────────┐
│   ROUTES (Camada de Apresentação)   │  ← FastAPI routes, templates
├──────────────────────────────────────┤
│   DTOs (Camada de Validação)        │  ← Pydantic models, validators
├──────────────────────────────────────┤
│   REPOSITORIES (Acesso a Dados)     │  ← Query execution, mapping
├──────────────────────────────────────┤
│   MODELS (Camada de Domínio)        │  ← Business entities
├──────────────────────────────────────┤
│   SQL (Camada de Persistência)      │  ← Query definitions
└──────────────────────────────────────┘
```

### Responsabilidades de Cada Camada

#### SQL Layer (`sql/`)
- Define estrutura das tabelas (`CRIAR_TABELA`)
- Define queries parametrizadas (INSERT, UPDATE, SELECT, DELETE)
- **NUNCA** contém lógica de negócio
- **NUNCA** concatena strings SQL (usa `?` placeholders)

**Exemplo:**
```python
# sql/categoria_sql.py
CRIAR_TABELA = """CREATE TABLE IF NOT EXISTS categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
)"""

INSERIR = "INSERT INTO categoria (nome, descricao) VALUES (?, ?)"
```

#### Models Layer (`model/`)
- Define entidades de domínio usando `@dataclass`
- Type hints obrigatórios em todos os campos
- Campos opcionais com `Optional[T]`
- Docstrings descrevendo a entidade

**Exemplo:**
```python
# model/categoria_model.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Categoria:
    """Model de categoria de atividades do AgendaFit."""
    id: int
    nome: str
    descricao: Optional[str] = None
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
```

#### Repository Layer (`repo/`)
- Executa queries e mapeia resultados para models
- Função privada `_row_to_<entidade>()` para conversão
- Usa context manager `with get_connection()`
- Retorna tipos adequados:
  - `Optional[T]` para registro único
  - `list[T]` para coleções
  - `bool` para sucesso/falha
  - `int` para IDs/contagens

**Exemplo:**
```python
# repo/categoria_repo.py
def _row_to_categoria(row) -> Categoria:
    """Converte linha do BD em objeto Categoria."""
    return Categoria(...)

def obter_por_id(id: int) -> Optional[Categoria]:
    """Obtém categoria por ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        return _row_to_categoria(row) if row else None
```

#### DTOs Layer (`dtos/`)
- Valida dados de entrada usando Pydantic `BaseModel`
- DTOs separados para Criar e Alterar
- Usa validadores reutilizáveis de `dtos/validators.py`
- Mensagens de erro claras e amigáveis

**Exemplo:**
```python
# dtos/categoria_dto.py
from pydantic import BaseModel, field_validator
from dtos.validators import validar_string_obrigatoria

class CriarCategoriaDTO(BaseModel):
    nome: str
    descricao: str = ""

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=50)
    )
```

#### Routes Layer (`routes/`)
- Define endpoints FastAPI
- Usa `APIRouter` com prefix
- Autenticação via `@requer_autenticacao`
- Rate limiting
- Flash messages para feedback
- Padrão PRG (Post/Redirect/Get)

**Exemplo:**
```python
# routes/admin_categorias_routes.py
from fastapi import APIRouter
from util.auth_utils import requer_autenticacao, Perfil

router = APIRouter(prefix="/admin/categorias")

@router.get("/listar")
@requer_autenticacao([Perfil.ADMIN.value])
async def get_listar(request: Request, usuario_logado: Optional[dict] = None):
    categorias = obter_todos()
    return templates.TemplateResponse(...)
```

---

## 2. PADRÃO CRUD COMPLETO

**Quando usar:** Entidades principais independentes que precisam de operações completas de Create, Read, Update, Delete.

### Estrutura de Arquivos

```
sql/entidade_sql.py          # Queries SQL
model/entidade_model.py      # Modelo de dados
repo/entidade_repo.py        # Repositório de acesso
dtos/entidade_dto.py         # DTOs de validação
routes/admin_entidade_routes.py  # Rotas administrativas
```

### Exemplos na Aplicação

- ✅ **Categoria** - Categorias de atividades
- ✅ **Atividade** - Atividades físicas/esportivas
- ✅ **Turma** - Classes de atividades
- ✅ **Matricula** - Matrículas de alunos
- ✅ **Usuario** - Usuários do sistema
- ✅ **Tarefa** - Tarefas/to-dos
- ✅ **Chamado** - Tickets de suporte

### Características

1. **5 camadas completas**
2. **CRUD completo:** CREATE, READ, UPDATE, DELETE
3. **Rotas próprias:** `/admin/entidades/`
4. **Validação completa:** DTOs para criar e alterar
5. **Integridade referencial:** Verifica dependências antes de deletar

### Checklist de Conformidade

Ao criar um novo CRUD completo, garanta:

- [ ] SQL com `id` simples (não prefixado)
- [ ] Campos `data_cadastro` e `data_atualizacao`
- [ ] Foreign Keys com `ON DELETE RESTRICT/CASCADE`
- [ ] Model com `@dataclass` e type hints
- [ ] Repo com `_row_to_<entidade>()` privado
- [ ] DTOs separados: `Criar<Entidade>DTO` e `Alterar<Entidade>DTO`
- [ ] Routes com autenticação e rate limiting
- [ ] Verificação de integridade antes de exclusão

---

## 3. PADRÃO FACADE

**Quando usar:** Tipos especializados de uma entidade base que não justificam tabela separada.

### Conceito

Um **Facade** reutiliza completamente a infraestrutura de uma entidade base, apenas especializando o comportamento através de filtros e validações.

### Exemplo: Aluno (Facade sobre Usuario)

```
Estrutura:
❌ sql/aluno_sql.py          - NÃO EXISTE
❌ model/aluno_model.py      - NÃO EXISTE
❌ repo/aluno_repo.py        - NÃO EXISTE
✅ dtos/aluno_dto.py         - EXISTE (especializado)
✅ routes/admin_alunos_routes.py - EXISTE (filtra por perfil)
```

### Implementação

**DTO Especializado:**
```python
# dtos/aluno_dto.py
class CriarAlunoDTO(BaseModel):
    """DTO para criação de aluno."""
    nome: str
    email: str
    senha: str
    perfil: str = Perfil.ALUNO.value  # ✅ Hardcoded!
```

**Rotas Especializadas:**
```python
# routes/admin_alunos_routes.py
@router.get("/listar")
async def get_listar(...):
    # ✅ Usa repo de Usuario, filtrando por perfil
    alunos = usuario_repo.obter_todos_por_perfil(Perfil.ALUNO.value)
    ...
```

### Quando Usar

✅ **Use Facade quando:**
- Tipos especializados de uma entidade base (ex: Admin, Professor, Aluno sobre Usuario)
- Comportamento é 90% igual, só muda filtros/validações
- Não há campos exclusivos do tipo especializado
- Quer evitar duplicação de código

❌ **NÃO use Facade quando:**
- A entidade especializada tem campos próprios
- A lógica de negócio é significativamente diferente
- Há relacionamentos exclusivos da especialização

### Vantagens

1. ✅ **Zero duplicação** de SQL/Model/Repo
2. ✅ **Manutenção centralizada** em Usuario
3. ✅ **Menos código** para manter
4. ✅ **Consistência** garantida

---

## 4. PADRÃO CHILD ENTITY

**Quando usar:** Entidades que SEMPRE dependem de uma entidade pai e não fazem sentido isoladamente.

### Conceito

Uma **Child Entity** (entidade filha) é aquela que:
1. Sempre tem FK obrigatória para o pai
2. É excluída quando o pai é excluído (CASCADE)
3. Não tem rotas próprias
4. É acessada sempre através do pai

### Exemplo: ChamadoInteracao (child de Chamado)

```
Estrutura:
✅ sql/chamado_interacao_sql.py    - SQL com FK ON DELETE CASCADE
✅ model/chamado_interacao_model.py - Model normal
✅ repo/chamado_interacao_repo.py   - Repo com queries filtradas por chamado_id
✅ dtos/chamado_interacao_dto.py    - DTOs
❌ routes/chamado_interacao_routes.py - NÃO EXISTE!
```

### Implementação

**SQL com CASCADE:**
```python
# sql/chamado_interacao_sql.py
CRIAR_TABELA = """CREATE TABLE IF NOT EXISTS chamado_interacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chamado_id INTEGER NOT NULL,  # ✅ FK obrigatória
    mensagem TEXT NOT NULL,
    FOREIGN KEY (chamado_id) REFERENCES chamado(id) ON DELETE CASCADE  # ✅ CASCADE!
)"""
```

**Queries Filtradas:**
```python
# Sempre filtrado pelo pai
OBTER_POR_CHAMADO = "SELECT * FROM chamado_interacao WHERE chamado_id = ?"
```

**Rotas do Pai:**
```python
# routes/admin_chamados_routes.py
@router.post("/{id}/adicionar_mensagem")  # ✅ Rota no pai!
async def post_adicionar_mensagem(id: int, mensagem: str):
    interacao = ChamadoInteracao(chamado_id=id, mensagem=mensagem)
    chamado_interacao_repo.inserir(interacao)
    ...
```

### Características

1. **FK obrigatória** para o pai
2. **ON DELETE CASCADE** no SQL
3. **Sem rotas próprias** - acesso via pai
4. **Operações limitadas** - geralmente só INSERT e SELECT
5. **Queries sempre filtradas** por pai_id

### Quando Usar

✅ **Use Child Entity quando:**
- A entidade não existe sem o pai
- A exclusão do pai deve excluir os filhos
- Acesso sempre via contexto do pai
- Exemplos: Itens de pedido, Mensagens de ticket, Respostas de post

❌ **NÃO use quando:**
- A entidade pode existir sem o pai
- Há acesso independente aos registros
- Múltiplos pais ou relacionamento many-to-many

---

## 5. PADRÃO SUBSISTEMA COESO

**Quando usar:** Conjunto de 2-4 tabelas que formam uma funcionalidade completa e são sempre usadas juntas.

### Conceito

Um **Subsistema Coeso** agrupa tabelas interdependentes que:
1. Formam uma funcionalidade completa
2. Raramente são acessadas separadamente
3. Têm forte coesão entre si

### Exemplo: Sistema de Chat (3 tabelas)

```
Subsistema Chat:
  - chat_sala (salas de conversa)
  - chat_participante (users em salas - many-to-many)
  - chat_mensagem (mensagens nas salas)

Estrutura:
✅ sql/chat_sala_sql.py
✅ sql/chat_participante_sql.py
✅ sql/chat_mensagem_sql.py
✅ model/chat_sala_model.py
✅ model/chat_participante_model.py
✅ model/chat_mensagem_model.py
✅ repo/chat_sala_repo.py
✅ repo/chat_participante_repo.py
✅ repo/chat_mensagem_repo.py
✅ dtos/chat_dto.py              # ✅ UM ÚNICO arquivo de DTOs!
✅ routes/chat_routes.py          # ✅ UMA ÚNICA rota!
```

### Características

1. **DTOs consolidados** em um arquivo
2. **Rotas consolidadas** em um arquivo
3. **Operações transversais** entre as 3 tabelas
4. **Forte integridade referencial** (CASCADE)

### Implementação

**DTOs Consolidados:**
```python
# dtos/chat_dto.py
class CriarSalaDTO(BaseModel):
    """DTO para criar sala."""
    outro_usuario_id: int

class EnviarMensagemDTO(BaseModel):
    """DTO para enviar mensagem."""
    sala_id: str
    mensagem: str

# ✅ Todos os DTOs do subsistema em um arquivo!
```

**Rotas Consolidadas:**
```python
# routes/chat_routes.py
router = APIRouter(prefix="/chat")

@router.post("/criar_sala")
async def criar_sala(...):
    # Usa chat_sala_repo E chat_participante_repo
    ...

@router.post("/{sala_id}/enviar")
async def enviar_mensagem(...):
    # Usa chat_mensagem_repo
    ...

# ✅ Todas as operações de chat em uma rota!
```

### Quando Usar

✅ **Use Subsistema Coeso quando:**
- 2-4 tabelas sempre usadas juntas
- Funcionalidade completa e fechada
- Raramente há acesso isolado a uma tabela
- Exemplos: Chat, Carrinho de compras, Sistema de pedidos, Fórum

❌ **NÃO use quando:**
- Tabelas são acessadas independentemente
- Baixa coesão entre as tabelas
- Cada tabela tem seu próprio ciclo de vida

### Vantagens

1. ✅ **Alta coesão** - tudo relacionado em um lugar
2. ✅ **Menos fragmentação** - não espalha 10+ arquivos
3. ✅ **Mais fácil de entender** - subsistema autocontido
4. ✅ **Operações transversais** facilitadas

---

## 6. PADRÃO KEY-VALUE STORE

**Quando usar:** Configurações dinâmicas do sistema que não justificam tabelas separadas.

### Exemplo: Configuracao

```
Estrutura:
✅ sql/configuracao_sql.py
✅ model/configuracao_model.py
✅ repo/configuracao_repo.py
✅ dtos/configuracao_dto.py
✅ routes/admin_configuracoes_routes.py
```

### Implementação

**SQL:**
```python
CRIAR_TABELA = """CREATE TABLE IF NOT EXISTS configuracao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave TEXT UNIQUE NOT NULL,    # ✅ Chave única!
    valor TEXT NOT NULL,
    descricao TEXT
)"""

# ✅ Query específica por chave
OBTER_POR_CHAVE = "SELECT * FROM configuracao WHERE chave = ?"
```

### Configurações Típicas

```python
# Exemplos de chaves:
nome_sistema = "AgendaFit"
email_contato = "contato@agendafit.com"
max_tentativas_login = "5"
tempo_sessao_minutos = "30"
```

### Quando Usar

✅ **Use Key-Value quando:**
- Configurações dinâmicas do sistema
- Não justifica criar tabela para cada config
- Valores são strings ou simples
- Cache é importante

❌ **NÃO use quando:**
- Configurações complexas (use tabela própria)
- Relacionamentos com outras entidades
- Validações específicas por tipo

---

## 7. VALIDAÇÃO E SEGURANÇA

### Validadores Reutilizáveis

A aplicação possui validadores centralizados em `dtos/validators.py`:

```python
# Strings
validar_string_obrigatoria(nome, tamanho_minimo, tamanho_maximo)
validar_comprimento(tamanho_maximo)
validar_nome_pessoa(nome)

# Formatos
validar_email(nome)
validar_senha_forte(nome)

# Números
validar_id_positivo(nome)

# Enums
validar_tipo(nome, valores_validos)
```

### Uso nos DTOs

```python
class CriarCategoriaDTO(BaseModel):
    nome: str

    _validar_nome = field_validator("nome")(
        validar_string_obrigatoria("Nome", tamanho_minimo=3, tamanho_maximo=50)
    )
```

### Segurança

1. **SQL Injection:** Queries parametrizadas (`?`) em 100% dos casos
2. **Autenticação:** `@requer_autenticacao` em todas as rotas admin
3. **Autorização:** Role-based via `Perfil` enum
4. **Rate Limiting:** `RateLimiter` em rotas de mutação
5. **CSRF:** Tokens em formulários
6. **Passwords:** Hash automático no repositório

---

## 8. QUANDO USAR CADA PADRÃO

### Árvore de Decisão

```
Nova funcionalidade?
│
├─ É tipo especializado de entidade existente?
│  └─ SIM → Use FACADE (ex: Aluno sobre Usuario)
│
├─ Sempre depende de outra entidade (não existe sem ela)?
│  └─ SIM → Use CHILD ENTITY (ex: ChamadoInteracao)
│
├─ São 2-4 tabelas sempre usadas juntas?
│  └─ SIM → Use SUBSISTEMA COESO (ex: Chat)
│
├─ É configuração dinâmica chave-valor?
│  └─ SIM → Use KEY-VALUE STORE (ex: Configuracao)
│
└─ Entidade principal independente?
   └─ SIM → Use CRUD COMPLETO (padrão)
```

### Tabela Comparativa

| Padrão | SQL | Model | Repo | DTO | Routes | Quando Usar |
|--------|-----|-------|------|-----|--------|-------------|
| **CRUD Completo** | ✅ | ✅ | ✅ | ✅ | ✅ | Entidade principal independente |
| **Facade** | ❌ | ❌ | ❌ | ✅ | ✅ | Tipo especializado de base |
| **Child Entity** | ✅ | ✅ | ✅ | ✅ | ❌ | Sempre depende do pai |
| **Subsistema** | ✅ | ✅ | ✅ | ✅* | ✅* | 2-4 tabelas coesas |
| **Key-Value** | ✅ | ✅ | ✅ | ✅ | ✅ | Config dinâmica |

*Consolidado em 1 arquivo

---

## CONCLUSÃO

A aplicação AgendaFit demonstra uso consistente de padrões arquiteturais bem definidos. Ao desenvolver novas funcionalidades:

1. ✅ **Identifique o padrão** adequado usando a árvore de decisão
2. ✅ **Siga a estrutura** do padrão escolhido
3. ✅ **Use o checklist** de conformidade
4. ✅ **Documente** decisões não-óbvias
5. ✅ **Mantenha consistência** com o código existente

**Referências:**
- Padrão CRUD: `sql/categoria_sql.py`, `model/categoria_model.py`, etc.
- Padrão Facade: `dtos/aluno_dto.py`
- Padrão Child: `model/chamado_interacao_model.py`
- Padrão Subsistema: `dtos/chat_dto.py`

---

**Documento criado em:** 2025-10-28
**Próxima revisão:** Quando novos padrões forem identificados
