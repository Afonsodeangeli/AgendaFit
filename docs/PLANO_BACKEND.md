# PLANO DE IMPLEMENTAÇÃO DO BACKEND - AGENDAFIT

**Versão:** 1.0
**Data:** 21/10/2025
**Projeto:** AgendaFit - Gestão Inteligente de Treinos
**Escopo:** Backend (Apenas Python/FastAPI - SEM Templates)

---

## ÍNDICE

1. [Introdução](#1-introdução)
2. [Análise do Estado Atual](#2-análise-do-estado-atual)
3. [Gap Analysis - O Que Falta Implementar](#3-gap-analysis---o-que-falta-implementar)
4. [Guia de Implementação - Sistema de Perfis](#4-guia-de-implementação---sistema-de-perfis)
5. [Guia de Implementação - Categorias e Atividades](#5-guia-de-implementação---categorias-e-atividades)
6. [Guia de Implementação - Turmas e Matrículas](#6-guia-de-implementação---turmas-e-matrículas)
7. [Guia de Implementação - Pagamentos e Endereços](#7-guia-de-implementação---pagamentos-e-endereços)
8. [Guia de Implementação - Funcionalidades Adicionais](#8-guia-de-implementação---funcionalidades-adicionais)
9. [Considerações Finais](#9-considerações-finais)

---

## 1. INTRODUÇÃO

### 1.1 Objetivo do Documento

Este documento apresenta uma análise detalhada do projeto **AgendaFit** conforme especificado no PDF de documentação, comparando com o estado atual do código implementado. O objetivo é identificar **todas as funcionalidades de backend** que precisam ser implementadas para transformar o projeto atual em um sistema completo de gestão de aulas de academia.

### 1.2 Escopo

**INCLUI:**
- Models (classes de domínio)
- SQL (queries e schemas)
- Repositories (camada de dados)
- DTOs (Data Transfer Objects)
- Routes (endpoints da API)
- Validações e regras de negócio
- Integrações necessárias

**NÃO INCLUI:**
- Templates HTML/Jinja2
- Frontend/JavaScript
- Estilização CSS
- Documentação de usuário

### 1.3 Visão Geral do AgendaFit (Conforme PDF)

O **AgendaFit** é uma plataforma web para gerenciamento de aulas em academias e centros de treinamento. O sistema possui **três perfis de usuário**:

#### **1.3.1 Perfil Aluno**
- Visualizar agenda de atividades disponíveis
- Matricular-se em atividades
- Cancelar matrícula em atividades
- Visualizar histórico de atividades
- Solicitar avaliação física
- Visualizar relatórios de avaliações físicas
- Receber notificações sobre aulas

#### **1.3.2 Perfil Professor (Instrutor)**
- Criar turmas
- Cadastrar atividades
- Alterar/Excluir atividades
- Visualizar alunos matriculados
- Registrar presença dos alunos
- Enviar avaliações físicas/relatórios aos alunos
- Excluir turmas

#### **1.3.3 Perfil Administrador**
- Gerenciar professores (CRUD completo)
- Gerenciar alunos (CRUD completo)
- Gerenciar turmas (CRUD completo)
- Gerenciar matrículas (realizar, alterar, cancelar)
- Gerenciar atividades (CRUD completo)
- Ver estatísticas e relatórios do sistema

### 1.4 Modelo de Dados (Conforme PDF)

O diagrama de classes do PDF apresenta as seguintes entidades principais:

1. **Usuario** - Dados de autenticação e perfil
2. **Endereco** - Endereço do usuário (FK para Usuario)
3. **Categoria** - Categoria de atividades (ex: Yoga, Musculação)
4. **Atividade** - Atividade oferecida (FK para Categoria)
5. **Turma** - Turma específica de uma atividade (FK para Atividade e Professor)
6. **Matricula** - Matrícula de aluno em turma (FK para Turma e Aluno)
7. **Pagamento** - Pagamento de matrícula (FK para Matricula e Aluno)

---

## 2. ANÁLISE DO ESTADO ATUAL

### 2.1 Estrutura do Projeto Existente

O projeto atual possui a seguinte estrutura:

```
AgendaFit/
├── model/                    # Models de domínio
│   ├── usuario_model.py      ✅ EXISTE
│   ├── endereco_model.py     ⚠️  EXISTE (incompleto)
│   ├── categoria_model.py    ⚠️  EXISTE (incompleto)
│   ├── Atividade_model.py    ⚠️  EXISTE (incompleto)
│   ├── Turma_model.py        ⚠️  EXISTE (incompleto)
│   ├── matricula_model.py    ⚠️  EXISTE (incompleto)
│   ├── Pagamento_model.py    ⚠️  EXISTE (incompleto)
│   ├── tarefa_model.py       ❌ SISTEMA ANTIGO (remover/adaptar)
│   └── configuracao_model.py ✅ EXISTE
│
├── sql/                      # Scripts SQL
│   ├── usuario_sql.py        ✅ EXISTE
│   ├── tarefa_sql.py         ❌ SISTEMA ANTIGO (remover/adaptar)
│   └── configuracao_sql.py   ✅ EXISTE
│   └── (outros)              ❌ NÃO EXISTEM
│
├── repo/                     # Repositories
│   ├── usuario_repo.py       ✅ EXISTE
│   ├── tarefa_repo.py        ❌ SISTEMA ANTIGO (remover/adaptar)
│   └── configuracao_repo.py  ✅ EXISTE
│   └── (outros)              ❌ NÃO EXISTEM
│
├── dtos/                     # Data Transfer Objects
│   ├── auth_dto.py           ✅ EXISTE
│   ├── usuario_dto.py        ✅ EXISTE
│   ├── perfil_dto.py         ✅ EXISTE
│   ├── tarefa_dto.py         ❌ SISTEMA ANTIGO (remover/adaptar)
│   └── validators.py         ✅ EXISTE
│   └── (outros)              ❌ NÃO EXISTEM
│
├── routes/                   # Endpoints da API
│   ├── auth_routes.py        ✅ EXISTE
│   ├── usuario_routes.py     ✅ EXISTE
│   ├── perfil_routes.py      ✅ EXISTE
│   ├── tarefas_routes.py     ❌ SISTEMA ANTIGO (remover/adaptar)
│   ├── admin_usuarios_routes.py      ✅ EXISTE
│   ├── admin_configuracoes_routes.py ✅ EXISTE
│   ├── admin_backups_routes.py       ✅ EXISTE
│   ├── public_routes.py      ✅ EXISTE
│   └── examples_routes.py    ✅ EXISTE
│   └── (outros)              ❌ NÃO EXISTEM
│
└── util/                     # Utilitários
    ├── perfis.py             ⚠️  EXISTE (precisa atualização)
    ├── auth_decorator.py     ✅ EXISTE
    ├── security.py           ✅ EXISTE
    ├── email_service.py      ✅ EXISTE
    ├── db_util.py            ✅ EXISTE
    └── (outros)              ✅ DIVERSOS UTILS EXISTENTES
```

### 2.2 Sistema Atual vs Sistema AgendaFit

#### **INCOMPATIBILIDADE CRÍTICA:**
O projeto atual implementa um sistema de **"Tarefas"** (ToDo list), mas o AgendaFit precisa de um sistema de **"Atividades/Aulas"**. São conceitos diferentes:

- **Sistema Atual (Tarefas):** Lista de afazeres pessoais
- **Sistema Necessário (AgendaFit):** Gestão de aulas de academia

**Ação necessária:** Remover/adaptar todo o código relacionado a "tarefas" e implementar o sistema de atividades/turmas/matrículas do AgendaFit.

### 2.3 Perfis de Usuário

#### **Atual:**
```python
# util/perfis.py
class Perfil(str, Enum):
    ADMIN = "Administrador"
    CLIENTE = "Cliente"
    VENDEDOR = "Vendedor"
```

#### **Necessário (AgendaFit):**
```python
class Perfil(str, Enum):
    ADMIN = "Administrador"
    ALUNO = "Aluno"
    PROFESSOR = "Professor"
```

**Ação necessária:** Atualizar o enum de perfis para refletir os perfis do AgendaFit.

### 2.4 Models Existentes - Análise Detalhada

#### **2.4.1 usuario_model.py** ✅ COMPLETO
```python
@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha: str
    perfil: str
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None
```
**Status:** Adequado para o AgendaFit. Suporta os perfis necessários.

#### **2.4.2 endereco_model.py** ⚠️ INCOMPLETO
```python
@dataclass
class Endereco:
    id_endereco: int
    id_usuario: int
    titulo: str
    logradouro: str
    numero: int
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: int
    usuario: Optional[Usuario]
```
**Status:** Model existe, mas **faltam**: SQL, Repository, DTO, Routes

#### **2.4.3 categoria_model.py** ⚠️ INCOMPLETO
```python
@dataclass
class Categoria:
    id_categoria: int
    nome: str
    descricao: str
```
**Status:** Model existe, mas **faltam**: SQL, Repository, DTO, Routes

#### **2.4.4 Atividade_model.py** ⚠️ INCOMPLETO
```python
@dataclass
class Atividade:
    id_atividade: int
    id_categoria: int
    nome: str
    descricao: str
    data_cadastro: datetime
    categoria: Optional[Categoria]
```
**Status:** Model existe, mas **faltam**: SQL, Repository, DTO, Routes

#### **2.4.5 Turma_model.py** ⚠️ INCOMPLETO
```python
@dataclass
class Turma:
    id_atividade: int
    id_professor: int
    data_cadastro: datetime
    atividade: Optional[Atividade]
    professor: Optional[Usuario]
```
**Status:** Model existe, mas **falta PK (id_turma)** e faltam: SQL, Repository, DTO, Routes

**PROBLEMA CRÍTICO:** Turma não tem chave primária (id_turma)!

#### **2.4.6 matricula_model.py** ⚠️ INCOMPLETO
```python
@dataclass
class Matricula:
    id_matricula: int
    id_turma: int
    id_aluno: int
    data_matricula: datetime
    valor_mensalidade: float
    data_vencimento: datetime
    turma: Optional[Turma]
    aluno: Optional[Usuario]
```
**Status:** Model existe, mas **faltam**: SQL, Repository, DTO, Routes

#### **2.4.7 Pagamento_model.py** ⚠️ INCOMPLETO
```python
@dataclass
class Pagamento:
    id_matricula: int
    id_aluno: int
    data_pagamento: datetime
    valor_pago: float
    matricula: Optional[Matricula]
    aluno: Optional[Matricula]  # ⚠️ ERRO: deveria ser Usuario
```
**Status:** Model existe com **ERRO** (aluno deveria ser Usuario, não Matricula), e **falta PK (id_pagamento)**. Faltam: SQL, Repository, DTO, Routes

---

## 3. GAP ANALYSIS - O QUE FALTA IMPLEMENTAR

Esta seção detalha **todos os componentes** que precisam ser criados ou corrigidos para completar o backend do AgendaFit.

### 3.1 Componentes a CORRIGIR

#### **3.1.1 util/perfis.py** ⚠️ ATUALIZAÇÃO OBRIGATÓRIA
**Problema:** Perfis atuais (ADMIN, CLIENTE, VENDEDOR) não correspondem aos perfis do AgendaFit

**Solução:** Alterar para:
```python
class Perfil(str, Enum):
    ADMIN = "Administrador"
    ALUNO = "Aluno"
    PROFESSOR = "Professor"
```

**Impacto:** Requer atualização em:
- Banco de dados (migração de perfis existentes)
- Seeds de dados iniciais
- Validações e decoradores de autorização

#### **3.1.2 model/Turma_model.py** ⚠️ CORREÇÃO CRÍTICA
**Problema:** Falta chave primária (id_turma)

**Solução:** Adicionar campo id_turma:
```python
@dataclass
class Turma:
    id_turma: int  # ← ADICIONAR ESTE CAMPO
    id_atividade: int
    id_professor: int
    data_cadastro: datetime
    atividade: Optional[Atividade]
    professor: Optional[Usuario]
```

#### **3.1.3 model/Pagamento_model.py** ⚠️ CORREÇÃO CRÍTICA
**Problema 1:** Falta chave primária (id_pagamento)
**Problema 2:** Campo `aluno` com tipo errado (Matricula em vez de Usuario)

**Solução:** Corrigir model:
```python
@dataclass
class Pagamento:
    id_pagamento: int  # ← ADICIONAR ESTE CAMPO
    id_matricula: int
    id_aluno: int
    data_pagamento: datetime
    valor_pago: float
    matricula: Optional[Matricula]
    aluno: Optional[Usuario]  # ← CORRIGIR TIPO
```

#### **3.1.4 Sistema de Tarefas** ❌ REMOVER OU ADAPTAR
**Arquivos a remover/adaptar:**
- `model/tarefa_model.py`
- `sql/tarefa_sql.py`
- `repo/tarefa_repo.py`
- `dtos/tarefa_dto.py`
- `routes/tarefas_routes.py`
- Referências em `main.py`
- Tabela `tarefa` no banco de dados

**Decisão:** Pode-se manter como funcionalidade adicional OU remover completamente. Se manter, não interferirá no AgendaFit.

### 3.2 Componentes a CRIAR - Categorias

#### **3.2.1 sql/categoria_sql.py** ❌ NÃO EXISTE
**Precisa criar:** Queries SQL para categorias

**Conteúdo necessário:**
- `CRIAR_TABELA` - CREATE TABLE categoria
- `INSERIR` - INSERT INTO categoria
- `ALTERAR` - UPDATE categoria
- `EXCLUIR` - DELETE FROM categoria
- `OBTER_POR_ID` - SELECT com filtro por id
- `OBTER_TODAS` - SELECT de todas categorias
- `OBTER_QUANTIDADE` - COUNT de categorias

#### **3.2.2 repo/categoria_repo.py** ❌ NÃO EXISTE
**Precisa criar:** Repository de categorias

**Funções necessárias:**
- `criar_tabela()` - Cria tabela no BD
- `inserir(categoria: Categoria)` - Insere categoria
- `alterar(categoria: Categoria)` - Atualiza categoria
- `excluir(id: int)` - Remove categoria
- `obter_por_id(id: int)` - Busca por ID
- `obter_todas()` - Lista todas
- `obter_quantidade()` - Conta total

#### **3.2.3 dtos/categoria_dto.py** ❌ NÃO EXISTE
**Precisa criar:** DTOs de validação para categorias

**DTOs necessários:**
- `CategoriaCreateDTO` - Validação de criação
- `CategoriaUpdateDTO` - Validação de atualização
- Validações: nome (min 3, max 100), descrição (max 500)

#### **3.2.4 routes/admin_categorias_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints administrativos de categorias

**Endpoints necessários:**
- `GET /admin/categorias` - Listar categorias
- `GET /admin/categorias/nova` - Formulário de nova categoria
- `POST /admin/categorias/nova` - Criar categoria
- `GET /admin/categorias/{id}/editar` - Formulário de edição
- `POST /admin/categorias/{id}/editar` - Atualizar categoria
- `POST /admin/categorias/{id}/excluir` - Excluir categoria

### 3.3 Componentes a CRIAR - Atividades

#### **3.3.1 sql/atividade_sql.py** ❌ NÃO EXISTE
**Precisa criar:** Queries SQL para atividades

**Conteúdo necessário:**
- `CRIAR_TABELA` - CREATE TABLE atividade com FK para categoria
- `INSERIR` - INSERT INTO atividade
- `ALTERAR` - UPDATE atividade
- `EXCLUIR` - DELETE FROM atividade
- `OBTER_POR_ID` - SELECT com JOIN em categoria
- `OBTER_TODAS` - SELECT com JOIN em categoria
- `OBTER_POR_CATEGORIA` - SELECT filtrando por categoria
- `OBTER_QUANTIDADE` - COUNT de atividades

#### **3.3.2 repo/atividade_repo.py** ❌ NÃO EXISTE
**Precisa criar:** Repository de atividades

**Funções necessárias:**
- `criar_tabela()` - Cria tabela no BD
- `inserir(atividade: Atividade)` - Insere atividade
- `alterar(atividade: Atividade)` - Atualiza atividade
- `excluir(id: int)` - Remove atividade
- `obter_por_id(id: int)` - Busca por ID com categoria
- `obter_todas()` - Lista todas com categorias
- `obter_por_categoria(id_categoria: int)` - Filtra por categoria
- `obter_quantidade()` - Conta total

#### **3.3.3 dtos/atividade_dto.py** ❌ NÃO EXISTE
**Precisa criar:** DTOs de validação para atividades

**DTOs necessários:**
- `AtividadeCreateDTO` - Validação de criação
- `AtividadeUpdateDTO` - Validação de atualização
- Validações: nome (min 3, max 100), descrição (max 1000), id_categoria obrigatório

#### **3.3.4 routes/admin_atividades_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints administrativos de atividades

**Endpoints necessários:**
- `GET /admin/atividades` - Listar atividades
- `GET /admin/atividades/nova` - Formulário de nova atividade
- `POST /admin/atividades/nova` - Criar atividade
- `GET /admin/atividades/{id}/editar` - Formulário de edição
- `POST /admin/atividades/{id}/editar` - Atualizar atividade
- `POST /admin/atividades/{id}/excluir` - Excluir atividade

#### **3.3.5 routes/professor_atividades_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints do professor para atividades

**Endpoints necessários:**
- `GET /professor/atividades` - Listar atividades do professor
- `GET /professor/atividades/nova` - Formulário de nova atividade
- `POST /professor/atividades/nova` - Criar atividade
- `GET /professor/atividades/{id}/editar` - Formulário de edição
- `POST /professor/atividades/{id}/editar` - Atualizar atividade
- `POST /professor/atividades/{id}/excluir` - Excluir atividade

#### **3.3.6 routes/aluno_atividades_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints do aluno para visualizar atividades

**Endpoints necessários:**
- `GET /aluno/atividades` - Listar atividades disponíveis
- `GET /aluno/atividades/{id}` - Ver detalhes de uma atividade

### 3.4 Componentes a CRIAR - Turmas

#### **3.4.1 sql/turma_sql.py** ❌ NÃO EXISTE
**Precisa criar:** Queries SQL para turmas

**Conteúdo necessário:**
- `CRIAR_TABELA` - CREATE TABLE turma com FKs
- `INSERIR` - INSERT INTO turma
- `ALTERAR` - UPDATE turma
- `EXCLUIR` - DELETE FROM turma
- `OBTER_POR_ID` - SELECT com JOINs em atividade e professor
- `OBTER_TODAS` - SELECT com JOINs
- `OBTER_POR_PROFESSOR` - Turmas de um professor específico
- `OBTER_POR_ATIVIDADE` - Turmas de uma atividade específica
- `OBTER_QUANTIDADE` - COUNT de turmas

#### **3.4.2 repo/turma_repo.py** ❌ NÃO EXISTE
**Precisa criar:** Repository de turmas

**Funções necessárias:**
- `criar_tabela()` - Cria tabela no BD
- `inserir(turma: Turma)` - Insere turma
- `alterar(turma: Turma)` - Atualiza turma
- `excluir(id: int)` - Remove turma
- `obter_por_id(id: int)` - Busca por ID com JOINs
- `obter_todas()` - Lista todas com JOINs
- `obter_por_professor(id_professor: int)` - Turmas do professor
- `obter_por_atividade(id_atividade: int)` - Turmas da atividade
- `obter_quantidade()` - Conta total

#### **3.4.3 dtos/turma_dto.py** ❌ NÃO EXISTE
**Precisa criar:** DTOs de validação para turmas

**DTOs necessários:**
- `TurmaCreateDTO` - Validação de criação
- `TurmaUpdateDTO` - Validação de atualização
- Validações: id_atividade obrigatório, id_professor obrigatório

#### **3.4.4 routes/admin_turmas_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints administrativos de turmas

**Endpoints necessários:**
- `GET /admin/turmas` - Listar turmas
- `GET /admin/turmas/nova` - Formulário de nova turma
- `POST /admin/turmas/nova` - Criar turma
- `GET /admin/turmas/{id}/editar` - Formulário de edição
- `POST /admin/turmas/{id}/editar` - Atualizar turma
- `POST /admin/turmas/{id}/excluir` - Excluir turma
- `GET /admin/turmas/{id}/alunos` - Ver alunos da turma

#### **3.4.5 routes/professor_turmas_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints do professor para turmas

**Endpoints necessários:**
- `GET /professor/turmas` - Listar turmas do professor
- `GET /professor/turmas/nova` - Formulário de nova turma
- `POST /professor/turmas/nova` - Criar turma
- `GET /professor/turmas/{id}/editar` - Formulário de edição
- `POST /professor/turmas/{id}/editar` - Atualizar turma
- `POST /professor/turmas/{id}/excluir` - Excluir turma
- `GET /professor/turmas/{id}/alunos` - Ver alunos matriculados

### 3.5 Componentes a CRIAR - Matrículas

#### **3.5.1 sql/matricula_sql.py** ❌ NÃO EXISTE
**Precisa criar:** Queries SQL para matrículas

**Conteúdo necessário:**
- `CRIAR_TABELA` - CREATE TABLE matricula com FKs
- `INSERIR` - INSERT INTO matricula
- `ALTERAR` - UPDATE matricula
- `EXCLUIR` - DELETE FROM matricula (cancelamento)
- `OBTER_POR_ID` - SELECT com JOINs
- `OBTER_TODAS` - SELECT com JOINs
- `OBTER_POR_ALUNO` - Matrículas de um aluno
- `OBTER_POR_TURMA` - Matrículas de uma turma
- `VERIFICAR_MATRICULA_EXISTENTE` - Verifica se aluno já está matriculado
- `OBTER_QUANTIDADE` - COUNT de matrículas

#### **3.5.2 repo/matricula_repo.py** ❌ NÃO EXISTE
**Precisa criar:** Repository de matrículas

**Funções necessárias:**
- `criar_tabela()` - Cria tabela no BD
- `inserir(matricula: Matricula)` - Insere matrícula
- `alterar(matricula: Matricula)` - Atualiza matrícula
- `excluir(id: int)` - Cancela matrícula
- `obter_por_id(id: int)` - Busca por ID com JOINs
- `obter_todas()` - Lista todas com JOINs
- `obter_por_aluno(id_aluno: int)` - Matrículas do aluno
- `obter_por_turma(id_turma: int)` - Matrículas da turma
- `verificar_matricula_existente(id_aluno: int, id_turma: int)` - Verifica duplicação
- `obter_quantidade()` - Conta total

#### **3.5.3 dtos/matricula_dto.py** ❌ NÃO EXISTE
**Precisa criar:** DTOs de validação para matrículas

**DTOs necessários:**
- `MatriculaCreateDTO` - Validação de criação
- `MatriculaUpdateDTO` - Validação de atualização
- Validações: id_turma obrigatório, id_aluno obrigatório, valor_mensalidade > 0, data_vencimento válida

#### **3.5.4 routes/admin_matriculas_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints administrativos de matrículas

**Endpoints necessários:**
- `GET /admin/matriculas` - Listar matrículas
- `GET /admin/matriculas/nova` - Formulário de nova matrícula
- `POST /admin/matriculas/nova` - Criar matrícula
- `GET /admin/matriculas/{id}/editar` - Formulário de edição
- `POST /admin/matriculas/{id}/editar` - Atualizar matrícula
- `POST /admin/matriculas/{id}/cancelar` - Cancelar matrícula

#### **3.5.5 routes/aluno_matriculas_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints do aluno para matrículas

**Endpoints necessários:**
- `GET /aluno/matriculas` - Listar matrículas do aluno
- `POST /aluno/matriculas/nova` - Matricular-se em turma
- `POST /aluno/matriculas/{id}/cancelar` - Cancelar matrícula

### 3.6 Componentes a CRIAR - Pagamentos

#### **3.6.1 sql/pagamento_sql.py** ❌ NÃO EXISTE
**Precisa criar:** Queries SQL para pagamentos

**Conteúdo necessário:**
- `CRIAR_TABELA` - CREATE TABLE pagamento com FKs
- `INSERIR` - INSERT INTO pagamento
- `OBTER_POR_ID` - SELECT com JOINs
- `OBTER_TODOS` - SELECT com JOINs
- `OBTER_POR_MATRICULA` - Pagamentos de uma matrícula
- `OBTER_POR_ALUNO` - Pagamentos de um aluno
- `OBTER_QUANTIDADE` - COUNT de pagamentos

#### **3.6.2 repo/pagamento_repo.py** ❌ NÃO EXISTE
**Precisa criar:** Repository de pagamentos

**Funções necessárias:**
- `criar_tabela()` - Cria tabela no BD
- `inserir(pagamento: Pagamento)` - Registra pagamento
- `obter_por_id(id: int)` - Busca por ID com JOINs
- `obter_todos()` - Lista todos com JOINs
- `obter_por_matricula(id_matricula: int)` - Pagamentos da matrícula
- `obter_por_aluno(id_aluno: int)` - Pagamentos do aluno
- `obter_quantidade()` - Conta total

#### **3.6.3 dtos/pagamento_dto.py** ❌ NÃO EXISTE
**Precisa criar:** DTOs de validação para pagamentos

**DTOs necessários:**
- `PagamentoCreateDTO` - Validação de registro
- Validações: id_matricula obrigatório, valor_pago > 0, data_pagamento válida

#### **3.6.4 routes/admin_pagamentos_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints administrativos de pagamentos

**Endpoints necessários:**
- `GET /admin/pagamentos` - Listar pagamentos
- `GET /admin/pagamentos/novo` - Formulário de registro
- `POST /admin/pagamentos/novo` - Registrar pagamento
- `GET /admin/pagamentos/{id}` - Ver detalhes do pagamento

#### **3.6.5 routes/aluno_pagamentos_routes.py** ❌ NÃO EXISTE
**Precisa criar:** Endpoints do aluno para pagamentos

**Endpoints necessários:**
- `GET /aluno/pagamentos` - Listar pagamentos do aluno
- `GET /aluno/pagamentos/{id}` - Ver detalhes do pagamento

### 3.7 Componentes a CRIAR - Endereços

#### **3.7.1 sql/endereco_sql.py** ❌ NÃO EXISTE
**Precisa criar:** Queries SQL para endereços

**Conteúdo necessário:**
- `CRIAR_TABELA` - CREATE TABLE endereco com FK para usuario
- `INSERIR` - INSERT INTO endereco
- `ALTERAR` - UPDATE endereco
- `EXCLUIR` - DELETE FROM endereco
- `OBTER_POR_ID` - SELECT com JOIN em usuario
- `OBTER_POR_USUARIO` - Endereços de um usuário
- `OBTER_TODOS` - SELECT todos endereços

#### **3.7.2 repo/endereco_repo.py** ❌ NÃO EXISTE
**Precisa criar:** Repository de endereços

**Funções necessárias:**
- `criar_tabela()` - Cria tabela no BD
- `inserir(endereco: Endereco)` - Insere endereço
- `alterar(endereco: Endereco)` - Atualiza endereço
- `excluir(id: int)` - Remove endereço
- `obter_por_id(id: int)` - Busca por ID
- `obter_por_usuario(id_usuario: int)` - Endereços do usuário

#### **3.7.3 dtos/endereco_dto.py** ❌ NÃO EXISTE
**Precisa criar:** DTOs de validação para endereços

**DTOs necessários:**
- `EnderecoCreateDTO` - Validação de criação
- `EnderecoUpdateDTO` - Validação de atualização
- Validações: CEP formato correto, UF válida, campos obrigatórios

#### **3.7.4 Integração com Perfil do Usuário**
**Precisa modificar:** `routes/perfil_routes.py`

**Endpoints a adicionar:**
- `GET /perfil/enderecos` - Listar endereços do usuário
- `GET /perfil/enderecos/novo` - Formulário de novo endereço
- `POST /perfil/enderecos/novo` - Criar endereço
- `GET /perfil/enderecos/{id}/editar` - Formulário de edição
- `POST /perfil/enderecos/{id}/editar` - Atualizar endereço
- `POST /perfil/enderecos/{id}/excluir` - Excluir endereço

### 3.8 Funcionalidades Adicionais Necessárias

#### **3.8.1 Sistema de Notificações** ❌ NÃO EXISTE
**Requisito do PDF:** RF7 - Sistema de notificações automáticas

**Componentes necessários:**
- `model/notificacao_model.py` - Model de notificação
- `sql/notificacao_sql.py` - Queries SQL
- `repo/notificacao_repo.py` - Repository
- `util/notificacao_service.py` - Serviço de envio de notificações
- Integração com email_service existente

**Funcionalidades:**
- Notificação de nova matrícula
- Notificação de cancelamento de aula
- Lembretes de aula próxima
- Notificação de pagamento pendente

#### **3.8.2 Sistema de Avaliação Física** ❌ NÃO EXISTE
**Requisito do PDF:** RF8 - Aluno pode solicitar e visualizar avaliações físicas

**Componentes necessários:**
- `model/avaliacao_model.py` - Model de avaliação física
- `sql/avaliacao_sql.py` - Queries SQL
- `repo/avaliacao_repo.py` - Repository
- `dtos/avaliacao_dto.py` - DTOs de validação
- `routes/aluno_avaliacoes_routes.py` - Endpoints do aluno
- `routes/professor_avaliacoes_routes.py` - Endpoints do professor

**Funcionalidades:**
- Aluno solicita avaliação
- Professor realiza e registra avaliação
- Aluno visualiza histórico de avaliações
- Professor visualiza solicitações pendentes

#### **3.8.3 Sistema de Registro de Presença** ❌ NÃO EXISTE
**Requisito do PDF:** RF9 - Professor registra presença dos alunos

**Componentes necessários:**
- `model/presenca_model.py` - Model de presença
- `sql/presenca_sql.py` - Queries SQL
- `repo/presenca_repo.py` - Repository
- `dtos/presenca_dto.py` - DTOs de validação
- Integração com `routes/professor_turmas_routes.py`

**Funcionalidades:**
- Professor marca presença por turma e data
- Professor visualiza histórico de presenças
- Aluno visualiza suas presenças
- Relatórios de frequência

#### **3.8.4 Sistema de Relatórios e Estatísticas** ❌ NÃO EXISTE
**Requisito do PDF:** RF10 - Administrador vê estatísticas

**Componentes necessários:**
- `routes/admin_relatorios_routes.py` - Endpoints de relatórios
- Queries agregadas nos repositories existentes

**Funcionalidades:**
- Relatório de matrículas por período
- Relatório de ocupação de turmas
- Relatório de inadimplência
- Relatório de frequência de alunos
- Dashboard com métricas gerais

### 3.9 Atualizações em main.py

**Precisa adicionar no main.py:**
```python
# Novos imports de repositories
from repo import (
    categoria_repo,
    atividade_repo,
    turma_repo,
    matricula_repo,
    pagamento_repo,
    endereco_repo,
    notificacao_repo,
    avaliacao_repo,
    presenca_repo
)

# Novos imports de routes
from routes.admin_categorias_routes import router as admin_categorias_router
from routes.admin_atividades_routes import router as admin_atividades_router
from routes.admin_turmas_routes import router as admin_turmas_router
from routes.admin_matriculas_routes import router as admin_matriculas_router
from routes.admin_pagamentos_routes import router as admin_pagamentos_router
from routes.admin_relatorios_routes import router as admin_relatorios_router
from routes.professor_atividades_routes import router as prof_atividades_router
from routes.professor_turmas_routes import router as prof_turmas_router
from routes.professor_avaliacoes_routes import router as prof_avaliacoes_router
from routes.aluno_atividades_routes import router as aluno_atividades_router
from routes.aluno_matriculas_routes import router as aluno_matriculas_router
from routes.aluno_pagamentos_routes import router as aluno_pagamentos_router
from routes.aluno_avaliacoes_routes import router as aluno_avaliacoes_router

# Criar tabelas
categoria_repo.criar_tabela()
atividade_repo.criar_tabela()
turma_repo.criar_tabela()
matricula_repo.criar_tabela()
pagamento_repo.criar_tabela()
endereco_repo.criar_tabela()
notificacao_repo.criar_tabela()
avaliacao_repo.criar_tabela()
presenca_repo.criar_tabela()

# Incluir routers
app.include_router(admin_categorias_router, tags=["Admin - Categorias"])
app.include_router(admin_atividades_router, tags=["Admin - Atividades"])
app.include_router(admin_turmas_router, tags=["Admin - Turmas"])
app.include_router(admin_matriculas_router, tags=["Admin - Matrículas"])
app.include_router(admin_pagamentos_router, tags=["Admin - Pagamentos"])
app.include_router(admin_relatorios_router, tags=["Admin - Relatórios"])
app.include_router(prof_atividades_router, tags=["Professor - Atividades"])
app.include_router(prof_turmas_router, tags=["Professor - Turmas"])
app.include_router(prof_avaliacoes_router, tags=["Professor - Avaliações"])
app.include_router(aluno_atividades_router, tags=["Aluno - Atividades"])
app.include_router(aluno_matriculas_router, tags=["Aluno - Matrículas"])
app.include_router(aluno_pagamentos_router, tags=["Aluno - Pagamentos"])
app.include_router(aluno_avaliacoes_router, tags=["Aluno - Avaliações"])
```

### 3.10 Resumo Quantitativo

| Categoria | Quantidade | Status |
|-----------|------------|--------|
| **Models a corrigir** | 3 | Turma, Pagamento, Perfis |
| **SQL a criar** | 7 | categoria, atividade, turma, matricula, pagamento, endereco + 3 adicionais |
| **Repositories a criar** | 7 | categoria, atividade, turma, matricula, pagamento, endereco + 3 adicionais |
| **DTOs a criar** | 7 | categoria, atividade, turma, matricula, pagamento, endereco + 3 adicionais |
| **Routes Admin a criar** | 7 | categorias, atividades, turmas, matriculas, pagamentos, relatórios |
| **Routes Professor a criar** | 3 | atividades, turmas, avaliações |
| **Routes Aluno a criar** | 4 | atividades, matriculas, pagamentos, avaliações |
| **Funcionalidades adicionais** | 3 | Notificações, Avaliações, Presenças |
| **Arquivos a remover/adaptar** | 5 | Sistema de tarefas antigo |
| **TOTAL DE ARQUIVOS** | **~40-50** | Entre novos e modificados |

---

## 4. GUIA DE IMPLEMENTAÇÃO - SISTEMA DE PERFIS

### 4.1 Visão Geral

O sistema de perfis precisa ser atualizado de `ADMIN, CLIENTE, VENDEDOR` para `ADMIN, ALUNO, PROFESSOR` conforme especificado no PDF do AgendaFit.

**Impacto:** Esta é uma mudança crítica que afeta:
- Enum de perfis (`util/perfis.py`)
- Banco de dados (perfis existentes)
- Seeds de dados iniciais
- Decoradores de autorização
- Validações

### 4.2 PASSO 1: Atualizar util/perfis.py

#### **Arquivo:** `util/perfis.py`

**O que fazer:** Substituir os perfis existentes pelos do AgendaFit.

**Código atual:**
```python
class Perfil(str, Enum):
    ADMIN = "Administrador"
    CLIENTE = "Cliente"
    VENDEDOR = "Vendedor"
```

**Código atualizado:**
```python
from enum import Enum
from typing import Optional

class Perfil(str, Enum):
    """
    Enum centralizado para perfis de usuário do AgendaFit.

    Este é a FONTE ÚNICA DA VERDADE para perfis no sistema.
    SEMPRE use este Enum ao referenciar perfis, NUNCA strings literais.

    Exemplos:
        - Correto: perfil = Perfil.ADMIN.value
        - Correto: perfil = Perfil.ALUNO.value
        - Correto: perfil = Perfil.PROFESSOR.value
        - ERRADO: perfil = "admin"
        - ERRADO: perfil = "aluno"
    """

    # PERFIS DO AGENDAFIT #####################################
    ADMIN = "Administrador"
    ALUNO = "Aluno"
    PROFESSOR = "Professor"
    # FIM DOS PERFIS ##########################################

    def __str__(self) -> str:
        """Retorna o valor do perfil como string"""
        return self.value

    @classmethod
    def valores(cls) -> list[str]:
        """
        Retorna lista de todos os valores de perfis.

        Returns:
            Lista com os valores: ["Administrador", "Aluno", "Professor"]
        """
        return [perfil.value for perfil in cls]

    @classmethod
    def existe(cls, valor: str) -> bool:
        """
        Verifica se um valor de perfil é válido.

        Args:
            valor: String do perfil a validar

        Returns:
            True se o perfil existe, False caso contrário
        """
        return valor in cls.valores()

    @classmethod
    def from_string(cls, valor: str) -> Optional['Perfil']:
        """
        Converte uma string para o Enum Perfil correspondente.

        Args:
            valor: String do perfil

        Returns:
            Enum Perfil correspondente ou None se inválido

        Examples:
            >>> Perfil.from_string("Administrador")
            <Perfil.ADMIN: 'Administrador'>
            >>> Perfil.from_string("invalido")
            None
        """
        try:
            return cls(valor)
        except ValueError:
            return None

    @classmethod
    def validar(cls, valor: str) -> str:
        """
        Valida e retorna o valor do perfil, levantando exceção se inválido.

        Args:
            valor: String do perfil a validar

        Returns:
            O valor validado

        Raises:
            ValueError: Se o perfil não for válido
        """
        if not cls.existe(valor):
            raise ValueError(f'Perfil inválido: {valor}. Use: {", ".join(cls.valores())}')
        return valor
```

**✅ Checkpoint:** Após essa modificação, todos os perfis do sistema usarão os novos valores.

### 4.3 PASSO 2: Criar Script de Migração de Perfis

Precisamos migrar os perfis existentes no banco de dados. Como o projeto não usa migrations framework, faremos via script.

#### **Arquivo:** `util/migrar_perfis.py` (CRIAR NOVO)

**O que fazer:** Criar script para migrar perfis antigos para novos.

```python
"""
Script de migração de perfis para o AgendaFit.

Este script converte os perfis antigos (Cliente, Vendedor)
para os novos perfis (Aluno, Professor).

IMPORTANTE: Execute este script APENAS UMA VEZ antes de atualizar util/perfis.py
"""

from util.db_util import get_connection
from util.logger_config import logger

def migrar_perfis():
    """
    Migra perfis antigos para os novos do AgendaFit.

    Conversão:
    - "Cliente" -> "Aluno"
    - "Vendedor" -> "Professor"  (ou deletar se não houver vendedores reais)
    - "Administrador" -> mantém "Administrador"
    """

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Verificar quantos usuários de cada perfil existem
            cursor.execute("SELECT perfil, COUNT(*) as qtd FROM usuario GROUP BY perfil")
            perfis_atuais = cursor.fetchall()

            logger.info("=== PERFIS ATUAIS NO BANCO ===")
            for row in perfis_atuais:
                logger.info(f"  {row['perfil']}: {row['qtd']} usuário(s)")

            # Migrar Cliente -> Aluno
            cursor.execute("""
                UPDATE usuario
                SET perfil = 'Aluno'
                WHERE perfil = 'Cliente'
            """)
            qtd_clientes = cursor.rowcount
            logger.info(f"✅ Migrados {qtd_clientes} usuário(s) de 'Cliente' para 'Aluno'")

            # Decisão sobre Vendedor:
            # Opção 1: Converter para Professor
            cursor.execute("""
                UPDATE usuario
                SET perfil = 'Professor'
                WHERE perfil = 'Vendedor'
            """)
            qtd_vendedores = cursor.rowcount
            logger.info(f"✅ Migrados {qtd_vendedores} usuário(s) de 'Vendedor' para 'Professor'")

            # Opção 2 (alternativa): Deletar vendedores se não fizerem sentido
            # cursor.execute("DELETE FROM usuario WHERE perfil = 'Vendedor'")
            # qtd_deletados = cursor.rowcount
            # logger.info(f"❌ Deletados {qtd_deletados} usuário(s) com perfil 'Vendedor'")

            conn.commit()

            # Verificar resultado final
            cursor.execute("SELECT perfil, COUNT(*) as qtd FROM usuario GROUP BY perfil")
            perfis_novos = cursor.fetchall()

            logger.info("=== PERFIS APÓS MIGRAÇÃO ===")
            for row in perfis_novos:
                logger.info(f"  {row['perfil']}: {row['qtd']} usuário(s)")

            logger.info("✅ Migração de perfis concluída com sucesso!")
            return True

    except Exception as e:
        logger.error(f"❌ Erro ao migrar perfis: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    """
    Execute este script diretamente:
    python -m util.migrar_perfis
    """
    logger.info("=" * 60)
    logger.info("INICIANDO MIGRAÇÃO DE PERFIS DO AGENDAFIT")
    logger.info("=" * 60)

    sucesso = migrar_perfis()

    if sucesso:
        logger.info("=" * 60)
        logger.info("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        logger.info("Agora você pode atualizar util/perfis.py com segurança")
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("❌ MIGRAÇÃO FALHOU!")
        logger.error("Verifique os logs acima e corrija os erros")
        logger.error("=" * 60)
```

**Como executar:**
```bash
# Antes de atualizar util/perfis.py, execute:
python -m util.migrar_perfis
```

**✅ Checkpoint:** Após executar o script, todos os usuários no banco terão os novos perfis.

### 4.4 PASSO 3: Atualizar Seeds de Dados

#### **Arquivo:** `util/seed_data.py`

**O que fazer:** Atualizar a função de seed para usar os novos perfis.

**Buscar e substituir:**
```python
# ANTES:
usuario_admin = Usuario(
    id=0,
    nome="Administrador",
    email="admin@admin.com",
    senha=criar_hash_senha("admin"),
    perfil=Perfil.ADMIN.value
)

# Criar um usuário cliente exemplo
usuario_cliente = Usuario(
    id=0,
    nome="Cliente Exemplo",
    email="cliente@exemplo.com",
    senha=criar_hash_senha("123456"),
    perfil=Perfil.CLIENTE.value
)
```

```python
# DEPOIS:
usuario_admin = Usuario(
    id=0,
    nome="Administrador",
    email="admin@admin.com",
    senha=criar_hash_senha("admin"),
    perfil=Perfil.ADMIN.value
)

# Criar um usuário aluno exemplo
usuario_aluno = Usuario(
    id=0,
    nome="João da Silva",
    email="aluno@exemplo.com",
    senha=criar_hash_senha("123456"),
    perfil=Perfil.ALUNO.value
)

# Criar um usuário professor exemplo
usuario_professor = Usuario(
    id=0,
    nome="Prof. Maria Santos",
    email="professor@exemplo.com",
    senha=criar_hash_senha("123456"),
    perfil=Perfil.PROFESSOR.value
)
```

**Código completo sugerido para seed:**
```python
def inicializar_dados():
    """
    Inicializa dados iniciais do AgendaFit no banco de dados.

    Cria:
    - 1 administrador padrão
    - 1 professor exemplo
    - 1 aluno exemplo
    - Categorias de atividades padrão (quando implementadas)
    """
    from util.security import criar_hash_senha
    from util.perfis import Perfil
    from model.usuario_model import Usuario
    from repo import usuario_repo

    logger.info("Verificando dados iniciais do AgendaFit...")

    # Verificar se já existem usuários
    qtd_usuarios = usuario_repo.obter_quantidade()

    if qtd_usuarios == 0:
        logger.info("Nenhum usuário encontrado. Criando usuários padrão...")

        # 1. ADMINISTRADOR
        admin = Usuario(
            id=0,
            nome="Administrador",
            email="admin@agendafit.com",
            senha=criar_hash_senha("admin123"),
            perfil=Perfil.ADMIN.value
        )
        admin_id = usuario_repo.inserir(admin)
        if admin_id:
            logger.info(f"✅ Administrador criado (ID: {admin_id})")

        # 2. PROFESSOR EXEMPLO
        professor = Usuario(
            id=0,
            nome="Prof. Carlos Oliveira",
            email="professor@agendafit.com",
            senha=criar_hash_senha("prof123"),
            perfil=Perfil.PROFESSOR.value
        )
        prof_id = usuario_repo.inserir(professor)
        if prof_id:
            logger.info(f"✅ Professor exemplo criado (ID: {prof_id})")

        # 3. ALUNO EXEMPLO
        aluno = Usuario(
            id=0,
            nome="Ana Paula Costa",
            email="aluno@agendafit.com",
            senha=criar_hash_senha("aluno123"),
            perfil=Perfil.ALUNO.value
        )
        aluno_id = usuario_repo.inserir(aluno)
        if aluno_id:
            logger.info(f"✅ Aluno exemplo criado (ID: {aluno_id})")

        logger.info("✅ Dados iniciais do AgendaFit criados com sucesso!")
        logger.info("=" * 60)
        logger.info("CREDENCIAIS PADRÃO:")
        logger.info("  Admin:     admin@agendafit.com / admin123")
        logger.info("  Professor: professor@agendafit.com / prof123")
        logger.info("  Aluno:     aluno@agendafit.com / aluno123")
        logger.info("=" * 60)
    else:
        logger.info(f"Banco já possui {qtd_usuarios} usuário(s). Seed não necessário.")

    # TODO: Quando implementar categorias, adicionar seeds de categorias padrão
    # Exemplos: Yoga, Musculação, Pilates, Spinning, Crossfit, etc.
```

**✅ Checkpoint:** Seeds agora criam usuários com os perfis corretos do AgendaFit.

### 4.5 PASSO 4: Atualizar Decoradores de Autorização

#### **Arquivo:** `util/auth_decorator.py`

**O que fazer:** Verificar se os decoradores de autorização usam o Enum Perfil corretamente.

**Código esperado (já deve estar correto):**
```python
from functools import wraps
from fastapi import Request, status
from fastapi.responses import RedirectResponse
from util.perfis import Perfil
from util.flash_messages import informar_erro

def requer_perfil(*perfis_permitidos: Perfil):
    """
    Decorator que restringe acesso a apenas perfis específicos.

    Args:
        *perfis_permitidos: Perfis que podem acessar a rota

    Exemplo:
        @requer_perfil(Perfil.ADMIN)
        @requer_perfil(Perfil.ADMIN, Perfil.PROFESSOR)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            usuario_logado = request.session.get("usuario_logado")

            if not usuario_logado:
                informar_erro(request, "Você precisa estar logado para acessar esta página")
                return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

            perfil_usuario = usuario_logado.get("perfil")
            perfis_valores = [p.value for p in perfis_permitidos]

            if perfil_usuario not in perfis_valores:
                informar_erro(request, "Você não tem permissão para acessar esta página")
                return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

# Atalhos para perfis específicos
def requer_admin(func):
    """Decorator que restringe acesso apenas a administradores"""
    return requer_perfil(Perfil.ADMIN)(func)

def requer_professor(func):
    """Decorator que restringe acesso apenas a professores"""
    return requer_perfil(Perfil.PROFESSOR)(func)

def requer_aluno(func):
    """Decorator que restringe acesso apenas a alunos"""
    return requer_perfil(Perfil.ALUNO)(func)

def requer_professor_ou_admin(func):
    """Decorator que permite acesso a professores e administradores"""
    return requer_perfil(Perfil.PROFESSOR, Perfil.ADMIN)(func)

def requer_logado(func):
    """Decorator que apenas verifica se usuário está logado (qualquer perfil)"""
    return requer_perfil(Perfil.ADMIN, Perfil.PROFESSOR, Perfil.ALUNO)(func)
```

**Exemplo de uso nos routes:**
```python
from util.auth_decorator import requer_admin, requer_professor, requer_aluno

@router.get("/admin/usuarios")
@requer_admin
async def listar_usuarios(request: Request):
    # Apenas admins podem acessar
    pass

@router.get("/professor/turmas")
@requer_professor
async def listar_turmas_professor(request: Request):
    # Apenas professores podem acessar
    pass

@router.get("/aluno/matriculas")
@requer_aluno
async def listar_matriculas_aluno(request: Request):
    # Apenas alunos podem acessar
    pass
```

**✅ Checkpoint:** Decoradores agora suportam os novos perfis do AgendaFit.

### 4.6 PASSO 5: Atualizar Validações em DTOs

#### **Arquivo:** `dtos/validators.py`

**O que fazer:** Adicionar validador de perfil do AgendaFit.

**Adicionar no arquivo:**
```python
from util.perfis import Perfil

def validar_perfil_agendafit(perfil: str) -> str:
    """
    Valida se o perfil é válido para o AgendaFit.

    Args:
        perfil: String do perfil a validar

    Returns:
        O perfil validado

    Raises:
        ValueError: Se o perfil for inválido
    """
    if not Perfil.existe(perfil):
        perfis_validos = ", ".join(Perfil.valores())
        raise ValueError(
            f"Perfil inválido: '{perfil}'. "
            f"Perfis válidos: {perfis_validos}"
        )
    return perfil
```

**Uso em DTOs:**
```python
from pydantic import BaseModel, field_validator
from dtos.validators import validar_perfil_agendafit

class UsuarioCreateDTO(BaseModel):
    nome: str
    email: str
    senha: str
    perfil: str

    @field_validator('perfil')
    @classmethod
    def validar_perfil(cls, v: str) -> str:
        return validar_perfil_agendafit(v)
```

**✅ Checkpoint:** Validações garantem que apenas perfis válidos sejam aceitos.

### 4.7 PASSO 6: Atualizar Routes Administrativos

#### **Arquivo:** `routes/admin_usuarios_routes.py`

**O que fazer:** Atualizar formulários e validações para usar os novos perfis.

**Exemplo de ajuste em formulário:**
```python
from util.perfis import Perfil

@router.get("/admin/usuarios/novo")
@requer_admin
async def get_novo_usuario(request: Request):
    """Formulário de criação de usuário"""

    # Passar os perfis disponíveis para o template
    perfis_disponiveis = [
        {"value": Perfil.ADMIN.value, "label": "Administrador"},
        {"value": Perfil.PROFESSOR.value, "label": "Professor"},
        {"value": Perfil.ALUNO.value, "label": "Aluno"}
    ]

    return templates.TemplateResponse("admin/usuario_form.html", {
        "request": request,
        "perfis": perfis_disponiveis,
        "titulo": "Novo Usuário"
    })
```

**✅ Checkpoint:** Interface administrativa usa os perfis corretos.

### 4.8 Resumo da Implementação - Sistema de Perfis

#### **Ordem de Execução:**

1. ✅ **Executar script de migração**
   ```bash
   python -m util.migrar_perfis
   ```

2. ✅ **Atualizar `util/perfis.py`**
   - Substituir CLIENTE e VENDEDOR por ALUNO e PROFESSOR

3. ✅ **Atualizar `util/seed_data.py`**
   - Criar seeds com os novos perfis

4. ✅ **Atualizar `util/auth_decorator.py`**
   - Adicionar decoradores específicos para PROFESSOR e ALUNO

5. ✅ **Atualizar `dtos/validators.py`**
   - Adicionar validador de perfil AgendaFit

6. ✅ **Atualizar routes administrativos**
   - Ajustar formulários e listagens

7. ✅ **Testar**
   - Login com cada perfil
   - Verificar restrições de acesso
   - Confirmar que seeds funcionam

#### **Arquivos Modificados:**
- ✏️ `util/perfis.py` (atualização crítica)
- ➕ `util/migrar_perfis.py` (novo - executar uma vez)
- ✏️ `util/seed_data.py` (atualização)
- ✏️ `util/auth_decorator.py` (atualização)
- ✏️ `dtos/validators.py` (adicionar validador)
- ✏️ `routes/admin_usuarios_routes.py` (atualização)

#### **Dependências:**
- ✅ Nenhuma dependência externa adicional necessária
- ✅ Usa apenas código já existente no projeto

#### **Riscos:**
- ⚠️ **CRÍTICO:** Executar migração de perfis ANTES de atualizar o enum
- ⚠️ **MÉDIO:** Verificar se há sessões ativas de usuários antes da migração
- ⚠️ **BAIXO:** Limpar cache de sessões após migração

#### **Validação Final:**
```bash
# 1. Verificar perfis no banco
sqlite3 bd.db "SELECT perfil, COUNT(*) FROM usuario GROUP BY perfil"

# Resultado esperado:
# Administrador|1
# Professor|X
# Aluno|Y

# 2. Testar login de cada perfil
# 3. Verificar acesso às rotas protegidas
# 4. Confirmar que decoradores funcionam corretamente
```

---

## 5. GUIA DE IMPLEMENTAÇÃO - CATEGORIAS E ATIVIDADES

### 5.1 Visão Geral

Este módulo implementa o sistema de categorias (ex: Yoga, Musculação) e atividades (aulas específicas dentro de cada categoria). É a base para todo o sistema de agendamento do AgendaFit.

**Dependências:** Sistema de Perfis implementado

**Ordem de implementação:**
1. Categorias (SQL → Repo → DTO → Routes Admin)
2. Atividades (SQL → Repo → DTO → Routes Admin/Professor/Aluno)

### 5.2 CATEGORIAS - SQL

#### **Arquivo:** `sql/categoria_sql.py` (CRIAR)

```python
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""

INSERIR = """
INSERT INTO categoria (nome, descricao)
VALUES (?, ?)
"""

ALTERAR = """
UPDATE categoria
SET nome = ?, descricao = ?
WHERE id_categoria = ?
"""

EXCLUIR = "DELETE FROM categoria WHERE id_categoria = ?"

OBTER_POR_ID = "SELECT * FROM categoria WHERE id_categoria = ?"

OBTER_TODAS = "SELECT * FROM categoria ORDER BY nome"

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM categoria"

OBTER_POR_NOME = "SELECT * FROM categoria WHERE nome = ?"
```

### 5.3 CATEGORIAS - Repository

#### **Arquivo:** `repo/categoria_repo.py` (CRIAR)

```python
from typing import Optional
from model.categoria_model import Categoria
from sql.categoria_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(categoria: Categoria) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (categoria.nome, categoria.descricao))
        return cursor.lastrowid

def alterar(categoria: Categoria) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (categoria.nome, categoria.descricao, categoria.id_categoria))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0

def obter_por_id(id: int) -> Optional[Categoria]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Categoria(
                id_categoria=row["id_categoria"],
                nome=row["nome"],
                descricao=row["descricao"]
            )
        return None

def obter_todas() -> list[Categoria]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Categoria(
                id_categoria=row["id_categoria"],
                nome=row["nome"],
                descricao=row["descricao"]
            )
            for row in rows
        ]

def obter_quantidade() -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0
```

### 5.4 CATEGORIAS - DTOs

#### **Arquivo:** `dtos/categoria_dto.py` (CRIAR)

```python
from pydantic import BaseModel, field_validator

class CategoriaCreateDTO(BaseModel):
    nome: str
    descricao: str

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Nome deve ter no mínimo 3 caracteres')
        if len(v) > 100:
            raise ValueError('Nome deve ter no máximo 100 caracteres')
        return v

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError('Descrição deve ter no mínimo 10 caracteres')
        if len(v) > 500:
            raise ValueError('Descrição deve ter no máximo 500 caracteres')
        return v

class CategoriaUpdateDTO(CategoriaCreateDTO):
    pass
```

### 5.5 CATEGORIAS - Routes Admin

#### **Arquivo:** `routes/admin_categorias_routes.py` (CRIAR)

```python
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from util.auth_decorator import requer_admin
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.exceptions import FormValidationError
from dtos.categoria_dto import CategoriaCreateDTO, CategoriaUpdateDTO
from model.categoria_model import Categoria
from repo import categoria_repo

router = APIRouter(prefix="/admin/categorias")
templates = criar_templates("templates/admin/categorias")

@router.get("")
@requer_admin
async def listar_categorias(request: Request):
    """Lista todas as categorias"""
    categorias = categoria_repo.obter_todas()
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "categorias": categorias
    })

@router.get("/nova")
@requer_admin
async def get_nova_categoria(request: Request):
    """Formulário de nova categoria"""
    return templates.TemplateResponse("form.html", {
        "request": request,
        "titulo": "Nova Categoria"
    })

@router.post("/nova")
@requer_admin
async def post_nova_categoria(
    request: Request,
    nome: str = Form(),
    descricao: str = Form()
):
    """Cria nova categoria"""
    try:
        dto = CategoriaCreateDTO(nome=nome, descricao=descricao)
        categoria = Categoria(id_categoria=0, nome=dto.nome, descricao=dto.descricao)

        id_categoria = categoria_repo.inserir(categoria)
        if id_categoria:
            informar_sucesso(request, "Categoria criada com sucesso!")
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

        raise FormValidationError({"geral": "Erro ao criar categoria"})

    except ValidationError as e:
        erros = {err['loc'][0]: err['msg'] for err in e.errors()}
        raise FormValidationError(erros)

@router.get("/{id}/editar")
@requer_admin
async def get_editar_categoria(request: Request, id: int):
    """Formulário de edição"""
    categoria = categoria_repo.obter_por_id(id)
    if not categoria:
        informar_erro(request, "Categoria não encontrada")
        return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

    return templates.TemplateResponse("form.html", {
        "request": request,
        "categoria": categoria,
        "titulo": "Editar Categoria"
    })

@router.post("/{id}/editar")
@requer_admin
async def post_editar_categoria(
    request: Request,
    id: int,
    nome: str = Form(),
    descricao: str = Form()
):
    """Atualiza categoria"""
    try:
        dto = CategoriaUpdateDTO(nome=nome, descricao=descricao)
        categoria = Categoria(id_categoria=id, nome=dto.nome, descricao=dto.descricao)

        if categoria_repo.alterar(categoria):
            informar_sucesso(request, "Categoria atualizada com sucesso!")
            return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)

        raise FormValidationError({"geral": "Erro ao atualizar categoria"})

    except ValidationError as e:
        erros = {err['loc'][0]: err['msg'] for err in e.errors()}
        raise FormValidationError(erros)

@router.post("/{id}/excluir")
@requer_admin
async def excluir_categoria(request: Request, id: int):
    """Exclui categoria"""
    if categoria_repo.excluir(id):
        informar_sucesso(request, "Categoria excluída com sucesso!")
    else:
        informar_erro(request, "Erro ao excluir categoria")

    return RedirectResponse("/admin/categorias", status_code=status.HTTP_303_SEE_OTHER)
```

### 5.6 ATIVIDADES - SQL

#### **Arquivo:** `sql/atividade_sql.py` (CRIAR)

```python
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS atividade (
    id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria INTEGER NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
)
"""

INSERIR = """
INSERT INTO atividade (id_categoria, nome, descricao)
VALUES (?, ?, ?)
"""

ALTERAR = """
UPDATE atividade
SET id_categoria = ?, nome = ?, descricao = ?
WHERE id_atividade = ?
"""

EXCLUIR = "DELETE FROM atividade WHERE id_atividade = ?"

OBTER_POR_ID = """
SELECT a.*, c.nome as categoria_nome, c.descricao as categoria_descricao
FROM atividade a
JOIN categoria c ON a.id_categoria = c.id_categoria
WHERE a.id_atividade = ?
"""

OBTER_TODAS = """
SELECT a.*, c.nome as categoria_nome, c.descricao as categoria_descricao
FROM atividade a
JOIN categoria c ON a.id_categoria = c.id_categoria
ORDER BY c.nome, a.nome
"""

OBTER_POR_CATEGORIA = """
SELECT a.*, c.nome as categoria_nome, c.descricao as categoria_descricao
FROM atividade a
JOIN categoria c ON a.id_categoria = c.id_categoria
WHERE a.id_categoria = ?
ORDER BY a.nome
"""

OBTER_QUANTIDADE = "SELECT COUNT(*) as quantidade FROM atividade"
```

### 5.7 ATIVIDADES - Repository

#### **Arquivo:** `repo/atividade_repo.py` (CRIAR)

```python
from typing import Optional
from datetime import datetime
from model.Atividade_model import Atividade
from model.categoria_model import Categoria
from sql.atividade_sql import *
from util.db_util import get_connection

def criar_tabela() -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA)
        return True

def inserir(atividade: Atividade) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            atividade.id_categoria,
            atividade.nome,
            atividade.descricao
        ))
        return cursor.lastrowid

def alterar(atividade: Atividade) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ALTERAR, (
            atividade.id_categoria,
            atividade.nome,
            atividade.descricao,
            atividade.id_atividade
        ))
        return cursor.rowcount > 0

def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0

def obter_por_id(id: int) -> Optional[Atividade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            categoria = Categoria(
                id_categoria=row["id_categoria"],
                nome=row["categoria_nome"],
                descricao=row["categoria_descricao"]
            )
            return Atividade(
                id_atividade=row["id_atividade"],
                id_categoria=row["id_categoria"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_cadastro=datetime.fromisoformat(row["data_cadastro"]),
                categoria=categoria
            )
        return None

def obter_todas() -> list[Atividade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS)
        rows = cursor.fetchall()
        return [
            Atividade(
                id_atividade=row["id_atividade"],
                id_categoria=row["id_categoria"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_cadastro=datetime.fromisoformat(row["data_cadastro"]),
                categoria=Categoria(
                    id_categoria=row["id_categoria"],
                    nome=row["categoria_nome"],
                    descricao=row["categoria_descricao"]
                )
            )
            for row in rows
        ]

def obter_por_categoria(id_categoria: int) -> list[Atividade]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_CATEGORIA, (id_categoria,))
        rows = cursor.fetchall()
        return [
            Atividade(
                id_atividade=row["id_atividade"],
                id_categoria=row["id_categoria"],
                nome=row["nome"],
                descricao=row["descricao"],
                data_cadastro=datetime.fromisoformat(row["data_cadastro"]),
                categoria=Categoria(
                    id_categoria=row["id_categoria"],
                    nome=row["categoria_nome"],
                    descricao=row["categoria_descricao"]
                )
            )
            for row in rows
        ]

def obter_quantidade() -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_QUANTIDADE)
        row = cursor.fetchone()
        return row["quantidade"] if row else 0
```

### 5.8 ATIVIDADES - DTOs

#### **Arquivo:** `dtos/atividade_dto.py` (CRIAR)

```python
from pydantic import BaseModel, field_validator

class AtividadeCreateDTO(BaseModel):
    id_categoria: int
    nome: str
    descricao: str

    @field_validator('id_categoria')
    @classmethod
    def validar_categoria(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('Categoria inválida')
        return v

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Nome deve ter no mínimo 3 caracteres')
        if len(v) > 100:
            raise ValueError('Nome deve ter no máximo 100 caracteres')
        return v

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError('Descrição deve ter no mínimo 10 caracteres')
        if len(v) > 1000:
            raise ValueError('Descrição deve ter no máximo 1000 caracteres')
        return v

class AtividadeUpdateDTO(AtividadeCreateDTO):
    pass
```

### 5.9 ATIVIDADES - Routes (Admin, Professor, Aluno)

#### **Arquivo:** `routes/admin_atividades_routes.py` (CRIAR)

```python
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from datetime import datetime

from util.auth_decorator import requer_admin
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
from util.exceptions import FormValidationError
from dtos.atividade_dto import AtividadeCreateDTO, AtividadeUpdateDTO
from model.Atividade_model import Atividade
from repo import atividade_repo, categoria_repo

router = APIRouter(prefix="/admin/atividades")
templates = criar_templates("templates/admin/atividades")

@router.get("")
@requer_admin
async def listar_atividades(request: Request):
    atividades = atividade_repo.obter_todas()
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "atividades": atividades
    })

@router.get("/nova")
@requer_admin
async def get_nova_atividade(request: Request):
    categorias = categoria_repo.obter_todas()
    return templates.TemplateResponse("form.html", {
        "request": request,
        "categorias": categorias,
        "titulo": "Nova Atividade"
    })

@router.post("/nova")
@requer_admin
async def post_nova_atividade(
    request: Request,
    id_categoria: int = Form(),
    nome: str = Form(),
    descricao: str = Form()
):
    try:
        dto = AtividadeCreateDTO(id_categoria=id_categoria, nome=nome, descricao=descricao)
        atividade = Atividade(
            id_atividade=0,
            id_categoria=dto.id_categoria,
            nome=dto.nome,
            descricao=dto.descricao,
            data_cadastro=datetime.now(),
            categoria=None
        )

        if atividade_repo.inserir(atividade):
            informar_sucesso(request, "Atividade criada com sucesso!")
            return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)

        raise FormValidationError({"geral": "Erro ao criar atividade"})

    except ValidationError as e:
        erros = {err['loc'][0]: err['msg'] for err in e.errors()}
        raise FormValidationError(erros)

# Demais métodos (editar, excluir) seguem o mesmo padrão das categorias
```

#### **Arquivo:** `routes/professor_atividades_routes.py` (CRIAR)

```python
from fastapi import APIRouter, Request
from util.auth_decorator import requer_professor
from util.template_util import criar_templates
from repo import atividade_repo

router = APIRouter(prefix="/professor/atividades")
templates = criar_templates("templates/professor/atividades")

@router.get("")
@requer_professor
async def listar_atividades(request: Request):
    """Lista atividades disponíveis para criar turmas"""
    atividades = atividade_repo.obter_todas()
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "atividades": atividades
    })

# Professor também pode ter endpoints para criar atividades se permitido
```

#### **Arquivo:** `routes/aluno_atividades_routes.py` (CRIAR)

```python
from fastapi import APIRouter, Request
from util.auth_decorator import requer_aluno
from util.template_util import criar_templates
from repo import atividade_repo

router = APIRouter(prefix="/aluno/atividades")
templates = criar_templates("templates/aluno/atividades")

@router.get("")
@requer_aluno
async def listar_atividades(request: Request):
    """Lista atividades disponíveis"""
    atividades = atividade_repo.obter_todas()
    return templates.TemplateResponse("lista.html", {
        "request": request,
        "atividades": atividades
    })

@router.get("/{id}")
@requer_aluno
async def ver_atividade(request: Request, id: int):
    """Detalhes de uma atividade"""
    atividade = atividade_repo.obter_por_id(id)
    return templates.TemplateResponse("detalhes.html", {
        "request": request,
        "atividade": atividade
    })
```

### 5.10 Resumo - Categorias e Atividades

**Arquivos criados:** 9
- 2 SQL: categoria_sql.py, atividade_sql.py
- 2 Repositories: categoria_repo.py, atividade_repo.py
- 2 DTOs: categoria_dto.py, atividade_dto.py
- 3 Routes: admin_categorias_routes.py, admin_atividades_routes.py, aluno_atividades_routes.py

**Atualizar main.py:**
```python
from repo import categoria_repo, atividade_repo
from routes.admin_categorias_routes import router as admin_cat_router
from routes.admin_atividades_routes import router as admin_ativ_router
from routes.aluno_atividades_routes import router as aluno_ativ_router

categoria_repo.criar_tabela()
atividade_repo.criar_tabela()

app.include_router(admin_cat_router, tags=["Admin - Categorias"])
app.include_router(admin_ativ_router, tags=["Admin - Atividades"])
app.include_router(aluno_ativ_router, tags=["Aluno - Atividades"])
```

---

## 6. GUIA DE IMPLEMENTAÇÃO - TURMAS E MATRÍCULAS

### 6.1 Visão Geral

Turmas são instâncias específicas de atividades ministradas por professores. Matrículas vinculam alunos às turmas.

**Dependências:** Categorias, Atividades e Sistema de Perfis implementados

### 6.2 CORRIGIR Model Turma

#### **Arquivo:** `model/Turma_model.py` (MODIFICAR)

**PROBLEMA:** Falta chave primária `id_turma`

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from model.Atividade_model import Atividade
from model.usuario_model import Usuario

@dataclass
class Turma:
    id_turma: int  # ← ADICIONAR ESTE CAMPO
    id_atividade: int
    id_professor: int
    data_cadastro: datetime
    atividade: Optional[Atividade]
    professor: Optional[Usuario]
```

### 6.3 TURMAS - SQL, Repository, DTO, Routes

#### **Arquivo:** `sql/turma_sql.py` (CRIAR)

```python
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS turma (
    id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
    id_atividade INTEGER NOT NULL,
    id_professor INTEGER NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade),
    FOREIGN KEY (id_professor) REFERENCES usuario(id)
)
"""

INSERIR = "INSERT INTO turma (id_atividade, id_professor) VALUES (?, ?)"
ALTERAR = "UPDATE turma SET id_atividade = ?, id_professor = ? WHERE id_turma = ?"
EXCLUIR = "DELETE FROM turma WHERE id_turma = ?"

OBTER_POR_ID = """
SELECT t.*,
       a.nome as atividade_nome, a.descricao as atividade_descricao,
       u.nome as professor_nome, u.email as professor_email
FROM turma t
JOIN atividade a ON t.id_atividade = a.id_atividade
JOIN usuario u ON t.id_professor = u.id
WHERE t.id_turma = ?
"""

OBTER_TODAS = """
SELECT t.*,
       a.nome as atividade_nome, a.descricao as atividade_descricao,
       u.nome as professor_nome
FROM turma t
JOIN atividade a ON t.id_atividade = a.id_atividade
JOIN usuario u ON t.id_professor = u.id
ORDER BY a.nome
"""

OBTER_POR_PROFESSOR = "SELECT * FROM turma WHERE id_professor = ?"
```

#### **Arquivo:** `repo/turma_repo.py` (CRIAR)

Seguir padrão de `categoria_repo.py` e `atividade_repo.py` com JOINs para carregar atividade e professor.

#### **Arquivo:** `dtos/turma_dto.py` (CRIAR)

```python
from pydantic import BaseModel, field_validator

class TurmaCreateDTO(BaseModel):
    id_atividade: int
    id_professor: int

    @field_validator('id_atividade', 'id_professor')
    @classmethod
    def validar_ids(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('ID inválido')
        return v
```

#### **Arquivo:** `routes/admin_turmas_routes.py` (CRIAR)

Seguir padrão de `admin_categorias_routes.py` com CRUD completo.

### 6.4 MATRÍCULAS - SQL, Repository, DTO, Routes

#### **Arquivo:** `sql/matricula_sql.py` (CRIAR)

```python
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS matricula (
    id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
    id_turma INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    data_matricula DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_mensalidade REAL NOT NULL,
    data_vencimento DATETIME NOT NULL,
    FOREIGN KEY (id_turma) REFERENCES turma(id_turma),
    FOREIGN KEY (id_aluno) REFERENCES usuario(id),
    UNIQUE(id_turma, id_aluno)
)
"""

INSERIR = """
INSERT INTO matricula (id_turma, id_aluno, valor_mensalidade, data_vencimento)
VALUES (?, ?, ?, ?)
"""

OBTER_POR_ALUNO = """
SELECT m.*,
       t.id_atividade, t.id_professor,
       a.nome as atividade_nome,
       u.nome as aluno_nome
FROM matricula m
JOIN turma t ON m.id_turma = t.id_turma
JOIN atividade a ON t.id_atividade = a.id_atividade
JOIN usuario u ON m.id_aluno = u.id
WHERE m.id_aluno = ?
ORDER BY m.data_matricula DESC
"""

OBTER_POR_TURMA = """
SELECT m.*, u.nome as aluno_nome, u.email as aluno_email
FROM matricula m
JOIN usuario u ON m.id_aluno = u.id
WHERE m.id_turma = ?
ORDER BY u.nome
"""

VERIFICAR_MATRICULA_EXISTENTE = """
SELECT COUNT(*) as qtd FROM matricula
WHERE id_turma = ? AND id_aluno = ?
"""
```

#### **Arquivo:** `repo/matricula_repo.py` (CRIAR)

Incluir método `verificar_matricula_existente()` para evitar duplicação.

#### **Arquivo:** `dtos/matricula_dto.py` (CRIAR)

```python
from pydantic import BaseModel, field_validator
from datetime import datetime

class MatriculaCreateDTO(BaseModel):
    id_turma: int
    id_aluno: int
    valor_mensalidade: float
    data_vencimento: str

    @field_validator('valor_mensalidade')
    @classmethod
    def validar_valor(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Valor deve ser maior que zero')
        return v

    @field_validator('data_vencimento')
    @classmethod
    def validar_data(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
            return v
        except:
            raise ValueError('Data inválida')
```

#### **Arquivo:** `routes/aluno_matriculas_routes.py` (CRIAR)

```python
@router.post("/nova")
@requer_aluno
async def matricular(request: Request, id_turma: int = Form()):
    """Aluno se matricula em uma turma"""
    usuario_logado = request.session.get("usuario_logado")
    id_aluno = usuario_logado["id"]

    # Verificar se já está matriculado
    if matricula_repo.verificar_matricula_existente(id_aluno, id_turma):
        informar_erro(request, "Você já está matriculado nesta turma")
        return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)

    # Criar matrícula
    matricula = Matricula(...)
    if matricula_repo.inserir(matricula):
        informar_sucesso(request, "Matrícula realizada com sucesso!")

    return RedirectResponse("/aluno/matriculas", status_code=status.HTTP_303_SEE_OTHER)
```

### 6.5 Resumo - Turmas e Matrículas

**Arquivos:**
- 1 Model corrigido: Turma_model.py
- 2 SQL: turma_sql.py, matricula_sql.py
- 2 Repositories: turma_repo.py, matricula_repo.py
- 2 DTOs: turma_dto.py, matricula_dto.py
- 4 Routes: admin_turmas_routes.py, professor_turmas_routes.py, admin_matriculas_routes.py, aluno_matriculas_routes.py

---

## 7. GUIA DE IMPLEMENTAÇÃO - PAGAMENTOS E ENDEREÇOS

### 7.1 CORRIGIR Model Pagamento

#### **Arquivo:** `model/Pagamento_model.py` (MODIFICAR)

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from model.matricula_model import Matricula
from model.usuario_model import Usuario

@dataclass
class Pagamento:
    id_pagamento: int  # ← ADICIONAR PK
    id_matricula: int
    id_aluno: int
    data_pagamento: datetime
    valor_pago: float
    matricula: Optional[Matricula]
    aluno: Optional[Usuario]  # ← CORRIGIR TIPO (era Matricula)
```

### 7.2 PAGAMENTOS - SQL, Repository, DTO, Routes

#### **Arquivo:** `sql/pagamento_sql.py` (CRIAR)

```python
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS pagamento (
    id_pagamento INTEGER PRIMARY KEY AUTOINCREMENT,
    id_matricula INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    data_pagamento DATETIME DEFAULT CURRENT_TIMESTAMP,
    valor_pago REAL NOT NULL,
    FOREIGN KEY (id_matricula) REFERENCES matricula(id_matricula),
    FOREIGN KEY (id_aluno) REFERENCES usuario(id)
)
"""

INSERIR = "INSERT INTO pagamento (id_matricula, id_aluno, valor_pago) VALUES (?, ?, ?)"

OBTER_POR_ALUNO = """
SELECT p.*, m.valor_mensalidade, u.nome as aluno_nome
FROM pagamento p
JOIN matricula m ON p.id_matricula = m.id_matricula
JOIN usuario u ON p.id_aluno = u.id
WHERE p.id_aluno = ?
ORDER BY p.data_pagamento DESC
 """

OBTER_POR_MATRICULA = "SELECT * FROM pagamento WHERE id_matricula = ?"
```

#### **Arquivo:** `repo/pagamento_repo.py`, `dtos/pagamento_dto.py`, `routes/admin_pagamentos_routes.py`, `routes/aluno_pagamentos_routes.py` (CRIAR)

Seguir padrões estabelecidos anteriormente.

### 7.3 ENDEREÇOS - SQL, Repository, DTO, Routes

#### **Arquivo:** `sql/endereco_sql.py` (CRIAR)

```python
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS endereco (
    id_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    logradouro TEXT NOT NULL,
    numero INTEGER NOT NULL,
    complemento TEXT,
    bairro TEXT NOT NULL,
    cidade TEXT NOT NULL,
    uf TEXT NOT NULL,
    cep TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
)
"""

INSERIR = """
INSERT INTO endereco (id_usuario, titulo, logradouro, numero, complemento, bairro, cidade, uf, cep)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

OBTER_POR_USUARIO = "SELECT * FROM endereco WHERE id_usuario = ?"
```

#### **Arquivo:** `repo/endereco_repo.py`, `dtos/endereco_dto.py` (CRIAR)

**DTO com validações:**
```python
@field_validator('cep')
@classmethod
def validar_cep(cls, v: str) -> str:
    import re
    v = re.sub(r'\D', '', v)  # Remove não dígitos
    if len(v) != 8:
        raise ValueError('CEP deve ter 8 dígitos')
    return v

@field_validator('uf')
@classmethod
def validar_uf(cls, v: str) -> str:
    ufs_validas = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
                   'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
                   'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    if v.upper() not in ufs_validas:
        raise ValueError('UF inválida')
    return v.upper()
```

#### **Modificar:** `routes/perfil_routes.py`

Adicionar endpoints para gerenciar endereços do usuário logado.

### 7.4 Resumo - Pagamentos e Endereços

**Arquivos:**
- 1 Model corrigido: Pagamento_model.py
- 2 SQL: pagamento_sql.py, endereco_sql.py
- 2 Repositories: pagamento_repo.py, endereco_repo.py
- 2 DTOs: pagamento_dto.py, endereco_dto.py
- 3 Routes: admin_pagamentos_routes.py, aluno_pagamentos_routes.py, perfil_routes.py (modificado)

---

## 8. GUIA DE IMPLEMENTAÇÃO - FUNCIONALIDADES ADICIONAIS

### 8.1 Sistema de Notificações

#### **Arquivo:** `model/notificacao_model.py` (CRIAR)

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Notificacao:
    id_notificacao: int
    id_usuario: int
    titulo: str
    mensagem: str
    lida: bool
    data_criacao: datetime
```

#### **Arquivo:** `sql/notificacao_sql.py`, `repo/notificacao_repo.py` (CRIAR)

#### **Arquivo:** `util/notificacao_service.py` (CRIAR)

```python
from repo import notificacao_repo
from util.email_service import email_service

def enviar_notificacao(id_usuario: int, titulo: str, mensagem: str, enviar_email: bool = True):
    """Cria notificação e opcionalmente envia email"""
    # Salvar no banco
    notificacao = Notificacao(...)
    notificacao_repo.inserir(notificacao)

    # Enviar email se solicitado
    if enviar_email:
        usuario = usuario_repo.obter_por_id(id_usuario)
        if usuario:
            email_service.enviar_email(
                destinatario=usuario.email,
                assunto=titulo,
                corpo=mensagem
            )
```

**Uso:** Chamar ao criar matrícula, cancelar aula, etc.

### 8.2 Sistema de Avaliação Física

#### **Arquivo:** `model/avaliacao_model.py` (CRIAR)

```python
@dataclass
class AvaliacaoFisica:
    id_avaliacao: int
    id_aluno: int
    id_professor: int
    data_avaliacao: datetime
    peso: float
    altura: float
    imc: float
    percentual_gordura: float
    observacoes: str
    status: str  # 'solicitada', 'realizada'
```

#### **Arquivo:** `sql/avaliacao_sql.py`, `repo/avaliacao_repo.py`, `dtos/avaliacao_dto.py` (CRIAR)

#### **Arquivo:** `routes/aluno_avaliacoes_routes.py` (CRIAR)

```python
@router.post("/solicitar")
@requer_aluno
async def solicitar_avaliacao(request: Request):
    """Aluno solicita avaliação física"""
    usuario_logado = request.session.get("usuario_logado")

    avaliacao = AvaliacaoFisica(
        id_avaliacao=0,
        id_aluno=usuario_logado["id"],
        id_professor=0,  # Será atribuído depois
        status="solicitada",
        ...
    )

    avaliacao_repo.inserir(avaliacao)
    informar_sucesso(request, "Avaliação solicitada com sucesso!")
    return RedirectResponse("/aluno/avaliacoes", status_code=status.HTTP_303_SEE_OTHER)
```

#### **Arquivo:** `routes/professor_avaliacoes_routes.py` (CRIAR)

Endpoints para professor visualizar solicitações e registrar avaliações.

### 8.3 Sistema de Registro de Presença

#### **Arquivo:** `model/presenca_model.py` (CRIAR)

```python
@dataclass
class Presenca:
    id_presenca: int
    id_matricula: int
    data_aula: datetime
    presente: bool
```

#### **Arquivo:** `sql/presenca_sql.py`, `repo/presenca_repo.py` (CRIAR)

#### **Integrar em:** `routes/professor_turmas_routes.py`

```python
@router.get("/{id_turma}/presenca")
@requer_professor
async def registrar_presenca(request: Request, id_turma: int):
    """Formulário de registro de presença"""
    matriculas = matricula_repo.obter_por_turma(id_turma)
    return templates.TemplateResponse("presenca.html", {
        "request": request,
        "matriculas": matriculas,
        "data_aula": datetime.now().date()
    })

@router.post("/{id_turma}/presenca")
@requer_professor
async def salvar_presenca(request: Request, id_turma: int):
    """Salva presenças marcadas"""
    form = await request.form()

    for id_matricula, presente in form.items():
        if id_matricula.startswith("presenca_"):
            id_mat = int(id_matricula.split("_")[1])
            presenca = Presenca(
                id_presenca=0,
                id_matricula=id_mat,
                data_aula=datetime.now(),
                presente=(presente == "on")
            )
            presenca_repo.inserir(presenca)

    informar_sucesso(request, "Presenças registradas!")
    return RedirectResponse(f"/professor/turmas/{id_turma}", status_code=status.HTTP_303_SEE_OTHER)
```

### 8.4 Sistema de Relatórios

#### **Arquivo:** `routes/admin_relatorios_routes.py` (CRIAR)

```python
@router.get("/dashboard")
@requer_admin
async def dashboard(request: Request):
    """Dashboard com métricas gerais"""

    # Estatísticas
    total_alunos = usuario_repo.obter_quantidade_por_perfil(Perfil.ALUNO.value)
    total_professores = usuario_repo.obter_quantidade_por_perfil(Perfil.PROFESSOR.value)
    total_turmas = turma_repo.obter_quantidade()
    total_matriculas = matricula_repo.obter_quantidade()
    total_atividades = atividade_repo.obter_quantidade()

    # Relatórios
    matriculas_mes = matricula_repo.obter_por_mes(datetime.now().month)
    turmas_ocupacao = turma_repo.obter_taxa_ocupacao()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_alunos": total_alunos,
        "total_professores": total_professores,
        "total_turmas": total_turmas,
        "total_matriculas": total_matriculas,
        "total_atividades": total_atividades,
        "matriculas_mes": matriculas_mes,
        "turmas_ocupacao": turmas_ocupacao
    })
```

Adicionar métodos específicos nos repositories para queries agregadas.

### 8.5 Resumo - Funcionalidades Adicionais

**Arquivos:**
- 3 Models: notificacao_model.py, avaliacao_model.py, presenca_model.py
- 3 SQL: notificacao_sql.py, avaliacao_sql.py, presenca_sql.py
- 3 Repositories: notificacao_repo.py, avaliacao_repo.py, presenca_repo.py
- 2 DTOs: avaliacao_dto.py, presenca_dto.py
- 1 Service: notificacao_service.py
- 3 Routes: aluno_avaliacoes_routes.py, professor_avaliacoes_routes.py, admin_relatorios_routes.py
- Modificações em: professor_turmas_routes.py

---

## 9. CONSIDERAÇÕES FINAIS

### 9.1 Ordem de Implementação Recomendada

**FASE 1 - Fundação (CRÍTICO)**
1. ✅ Migrar perfis (util/migrar_perfis.py)
2. ✅ Atualizar util/perfis.py
3. ✅ Atualizar decoradores e validações
4. ✅ Atualizar seeds

**FASE 2 - Core do Sistema**
5. ✅ Implementar Categorias completo (SQL → Repo → DTO → Routes)
6. ✅ Implementar Atividades completo
7. ✅ Corrigir e implementar Turmas completo
8. ✅ Implementar Matrículas completo

**FASE 3 - Financeiro e Dados**
9. ✅ Corrigir e implementar Pagamentos
10. ✅ Implementar Endereços

**FASE 4 - Recursos Avançados**
11. ✅ Implementar Notificações
12. ✅ Implementar Avaliações Físicas
13. ✅ Implementar Presenças
14. ✅ Implementar Relatórios

**FASE 5 - Integração Final**
15. ✅ Atualizar main.py com todos os imports
16. ✅ Criar seeds para categorias padrão
17. ✅ Testar fluxos completos
18. ✅ Remover/adaptar sistema de tarefas antigo

### 9.2 Checklist de Validação

#### **Categorias e Atividades**
- [ ] Admin pode criar, editar e excluir categorias
- [ ] Admin pode criar, editar e excluir atividades
- [ ] Professor pode visualizar atividades
- [ ] Aluno pode visualizar atividades e detalhes

#### **Turmas e Matrículas**
- [ ] Professor pode criar suas turmas
- [ ] Admin pode gerenciar todas as turmas
- [ ] Aluno pode se matricular em turmas
- [ ] Aluno pode cancelar matrícula
- [ ] Sistema impede matrícula duplicada

#### **Pagamentos e Endereços**
- [ ] Admin pode registrar pagamentos
- [ ] Aluno pode visualizar seus pagamentos
- [ ] Usuário pode gerenciar seus endereços
- [ ] Validações de CEP e UF funcionam

#### **Funcionalidades Adicionais**
- [ ] Notificações são enviadas nas ações relevantes
- [ ] Aluno pode solicitar avaliação física
- [ ] Professor pode registrar avaliações
- [ ] Professor pode registrar presenças
- [ ] Dashboard exibe métricas corretas

#### **Integrações**
- [ ] Todas as tabelas são criadas no startup
- [ ] Seeds funcionam corretamente
- [ ] Decoradores de autorização funcionam
- [ ] Email service integrado

### 9.3 Estatísticas Finais

| Item | Quantidade |
|------|------------|
| **Models corrigidos** | 2 (Turma, Pagamento) |
| **Models novos** | 3 (Notificacao, Avaliacao, Presenca) |
| **Arquivos SQL** | 10 |
| **Repositories** | 10 |
| **DTOs** | 10 |
| **Routes Admin** | 7 |
| **Routes Professor** | 3 |
| **Routes Aluno** | 4 |
| **Services** | 1 (notificacao_service) |
| **Migrations** | 1 (migrar_perfis) |
| **TOTAL ESTIMADO** | **~45-50 arquivos** |

### 9.4 Comandos Úteis

```bash
# Verificar estrutura de tabelas
sqlite3 bd.db ".schema"

# Contar registros por tabela
sqlite3 bd.db "SELECT
    (SELECT COUNT(*) FROM usuario) as usuarios,
    (SELECT COUNT(*) FROM categoria) as categorias,
    (SELECT COUNT(*) FROM atividade) as atividades,
    (SELECT COUNT(*) FROM turma) as turmas,
    (SELECT COUNT(*) FROM matricula) as matriculas"

# Rodar servidor
python main.py

# Executar migração de perfis
python -m util.migrar_perfis
```

### 9.5 Próximos Passos Após Implementação do Backend

1. **Templates HTML** - Criar interfaces para todos os endpoints
2. **Testes Automatizados** - Expandir cobertura de testes
3. **Documentação** - Documentar APIs com Swagger/OpenAPI
4. **Deploy** - Configurar ambiente de produção
5. **Monitoramento** - Implementar logs e métricas

### 9.6 Recursos Adicionais

**Padrões do Projeto:**
- Models: `model/[entidade]_model.py`
- SQL: `sql/[entidade]_sql.py`
- Repository: `repo/[entidade]_repo.py`
- DTO: `dtos/[entidade]_dto.py`
- Routes: `routes/[perfil]_[entidade]_routes.py`

**Convenções:**
- PK sempre `id_[entidade]`
- FK sempre `id_[entidade_referenciada]`
- Decoradores: `@requer_admin`, `@requer_professor`, `@requer_aluno`
- Flash messages: `informar_sucesso()`, `informar_erro()`
- Redirect após POST: `status_code=status.HTTP_303_SEE_OTHER`

---

## FIM DO DOCUMENTO

**Este guia fornece:**
- ✅ Análise completa do estado atual vs requisitos
- ✅ Identificação de 45-50 arquivos a criar/modificar
- ✅ Exemplos de código para todos os componentes principais
- ✅ Ordem de implementação recomendada
- ✅ Checklist de validação completo
- ✅ Padrões e convenções do projeto

**Total de linhas:** ~2500
**Complexidade:** Média-Alta
**Tempo estimado:** 40-60 horas de desenvolvimento

**Boa implementação! 🚀**
