# Melhores Práticas de Desenvolvimento - AgendaFit

**Data:** 2025-10-28
**Versão:** 1.0
**Objetivo:** Guia de boas práticas para manter código de qualidade

---

## ÍNDICE

1. [Nomenclatura](#1-nomenclatura)
2. [Estrutura de Código](#2-estrutura-de-código)
3. [Documentação](#3-documentação)
4. [Segurança](#4-segurança)
5. [Performance](#5-performance)
6. [Testes](#6-testes)
7. [Git e Controle de Versão](#7-git-e-controle-de-versão)
8. [Code Review](#8-code-review)

---

## 1. NOMENCLATURA

### 1.1 Arquivos e Módulos

✅ **FAÇA:**
```python
# Arquivos em snake_case
categoria_sql.py
categoria_model.py
categoria_repo.py
admin_categorias_routes.py
```

❌ **NÃO FAÇA:**
```python
# Evite CamelCase ou espaços em arquivos
CategoriaSql.py
categoria-sql.py
Categoria SQL.py
```

### 1.2 Classes

✅ **FAÇA:**
```python
# Classes em PascalCase
class Categoria:
    pass

class CriarCategoriaDTO:
    pass

class StatusChamado(Enum):
    pass
```

### 1.3 Funções e Variáveis

✅ **FAÇA:**
```python
# Funções e variáveis em snake_case
def obter_por_id(id: int):
    pass

def _row_to_categoria(row):  # Privadas com _
    pass

usuario_logado = get_usuario()
data_cadastro = datetime.now()
```

❌ **NÃO FAÇA:**
```python
# Evite camelCase para funções/variáveis
def obterPorId(id):
    pass

usuarioLogado = get_usuario()
```

### 1.4 Constantes

✅ **FAÇA:**
```python
# Constantes em UPPER_SNAKE_CASE
MAX_TENTATIVAS_LOGIN = 5
TEMPO_SESSAO_MINUTOS = 30

# Queries SQL como constantes
CRIAR_TABELA = """..."""
INSERIR = """..."""
```

### 1.5 Campos de Banco de Dados

✅ **FAÇA:**
```python
# IDs simples (padrão atual)
id INTEGER PRIMARY KEY
id_categoria INTEGER NOT NULL  # FK

# Timestamps padronizados
data_cadastro DATETIME
data_atualizacao DATETIME
data_conclusao DATETIME  # Específicos OK
```

❌ **NÃO FAÇA:**
```python
# Evite IDs prefixados (padrão antigo)
id_atividade INTEGER PRIMARY KEY  # Use apenas 'id'

# Evite inconsistência de nomenclatura
data_criacao  # Use data_cadastro
data_abertura  # Use data_cadastro
```

---

## 2. ESTRUTURA DE CÓDIGO

### 2.1 Organização de Imports

✅ **FAÇA:**
```python
# 1. Bibliotecas padrão Python
from datetime import datetime
from typing import Optional

# 2. Bibliotecas de terceiros
from fastapi import APIRouter, Request
from pydantic import BaseModel

# 3. Imports locais
from model.categoria_model import Categoria
from sql.categoria_sql import *
from util.db_util import get_connection
```

### 2.2 Ordem dos Elementos em Arquivos

✅ **FAÇA:**
```python
"""Docstring do módulo."""

# Imports

# Constantes globais
CONSTANTE = "valor"

# Funções/classes privadas (com _)
def _funcao_privada():
    pass

# Funções/classes públicas
def funcao_publica():
    pass

class MinhaClasse:
    pass
```

### 2.3 Tamanho de Funções

✅ **FAÇA:**
- Funções com 20-50 linhas idealmente
- Máximo de 100 linhas
- Se maior, refatore em funções menores

❌ **NÃO FAÇA:**
- Funções com 200+ linhas
- God functions que fazem tudo

### 2.4 Responsabilidade Única

✅ **FAÇA:**
```python
# Cada função faz UMA coisa bem feita
def obter_por_id(id: int) -> Optional[Categoria]:
    """Obtém categoria por ID."""
    # Apenas busca e retorna
    ...

def validar_categoria(categoria: Categoria) -> bool:
    """Valida dados da categoria."""
    # Apenas valida
    ...
```

❌ **NÃO FAÇA:**
```python
def obter_e_validar_e_salvar_categoria(id: int):
    """Faz tudo!"""
    # Busca, valida, salva, envia email, faz café...
    # MUITO ACOPLADO!
    ...
```

---

## 3. DOCUMENTAÇÃO

### 3.1 Docstrings de Módulo

✅ **SEMPRE inclua** no início de cada arquivo:
```python
"""
Descrição breve do módulo.

Descrição mais detalhada se necessário. Explique:
- Propósito do módulo
- Padrões utilizados
- Dependências importantes
- Exemplos de uso

Exemplo:
    >>> from repo import categoria_repo
    >>> categoria = categoria_repo.obter_por_id(1)
"""
```

### 3.2 Docstrings de Funções

✅ **SEMPRE inclua** em funções públicas:
```python
def obter_por_id(id: int) -> Optional[Categoria]:
    """
    Obtém uma categoria pelo seu ID.

    Args:
        id: Identificador único da categoria

    Returns:
        Objeto Categoria se encontrado, None caso contrário

    Raises:
        ValueError: Se id for negativo (se aplicável)

    Example:
        >>> categoria = obter_por_id(5)
        >>> print(categoria.nome)
    """
```

### 3.3 Comentários Inline

✅ **FAÇA:**
```python
# Explique o POR QUÊ, não o QUE
# Corrige bug #123: usuário pode ter múltiplos endereços
if len(enderecos) > 1:
    endereco = enderecos[0]  # Usa o primeiro como padrão
```

❌ **NÃO FAÇA:**
```python
# Comentários óbvios
# Incrementa i
i += 1

# Verifica se nome é vazio
if nome == "":
    pass
```

### 3.4 Type Hints

✅ **SEMPRE use** type hints:
```python
from typing import Optional

def obter_por_id(id: int) -> Optional[Categoria]:
    pass

def obter_todos() -> list[Categoria]:
    pass

def alterar(categoria: Categoria) -> bool:
    pass
```

❌ **NÃO FAÇA:**
```python
# Sem type hints
def obter_por_id(id):  # id é int? str?
    pass

def obter_todos():  # Retorna o quê?
    pass
```

---

## 4. SEGURANÇA

### 4.1 SQL Injection

✅ **SEMPRE use** queries parametrizadas:
```python
# ✅ CORRETO - Parametrizado
cursor.execute("SELECT * FROM usuario WHERE id = ?", (id,))
cursor.execute("INSERT INTO categoria (nome) VALUES (?)", (nome,))
```

❌ **NUNCA faça** concatenação:
```python
# ❌ VULNERÁVEL - SQL Injection!
cursor.execute(f"SELECT * FROM usuario WHERE id = {id}")
cursor.execute("INSERT INTO categoria (nome) VALUES ('" + nome + "')")
```

### 4.2 Autenticação e Autorização

✅ **SEMPRE proteja** rotas administrativas:
```python
@router.post("/admin/categorias/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])  # ✅ Obrigatório!
async def post_cadastrar(...):
    pass
```

❌ **NUNCA exponha** endpoints sem proteção:
```python
@router.post("/admin/categorias/cadastrar")
# ❌ SEM AUTENTICAÇÃO!
async def post_cadastrar(...):
    pass
```

### 4.3 Senhas

✅ **SEMPRE use** hash:
```python
from util.auth_utils import criar_hash_senha

# ✅ Hash antes de salvar
usuario.senha = criar_hash_senha(senha_plain)
inserir(usuario)
```

❌ **NUNCA salve** senhas em plain text:
```python
# ❌ INSEGURO!
usuario.senha = senha_plain
inserir(usuario)
```

### 4.4 Rate Limiting

✅ **SEMPRE aplique** em rotas de mutação:
```python
limiter = RateLimiter(max_tentativas=10, janela_minutos=1)

@router.post("/cadastrar")
@requer_autenticacao([Perfil.ADMIN.value])
async def post_cadastrar(...):
    # ✅ Rate limiting previne abuso
    pass
```

### 4.5 Validação de Entrada

✅ **SEMPRE valide** com DTOs:
```python
@router.post("/cadastrar")
async def post_cadastrar(nome: str = Form(...), ...):
    try:
        # ✅ Valida ANTES de usar
        dto = CriarCategoriaDTO(nome=nome, ...)
        # Agora é seguro usar
    except FormValidationError as e:
        # Trata erro de validação
        pass
```

❌ **NUNCA confie** em dados do usuário:
```python
@router.post("/cadastrar")
async def post_cadastrar(nome: str = Form(...)):
    # ❌ Usa direto sem validar!
    categoria = Categoria(nome=nome)
    inserir(categoria)
```

---

## 5. PERFORMANCE

### 5.1 Queries de Banco

✅ **FAÇA:**
```python
# Busque apenas o necessário
SELECT id, nome, email FROM usuario WHERE id = ?

# Use JOIN quando precisar de dados relacionados
SELECT a.*, c.nome as categoria_nome
FROM atividade a
JOIN categoria c ON a.id_categoria = c.id
```

❌ **NÃO FAÇA:**
```python
# Evite SELECT *
SELECT * FROM usuario

# Evite N+1 queries (buscar em loop)
for atividade in atividades:
    # ❌ Query dentro do loop!
    categoria = obter_categoria(atividade.id_categoria)
```

### 5.2 Context Managers

✅ **SEMPRE use** context managers:
```python
# ✅ Fecha conexão automaticamente
with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute(query)
    # Conexão fechada ao sair do bloco
```

❌ **NÃO FAÇA:**
```python
# ❌ Risco de vazamento de conexão
conn = get_connection()
cursor = conn.cursor()
cursor.execute(query)
# Esqueceu de fechar!
```

### 5.3 Caching

✅ **USE quando** apropriado:
```python
# Cache de configurações que mudam raramente
from functools import lru_cache

@lru_cache(maxsize=128)
def obter_configuracao(chave: str) -> str:
    # Busca uma vez, cacheia
    return obter_por_chave(chave)
```

---

## 6. TESTES

### 6.1 Cobertura

✅ **OBJETIVO:** 80%+ de cobertura

**Priorize testar:**
1. Repositórios (CRUD)
2. Validadores (DTOs)
3. Lógica de negócio complexa
4. Rotas críticas

### 6.2 Estrutura de Testes

✅ **FAÇA:**
```python
# tests/repo/test_categoria_repo.py
def test_inserir_categoria():
    """Testa inserção de categoria válida."""
    # Arrange
    categoria = Categoria(id=0, nome="Teste", ...)

    # Act
    id_inserido = inserir(categoria)

    # Assert
    assert id_inserido is not None
    assert id_inserido > 0

def test_inserir_categoria_duplicada():
    """Testa que não permite nome duplicado."""
    # ...
```

### 6.3 Testes Unitários vs Integração

✅ **Testes Unitários:**
- Testam função isolada
- Mock de dependências
- Rápidos

✅ **Testes de Integração:**
- Testam fluxo completo
- Banco de teste real
- Mais lentos mas mais confiáveis

---

## 7. GIT E CONTROLE DE VERSÃO

### 7.1 Commits

✅ **FAÇA mensagens descritivas:**
```bash
# ✅ Boas mensagens
git commit -m "feat: adiciona campo data_atualizacao em Categoria"
git commit -m "fix: corrige validação de email em CriarAlunoDTO"
git commit -m "refactor: extrai função _row_to_categoria para reutilização"
git commit -m "docs: adiciona docstrings em categoria_repo"
```

❌ **NÃO FAÇA:**
```bash
# ❌ Mensagens vagas
git commit -m "atualização"
git commit -m "fix"
git commit -m "mudanças"
```

### 7.2 Convenção de Commits

Use prefixos:
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `refactor:` Refatoração (sem mudar comportamento)
- `docs:` Documentação
- `test:` Testes
- `style:` Formatação (sem mudar lógica)
- `chore:` Tarefas de build/configuração

### 7.3 Branches

✅ **FAÇA:**
```bash
# Branches descritivas
git checkout -b feature/adicionar-campo-data-atualizacao
git checkout -b fix/corrigir-validacao-email
git checkout -b docs/adicionar-docstrings-repos
```

### 7.4 Pull Requests

✅ **Antes de criar PR:**
- [ ] Código testado localmente
- [ ] Testes passando
- [ ] Sem warnings
- [ ] Documentação atualizada
- [ ] Code review próprio feito

---

## 8. CODE REVIEW

### 8.1 Como Autor

✅ **FAÇA:**
- Descreva o que mudou e por quê
- Referencie issues relacionadas
- Adicione screenshots se for UI
- Peça review específico ("Por favor revise a lógica de validação")

### 8.2 Como Revisor

✅ **VERIFIQUE:**
- [ ] Código segue padrões da aplicação
- [ ] Nomenclatura consistente
- [ ] Docstrings presentes
- [ ] Type hints corretos
- [ ] Sem código duplicado
- [ ] Segurança (SQL injection, validação, autenticação)
- [ ] Performance (queries eficientes, sem N+1)
- [ ] Testes incluídos
- [ ] Sem código comentado/debug

✅ **SEJA CONSTRUTIVO:**
```
# ✅ Feedback construtivo
"Considere extrair esta lógica para uma função separada
para melhor testabilidade."

"Sugiro adicionar validação de tamanho mínimo aqui
para prevenir strings vazias."
```

❌ **EVITE:**
```
# ❌ Feedback não construtivo
"Isso está errado."
"Código ruim."
```

---

## 9. CHECKLIST GERAL DE QUALIDADE

Antes de considerar uma tarefa completa:

### Funcionalidade
- [ ] Funciona conforme especificado
- [ ] Edge cases tratados
- [ ] Erros tratados apropriadamente

### Código
- [ ] Segue padrões de nomenclatura
- [ ] Sem código duplicado
- [ ] Funções com responsabilidade única
- [ ] Sem magic numbers (use constantes)

### Documentação
- [ ] Docstrings em módulos e funções públicas
- [ ] Type hints em todas as funções
- [ ] Comentários explicando "por quê" (não "o quê")
- [ ] README atualizado se necessário

### Segurança
- [ ] Queries parametrizadas
- [ ] Validação de entrada
- [ ] Autenticação em rotas protegidas
- [ ] Rate limiting aplicado
- [ ] Senhas com hash

### Performance
- [ ] Queries eficientes
- [ ] Sem N+1
- [ ] Context managers usados
- [ ] Cache quando apropriado

### Testes
- [ ] Testes unitários escritos
- [ ] Testes passando
- [ ] Cobertura adequada (80%+)

### Git
- [ ] Commits com mensagens descritivas
- [ ] Branch nomeada adequadamente
- [ ] PR com descrição clara

---

## 10. RECURSOS E REFERÊNCIAS

### Documentação do Projeto
- `docs/PADROES_ARQUITETURAIS.md` - Padrões de design
- `docs/CHECKLIST_CONFORMIDADE.md` - Checklist para novos CRUDs
- `docs/PARECER.md` - Análise técnica completa
- `docs/MUDANCAS_IMPLEMENTADAS.md` - Histórico de mudanças

### Exemplos de Referência
- **CRUD Completo:** `sql/categoria_sql.py`, `model/categoria_model.py`, etc.
- **Facade Pattern:** `dtos/aluno_dto.py`
- **Child Entity:** `model/chamado_interacao_model.py`
- **Subsistema Coeso:** `dtos/chat_dto.py`

### Ferramentas Úteis
- **Formatação:** `black` ou `autopep8`
- **Linting:** `pylint` ou `flake8`
- **Type checking:** `mypy`
- **Testes:** `pytest`
- **Cobertura:** `pytest-cov`

---

## CONCLUSÃO

Seguir estas melhores práticas garante:
- ✅ Código mais legível e manutenível
- ✅ Menos bugs e vulnerabilidades
- ✅ Melhor colaboração em equipe
- ✅ Facilita onboarding de novos desenvolvedores
- ✅ Reduz débito técnico

**Lembre-se:** Código é lido muito mais vezes do que é escrito. Invista tempo em fazer código de qualidade!

---

**Documento criado em:** 2025-10-28
**Última atualização:** 2025-10-28
**Próxima revisão:** Conforme evolução do projeto
