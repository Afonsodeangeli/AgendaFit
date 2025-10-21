# 📘 GUIA COMPLETO DE IMPLEMENTAÇÃO - AGENDAFIT

> Guia didático passo a passo para transformar o DefaultWebApp no AgendaFit
> Sistema de Gestão Inteligente de Treinos para Academias

**Versão:** 2.0 - Completa e Detalhada
**Data:** 20 de outubro de 2025
**Tempo Estimado Total:** 18 semanas (~350 horas)
**Projeto Integrador** - IFES Campus Cachoeiro de Itapemirim

---

## 📑 ÍNDICE GERAL

### **[FASE 1: ADAPTAÇÕES BASE](#fase-1-adaptações-base)** (20h - 1 semana)
- 1.1 Atualizar Sistema de Perfis
- 1.2 Expandir Modelo Usuario
- 1.3 Atualizar SQL e Repositório
- 1.4 Atualizar DTOs e Validações
- 1.5 Atualizar Seeds e Templates
- 1.6 Remover Entidade Tarefa
- 1.7 Testes da Fase 1

### **[FASE 2: INFRAESTRUTURA DE DADOS](#fase-2-infraestrutura-de-dados)** (40h - 2 semanas)
- 2.1 Repositório de Categoria
- 2.2 Repositório de Atividade
- 2.3 Repositório de Turma
- 2.4 Repositório de Matrícula
- 2.5 Repositório de Pagamento
- 2.6 Repositório de Endereço
- 2.7 **NOVO:** Repositório de Presença
- 2.8 **NOVO:** Repositório de Avaliação Física
- 2.9 DTOs Completos
- 2.10 Seeds de Dados
- 2.11 Testes da Fase 2

### **[FASE 3: CRUDS ADMINISTRATIVOS](#fase-3-cruds-administrativos)** (60h - 3 semanas)
- 3.1 CRUD Completo de Categorias
- 3.2 CRUD Completo de Atividades
- 3.3 CRUD Completo de Turmas
- 3.4 Dashboard Administrativo
- 3.5 Testes da Fase 3

### **[FASE 4: ÁREA DO ALUNO](#fase-4-área-do-aluno)** (60h - 3 semanas)
- 4.1 Dashboard do Aluno
- 4.2 Explorar Atividades Disponíveis
- 4.3 Sistema de Matrícula
- 4.4 Cancelamento de Matrícula
- 4.5 Visualizar Avaliações Físicas
- 4.6 Relatórios de Participação
- 4.7 Meus Pagamentos
- 4.8 Testes da Fase 4

### **[FASE 5: ÁREA DO PROFESSOR](#fase-5-área-do-professor)** (50h - 2,5 semanas)
- 5.1 Dashboard do Professor
- 5.2 Gestão de Turmas
- 5.3 Sistema de Presença
- 5.4 CRUD de Avaliações Físicas
- 5.5 Visualização de Alunos
- 5.6 Testes da Fase 5

### **[FASE 6: SISTEMAS AVANÇADOS](#fase-6-sistemas-avançados)** (60h - 3 semanas)
- 6.1 Calendário Visual de Aulas
- 6.2 Sistema de Notificações
- 6.3 Relatórios e Estatísticas
- 6.4 Sistema de Pagamentos Completo
- 6.5 Testes da Fase 6

### **[FASE 7: TESTES E REFINAMENTOS](#fase-7-testes-e-refinamentos)** (40h - 2 semanas)
- 7.1 Testes Unitários
- 7.2 Testes de Integração
- 7.3 Testes E2E
- 7.4 Ajustes de UI/UX
- 7.5 Performance

### **[FASE 8: DOCUMENTAÇÃO](#fase-8-documentação)** (20h - 1 semana)
- 8.1 Documentação Técnica
- 8.2 Manual do Usuário
- 8.3 Guia de Instalação
- 8.4 Documentação de API

### **[APÊNDICES](#apêndices)**
- A. JavaScript e AJAX
- B. CSS Customizado
- C. Boas Práticas
- D. Troubleshooting Completo
- E. Diagramas de Fluxo

---

## 🎯 COMO USAR ESTE GUIA

### ✅ Antes de Começar

- [ ] Python 3.10+ instalado
- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Aplicação rodando sem erros
- [ ] Leu `docs/ANALISE_INICIAL.md`
- [ ] Git configurado

### 📚 Estrutura do Guia

Cada seção contém:
- **📝 Objetivo**: O que você vai implementar
- **📍 Localização**: Onde criar/modificar arquivos
- **💻 Código Completo**: Todo o código necessário
- **✅ Checklist**: Itens para validar
- **🧪 Testes**: Como testar

### 🔄 Fluxo de Trabalho Recomendado

1. Leia a seção completa antes de começar
2. Siga os passos na ordem
3. Teste cada etapa
4. Marque os checkboxes
5. Commit no Git
6. Avance para próxima seção

---

# FASE 1: ADAPTAÇÕES BASE

**Duração:** 20 horas (1 semana)
**Objetivo:** Preparar a base do projeto para o domínio de academias

---

## 1.1 Atualizar Sistema de Perfis

### 📝 Objetivo
Alterar os perfis de usuário de `CLIENTE/VENDEDOR` para `ALUNO/PROFESSOR` conforme especificação do AgendaFit.

### 📍 Arquivo a Modificar
`util/perfis.py`

### 💻 Código Completo

```python
# util/perfis.py
from enum import Enum
from typing import Optional

class Perfil(str, Enum):
    """
    Enum centralizado para perfis de usuário do AgendaFit.

    Este é a FONTE ÚNICA DA VERDADE para perfis no sistema.
    SEMPRE use este Enum ao referenciar perfis, NUNCA strings literais.

    Perfis disponíveis:
    - ADMIN: Administrador do sistema (gestão completa)
    - ALUNO: Aluno da academia (visualiza, matricula, cancela)
    - PROFESSOR: Professor/Instrutor (gerencia turmas, presenças, avaliações)

    Exemplos:
        - Correto: perfil = Perfil.ADMIN.value
        - Correto: perfil = Perfil.ALUNO.value
        - Correto: perfil = Perfil.PROFESSOR.value
        - ERRADO: perfil = "Aluno"
        - ERRADO: perfil = "Professor"
    """

    # PERFIS DO AGENDAFIT ####################################
    ADMIN = "Administrador"
    ALUNO = "Aluno"
    PROFESSOR = "Professor"
    # FIM DOS PERFIS #########################################

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

        Examples:
            >>> Perfil.existe("Aluno")
            True
            >>> Perfil.existe("invalido")
            False
        """
        return valor in cls.valores()

    @classmethod
    def from_string(cls, valor: str) -> Optional['Perfil']:
        """
        Converte uma string para o Enum Perfil correspondente.

        Args:
            valor: String do perfil ("Administrador", "Aluno" ou "Professor")

        Returns:
            Enum Perfil correspondente ou None se inválido

        Examples:
            >>> Perfil.from_string("Aluno")
            <Perfil.ALUNO: 'Aluno'>
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

        Examples:
            >>> Perfil.validar("Aluno")
            'Aluno'
            >>> Perfil.validar("invalido")
            ValueError: Perfil inválido: invalido...
        """
        if not cls.existe(valor):
            raise ValueError(f'Perfil inválido: {valor}. Use: {", ".join(cls.valores())}')
        return valor

    @classmethod
    def eh_aluno(cls, perfil: str) -> bool:
        """Verifica se o perfil é ALUNO"""
        return perfil == cls.ALUNO.value

    @classmethod
    def eh_professor(cls, perfil: str) -> bool:
        """Verifica se o perfil é PROFESSOR"""
        return perfil == cls.PROFESSOR.value

    @classmethod
    def eh_admin(cls, perfil: str) -> bool:
        """Verifica se o perfil é ADMIN"""
        return perfil == cls.ADMIN.value
```

### ✅ Checklist

- [ ] Arquivo `util/perfis.py` modificado
- [ ] Perfis alterados: `ALUNO` e `PROFESSOR`
- [ ] Métodos auxiliares adicionados (`eh_aluno`, etc)
- [ ] Documentação atualizada
- [ ] **Commit:** `refactor(perfis): alterar perfis para Aluno e Professor`

---

## 1.2 Expandir Modelo Usuario

### 📝 Objetivo
Adicionar campos necessários ao modelo Usuario conforme diagrama de classes do PDF.

### 📍 Arquivo a Modificar
`model/usuario_model.py`

### 💻 Código Completo

```python
# model/usuario_model.py
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Usuario:
    """
    Model de usuário do sistema AgendaFit.

    Attributes:
        id: Identificador único do usuário
        nome: Nome completo do usuário
        email: E-mail único do usuário (usado para login)
        senha: Hash da senha do usuário (bcrypt)
        perfil: Perfil do usuário ("Administrador", "Aluno" ou "Professor")
        data_nascimento: Data de nascimento do usuário
        numero_documento: CPF do usuário (máscara: 000.000.000-00)
        telefone: Telefone de contato (máscara: (00) 00000-0000)
        confirmado: Indica se a conta foi confirmada por email
        token_redefinicao: Token para redefinição de senha (opcional)
        data_token: Data de expiração do token (opcional)
        data_cadastro: Data de cadastro do usuário (opcional, gerado automaticamente)

    Nota:
        - A foto do usuário é armazenada no filesystem em /static/img/usuarios/{id:06d}.jpg
        - Use util.foto_util para manipular fotos de usuários
        - numero_documento é opcional (permite cadastro sem CPF)
        - confirmado=False até que usuário confirme email (futuro)
    """
    id: int
    nome: str
    email: str
    senha: str
    perfil: str
    data_nascimento: Optional[date] = None
    numero_documento: Optional[str] = None
    telefone: Optional[str] = None
    confirmado: bool = False
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None
    data_cadastro: Optional[str] = None

    def __repr__(self) -> str:
        """Representação string do usuário (sem mostrar senha)"""
        return f"Usuario(id={self.id}, nome='{self.nome}', email='{self.email}', perfil='{self.perfil}')"

    @property
    def nome_primeiro(self) -> str:
        """Retorna o primeiro nome do usuário"""
        return self.nome.split()[0] if self.nome else ""

    @property
    def idade(self) -> Optional[int]:
        """Calcula a idade do usuário baseado na data de nascimento"""
        if not self.data_nascimento:
            return None
        from datetime import date as dt
        hoje = dt.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
```

### ✅ Checklist

- [ ] Arquivo `model/usuario_model.py` modificado
- [ ] Campos novos adicionados (data_nascimento, numero_documento, telefone, confirmado)
- [ ] Imports necessários adicionados (`from datetime import date`)
- [ ] Métodos auxiliares implementados (`nome_primeiro`, `idade`)
- [ ] Documentação completa
- [ ] **Commit:** `feat(usuario): adicionar campos ao modelo Usuario`

---

## 1.3 Atualizar SQL e Repositório do Usuario

### 📝 Objetivo
Atualizar scripts SQL e funções do repositório para trabalhar com os novos campos.

### 📍 Arquivo 1: SQL
`sql/usuario_sql.py`

### 💻 Código Completo

```python
# sql/usuario_sql.py
"""
Scripts SQL para a tabela usuario.

Contém todas as queries SQL utilizadas pelo repositório de usuários.
"""

SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        perfil TEXT NOT NULL,
        data_nascimento TEXT,
        numero_documento TEXT UNIQUE,
        telefone TEXT,
        confirmado INTEGER DEFAULT 0,
        token_redefinicao TEXT,
        data_token TEXT,
        data_cadastro TEXT DEFAULT (datetime('now','localtime'))
    )
"""

SQL_INSERIR = """
    INSERT INTO usuario
    (nome, email, senha, perfil, data_nascimento, numero_documento, telefone, confirmado)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, email, senha, perfil, data_nascimento, numero_documento,
           telefone, confirmado, token_redefinicao, data_token, data_cadastro
    FROM usuario
    ORDER BY nome
"""

SQL_OBTER_POR_ID = """
    SELECT id, nome, email, senha, perfil, data_nascimento, numero_documento,
           telefone, confirmado, token_redefinicao, data_token, data_cadastro
    FROM usuario
    WHERE id = ?
"""

SQL_OBTER_POR_EMAIL = """
    SELECT id, nome, email, senha, perfil, data_nascimento, numero_documento,
           telefone, confirmado, token_redefinicao, data_token, data_cadastro
    FROM usuario
    WHERE email = ?
"""

SQL_OBTER_POR_TOKEN = """
    SELECT id, nome, email, senha, perfil, data_nascimento, numero_documento,
           telefone, confirmado, token_redefinicao, data_token, data_cadastro
    FROM usuario
    WHERE token_redefinicao = ?
"""

SQL_OBTER_POR_PERFIL = """
    SELECT id, nome, email, senha, perfil, data_nascimento, numero_documento,
           telefone, confirmado, token_redefinicao, data_token, data_cadastro
    FROM usuario
    WHERE perfil = ?
    ORDER BY nome
"""

SQL_ATUALIZAR = """
    UPDATE usuario
    SET nome = ?, email = ?, perfil = ?, data_nascimento = ?,
        numero_documento = ?, telefone = ?
    WHERE id = ?
"""

SQL_ATUALIZAR_SENHA = """
    UPDATE usuario
    SET senha = ?
    WHERE id = ?
"""

SQL_ATUALIZAR_TOKEN = """
    UPDATE usuario
    SET token_redefinicao = ?, data_token = ?
    WHERE id = ?
"""

SQL_CONFIRMAR_CONTA = """
    UPDATE usuario
    SET confirmado = 1
    WHERE id = ?
"""

SQL_EXCLUIR = """
    DELETE FROM usuario
    WHERE id = ?
"""

SQL_CONTAR_POR_PERFIL = """
    SELECT COUNT(*) FROM usuario WHERE perfil = ?
"""

SQL_BUSCAR_POR_NOME = """
    SELECT id, nome, email, senha, perfil, data_nascimento, numero_documento,
           telefone, confirmado, token_redefinicao, data_token, data_cadastro
    FROM usuario
    WHERE nome LIKE ?
    ORDER BY nome
```

### 📍 Arquivo 2: Repositório
`repo/usuario_repo.py`

### 💻 Código Completo (Funções Modificadas/Novas)

```python
# repo/usuario_repo.py
"""
Repositório para gerenciamento de usuários.

Importante: Este arquivo já existe. Você deve MODIFICAR as funções existentes
e ADICIONAR as novas funções indicadas.
"""

import sqlite3
from typing import Optional
from datetime import date, datetime
from model.usuario_model import Usuario
from sql.usuario_sql import *
from util.db_util import obter_conexao, fechar_conexao
from util.logger_config import logger


# ============================================================
# FUNÇÃO EXISTENTE - MODIFICAR
# ============================================================

def inserir(usuario: Usuario) -> Optional[Usuario]:
    """
    Insere um novo usuário no banco de dados.

    Args:
        usuario: Objeto Usuario com os dados a inserir

    Returns:
        Usuario com ID atribuído ou None em caso de erro
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_INSERIR,
            (
                usuario.nome,
                usuario.email,
                usuario.senha,
                usuario.perfil,
                usuario.data_nascimento.isoformat() if usuario.data_nascimento else None,
                usuario.numero_documento,
                usuario.telefone,
                int(usuario.confirmado)  # SQLite usa INTEGER para boolean
            )
        )
        conn.commit()
        usuario.id = cursor.lastrowid
        logger.info(f"Usuário inserido: {usuario.email} (ID: {usuario.id})")
        return usuario
    except sqlite3.IntegrityError as e:
        logger.error(f"Erro de integridade ao inserir usuário: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao inserir usuário: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


# ============================================================
# FUNÇÃO AUXILIAR - ADICIONAR
# ============================================================

def _row_para_usuario(row: tuple) -> Usuario:
    """
    Converte uma row do banco em objeto Usuario.

    Args:
        row: Tupla com os dados do banco (12 campos)

    Returns:
        Objeto Usuario preenchido
    """
    return Usuario(
        id=row[0],
        nome=row[1],
        email=row[2],
        senha=row[3],
        perfil=row[4],
        data_nascimento=date.fromisoformat(row[5]) if row[5] else None,
        numero_documento=row[6],
        telefone=row[7],
        confirmado=bool(row[8]),  # Converter INTEGER para bool
        token_redefinicao=row[9],
        data_token=row[10],
        data_cadastro=row[11]
    )


# ============================================================
# FUNÇÕES EXISTENTES - MODIFICAR (usar _row_para_usuario)
# ============================================================

def obter_por_id(id: int) -> Optional[Usuario]:
    """Busca usuário por ID"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_ID, (id,))
        row = cursor.fetchone()

        if row:
            return _row_para_usuario(row)
        return None
    except Exception as e:
        logger.error(f"Erro ao obter usuário {id}: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def obter_por_email(email: str) -> Optional[Usuario]:
    """Busca usuário por email"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_EMAIL, (email,))
        row = cursor.fetchone()

        if row:
            return _row_para_usuario(row)
        return None
    except Exception as e:
        logger.error(f"Erro ao obter usuário por email: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def obter_todos() -> list[Usuario]:
    """Retorna todos os usuários"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_TODOS)
        rows = cursor.fetchall()

        usuarios = [_row_para_usuario(row) for row in rows]
        logger.info(f"Obtidos {len(usuarios)} usuários")
        return usuarios
    except Exception as e:
        logger.error(f"Erro ao obter usuários: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def atualizar(usuario: Usuario) -> bool:
    """Atualiza os dados de um usuário"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_ATUALIZAR,
            (
                usuario.nome,
                usuario.email,
                usuario.perfil,
                usuario.data_nascimento.isoformat() if usuario.data_nascimento else None,
                usuario.numero_documento,
                usuario.telefone,
                usuario.id
            )
        )
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Usuário {usuario.id} atualizado")
            return True
        return False
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


# ============================================================
# FUNÇÕES NOVAS - ADICIONAR
# ============================================================

def confirmar_conta(id: int) -> bool:
    """
    Marca uma conta de usuário como confirmada.

    Args:
        id: ID do usuário

    Returns:
        True se confirmado com sucesso, False caso contrário
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_CONFIRMAR_CONTA, (id,))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Conta do usuário {id} confirmada")
            return True
        return False
    except Exception as e:
        logger.error(f"Erro ao confirmar conta: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def obter_por_perfil(perfil: str) -> list[Usuario]:
    """
    Retorna todos os usuários de um perfil específico.

    Args:
        perfil: Perfil a buscar ("Aluno", "Professor" ou "Administrador")

    Returns:
        Lista de usuários do perfil
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_PERFIL, (perfil,))
        rows = cursor.fetchall()

        usuarios = [_row_para_usuario(row) for row in rows]
        logger.info(f"Obtidos {len(usuarios)} usuários do perfil {perfil}")
        return usuarios
    except Exception as e:
        logger.error(f"Erro ao obter usuários por perfil: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def contar_por_perfil(perfil: str) -> int:
    """
    Conta quantos usuários existem de um perfil específico.

    Args:
        perfil: Perfil a contar

    Returns:
        Número de usuários do perfil
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_CONTAR_POR_PERFIL, (perfil,))
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        logger.error(f"Erro ao contar usuários: {e}", exc_info=True)
        return 0
    finally:
        fechar_conexao(conn)


def buscar_por_nome(termo: str) -> list[Usuario]:
    """
    Busca usuários cujo nome contenha o termo.

    Args:
        termo: Termo de busca

    Returns:
        Lista de usuários encontrados
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_BUSCAR_POR_NOME, (f"%{termo}%",))
        rows = cursor.fetchall()

        usuarios = [_row_para_usuario(row) for row in rows]
        return usuarios
    except Exception as e:
        logger.error(f"Erro ao buscar usuários: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)
```

### ✅ Checklist

- [ ] Arquivo `sql/usuario_sql.py` atualizado
- [ ] Arquivo `repo/usuario_repo.py` modificado
- [ ] Função `_row_para_usuario()` criada
- [ ] Funções existentes atualizadas (inserir, obter_*, atualizar)
- [ ] Funções novas adicionadas (confirmar_conta, obter_por_perfil, contar_por_perfil, buscar_por_nome)
- [ ] **Commit:** `feat(usuario): atualizar SQL e repositório com novos campos`

---

## 1.4 Atualizar DTOs e Validações

### 📝 Objetivo
Adicionar validações para os novos campos do usuário usando Pydantic.

### 📍 Arquivo a Modificar
`dtos/usuario_dto.py`

### 💻 Código Completo

```python
# dtos/usuario_dto.py
from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional
from dtos.validators import (
    validar_nome_completo,
    validar_senha_forte,
    validar_cpf,
    validar_telefone_celular
)


class UsuarioCadastroDTO(BaseModel):
    """
    DTO para cadastro de novo usuário.

    Valida todos os campos necessários para criar uma conta.
    """
    nome: str
    email: EmailStr
    senha: str
    perfil: str
    data_nascimento: Optional[date] = None
    numero_documento: Optional[str] = None
    telefone: Optional[str] = None

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        """Valida que o nome é completo (nome e sobrenome)"""
        validar_nome_completo(v)
        return v.strip()

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        """Valida que a senha é forte"""
        validar_senha_forte(v)
        return v

    @field_validator('numero_documento')
    @classmethod
    def validar_documento(cls, v: Optional[str]) -> Optional[str]:
        """Valida CPF se fornecido"""
        if v:
            # Remove formatação
            cpf_limpo = v.replace(".", "").replace("-", "")
            validar_cpf(cpf_limpo)
            return cpf_limpo
        return None

    @field_validator('telefone')
    @classmethod
    def validar_tel(cls, v: Optional[str]) -> Optional[str]:
        """Valida telefone se fornecido"""
        if v:
            # Remove formatação
            tel_limpo = v.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
            validar_telefone_celular(tel_limpo)
            return tel_limpo
        return None

    @field_validator('data_nascimento')
    @classmethod
    def validar_data(cls, v: Optional[date]) -> Optional[date]:
        """Valida data de nascimento se fornecida"""
        if v:
            from datetime import date as dt
            hoje = dt.today()
            idade = hoje.year - v.year - ((hoje.month, hoje.day) < (v.month, v.day))

            if idade < 10:
                raise ValueError("Usuário deve ter pelo menos 10 anos")
            if idade > 120:
                raise ValueError("Data de nascimento inválida")

        return v

    @field_validator('perfil')
    @classmethod
    def validar_perfil(cls, v: str) -> str:
        """Valida que o perfil é válido"""
        from util.perfis import Perfil
        Perfil.validar(v)
        return v


class UsuarioEdicaoDTO(BaseModel):
    """
    DTO para edição de dados do usuário.

    Similar ao cadastro, mas sem a senha (tem endpoint separado).
    """
    nome: str
    email: EmailStr
    perfil: str
    data_nascimento: Optional[date] = None
    numero_documento: Optional[str] = None
    telefone: Optional[str] = None

    # Mesmos validators do UsuarioCadastroDTO (copiar todos exceto senha)
    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validar_nome_completo(v)
        return v.strip()

    @field_validator('numero_documento')
    @classmethod
    def validar_documento(cls, v: Optional[str]) -> Optional[str]:
        if v:
            cpf_limpo = v.replace(".", "").replace("-", "")
            validar_cpf(cpf_limpo)
            return cpf_limpo
        return None

    @field_validator('telefone')
    @classmethod
    def validar_tel(cls, v: Optional[str]) -> Optional[str]:
        if v:
            tel_limpo = v.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
            validar_telefone_celular(tel_limpo)
            return tel_limpo
        return None

    @field_validator('data_nascimento')
    @classmethod
    def validar_data(cls, v: Optional[date]) -> Optional[date]:
        if v:
            from datetime import date as dt
            hoje = dt.today()
            idade = hoje.year - v.year - ((hoje.month, hoje.day) < (v.month, v.day))
            if idade < 10:
                raise ValueError("Usuário deve ter pelo menos 10 anos")
            if idade > 120:
                raise ValueError("Data de nascimento inválida")
        return v

    @field_validator('perfil')
    @classmethod
    def validar_perfil(cls, v: str) -> str:
        from util.perfis import Perfil
        Perfil.validar(v)
        return v


class UsuarioPerfilPublicoDTO(BaseModel):
    """
    DTO para exibir perfil público de usuário.

    Contém apenas dados não sensíveis que podem ser mostrados publicamente.
    """
    id: int
    nome: str
    perfil: str
    data_cadastro: Optional[str] = None

    # Não inclui: email, telefone, CPF, senha, etc
```

### ✅ Checklist

- [ ] Arquivo `dtos/usuario_dto.py` atualizado
- [ ] `UsuarioCadastroDTO` com todos os campos e validações
- [ ] `UsuarioEdicaoDTO` criado
- [ ] `UsuarioPerfilPublicoDTO` criado
- [ ] Validadores aplicados (nome, CPF, telefone, data)
- [ ] **Commit:** `feat(dto): adicionar DTOs completos de usuário`

---

## 1.5 Atualizar Seeds e Templates

### 📝 Objetivo
Atualizar dados iniciais e formulários HTML para os novos campos.

### 📍 Arquivo 1: Seeds
`util/seed_data.py`

### 💻 Código (Função Modificada)

```python
# util/seed_data.py
from datetime import date

def criar_usuarios_padrao():
    """Cria os usuários padrão do sistema AgendaFit"""
    from repo import usuario_repo
    from model.usuario_model import Usuario
    from util.perfis import Perfil
    from util.senha_util import hash_senha

    usuarios_padrao = [
        Usuario(
            id=0,
            nome="Administrador do Sistema",
            email="administrador@email.com",
            senha=hash_senha("1234aA@#"),
            perfil=Perfil.ADMIN.value,
            data_nascimento=date(1990, 1, 1),
            numero_documento="11111111111",
            telefone="28999999999",
            confirmado=True
        ),
        Usuario(
            id=0,
            nome="João Silva Aluno",
            email="aluno@email.com",
            senha=hash_senha("1234aA@#"),
            perfil=Perfil.ALUNO.value,
            data_nascimento=date(1995, 5, 15),
            numero_documento="22222222222",
            telefone="28988888888",
            confirmado=True
        ),
        Usuario(
            id=0,
            nome="Maria Santos Professora",
            email="professor@email.com",
            senha=hash_senha("1234aA@#"),
            perfil=Perfil.PROFESSOR.value,
            data_nascimento=date(1988, 8, 20),
            numero_documento="33333333333",
            telefone="28977777777",
            confirmado=True
        )
    ]

    for usuario in usuarios_padrao:
        usuario_existe = usuario_repo.obter_por_email(usuario.email)
        if not usuario_existe:
            usuario_repo.inserir(usuario)
            logger.info(f"Usuário seed criado: {usuario.email} ({usuario.perfil})")
        else:
            logger.info(f"Usuário seed já existe: {usuario.email}")
```

### 📍 Arquivo 2: Template de Cadastro
`templates/auth/cadastro.html`

### 💻 Código Completo

```html
<!-- templates/auth/cadastro.html -->
{% extends "base_publica.html" %}
{% from 'macros/form_fields.html' import text_field, email_field, password_field, date_field, select_field %}

{% block titulo %}Criar Conta - AgendaFit{% endblock %}

{% block conteudo %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="bi bi-person-plus-fill me-2"></i>
                        Criar Conta
                    </h4>
                </div>
                <div class="card-body">
                    <p class="text-muted">
                        Preencha os dados abaixo para criar sua conta no AgendaFit
                    </p>

                    <form method="POST" action="/auth/cadastro">

                        <!-- Nome Completo -->
                        {{ text_field(
                            'nome',
                            'Nome Completo',
                            required=True,
                            icon='person-fill',
                            placeholder='Ex: João Silva'
                        ) }}

                        <!-- Email -->
                        {{ email_field(
                            'email',
                            'E-mail',
                            required=True,
                            icon='envelope-fill',
                            placeholder='seu@email.com'
                        ) }}

                        <!-- Senha -->
                        {{ password_field(
                            'senha',
                            'Senha',
                            required=True,
                            icon='lock-fill',
                            help_text='Mínimo 8 caracteres, com letras maiúsculas, minúsculas, números e símbolos'
                        ) }}

                        <hr class="my-4">
                        <h6 class="text-muted mb-3">Informações Pessoais (Opcional)</h6>

                        <div class="row">
                            <div class="col-md-6">
                                <!-- Data de Nascimento -->
                                {{ date_field(
                                    'data_nascimento',
                                    'Data de Nascimento',
                                    icon='calendar-fill'
                                ) }}
                            </div>
                            <div class="col-md-6">
                                <!-- Telefone -->
                                {{ text_field(
                                    'telefone',
                                    'Telefone',
                                    icon='telephone-fill',
                                    mask='(00) 00000-0000',
                                    placeholder='(28) 99999-9999'
                                ) }}
                            </div>
                        </div>

                        <!-- CPF -->
                        {{ text_field(
                            'numero_documento',
                            'CPF',
                            icon='card-text',
                            mask='000.000.000-00',
                            placeholder='000.000.000-00'
                        ) }}

                        <hr class="my-4">

                        <!-- Perfil -->
                        {{ select_field(
                            'perfil',
                            'Você é:',
                            options=[
                                ('Aluno', 'Aluno - Quero treinar'),
                                ('Professor', 'Professor - Sou instrutor')
                            ],
                            required=True,
                            icon='people-fill'
                        ) }}

                        <div class="form-check mb-3">
                            <input class="form-check-input" type="checkbox" id="termos" required>
                            <label class="form-check-label small" for="termos">
                                Concordo com os <a href="/termos" target="_blank">termos de uso</a>
                                e <a href="/privacidade" target="_blank">política de privacidade</a>
                            </label>
                        </div>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="bi bi-check-circle-fill me-2"></i>
                                Criar Conta
                            </button>
                        </div>
                    </form>

                    <div class="text-center mt-4">
                        <p class="mb-0">
                            Já tem uma conta?
                            <a href="/auth/login" class="fw-bold">Fazer login</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    // Aplicar máscaras de input
    document.addEventListener('DOMContentLoaded', function() {
        // CPF
        const cpfInput = document.querySelector('input[name="numero_documento"]');
        if (cpfInput) {
            IMask(cpfInput, {mask: '000.000.000-00'});
        }

        // Telefone
        const telInput = document.querySelector('input[name="telefone"]');
        if (telInput) {
            IMask(telInput, {mask: '(00) 00000-0000'});
        }
    });
</script>
{% endblock %}
```

### 📍 Arquivo 3: Template de Edição de Perfil
`templates/perfil/editar.html`

Usar estrutura similar ao cadastro, removendo senha e adicionando os novos campos.

### ✅ Checklist

- [ ] `util/seed_data.py` atualizado
- [ ] Usuários seed com novos campos
- [ ] `templates/auth/cadastro.html` atualizado
- [ ] Máscaras de input configuradas (CPF, telefone)
- [ ] `templates/perfil/editar.html` atualizado (similar)
- [ ] **Commit:** `feat: atualizar seeds e templates com novos campos`

---

## 1.6 Atualizar Rotas de Autenticação

### 📝 Objetivo
Processar os novos campos no cadastro e edição de usuários.

### 📍 Arquivo
`routes/auth_routes.py`

### 💻 Código (Endpoint POST cadastro - modificar)

```python
# routes/auth_routes.py

@router.post("/auth/cadastro")
async def post_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    perfil: str = Form(...),
    data_nascimento: str = Form(None),
    numero_documento: str = Form(None),
    telefone: str = Form(None)
):
    """Processa o cadastro de novo usuário"""
    try:
        from datetime import datetime

        # Converter data de nascimento
        data_nasc = None
        if data_nascimento:
            try:
                data_nasc = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
            except ValueError:
                adicionar_mensagem_erro(request, "Data de nascimento inválida")
                return RedirectResponse("/auth/cadastro", status_code=303)

        # Criar DTO e validar
        usuario_dto = UsuarioCadastroDTO(
            nome=nome,
            email=email,
            senha=senha,
            perfil=perfil,
            data_nascimento=data_nasc,
            numero_documento=numero_documento,
            telefone=telefone
        )

        # Verificar se email já existe
        if usuario_repo.obter_por_email(email):
            adicionar_mensagem_erro(request, "E-mail já cadastrado")
            return RedirectResponse("/auth/cadastro", status_code=303)

        # Verificar se CPF já existe (se fornecido)
        if usuario_dto.numero_documento:
            usuarios = usuario_repo.obter_todos()
            if any(u.numero_documento == usuario_dto.numero_documento for u in usuarios):
                adicionar_mensagem_erro(request, "CPF já cadastrado")
                return RedirectResponse("/auth/cadastro", status_code=303)

        # Criar usuário
        usuario = Usuario(
            id=0,
            nome=usuario_dto.nome,
            email=usuario_dto.email,
            senha=hash_senha(usuario_dto.senha),
            perfil=usuario_dto.perfil,
            data_nascimento=usuario_dto.data_nascimento,
            numero_documento=usuario_dto.numero_documento,
            telefone=usuario_dto.telefone,
            confirmado=False  # Futuro: enviar email de confirmação
        )

        usuario_inserido = usuario_repo.inserir(usuario)

        if usuario_inserido:
            adicionar_mensagem_sucesso(
                request,
                f"Conta criada com sucesso! Bem-vindo(a), {usuario_dto.nome}!"
            )
            # TODO: Enviar email de confirmação
            return RedirectResponse("/auth/login", status_code=303)
        else:
            adicionar_mensagem_erro(request, "Erro ao criar conta. Tente novamente.")
            return RedirectResponse("/auth/cadastro", status_code=303)

    except ValidationError as e:
        for error in e.errors():
            adicionar_mensagem_erro(request, error['msg'])
        return RedirectResponse("/auth/cadastro", status_code=303)
    except Exception as e:
        logger.error(f"Erro ao cadastrar usuário: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro inesperado. Tente novamente.")
        return RedirectResponse("/auth/cadastro", status_code=303)
```

### ✅ Checklist

- [ ] Endpoint POST `/auth/cadastro` modificado
- [ ] Novos campos processados
- [ ] Validações aplicadas (email único, CPF único)
- [ ] Mensagens de erro/sucesso apropriadas
- [ ] **Commit:** `feat(auth): processar novos campos no cadastro`

---

## 1.7 Remover Entidade Tarefa (Exemplo)

### 📝 Objetivo
Remover a entidade "Tarefa" que foi usada apenas como exemplo no boilerplate.

### 🗑️ Arquivos a Remover

Execute os seguintes comandos:

```bash
# Remover model
rm model/tarefa_model.py

# Remover repo
rm repo/tarefa_repo.py

# Remover SQL
rm sql/tarefa_sql.py

# Remover rotas
rm routes/tarefas_routes.py

# Remover DTO
rm dtos/tarefa_dto.py

# Remover templates
rm -rf templates/tarefas/

# Remover testes
rm tests/test_tarefas.py
```

### 📝 Arquivos a Modificar

**`main.py`** - Remover imports e referências:

```python
# main.py

# REMOVER estas linhas:
# from repo import usuario_repo, configuracao_repo, tarefa_repo  # <-- REMOVER tarefa_repo
# from routes.tarefas_routes import router as tarefas_router     # <-- REMOVER esta linha
# app.include_router(tarefas_router, tags=["Tarefas"])           # <-- REMOVER esta linha
# tarefa_repo.criar_tabela()                                     # <-- REMOVER esta linha

# MANTER apenas:
from repo import usuario_repo, configuracao_repo

# ... resto do código ...
```

**`repo/__init__.py`** - Remover export:

```python
# repo/__init__.py

# REMOVER:
# from .tarefa_repo import *

# MANTER:
from .usuario_repo import *
from .configuracao_repo import *
```

### ✅ Checklist

- [ ] Arquivos da entidade tarefa removidos
- [ ] `main.py` limpo
- [ ] `repo/__init__.py` atualizado
- [ ] Aplicação inicia sem erros
- [ ] Sem referências à tarefa no código
- [ ] **Commit:** `refactor: remover entidade tarefa de exemplo`

---

## 1.8 Testar Fase 1

### 🧪 Testes Manuais

#### 1. Iniciar Aplicação
```bash
python main.py
```

Deve iniciar sem erros e mostrar:
- Tabela `usuario` criada/verificada
- Usuários seed criados

#### 2. Testar Cadastro

1. Abrir `http://localhost:8400/auth/cadastro`
2. Preencher todos os campos (com CPF e telefone)
3. Clicar em "Criar Conta"
4. Verificar:
   - Redirecionou para login
   - Mensagem de sucesso
   - Usuário salvo no banco

#### 3. Testar Login

1. Fazer login com:
   - Email: `aluno@email.com`
   - Senha: `1234aA@#`
2. Verificar:
   - Login bem-sucedido
   - Navbar mostra "João Silva Aluno"
   - Perfil é "Aluno"

#### 4. Testar Edição de Perfil

1. Acessar `/perfil`
2. Verificar que novos campos aparecem
3. Editar telefone
4. Salvar
5. Verificar que salvou

#### 5. Verificar Banco de Dados

Abrir `data/agendafit.db` no DB Browser e verificar:
- Tabela `usuario` tem todos os campos
- Usuários seed estão lá
- Dados do novo usuário estão corretos

### ✅ Checklist Final da Fase 1

- [ ] Perfis alterados (ALUNO, PROFESSOR)
- [ ] Modelo Usuario expandido
- [ ] SQL atualizado
- [ ] Repositório atualizado
- [ ] DTOs atualizados
- [ ] Seeds atualizados
- [ ] Templates atualizados
- [ ] Rotas atualizadas
- [ ] Entidade tarefa removida
- [ ] Aplicação inicia sem erros
- [ ] Todos os testes manuais passando
- [ ] **Commit final:** `feat: concluir Fase 1 - adaptações base`

### 🎯 Critério de Conclusão

✅ **Fase 1 está completa quando:**
- Aplicação roda sem erros
- Consegue criar usuário com todos os campos
- Login funciona
- Perfis são Aluno/Professor
- Todas as funcionalidades básicas funcionam

---

# FASE 2: INFRAESTRUTURA DE DADOS

**Duração:** 40 horas (2 semanas)
**Objetivo:** Criar toda a camada de acesso a dados para as entidades do AgendaFit

Esta fase é CRÍTICA pois todas as fases seguintes dependem dela. Vamos criar:
- 6 repositórios principais
- 2 repositórios novos (Presença e Avaliação Física)
- Todos os SQL scripts
- DTOs de validação
- Seeds de dados

---

## 2.1 Repositório de Categoria

### 📝 Objetivo
Criar repositório completo para gerenciar categorias de atividades.

### 📍 Arquivos a Criar
1. `sql/categoria_sql.py`
2. `repo/categoria_repo.py`

### 💻 Código Completo - SQL

```python
# sql/categoria_sql.py
"""
Scripts SQL para a tabela categoria.

Categoria representa os tipos de atividades oferecidas pela academia
(ex: Musculação, Aeróbico, Yoga, Pilates, etc).
"""

SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT
    )
"""

SQL_INSERIR = """
    INSERT INTO categoria (nome, descricao)
    VALUES (?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id_categoria, nome, descricao
    FROM categoria
    ORDER BY nome
"""

SQL_OBTER_POR_ID = """
    SELECT id_categoria, nome, descricao
    FROM categoria
    WHERE id_categoria = ?
"""

SQL_OBTER_POR_NOME = """
    SELECT id_categoria, nome, descricao
    FROM categoria
    WHERE nome = ?
"""

SQL_ATUALIZAR = """
    UPDATE categoria
    SET nome = ?, descricao = ?
    WHERE id_categoria = ?
"""

SQL_EXCLUIR = """
    DELETE FROM categoria
    WHERE id_categoria = ?
"""

SQL_CONTAR = """
    SELECT COUNT(*) FROM categoria
"""
```

### 💻 Código Completo - Repositório

```python
# repo/categoria_repo.py
"""
Repositório para gerenciamento de categorias de atividades.

Fornece operações CRUD completas para a entidade Categoria.
"""

import sqlite3
from typing import Optional
from model.categoria_model import Categoria
from sql.categoria_sql import *
from util.db_util import obter_conexao, fechar_conexao
from util.logger_config import logger


def criar_tabela():
    """Cria a tabela categoria se não existir"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_CRIAR_TABELA)
        conn.commit()
        logger.info("Tabela categoria criada/verificada com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar tabela categoria: {e}", exc_info=True)
        raise
    finally:
        fechar_conexao(conn)


def inserir(categoria: Categoria) -> Optional[Categoria]:
    """
    Insere uma nova categoria no banco.

    Args:
        categoria: Objeto Categoria com os dados

    Returns:
        Categoria com ID atribuído ou None em caso de erro
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_INSERIR,
            (categoria.nome, categoria.descricao)
        )
        conn.commit()
        categoria.id_categoria = cursor.lastrowid
        logger.info(f"Categoria inserida: {categoria.nome} (ID: {categoria.id_categoria})")
        return categoria
    except sqlite3.IntegrityError as e:
        logger.error(f"Erro de integridade (nome já existe?): {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao inserir categoria: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def obter_todos() -> list[Categoria]:
    """
    Retorna todas as categorias cadastradas.

    Returns:
        Lista de objetos Categoria ordenada por nome
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_TODOS)
        rows = cursor.fetchall()

        categorias = [
            Categoria(
                id_categoria=row[0],
                nome=row[1],
                descricao=row[2]
            )
            for row in rows
        ]

        logger.info(f"Obtidas {len(categorias)} categorias")
        return categorias
    except Exception as e:
        logger.error(f"Erro ao obter categorias: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def obter_por_id(id_categoria: int) -> Optional[Categoria]:
    """
    Busca uma categoria por ID.

    Args:
        id_categoria: ID da categoria

    Returns:
        Objeto Categoria ou None se não encontrado
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_ID, (id_categoria,))
        row = cursor.fetchone()

        if row:
            return Categoria(
                id_categoria=row[0],
                nome=row[1],
                descricao=row[2]
            )
        return None
    except Exception as e:
        logger.error(f"Erro ao obter categoria {id_categoria}: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def obter_por_nome(nome: str) -> Optional[Categoria]:
    """
    Busca uma categoria por nome.

    Args:
        nome: Nome da categoria

    Returns:
        Objeto Categoria ou None se não encontrado
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_NOME, (nome,))
        row = cursor.fetchone()

        if row:
            return Categoria(
                id_categoria=row[0],
                nome=row[1],
                descricao=row[2]
            )
        return None
    except Exception as e:
        logger.error(f"Erro ao obter categoria por nome: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def atualizar(categoria: Categoria) -> bool:
    """
    Atualiza os dados de uma categoria.

    Args:
        categoria: Objeto Categoria com dados atualizados

    Returns:
        True se atualizado com sucesso, False caso contrário
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_ATUALIZAR,
            (categoria.nome, categoria.descricao, categoria.id_categoria)
        )
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Categoria {categoria.id_categoria} atualizada")
            return True
        return False
    except sqlite3.IntegrityError as e:
        logger.error(f"Erro de integridade ao atualizar: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro ao atualizar categoria: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def excluir(id_categoria: int) -> bool:
    """
    Exclui uma categoria do banco.

    Args:
        id_categoria: ID da categoria a excluir

    Returns:
        True se excluído com sucesso, False caso contrário

    Note:
        Falhará se existirem atividades vinculadas a esta categoria
        devido a constraint de foreign key.
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_EXCLUIR, (id_categoria,))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Categoria {id_categoria} excluída")
            return True
        return False
    except sqlite3.IntegrityError:
        logger.warning(f"Não é possível excluir categoria {id_categoria} - possui atividades vinculadas")
        return False
    except Exception as e:
        logger.error(f"Erro ao excluir categoria: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def contar() -> int:
    """
    Conta o total de categorias cadastradas.

    Returns:
        Número de categorias
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_CONTAR)
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        logger.error(f"Erro ao contar categorias: {e}", exc_info=True)
        return 0
    finally:
        fechar_conexao(conn)
```

### 📝 Registrar no Main

```python
# main.py

# Adicionar import
from repo import usuario_repo, configuracao_repo, categoria_repo

# Adicionar na seção de criação de tabelas:
categoria_repo.criar_tabela()
logger.info("Tabela 'categoria' criada/verificada")
```

### ✅ Checklist

- [ ] `sql/categoria_sql.py` criado
- [ ] `repo/categoria_repo.py` criado
- [ ] Registrado em `main.py`
- [ ] Aplicação inicia sem erros
- [ ] Tabela criada no banco
- [ ] **Commit:** `feat(categoria): criar repositório e SQL de categoria`

---

## 2.2 Repositório de Atividade

### 📝 Objetivo
Criar repositório para gerenciar atividades (ex: "Musculação Iniciante", "Spinning").

**ATENÇÃO:** Atividades têm relacionamento com Categoria (FK)!

### 📍 Arquivos a Criar
1. `sql/atividade_sql.py`
2. `repo/atividade_repo.py`

### 💻 Código Completo - SQL

```python
# sql/atividade_sql.py
"""
Scripts SQL para a tabela atividade.

Atividade representa uma aula/modalidade específica oferecida,
vinculada a uma categoria.
"""

SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS atividade (
        id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
        id_categoria INTEGER NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        data_cadastro TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
    )
"""

SQL_INSERIR = """
    INSERT INTO atividade (id_categoria, nome, descricao, data_cadastro)
    VALUES (?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT
        a.id_atividade,
        a.id_categoria,
        a.nome,
        a.descricao,
        a.data_cadastro,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao
    FROM atividade a
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    ORDER BY a.nome
"""

SQL_OBTER_POR_ID = """
    SELECT
        a.id_atividade,
        a.id_categoria,
        a.nome,
        a.descricao,
        a.data_cadastro,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao
    FROM atividade a
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    WHERE a.id_atividade = ?
"""

SQL_OBTER_POR_CATEGORIA = """
    SELECT
        a.id_atividade,
        a.id_categoria,
        a.nome,
        a.descricao,
        a.data_cadastro,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao
    FROM atividade a
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    WHERE a.id_categoria = ?
    ORDER BY a.nome
"""

SQL_ATUALIZAR = """
    UPDATE atividade
    SET id_categoria = ?, nome = ?, descricao = ?
    WHERE id_atividade = ?
"""

SQL_EXCLUIR = """
    DELETE FROM atividade
    WHERE id_atividade = ?
"""

SQL_BUSCAR_POR_NOME = """
    SELECT
        a.id_atividade,
        a.id_categoria,
        a.nome,
        a.descricao,
        a.data_cadastro,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao
    FROM atividade a
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    WHERE a.nome LIKE ?
    ORDER BY a.nome
"""
```

### 💻 Código Completo - Repositório

```python
# repo/atividade_repo.py
"""
Repositório para gerenciamento de atividades.

Fornece operações CRUD para a entidade Atividade, incluindo
relacionamentos com Categoria.
"""

import sqlite3
from typing import Optional
from datetime import datetime
from model.Atividade_model import Atividade
from model.categoria_model import Categoria
from sql.atividade_sql import *
from util.db_util import obter_conexao, fechar_conexao
from util.logger_config import logger


def criar_tabela():
    """Cria a tabela atividade se não existir"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_CRIAR_TABELA)
        conn.commit()
        logger.info("Tabela atividade criada/verificada com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar tabela atividade: {e}", exc_info=True)
        raise
    finally:
        fechar_conexao(conn)


def _row_para_atividade(row: tuple) -> Atividade:
    """
    Converte uma row do banco em objeto Atividade.

    Args:
        row: Tupla com 7 campos (join com categoria)

    Returns:
        Objeto Atividade preenchido
    """
    return Atividade(
        id_atividade=row[0],
        id_categoria=row[1],
        nome=row[2],
        descricao=row[3],
        data_cadastro=datetime.fromisoformat(row[4]) if row[4] else datetime.now(),
        categoria=Categoria(
            id_categoria=row[1],
            nome=row[5],
            descricao=row[6]
        ) if row[5] else None
    )


def inserir(atividade: Atividade) -> Optional[Atividade]:
    """
    Insere uma nova atividade no banco.

    Args:
        atividade: Objeto Atividade com os dados

    Returns:
        Atividade com ID atribuído ou None em caso de erro
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_INSERIR,
            (
                atividade.id_categoria,
                atividade.nome,
                atividade.descricao,
                atividade.data_cadastro.isoformat() if atividade.data_cadastro else None
            )
        )
        conn.commit()
        atividade.id_atividade = cursor.lastrowid
        logger.info(f"Atividade inserida: {atividade.nome} (ID: {atividade.id_atividade})")
        return atividade
    except Exception as e:
        logger.error(f"Erro ao inserir atividade: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def obter_todos() -> list[Atividade]:
    """
    Retorna todas as atividades cadastradas com suas categorias.

    Returns:
        Lista de objetos Atividade ordenada por nome
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_TODOS)
        rows = cursor.fetchall()

        atividades = [_row_para_atividade(row) for row in rows]
        logger.info(f"Obtidas {len(atividades)} atividades")
        return atividades
    except Exception as e:
        logger.error(f"Erro ao obter atividades: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def obter_por_id(id_atividade: int) -> Optional[Atividade]:
    """
    Busca uma atividade por ID.

    Args:
        id_atividade: ID da atividade

    Returns:
        Objeto Atividade ou None se não encontrado
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_ID, (id_atividade,))
        row = cursor.fetchone()

        if row:
            return _row_para_atividade(row)
        return None
    except Exception as e:
        logger.error(f"Erro ao obter atividade {id_atividade}: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def obter_por_categoria(id_categoria: int) -> list[Atividade]:
    """
    Retorna todas as atividades de uma categoria.

    Args:
        id_categoria: ID da categoria

    Returns:
        Lista de atividades da categoria
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_CATEGORIA, (id_categoria,))
        rows = cursor.fetchall()

        atividades = [_row_para_atividade(row) for row in rows]
        return atividades
    except Exception as e:
        logger.error(f"Erro ao obter atividades por categoria: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def atualizar(atividade: Atividade) -> bool:
    """
    Atualiza os dados de uma atividade.

    Args:
        atividade: Objeto Atividade com dados atualizados

    Returns:
        True se atualizado com sucesso, False caso contrário
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_ATUALIZAR,
            (
                atividade.id_categoria,
                atividade.nome,
                atividade.descricao,
                atividade.id_atividade
            )
        )
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Atividade {atividade.id_atividade} atualizada")
            return True
        return False
    except Exception as e:
        logger.error(f"Erro ao atualizar atividade: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def excluir(id_atividade: int) -> bool:
    """
    Exclui uma atividade do banco.

    Args:
        id_atividade: ID da atividade a excluir

    Returns:
        True se excluído com sucesso, False caso contrário
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_EXCLUIR, (id_atividade,))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Atividade {id_atividade} excluída")
            return True
        return False
    except sqlite3.IntegrityError:
        logger.warning(f"Não é possível excluir atividade {id_atividade} - possui turmas vinculadas")
        return False
    except Exception as e:
        logger.error(f"Erro ao excluir atividade: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def buscar_por_nome(termo: str) -> list[Atividade]:
    """
    Busca atividades cujo nome contenha o termo.

    Args:
        termo: Termo de busca

    Returns:
        Lista de atividades encontradas
    """
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_BUSCAR_POR_NOME, (f"%{termo}%",))
        rows = cursor.fetchall()

        atividades = [_row_para_atividade(row) for row in rows]
        return atividades
    except Exception as e:
        logger.error(f"Erro ao buscar atividades: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)
```

### 📝 Registrar no Main

```python
# main.py

# Adicionar import
from repo import usuario_repo, configuracao_repo, categoria_repo, atividade_repo

# Adicionar na seção de criação de tabelas (DEPOIS de categoria):
atividade_repo.criar_tabela()
logger.info("Tabela 'atividade' criada/verificada")
```

### ✅ Checklist

- [ ] `sql/atividade_sql.py` criado
- [ ] `repo/atividade_repo.py` criado
- [ ] Função `_row_para_atividade()` implementada
- [ ] JOINs com categoria funcionando
- [ ] Registrado em `main.py`
- [ ] **Commit:** `feat(atividade): criar repositório e SQL de atividade`

---

## 2.3 Repositório de Turma

### 📝 Objetivo

Criar o repositório completo para gerenciar turmas de atividades. A turma possui relacionamento com Atividade (qual atividade) e com Usuario/Professor (quem ministra). É uma entidade central do sistema.

### 📍 Localização

- `sql/turma_sql.py` (novo arquivo)
- `repo/turma_repo.py` (novo arquivo)
- `main.py` (adicionar criação de tabela)

### 💻 Código Completo

#### Arquivo: `sql/turma_sql.py`

```python
SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS turma (
        id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
        id_atividade INTEGER NOT NULL,
        id_professor INTEGER NOT NULL,
        nome VARCHAR(100) NOT NULL,
        descricao TEXT,
        vagas INTEGER NOT NULL,
        vagas_ocupadas INTEGER DEFAULT 0,
        horario VARCHAR(50) NOT NULL,
        dias_semana VARCHAR(50) NOT NULL,
        data_inicio DATE NOT NULL,
        data_fim DATE,
        ativa BOOLEAN DEFAULT 1,
        FOREIGN KEY (id_atividade) REFERENCES atividade(id_atividade) ON DELETE RESTRICT,
        FOREIGN KEY (id_professor) REFERENCES usuario(id_usuario) ON DELETE RESTRICT
    )
"""

SQL_INSERIR = """
    INSERT INTO turma
    (id_atividade, id_professor, nome, descricao, vagas, vagas_ocupadas,
     horario, dias_semana, data_inicio, data_fim, ativa)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT
        t.*,
        a.nome as atividade_nome,
        a.descricao as atividade_descricao,
        a.duracao_minutos as atividade_duracao,
        a.nivel_dificuldade as atividade_nivel,
        a.equipamento_necessario as atividade_equipamento,
        c.id_categoria,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao,
        u.nome as professor_nome,
        u.email as professor_email
    FROM turma t
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    INNER JOIN usuario u ON t.id_professor = u.id_usuario
    ORDER BY t.data_inicio DESC, t.nome
"""

SQL_OBTER_POR_ID = """
    SELECT
        t.*,
        a.nome as atividade_nome,
        a.descricao as atividade_descricao,
        a.duracao_minutos as atividade_duracao,
        a.nivel_dificuldade as atividade_nivel,
        a.equipamento_necessario as atividade_equipamento,
        c.id_categoria,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao,
        u.nome as professor_nome,
        u.email as professor_email
    FROM turma t
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    INNER JOIN usuario u ON t.id_professor = u.id_usuario
    WHERE t.id_turma = ?
"""

SQL_ATUALIZAR = """
    UPDATE turma
    SET id_atividade = ?, id_professor = ?, nome = ?, descricao = ?,
        vagas = ?, vagas_ocupadas = ?, horario = ?, dias_semana = ?,
        data_inicio = ?, data_fim = ?, ativa = ?
    WHERE id_turma = ?
"""

SQL_EXCLUIR = """
    DELETE FROM turma WHERE id_turma = ?
"""

SQL_OBTER_POR_PROFESSOR = """
    SELECT
        t.*,
        a.nome as atividade_nome,
        a.descricao as atividade_descricao,
        a.duracao_minutos as atividade_duracao,
        a.nivel_dificuldade as atividade_nivel,
        a.equipamento_necessario as atividade_equipamento,
        c.id_categoria,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao,
        u.nome as professor_nome,
        u.email as professor_email
    FROM turma t
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    INNER JOIN usuario u ON t.id_professor = u.id_usuario
    WHERE t.id_professor = ?
    ORDER BY t.data_inicio DESC, t.nome
"""

SQL_OBTER_POR_ATIVIDADE = """
    SELECT
        t.*,
        a.nome as atividade_nome,
        a.descricao as atividade_descricao,
        a.duracao_minutos as atividade_duracao,
        a.nivel_dificuldade as atividade_nivel,
        a.equipamento_necessario as atividade_equipamento,
        c.id_categoria,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao,
        u.nome as professor_nome,
        u.email as professor_email
    FROM turma t
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    INNER JOIN usuario u ON t.id_professor = u.id_usuario
    WHERE t.id_atividade = ?
    ORDER BY t.data_inicio DESC, t.nome
"""

SQL_OBTER_ATIVAS = """
    SELECT
        t.*,
        a.nome as atividade_nome,
        a.descricao as atividade_descricao,
        a.duracao_minutos as atividade_duracao,
        a.nivel_dificuldade as atividade_nivel,
        a.equipamento_necessario as atividade_equipamento,
        c.id_categoria,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao,
        u.nome as professor_nome,
        u.email as professor_email
    FROM turma t
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    INNER JOIN usuario u ON t.id_professor = u.id_usuario
    WHERE t.ativa = 1
    ORDER BY t.data_inicio DESC, t.nome
"""

SQL_OBTER_COM_VAGAS = """
    SELECT
        t.*,
        a.nome as atividade_nome,
        a.descricao as atividade_descricao,
        a.duracao_minutos as atividade_duracao,
        a.nivel_dificuldade as atividade_nivel,
        a.equipamento_necessario as atividade_equipamento,
        c.id_categoria,
        c.nome as categoria_nome,
        c.descricao as categoria_descricao,
        u.nome as professor_nome,
        u.email as professor_email
    FROM turma t
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    LEFT JOIN categoria c ON a.id_categoria = c.id_categoria
    INNER JOIN usuario u ON t.id_professor = u.id_usuario
    WHERE t.ativa = 1 AND t.vagas_ocupadas < t.vagas
    ORDER BY t.data_inicio DESC, t.nome
"""

SQL_ATUALIZAR_VAGAS_OCUPADAS = """
    UPDATE turma
    SET vagas_ocupadas = ?
    WHERE id_turma = ?
"""

SQL_INCREMENTAR_VAGAS_OCUPADAS = """
    UPDATE turma
    SET vagas_ocupadas = vagas_ocupadas + 1
    WHERE id_turma = ?
"""

SQL_DECREMENTAR_VAGAS_OCUPADAS = """
    UPDATE turma
    SET vagas_ocupadas = vagas_ocupadas - 1
    WHERE id_turma = ? AND vagas_ocupadas > 0
"""
```

#### Arquivo: `repo/turma_repo.py`

```python
from typing import Optional
from model.turma_model import Turma
from model.atividade_model import Atividade
from model.categoria_model import Categoria
from model.usuario_model import Usuario
from sql.turma_sql import *
from util.database import obter_conexao, fechar_conexao
from util.logger_config import logger


def criar_tabela():
    """Cria a tabela turma no banco de dados"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_CRIAR_TABELA)
        conn.commit()
        logger.info("Tabela 'turma' criada/verificada com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar tabela turma: {e}", exc_info=True)
        raise
    finally:
        fechar_conexao(conn)


def _row_para_turma(row: tuple) -> Turma:
    """
    Converte uma linha do banco em objeto Turma com relacionamentos

    A linha deve conter:
    - 11 campos da turma (id_turma até ativa)
    - 5 campos da atividade (nome, descricao, duracao, nivel, equipamento)
    - 3 campos da categoria (id, nome, descricao)
    - 2 campos do professor (nome, email)
    """
    # Criar categoria (se existir)
    categoria = None
    if row[16] is not None:  # id_categoria
        categoria = Categoria(
            id_categoria=row[16],
            nome=row[17],
            descricao=row[18]
        )

    # Criar atividade completa
    atividade = Atividade(
        id_atividade=row[1],  # id_atividade da turma
        nome=row[11],
        descricao=row[12],
        duracao_minutos=row[13],
        nivel_dificuldade=row[14],
        equipamento_necessario=row[15],
        id_categoria=row[16] if row[16] else None,
        categoria=categoria
    )

    # Criar professor (objeto Usuario simplificado, só com dados básicos)
    professor = Usuario(
        id_usuario=row[2],  # id_professor da turma
        nome=row[19],
        email=row[20],
        senha="",  # Não retornamos senha por segurança
        perfil=""  # Sabemos que é professor
    )

    # Criar turma completa
    turma = Turma(
        id_turma=row[0],
        id_atividade=row[1],
        id_professor=row[2],
        nome=row[3],
        descricao=row[4],
        vagas=row[5],
        vagas_ocupadas=row[6],
        horario=row[7],
        dias_semana=row[8],
        data_inicio=row[9],
        data_fim=row[10],
        ativa=bool(row[11]) if row[11] is not None else True,
        atividade=atividade,
        professor=professor
    )

    return turma


def inserir(turma: Turma) -> Optional[Turma]:
    """Insere uma nova turma no banco de dados"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_INSERIR,
            (
                turma.id_atividade,
                turma.id_professor,
                turma.nome,
                turma.descricao,
                turma.vagas,
                turma.vagas_ocupadas,
                turma.horario,
                turma.dias_semana,
                turma.data_inicio,
                turma.data_fim,
                turma.ativa
            )
        )
        conn.commit()

        turma.id_turma = cursor.lastrowid
        logger.info(f"Turma inserida com ID: {turma.id_turma}")
        return turma
    except Exception as e:
        logger.error(f"Erro ao inserir turma: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def obter_todos() -> list[Turma]:
    """Retorna todas as turmas com seus relacionamentos"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_TODOS)
        rows = cursor.fetchall()

        turmas = [_row_para_turma(row) for row in rows]
        logger.info(f"{len(turmas)} turma(s) encontrada(s)")
        return turmas
    except Exception as e:
        logger.error(f"Erro ao obter turmas: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def obter_por_id(id_turma: int) -> Optional[Turma]:
    """Retorna uma turma pelo ID com seus relacionamentos"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_ID, (id_turma,))
        row = cursor.fetchone()

        if row:
            turma = _row_para_turma(row)
            logger.info(f"Turma encontrada: {turma.nome}")
            return turma

        logger.warning(f"Turma com ID {id_turma} não encontrada")
        return None
    except Exception as e:
        logger.error(f"Erro ao obter turma por ID: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def atualizar(turma: Turma) -> bool:
    """Atualiza uma turma existente"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_ATUALIZAR,
            (
                turma.id_atividade,
                turma.id_professor,
                turma.nome,
                turma.descricao,
                turma.vagas,
                turma.vagas_ocupadas,
                turma.horario,
                turma.dias_semana,
                turma.data_inicio,
                turma.data_fim,
                turma.ativa,
                turma.id_turma
            )
        )
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Turma {turma.id_turma} atualizada com sucesso")
            return True

        logger.warning(f"Nenhuma turma foi atualizada com ID {turma.id_turma}")
        return False
    except Exception as e:
        logger.error(f"Erro ao atualizar turma: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def excluir(id_turma: int) -> bool:
    """Exclui uma turma do banco de dados"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_EXCLUIR, (id_turma,))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Turma {id_turma} excluída com sucesso")
            return True

        logger.warning(f"Nenhuma turma foi excluída com ID {id_turma}")
        return False
    except Exception as e:
        logger.error(f"Erro ao excluir turma: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def obter_por_professor(id_professor: int) -> list[Turma]:
    """Retorna todas as turmas de um professor específico"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_PROFESSOR, (id_professor,))
        rows = cursor.fetchall()

        turmas = [_row_para_turma(row) for row in rows]
        logger.info(f"{len(turmas)} turma(s) encontrada(s) para o professor {id_professor}")
        return turmas
    except Exception as e:
        logger.error(f"Erro ao obter turmas por professor: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def obter_por_atividade(id_atividade: int) -> list[Turma]:
    """Retorna todas as turmas de uma atividade específica"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_ATIVIDADE, (id_atividade,))
        rows = cursor.fetchall()

        turmas = [_row_para_turma(row) for row in rows]
        logger.info(f"{len(turmas)} turma(s) encontrada(s) para a atividade {id_atividade}")
        return turmas
    except Exception as e:
        logger.error(f"Erro ao obter turmas por atividade: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def obter_ativas() -> list[Turma]:
    """Retorna todas as turmas ativas"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_ATIVAS)
        rows = cursor.fetchall()

        turmas = [_row_para_turma(row) for row in rows]
        logger.info(f"{len(turmas)} turma(s) ativa(s) encontrada(s)")
        return turmas
    except Exception as e:
        logger.error(f"Erro ao obter turmas ativas: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def obter_com_vagas() -> list[Turma]:
    """Retorna todas as turmas ativas que ainda têm vagas disponíveis"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_COM_VAGAS)
        rows = cursor.fetchall()

        turmas = [_row_para_turma(row) for row in rows]
        logger.info(f"{len(turmas)} turma(s) com vagas encontrada(s)")
        return turmas
    except Exception as e:
        logger.error(f"Erro ao obter turmas com vagas: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def atualizar_vagas_ocupadas(id_turma: int, novas_vagas_ocupadas: int) -> bool:
    """Atualiza o número de vagas ocupadas de uma turma"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_ATUALIZAR_VAGAS_OCUPADAS, (novas_vagas_ocupadas, id_turma))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Vagas ocupadas da turma {id_turma} atualizadas para {novas_vagas_ocupadas}")
            return True

        return False
    except Exception as e:
        logger.error(f"Erro ao atualizar vagas ocupadas: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def incrementar_vagas_ocupadas(id_turma: int) -> bool:
    """Incrementa em 1 o número de vagas ocupadas (quando aluno se matricula)"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_INCREMENTAR_VAGAS_OCUPADAS, (id_turma,))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Vagas ocupadas da turma {id_turma} incrementadas")
            return True

        return False
    except Exception as e:
        logger.error(f"Erro ao incrementar vagas ocupadas: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def decrementar_vagas_ocupadas(id_turma: int) -> bool:
    """Decrementa em 1 o número de vagas ocupadas (quando aluno cancela matrícula)"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_DECREMENTAR_VAGAS_OCUPADAS, (id_turma,))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Vagas ocupadas da turma {id_turma} decrementadas")
            return True

        return False
    except Exception as e:
        logger.error(f"Erro ao decrementar vagas ocupadas: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)
```

### 📝 Registrar no Main

```python
# main.py

# Adicionar import
from repo import usuario_repo, configuracao_repo, categoria_repo, atividade_repo, turma_repo

# Adicionar na seção de criação de tabelas (DEPOIS de atividade):
turma_repo.criar_tabela()
logger.info("Tabela 'turma' criada/verificada")
```

### ✅ Checklist

- [ ] `sql/turma_sql.py` criado com todas as queries (incluindo filtros especiais)
- [ ] `repo/turma_repo.py` criado com todas as funções CRUD
- [ ] Função `_row_para_turma()` implementada com JOINs triplos
- [ ] Funções especiais de vagas implementadas (incrementar/decrementar)
- [ ] Registrado em `main.py`
- [ ] **Commit:** `feat(turma): criar repositório e SQL de turma com relacionamentos`

---

## 2.4 Repositório de Matrícula

### 📝 Objetivo

Criar o repositório para gerenciar matrículas dos alunos nas turmas. É a entidade que conecta Usuario (aluno) com Turma. Inclui controle de status da matrícula e data de inscrição.

### 📍 Localização

- `sql/matricula_sql.py` (novo arquivo)
- `repo/matricula_repo.py` (novo arquivo)
- `main.py` (adicionar criação de tabela)

### 💻 Código Completo

#### Arquivo: `sql/matricula_sql.py`

```python
SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS matricula (
        id_matricula INTEGER PRIMARY KEY AUTOINCREMENT,
        id_turma INTEGER NOT NULL,
        id_aluno INTEGER NOT NULL,
        data_matricula DATE NOT NULL,
        status VARCHAR(20) DEFAULT 'ATIVA',
        observacoes TEXT,
        FOREIGN KEY (id_turma) REFERENCES turma(id_turma) ON DELETE RESTRICT,
        FOREIGN KEY (id_aluno) REFERENCES usuario(id_usuario) ON DELETE RESTRICT,
        UNIQUE(id_turma, id_aluno)
    )
"""

SQL_INSERIR = """
    INSERT INTO matricula (id_turma, id_aluno, data_matricula, status, observacoes)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT
        m.*,
        u.nome as aluno_nome,
        u.email as aluno_email,
        t.nome as turma_nome,
        t.horario as turma_horario,
        t.dias_semana as turma_dias,
        a.nome as atividade_nome
    FROM matricula m
    INNER JOIN usuario u ON m.id_aluno = u.id_usuario
    INNER JOIN turma t ON m.id_turma = t.id_turma
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    ORDER BY m.data_matricula DESC
"""

SQL_OBTER_POR_ID = """
    SELECT
        m.*,
        u.nome as aluno_nome,
        u.email as aluno_email,
        t.nome as turma_nome,
        t.horario as turma_horario,
        t.dias_semana as turma_dias,
        a.nome as atividade_nome
    FROM matricula m
    INNER JOIN usuario u ON m.id_aluno = u.id_usuario
    INNER JOIN turma t ON m.id_turma = t.id_turma
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    WHERE m.id_matricula = ?
"""

SQL_ATUALIZAR = """
    UPDATE matricula
    SET id_turma = ?, id_aluno = ?, data_matricula = ?, status = ?, observacoes = ?
    WHERE id_matricula = ?
"""

SQL_EXCLUIR = """
    DELETE FROM matricula WHERE id_matricula = ?
"""

SQL_OBTER_POR_ALUNO = """
    SELECT
        m.*,
        u.nome as aluno_nome,
        u.email as aluno_email,
        t.nome as turma_nome,
        t.horario as turma_horario,
        t.dias_semana as turma_dias,
        a.nome as atividade_nome
    FROM matricula m
    INNER JOIN usuario u ON m.id_aluno = u.id_usuario
    INNER JOIN turma t ON m.id_turma = t.id_turma
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    WHERE m.id_aluno = ?
    ORDER BY m.data_matricula DESC
"""

SQL_OBTER_POR_TURMA = """
    SELECT
        m.*,
        u.nome as aluno_nome,
        u.email as aluno_email,
        t.nome as turma_nome,
        t.horario as turma_horario,
        t.dias_semana as turma_dias,
        a.nome as atividade_nome
    FROM matricula m
    INNER JOIN usuario u ON m.id_aluno = u.id_usuario
    INNER JOIN turma t ON m.id_turma = t.id_turma
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    WHERE m.id_turma = ?
    ORDER BY m.data_matricula DESC
"""

SQL_OBTER_POR_STATUS = """
    SELECT
        m.*,
        u.nome as aluno_nome,
        u.email as aluno_email,
        t.nome as turma_nome,
        t.horario as turma_horario,
        t.dias_semana as turma_dias,
        a.nome as atividade_nome
    FROM matricula m
    INNER JOIN usuario u ON m.id_aluno = u.id_usuario
    INNER JOIN turma t ON m.id_turma = t.id_turma
    INNER JOIN atividade a ON t.id_atividade = a.id_atividade
    WHERE m.status = ?
    ORDER BY m.data_matricula DESC
"""

SQL_VERIFICAR_MATRICULA_EXISTENTE = """
    SELECT COUNT(*) FROM matricula
    WHERE id_turma = ? AND id_aluno = ?
"""

SQL_ATUALIZAR_STATUS = """
    UPDATE matricula
    SET status = ?
    WHERE id_matricula = ?
"""

SQL_CONTAR_POR_TURMA = """
    SELECT COUNT(*) FROM matricula
    WHERE id_turma = ? AND status = 'ATIVA'
"""
```

#### Arquivo: `repo/matricula_repo.py`

```python
from typing import Optional
from model.matricula_model import Matricula
from model.turma_model import Turma
from model.usuario_model import Usuario
from model.atividade_model import Atividade
from sql.matricula_sql import *
from util.database import obter_conexao, fechar_conexao
from util.logger_config import logger


def criar_tabela():
    """Cria a tabela matricula no banco de dados"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_CRIAR_TABELA)
        conn.commit()
        logger.info("Tabela 'matricula' criada/verificada com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar tabela matricula: {e}", exc_info=True)
        raise
    finally:
        fechar_conexao(conn)


def _row_para_matricula(row: tuple) -> Matricula:
    """
    Converte uma linha do banco em objeto Matricula com relacionamentos

    A linha deve conter:
    - 6 campos da matricula
    - 2 campos do aluno (nome, email)
    - 3 campos da turma (nome, horario, dias)
    - 1 campo da atividade (nome)
    """
    # Criar aluno (objeto Usuario simplificado)
    aluno = Usuario(
        id_usuario=row[2],  # id_aluno
        nome=row[6],
        email=row[7],
        senha="",
        perfil=""
    )

    # Criar atividade (objeto simplificado)
    atividade = Atividade(
        id_atividade=0,  # Não temos o id aqui
        nome=row[11],
        descricao="",
        duracao_minutos=0,
        nivel_dificuldade="",
        equipamento_necessario=""
    )

    # Criar turma (objeto simplificado)
    turma = Turma(
        id_turma=row[1],  # id_turma
        nome=row[8],
        horario=row[9],
        dias_semana=row[10],
        id_atividade=0,
        id_professor=0,
        descricao="",
        vagas=0,
        vagas_ocupadas=0,
        data_inicio="",
        data_fim=None,
        ativa=True,
        atividade=atividade
    )

    # Criar matrícula completa
    matricula = Matricula(
        id_matricula=row[0],
        id_turma=row[1],
        id_aluno=row[2],
        data_matricula=row[3],
        status=row[4],
        observacoes=row[5],
        aluno=aluno,
        turma=turma
    )

    return matricula


def inserir(matricula: Matricula) -> Optional[Matricula]:
    """Insere uma nova matrícula no banco de dados"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_INSERIR,
            (
                matricula.id_turma,
                matricula.id_aluno,
                matricula.data_matricula,
                matricula.status,
                matricula.observacoes
            )
        )
        conn.commit()

        matricula.id_matricula = cursor.lastrowid
        logger.info(f"Matrícula inserida com ID: {matricula.id_matricula}")
        return matricula
    except Exception as e:
        logger.error(f"Erro ao inserir matrícula: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def obter_todos() -> list[Matricula]:
    """Retorna todas as matrículas com seus relacionamentos"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_TODOS)
        rows = cursor.fetchall()

        matriculas = [_row_para_matricula(row) for row in rows]
        logger.info(f"{len(matriculas)} matrícula(s) encontrada(s)")
        return matriculas
    except Exception as e:
        logger.error(f"Erro ao obter matrículas: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def obter_por_id(id_matricula: int) -> Optional[Matricula]:
    """Retorna uma matrícula pelo ID com seus relacionamentos"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_ID, (id_matricula,))
        row = cursor.fetchone()

        if row:
            matricula = _row_para_matricula(row)
            logger.info(f"Matrícula encontrada: {matricula.id_matricula}")
            return matricula

        logger.warning(f"Matrícula com ID {id_matricula} não encontrada")
        return None
    except Exception as e:
        logger.error(f"Erro ao obter matrícula por ID: {e}", exc_info=True)
        return None
    finally:
        fechar_conexao(conn)


def atualizar(matricula: Matricula) -> bool:
    """Atualiza uma matrícula existente"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(
            SQL_ATUALIZAR,
            (
                matricula.id_turma,
                matricula.id_aluno,
                matricula.data_matricula,
                matricula.status,
                matricula.observacoes,
                matricula.id_matricula
            )
        )
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Matrícula {matricula.id_matricula} atualizada com sucesso")
            return True

        logger.warning(f"Nenhuma matrícula foi atualizada com ID {matricula.id_matricula}")
        return False
    except Exception as e:
        logger.error(f"Erro ao atualizar matrícula: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def excluir(id_matricula: int) -> bool:
    """Exclui uma matrícula do banco de dados"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_EXCLUIR, (id_matricula,))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Matrícula {id_matricula} excluída com sucesso")
            return True

        logger.warning(f"Nenhuma matrícula foi excluída com ID {id_matricula}")
        return False
    except Exception as e:
        logger.error(f"Erro ao excluir matrícula: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def obter_por_aluno(id_aluno: int) -> list[Matricula]:
    """Retorna todas as matrículas de um aluno específico"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_ALUNO, (id_aluno,))
        rows = cursor.fetchall()

        matriculas = [_row_para_matricula(row) for row in rows]
        logger.info(f"{len(matriculas)} matrícula(s) encontrada(s) para o aluno {id_aluno}")
        return matriculas
    except Exception as e:
        logger.error(f"Erro ao obter matrículas por aluno: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def obter_por_turma(id_turma: int) -> list[Matricula]:
    """Retorna todas as matrículas de uma turma específica"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_TURMA, (id_turma,))
        rows = cursor.fetchall()

        matriculas = [_row_para_matricula(row) for row in rows]
        logger.info(f"{len(matriculas)} matrícula(s) encontrada(s) para a turma {id_turma}")
        return matriculas
    except Exception as e:
        logger.error(f"Erro ao obter matrículas por turma: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def obter_por_status(status: str) -> list[Matricula]:
    """Retorna todas as matrículas com um status específico"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_OBTER_POR_STATUS, (status,))
        rows = cursor.fetchall()

        matriculas = [_row_para_matricula(row) for row in rows]
        logger.info(f"{len(matriculas)} matrícula(s) encontrada(s) com status {status}")
        return matriculas
    except Exception as e:
        logger.error(f"Erro ao obter matrículas por status: {e}", exc_info=True)
        return []
    finally:
        fechar_conexao(conn)


def verificar_matricula_existente(id_turma: int, id_aluno: int) -> bool:
    """Verifica se já existe uma matrícula para o aluno na turma"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_VERIFICAR_MATRICULA_EXISTENTE, (id_turma, id_aluno))
        count = cursor.fetchone()[0]

        existe = count > 0
        logger.info(f"Matrícula {'existe' if existe else 'não existe'} para aluno {id_aluno} na turma {id_turma}")
        return existe
    except Exception as e:
        logger.error(f"Erro ao verificar matrícula existente: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def atualizar_status(id_matricula: int, novo_status: str) -> bool:
    """Atualiza apenas o status de uma matrícula"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_ATUALIZAR_STATUS, (novo_status, id_matricula))
        conn.commit()

        if cursor.rowcount > 0:
            logger.info(f"Status da matrícula {id_matricula} atualizado para {novo_status}")
            return True

        return False
    except Exception as e:
        logger.error(f"Erro ao atualizar status da matrícula: {e}", exc_info=True)
        return False
    finally:
        fechar_conexao(conn)


def contar_por_turma(id_turma: int) -> int:
    """Conta quantas matrículas ativas existem em uma turma"""
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        cursor.execute(SQL_CONTAR_POR_TURMA, (id_turma,))
        count = cursor.fetchone()[0]

        logger.info(f"Turma {id_turma} tem {count} matrícula(s) ativa(s)")
        return count
    except Exception as e:
        logger.error(f"Erro ao contar matrículas por turma: {e}", exc_info=True)
        return 0
    finally:
        fechar_conexao(conn)
```

### 📝 Registrar no Main

```python
# main.py

# Adicionar import
from repo import (usuario_repo, configuracao_repo, categoria_repo,
                  atividade_repo, turma_repo, matricula_repo)

# Adicionar na seção de criação de tabelas (DEPOIS de turma):
matricula_repo.criar_tabela()
logger.info("Tabela 'matricula' criada/verificada")
```

### ✅ Checklist

- [ ] `sql/matricula_sql.py` criado
- [ ] `repo/matricula_repo.py` criado
- [ ] Constraint UNIQUE (id_turma, id_aluno) funcionando
- [ ] Funções especiais implementadas (verificar existente, contar, atualizar status)
- [ ] Registrado em `main.py`
- [ ] **Commit:** `feat(matricula): criar repositório e SQL de matrícula`

---

## 2.5 Repositórios de Pagamento e Endereço

### 📝 Objetivo

Criar os dois repositórios restantes mais simples: Pagamento e Endereço. Ambos são entidades auxiliares com relacionamentos diretos.

### 📝 Instruções Resumidas

Para **Pagamento** e **Endereço**, siga o padrão estabelecido nos repositórios anteriores:

#### Repositório de Pagamento

1. **Criar `sql/pagamento_sql.py`** com:
   - SQL_CRIAR_TABELA (campos: id_pagamento, id_matricula FK, valor, data_pagamento, forma_pagamento, status_pagamento, comprovante)
   - SQL_INSERIR, SQL_OBTER_TODOS, SQL_OBTER_POR_ID, SQL_ATUALIZAR, SQL_EXCLUIR
   - SQL_OBTER_POR_MATRICULA (JOIN com matricula)
   - SQL_OBTER_POR_STATUS
   - SQL_OBTER_POR_PERIODO (com WHERE data_pagamento BETWEEN ? AND ?)

2. **Criar `repo/pagamento_repo.py`** com:
   - `criar_tabela()`
   - `_row_para_pagamento(row)` - incluir objeto Matricula relacionado
   - `inserir(pagamento)`, `obter_todos()`, `obter_por_id(id)`, `atualizar(pagamento)`, `excluir(id)`
   - `obter_por_matricula(id_matricula)`
   - `obter_por_status(status)`
   - `obter_por_periodo(data_inicio, data_fim)`

3. **Registrar em `main.py`**:
   ```python
   from repo import (..., pagamento_repo)
   pagamento_repo.criar_tabela()
   ```

#### Repositório de Endereço

1. **Criar `sql/endereco_sql.py`** com:
   - SQL_CRIAR_TABELA (campos: id_endereco, id_usuario FK, cep, logradouro, numero, complemento, bairro, cidade, estado)
   - SQL_INSERIR, SQL_OBTER_TODOS, SQL_OBTER_POR_ID, SQL_ATUALIZAR, SQL_EXCLUIR
   - SQL_OBTER_POR_USUARIO (JOIN com usuario)
   - SQL_OBTER_POR_CIDADE

2. **Criar `repo/endereco_repo.py`** com:
   - `criar_tabela()`
   - `_row_para_endereco(row)` - incluir objeto Usuario relacionado
   - `inserir(endereco)`, `obter_todos()`, `obter_por_id(id)`, `atualizar(endereco)`, `excluir(id)`
   - `obter_por_usuario(id_usuario)`
   - `obter_por_cidade(cidade)`

3. **Registrar em `main.py`**:
   ```python
   from repo import (..., endereco_repo)
   endereco_repo.criar_tabela()
   ```

### ✅ Checklist

- [ ] `sql/pagamento_sql.py` e `repo/pagamento_repo.py` criados
- [ ] `sql/endereco_sql.py` e `repo/endereco_repo.py` criados
- [ ] Ambos registrados em `main.py`
- [ ] Testar criação de tabelas: `python main.py`
- [ ] **Commit:** `feat(pagamento,endereco): criar repositórios de pagamento e endereço`

---

## 2.6 DTOs para Novas Entidades

### 📝 Objetivo

Criar os DTOs (Data Transfer Objects) para as novas entidades, utilizando Pydantic para validação de dados nas rotas da API.

### 📍 Localização

- `dto/categoria_dto.py` (novo arquivo)
- `dto/atividade_dto.py` (novo arquivo)
- `dto/turma_dto.py` (novo arquivo)
- `dto/matricula_dto.py` (novo arquivo)
- `dto/pagamento_dto.py` (novo arquivo)
- `dto/endereco_dto.py` (novo arquivo)

### 💻 Exemplos de DTOs

#### Arquivo: `dto/categoria_dto.py`

```python
from pydantic import BaseModel, field_validator


class CategoriaCreateDTO(BaseModel):
    """DTO para criação de categoria"""
    nome: str
    descricao: str | None = None

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        if not v or len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        if len(v) > 50:
            raise ValueError("Nome deve ter no máximo 50 caracteres")
        return v.strip()


class CategoriaUpdateDTO(BaseModel):
    """DTO para atualização de categoria"""
    id_categoria: int
    nome: str
    descricao: str | None = None

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        if not v or len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        if len(v) > 50:
            raise ValueError("Nome deve ter no máximo 50 caracteres")
        return v.strip()
```

#### Arquivo: `dto/atividade_dto.py`

```python
from pydantic import BaseModel, field_validator


class AtividadeCreateDTO(BaseModel):
    """DTO para criação de atividade"""
    nome: str
    descricao: str | None = None
    duracao_minutos: int
    nivel_dificuldade: str
    equipamento_necessario: str | None = None
    id_categoria: int | None = None

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        if not v or len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return v.strip()

    @field_validator("duracao_minutos")
    @classmethod
    def validar_duracao(cls, v: int) -> int:
        if v < 15:
            raise ValueError("Duração mínima é de 15 minutos")
        if v > 240:
            raise ValueError("Duração máxima é de 240 minutos")
        return v

    @field_validator("nivel_dificuldade")
    @classmethod
    def validar_nivel(cls, v: str) -> str:
        niveis_validos = ["INICIANTE", "INTERMEDIÁRIO", "AVANÇADO"]
        v_upper = v.upper()
        if v_upper not in niveis_validos:
            raise ValueError(f"Nível deve ser um de: {', '.join(niveis_validos)}")
        return v_upper


class AtividadeUpdateDTO(BaseModel):
    """DTO para atualização de atividade"""
    id_atividade: int
    nome: str
    descricao: str | None = None
    duracao_minutos: int
    nivel_dificuldade: str
    equipamento_necessario: str | None = None
    id_categoria: int | None = None

    # (incluir os mesmos validators de AtividadeCreateDTO)
```

#### Arquivo: `dto/turma_dto.py`

```python
from pydantic import BaseModel, field_validator
from datetime import date


class TurmaCreateDTO(BaseModel):
    """DTO para criação de turma"""
    id_atividade: int
    id_professor: int
    nome: str
    descricao: str | None = None
    vagas: int
    horario: str
    dias_semana: str
    data_inicio: str  # Formato: YYYY-MM-DD
    data_fim: str | None = None
    ativa: bool = True

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        if not v or len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        return v.strip()

    @field_validator("vagas")
    @classmethod
    def validar_vagas(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Turma deve ter pelo menos 1 vaga")
        if v > 50:
            raise ValueError("Turma não pode ter mais de 50 vagas")
        return v

    @field_validator("dias_semana")
    @classmethod
    def validar_dias(cls, v: str) -> str:
        dias_validos = ["SEG", "TER", "QUA", "QUI", "SEX", "SAB", "DOM"]
        dias = [d.strip().upper() for d in v.split(",")]
        for dia in dias:
            if dia not in dias_validos:
                raise ValueError(f"Dia inválido: {dia}. Use: {', '.join(dias_validos)}")
        return v.upper()


class TurmaUpdateDTO(BaseModel):
    """DTO para atualização de turma"""
    id_turma: int
    id_atividade: int
    id_professor: int
    nome: str
    descricao: str | None = None
    vagas: int
    vagas_ocupadas: int
    horario: str
    dias_semana: str
    data_inicio: str
    data_fim: str | None = None
    ativa: bool

    # (incluir os mesmos validators de TurmaCreateDTO)
```

### 📝 Instruções para DTOs Restantes

Siga o mesmo padrão para criar:

1. **`dto/matricula_dto.py`**:
   - MatriculaCreateDTO (id_turma, id_aluno, data_matricula, observacoes)
   - MatriculaUpdateDTO (+ status)
   - Validar: status deve ser "ATIVA", "CANCELADA" ou "CONCLUÍDA"

2. **`dto/pagamento_dto.py`**:
   - PagamentoCreateDTO (id_matricula, valor, data_pagamento, forma_pagamento, comprovante)
   - PagamentoUpdateDTO (+ status_pagamento)
   - Validar: valor > 0, forma_pagamento em ["DINHEIRO", "CARTÃO", "PIX", "TRANSFERÊNCIA"]

3. **`dto/endereco_dto.py`**:
   - EnderecoCreateDTO (id_usuario, cep, logradouro, numero, complemento, bairro, cidade, estado)
   - EnderecoUpdateDTO (+ id_endereco)
   - Validar: CEP com 8 dígitos, estado com 2 letras

### ✅ Checklist

- [ ] `dto/categoria_dto.py` criado
- [ ] `dto/atividade_dto.py` criado
- [ ] `dto/turma_dto.py` criado
- [ ] `dto/matricula_dto.py` criado
- [ ] `dto/pagamento_dto.py` criado
- [ ] `dto/endereco_dto.py` criado
- [ ] Todos os validators implementados
- [ ] **Commit:** `feat(dto): criar DTOs para todas as novas entidades`

---

## 2.7 Seeds para Dados Iniciais

### 📝 Objetivo

Adicionar dados de exemplo (seeds) para categorias, atividades e turmas no arquivo `util/seed_data.py`, permitindo testar o sistema com dados realistas.

### 📍 Localização

- `util/seed_data.py` (arquivo existente, adicionar seeds)

### 💻 Código Completo

```python
# util/seed_data.py

# Adicionar imports
from repo import categoria_repo, atividade_repo, turma_repo
from model.categoria_model import Categoria
from model.atividade_model import Atividade
from model.turma_model import Turma
from datetime import date, timedelta


def seed_categorias():
    """Cria categorias de exemplo se não existirem"""
    categorias_existentes = categoria_repo.obter_todos()
    if len(categorias_existentes) > 0:
        logger.info("Categorias já existem, pulando seed")
        return

    categorias = [
        Categoria(nome="Musculação", descricao="Treinos de força e hipertrofia"),
        Categoria(nome="Cardio", descricao="Atividades aeróbicas e cardiovasculares"),
        Categoria(nome="Funcional", descricao="Treinos funcionais e mobilidade"),
        Categoria(nome="Lutas", descricao="Artes marciais e defesa pessoal"),
        Categoria(nome="Dança", descricao="Atividades rítmicas e coreografadas"),
    ]

    for cat in categorias:
        resultado = categoria_repo.inserir(cat)
        if resultado:
            logger.info(f"Categoria '{cat.nome}' criada com ID {resultado.id_categoria}")


def seed_atividades():
    """Cria atividades de exemplo se não existirem"""
    atividades_existentes = atividade_repo.obter_todos()
    if len(atividades_existentes) > 0:
        logger.info("Atividades já existem, pulando seed")
        return

    # Obter categorias para relacionamento
    categorias = categoria_repo.obter_todos()
    cat_dict = {cat.nome: cat.id_categoria for cat in categorias}

    atividades = [
        Atividade(
            nome="Musculação Livre",
            descricao="Treino livre de musculação com equipamentos",
            duracao_minutos=60,
            nivel_dificuldade="INTERMEDIÁRIO",
            equipamento_necessario="Halteres, barras, máquinas",
            id_categoria=cat_dict.get("Musculação")
        ),
        Atividade(
            nome="Crossfit",
            descricao="Treino funcional de alta intensidade",
            duracao_minutos=50,
            nivel_dificuldade="AVANÇADO",
            equipamento_necessario="Kettlebells, caixas, cordas",
            id_categoria=cat_dict.get("Funcional")
        ),
        Atividade(
            nome="Spinning",
            descricao="Ciclismo indoor com música",
            duracao_minutos=45,
            nivel_dificuldade="INTERMEDIÁRIO",
            equipamento_necessario="Bicicleta ergométrica",
            id_categoria=cat_dict.get("Cardio")
        ),
        Atividade(
            nome="Yoga",
            descricao="Práticas de yoga para flexibilidade e equilíbrio",
            duracao_minutos=60,
            nivel_dificuldade="INICIANTE",
            equipamento_necessario="Tapete de yoga",
            id_categoria=cat_dict.get("Funcional")
        ),
        Atividade(
            nome="Muay Thai",
            descricao="Arte marcial tailandesa",
            duracao_minutos=60,
            nivel_dificuldade="INTERMEDIÁRIO",
            equipamento_necessario="Luvas, protetor bucal, caneleiras",
            id_categoria=cat_dict.get("Lutas")
        ),
        Atividade(
            nome="Zumba",
            descricao="Dança fitness com ritmos latinos",
            duracao_minutos=50,
            nivel_dificuldade="INICIANTE",
            equipamento_necessario="Nenhum",
            id_categoria=cat_dict.get("Dança")
        ),
    ]

    for atv in atividades:
        resultado = atividade_repo.inserir(atv)
        if resultado:
            logger.info(f"Atividade '{atv.nome}' criada com ID {resultado.id_atividade}")


def seed_turmas():
    """Cria turmas de exemplo se não existirem"""
    turmas_existentes = turma_repo.obter_todos()
    if len(turmas_existentes) > 0:
        logger.info("Turmas já existem, pulando seed")
        return

    # Obter atividades e professores
    atividades = atividade_repo.obter_todos()
    atv_dict = {atv.nome: atv.id_atividade for atv in atividades}

    # Buscar professores (usuarios com perfil PROFESSOR)
    from util.perfis import Perfil
    professores = usuario_repo.obter_por_perfil(Perfil.PROFESSOR)

    if len(professores) == 0:
        logger.warning("Nenhum professor encontrado, criando professor exemplo")
        # Criar um professor exemplo
        from model.usuario_model import Usuario
        import bcrypt

        professor_exemplo = Usuario(
            nome="Prof. João Silva",
            email="joao.professor@agendafit.com",
            senha=bcrypt.hashpw("senha123".encode(), bcrypt.gensalt()).decode(),
            perfil=Perfil.PROFESSOR,
            data_nascimento="1985-05-15",
            numero_documento="123.456.789-00",
            telefone="(27) 98888-7777",
            confirmado=True
        )
        professor_exemplo = usuario_repo.inserir(professor_exemplo)
        professores = [professor_exemplo]

    # Usar primeiro professor para todas as turmas (pode expandir depois)
    id_professor = professores[0].id_usuario

    hoje = date.today()
    turmas = [
        Turma(
            nome="Musculação Manhã",
            descricao="Turma de musculação para o período da manhã",
            id_atividade=atv_dict.get("Musculação Livre"),
            id_professor=id_professor,
            vagas=20,
            vagas_ocupadas=0,
            horario="06:00 - 07:00",
            dias_semana="SEG,QUA,SEX",
            data_inicio=(hoje + timedelta(days=7)).isoformat(),
            data_fim=(hoje + timedelta(days=97)).isoformat(),
            ativa=True
        ),
        Turma(
            nome="Crossfit Noite",
            descricao="Crossfit para alunos avançados no período noturno",
            id_atividade=atv_dict.get("Crossfit"),
            id_professor=id_professor,
            vagas=15,
            vagas_ocupadas=0,
            horario="19:00 - 19:50",
            dias_semana="TER,QUI",
            data_inicio=(hoje + timedelta(days=7)).isoformat(),
            data_fim=(hoje + timedelta(days=97)).isoformat(),
            ativa=True
        ),
        Turma(
            nome="Spinning Tarde",
            descricao="Aula de spinning com música animada",
            id_atividade=atv_dict.get("Spinning"),
            id_professor=id_professor,
            vagas=25,
            vagas_ocupadas=0,
            horario="15:00 - 15:45",
            dias_semana="SEG,QUA,SEX",
            data_inicio=(hoje + timedelta(days=7)).isoformat(),
            data_fim=(hoje + timedelta(days=97)).isoformat(),
            ativa=True
        ),
        Turma(
            nome="Yoga Matinal",
            descricao="Yoga para iniciantes ao amanhecer",
            id_atividade=atv_dict.get("Yoga"),
            id_professor=id_professor,
            vagas=12,
            vagas_ocupadas=0,
            horario="07:00 - 08:00",
            dias_semana="TER,QUI,SAB",
            data_inicio=(hoje + timedelta(days=7)).isoformat(),
            data_fim=(hoje + timedelta(days=97)).isoformat(),
            ativa=True
        ),
    ]

    for turma in turmas:
        resultado = turma_repo.inserir(turma)
        if resultado:
            logger.info(f"Turma '{turma.nome}' criada com ID {resultado.id_turma}")


def inicializar_dados():
    """Função principal que chama todos os seeds em ordem"""
    try:
        # Seeds anteriores (admin, configuracoes, etc.)
        # ... código existente ...

        # Novos seeds
        logger.info("Iniciando seed de categorias...")
        seed_categorias()

        logger.info("Iniciando seed de atividades...")
        seed_atividades()

        logger.info("Iniciando seed de turmas...")
        seed_turmas()

        logger.info("Seeds concluídos com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao executar seeds: {e}", exc_info=True)
```

### ✅ Checklist

- [ ] Seeds de categorias implementados
- [ ] Seeds de atividades implementados (com relacionamento)
- [ ] Seeds de turmas implementados (com datas dinâmicas)
- [ ] Validação de existência (não duplicar seeds)
- [ ] Criação automática de professor se não existir
- [ ] Testar: `python main.py` e verificar logs
- [ ] **Commit:** `feat(seeds): adicionar seeds de categorias, atividades e turmas`

---

## 2.8 Testes dos Repositórios

### 📝 Objetivo

Testar manualmente todos os repositórios criados para garantir que as operações CRUD estão funcionando corretamente.

### 🧪 Roteiro de Testes

Execute o servidor e teste cada operação:

```bash
python main.py
```

Verifique nos logs:
1. ✅ Todas as tabelas foram criadas (categoria, atividade, turma, matricula, pagamento, endereco)
2. ✅ Seeds foram executados com sucesso
3. ✅ Nenhum erro de FK ou constraint

### 🐍 Teste via Python Console

Crie um arquivo `test_repos.py` temporário para testar:

```python
from repo import categoria_repo, atividade_repo, turma_repo, matricula_repo

# Teste 1: Listar categorias
print("=== CATEGORIAS ===")
categorias = categoria_repo.obter_todos()
for cat in categorias:
    print(f"- {cat.nome}: {cat.descricao}")

# Teste 2: Listar atividades com categoria
print("\n=== ATIVIDADES ===")
atividades = atividade_repo.obter_todos()
for atv in atividades:
    cat_nome = atv.categoria.nome if atv.categoria else "Sem categoria"
    print(f"- {atv.nome} ({cat_nome}) - {atv.duracao_minutos}min")

# Teste 3: Listar turmas com relacionamentos
print("\n=== TURMAS ===")
turmas = turma_repo.obter_todos()
for turma in turmas:
    print(f"- {turma.nome}")
    print(f"  Atividade: {turma.atividade.nome if turma.atividade else 'N/A'}")
    print(f"  Professor: {turma.professor.nome if turma.professor else 'N/A'}")
    print(f"  Vagas: {turma.vagas_ocupadas}/{turma.vagas}")

# Teste 4: Criar uma matrícula (se houver aluno e turma)
# from model.matricula_model import Matricula
# from datetime import date
# nova_matricula = Matricula(
#     id_turma=1,
#     id_aluno=2,  # Assumindo que existe um aluno com ID 2
#     data_matricula=date.today().isoformat(),
#     status="ATIVA"
# )
# resultado = matricula_repo.inserir(nova_matricula)
# print(f"\nMatrícula criada: {resultado.id_matricula if resultado else 'ERRO'}")

print("\n✅ Testes concluídos!")
```

Execute:
```bash
python test_repos.py
```

### ✅ Checklist

- [ ] Todas as tabelas criadas sem erro
- [ ] Seeds executados corretamente
- [ ] `test_repos.py` executa sem erros
- [ ] JOINs retornam objetos relacionados corretamente
- [ ] FKs impedem exclusão de registros referenciados
- [ ] **Commit:** `test(repos): validar funcionamento de todos os repositórios`

---

## 2.9 Limpeza de Código e Ajustes Finais

### 📝 Objetivo

Remover código desnecessário e garantir consistência em todo o projeto antes de avançar para as rotas.

### ✅ Tarefas de Limpeza

1. **Remover imports não utilizados** em `main.py`:
   ```python
   # Remover se não estiver mais usando tarefa_repo
   # from repo import tarefa_repo
   ```

2. **Verificar models não utilizados**:
   - Se `tarefa_model.py` ainda existe e não está sendo usado, excluir
   - Se `sql/tarefa_sql.py` ainda existe, excluir
   - Se `repo/tarefa_repo.py` ainda existe, excluir

3. **Atualizar imports em `repo/__init__.py`** (se existir):
   ```python
   from .usuario_repo import *
   from .configuracao_repo import *
   from .categoria_repo import *
   from .atividade_repo import *
   from .turma_repo import *
   from .matricula_repo import *
   from .pagamento_repo import *
   from .endereco_repo import *
   ```

4. **Verificar ordem de criação de tabelas** em `main.py`:
   ```python
   # Deve respeitar as dependências de FK:
   usuario_repo.criar_tabela()  # Primeiro
   configuracao_repo.criar_tabela()
   categoria_repo.criar_tabela()
   atividade_repo.criar_tabela()  # Depende de categoria
   turma_repo.criar_tabela()  # Depende de atividade e usuario
   matricula_repo.criar_tabela()  # Depende de turma e usuario
   pagamento_repo.criar_tabela()  # Depende de matricula
   endereco_repo.criar_tabela()  # Depende de usuario
   ```

5. **Documentar funções sem docstring**:
   - Adicionar docstrings em todas as funções dos repositórios
   - Seguir padrão: `"""Descrição breve da função"""`

6. **Verificar tratamento de erros**:
   - Todas as funções devem ter try/except
   - Logs apropriados em caso de erro
   - Retornar valores seguros (None, [], False) em caso de erro

### ✅ Checklist Final da Fase 2

- [ ] Código limpo e organizado
- [ ] Imports atualizados
- [ ] Ordem de criação de tabelas correta
- [ ] Todas as funções documentadas
- [ ] Tratamento de erros consistente
- [ ] **Commit:** `refactor(fase2): limpar código e ajustar estrutura`

---

## 📊 Progresso da Fase 2

✅ **Concluído:**
- 2.1 Repositório de Categoria
- 2.2 Repositório de Atividade
- 2.3 Repositório de Turma
- 2.4 Repositório de Matrícula
- 2.5 Repositórios de Pagamento e Endereço
- 2.6 DTOs para Novas Entidades
- 2.7 Seeds para Dados Iniciais
- 2.8 Testes dos Repositórios
- 2.9 Limpeza de Código

**Estimativa de tempo:** 40-50 horas
**Próxima fase:** FASE 3 - CRUDs Administrativos

---

# FASE 3: CRUDs ADMINISTRATIVOS

## 3.1 CRUD de Categorias (Admin)

### 📝 Objetivo

Criar interface completa de administração de categorias: listar, criar, editar e excluir categorias. Esta será a primeira implementação completa (Route + Template), servindo de modelo para as demais.

### 📍 Localização

- `routes/admin_categorias_routes.py` (novo arquivo)
- `templates/admin/categorias/` (nova pasta)
  - `listar.html`
  - `criar.html`
  - `editar.html`

### 💻 Código Completo

#### Arquivo: `routes/admin_categorias_routes.py`

```python
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth import obter_usuario_logado, exigir_admin
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro
from repo import categoria_repo
from dto.categoria_dto import CategoriaCreateDTO, CategoriaUpdateDTO
from model.categoria_model import Categoria
from util.logger_config import logger

router = APIRouter(prefix="/admin/categorias")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def listar_categorias(request: Request):
    """Lista todas as categorias"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        categorias = categoria_repo.obter_todos()
        return templates.TemplateResponse(
            "admin/categorias/listar.html",
            {
                "request": request,
                "usuario": usuario,
                "categorias": categorias
            }
        )
    except Exception as e:
        logger.error(f"Erro ao listar categorias: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar categorias")
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/criar")
async def exibir_form_criar(request: Request):
    """Exibe formulário de criação de categoria"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    return templates.TemplateResponse(
        "admin/categorias/criar.html",
        {
            "request": request,
            "usuario": usuario
        }
    )


@router.post("/criar")
async def criar_categoria(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(None)
):
    """Processa criação de nova categoria"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        # Validar com DTO
        dto = CategoriaCreateDTO(nome=nome, descricao=descricao)

        # Criar categoria
        nova_categoria = Categoria(
            nome=dto.nome,
            descricao=dto.descricao
        )

        resultado = categoria_repo.inserir(nova_categoria)

        if resultado:
            adicionar_mensagem_sucesso(request, f"Categoria '{nome}' criada com sucesso!")
            return RedirectResponse(
                "/admin/categorias",
                status_code=status.HTTP_303_SEE_OTHER
            )
        else:
            adicionar_mensagem_erro(request, "Erro ao criar categoria")
            return RedirectResponse(
                "/admin/categorias/criar",
                status_code=status.HTTP_303_SEE_OTHER
            )
    except ValueError as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse(
            "/admin/categorias/criar",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        logger.error(f"Erro ao criar categoria: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro inesperado ao criar categoria")
        return RedirectResponse(
            "/admin/categorias/criar",
            status_code=status.HTTP_303_SEE_OTHER
        )


@router.get("/{id_categoria}/editar")
async def exibir_form_editar(request: Request, id_categoria: int):
    """Exibe formulário de edição de categoria"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        categoria = categoria_repo.obter_por_id(id_categoria)

        if not categoria:
            adicionar_mensagem_erro(request, "Categoria não encontrada")
            return RedirectResponse(
                "/admin/categorias",
                status_code=status.HTTP_303_SEE_OTHER
            )

        return templates.TemplateResponse(
            "admin/categorias/editar.html",
            {
                "request": request,
                "usuario": usuario,
                "categoria": categoria
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar categoria para edição: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar categoria")
        return RedirectResponse(
            "/admin/categorias",
            status_code=status.HTTP_303_SEE_OTHER
        )


@router.post("/{id_categoria}/editar")
async def editar_categoria(
    request: Request,
    id_categoria: int,
    nome: str = Form(...),
    descricao: str = Form(None)
):
    """Processa edição de categoria"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        # Validar com DTO
        dto = CategoriaUpdateDTO(
            id_categoria=id_categoria,
            nome=nome,
            descricao=descricao
        )

        # Atualizar categoria
        categoria = Categoria(
            id_categoria=dto.id_categoria,
            nome=dto.nome,
            descricao=dto.descricao
        )

        sucesso = categoria_repo.atualizar(categoria)

        if sucesso:
            adicionar_mensagem_sucesso(request, f"Categoria '{nome}' atualizada com sucesso!")
            return RedirectResponse(
                "/admin/categorias",
                status_code=status.HTTP_303_SEE_OTHER
            )
        else:
            adicionar_mensagem_erro(request, "Erro ao atualizar categoria")
            return RedirectResponse(
                f"/admin/categorias/{id_categoria}/editar",
                status_code=status.HTTP_303_SEE_OTHER
            )
    except ValueError as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse(
            f"/admin/categorias/{id_categoria}/editar",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        logger.error(f"Erro ao editar categoria: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro inesperado ao editar categoria")
        return RedirectResponse(
            f"/admin/categorias/{id_categoria}/editar",
            status_code=status.HTTP_303_SEE_OTHER
        )


@router.post("/{id_categoria}/excluir")
async def excluir_categoria(request: Request, id_categoria: int):
    """Exclui uma categoria"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        # Verificar se categoria existe
        categoria = categoria_repo.obter_por_id(id_categoria)
        if not categoria:
            adicionar_mensagem_erro(request, "Categoria não encontrada")
            return RedirectResponse(
                "/admin/categorias",
                status_code=status.HTTP_303_SEE_OTHER
            )

        # Tentar excluir
        sucesso = categoria_repo.excluir(id_categoria)

        if sucesso:
            adicionar_mensagem_sucesso(request, f"Categoria '{categoria.nome}' excluída com sucesso!")
        else:
            adicionar_mensagem_erro(
                request,
                "Não foi possível excluir a categoria. Ela pode estar sendo usada por atividades."
            )

        return RedirectResponse(
            "/admin/categorias",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        logger.error(f"Erro ao excluir categoria: {e}", exc_info=True)
        adicionar_mensagem_erro(
            request,
            "Erro ao excluir categoria. Ela pode estar sendo usada por atividades."
        )
        return RedirectResponse(
            "/admin/categorias",
            status_code=status.HTTP_303_SEE_OTHER
        )
```

#### Arquivo: `templates/admin/categorias/listar.html`

```html
{% extends "base.html" %}

{% block title %}Categorias - Admin{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row mb-4">
        <div class="col">
            <h2>Gerenciar Categorias</h2>
            <p class="text-muted">Categorias de atividades disponíveis no sistema</p>
        </div>
        <div class="col-auto">
            <a href="/admin/categorias/criar" class="btn btn-primary">
                <i class="bi bi-plus-circle"></i> Nova Categoria
            </a>
        </div>
    </div>

    {% if categorias %}
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Descrição</th>
                            <th class="text-end">Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for categoria in categorias %}
                        <tr>
                            <td>{{ categoria.id_categoria }}</td>
                            <td><strong>{{ categoria.nome }}</strong></td>
                            <td>{{ categoria.descricao or '-' }}</td>
                            <td class="text-end">
                                <a href="/admin/categorias/{{ categoria.id_categoria }}/editar"
                                   class="btn btn-sm btn-outline-primary">
                                    <i class="bi bi-pencil"></i> Editar
                                </a>
                                <form method="post"
                                      action="/admin/categorias/{{ categoria.id_categoria }}/excluir"
                                      style="display: inline;"
                                      onsubmit="return confirm('Deseja realmente excluir esta categoria?');">
                                    <button type="submit" class="btn btn-sm btn-outline-danger">
                                        <i class="bi bi-trash"></i> Excluir
                                    </button>
                                </form>
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
        <i class="bi bi-info-circle"></i> Nenhuma categoria cadastrada ainda.
        <a href="/admin/categorias/criar">Criar primeira categoria</a>
    </div>
    {% endif %}

    <div class="mt-3">
        <a href="/admin" class="btn btn-secondary">
            <i class="bi bi-arrow-left"></i> Voltar ao Painel Admin
        </a>
    </div>
</div>
{% endblock %}
```

#### Arquivo: `templates/admin/categorias/criar.html`

```html
{% extends "base.html" %}

{% block title %}Nova Categoria - Admin{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Nova Categoria</h4>
                </div>
                <div class="card-body">
                    <form method="post" action="/admin/categorias/criar">
                        <div class="mb-3">
                            <label for="nome" class="form-label">Nome <span class="text-danger">*</span></label>
                            <input type="text"
                                   class="form-control"
                                   id="nome"
                                   name="nome"
                                   required
                                   maxlength="50"
                                   placeholder="Ex: Musculação">
                            <div class="form-text">Mínimo 3 caracteres, máximo 50</div>
                        </div>

                        <div class="mb-3">
                            <label for="descricao" class="form-label">Descrição</label>
                            <textarea class="form-control"
                                      id="descricao"
                                      name="descricao"
                                      rows="3"
                                      placeholder="Descreva brevemente esta categoria"></textarea>
                        </div>

                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="/admin/categorias" class="btn btn-secondary">
                                <i class="bi bi-x-circle"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-check-circle"></i> Criar Categoria
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

#### Arquivo: `templates/admin/categorias/editar.html`

```html
{% extends "base.html" %}

{% block title %}Editar Categoria - Admin{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Editar Categoria</h4>
                </div>
                <div class="card-body">
                    <form method="post" action="/admin/categorias/{{ categoria.id_categoria }}/editar">
                        <div class="mb-3">
                            <label for="nome" class="form-label">Nome <span class="text-danger">*</span></label>
                            <input type="text"
                                   class="form-control"
                                   id="nome"
                                   name="nome"
                                   required
                                   maxlength="50"
                                   value="{{ categoria.nome }}">
                        </div>

                        <div class="mb-3">
                            <label for="descricao" class="form-label">Descrição</label>
                            <textarea class="form-control"
                                      id="descricao"
                                      name="descricao"
                                      rows="3">{{ categoria.descricao or '' }}</textarea>
                        </div>

                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="/admin/categorias" class="btn btn-secondary">
                                <i class="bi bi-x-circle"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-check-circle"></i> Salvar Alterações
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 📝 Registrar Router no Main

```python
# main.py

# Adicionar import
from routes.admin_categorias_routes import router as admin_categorias_router

# Adicionar após outros routers admin
app.include_router(admin_categorias_router, tags=["Admin - Categorias"])
logger.info("Router admin de categorias incluído")
```

### ✅ Checklist

- [ ] `routes/admin_categorias_routes.py` criado
- [ ] `templates/admin/categorias/listar.html` criado
- [ ] `templates/admin/categorias/criar.html` criado
- [ ] `templates/admin/categorias/editar.html` criado
- [ ] Router registrado em `main.py`
- [ ] Testar: Acessar `/admin/categorias` como admin
- [ ] Testar: Criar nova categoria
- [ ] Testar: Editar categoria existente
- [ ] Testar: Excluir categoria
- [ ] Verificar validações do DTO
- [ ] Verificar proteção de FK (não excluir se houver atividades)
- [ ] **Commit:** `feat(admin): criar CRUD completo de categorias`

---

## 3.2 CRUD de Atividades (Admin)

### 📝 Objetivo

Criar interface completa de administração de atividades com relacionamento a categorias. Similar ao CRUD de categorias, mas com campos adicionais e seleção de categoria.

### 📍 Localização

- `routes/admin_atividades_routes.py` (novo arquivo)
- `templates/admin/atividades/` (nova pasta)
  - `listar.html`
  - `criar.html`
  - `editar.html`

### 💻 Código Completo

#### Arquivo: `routes/admin_atividades_routes.py`

```python
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth import obter_usuario_logado, exigir_admin
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro
from repo import atividade_repo, categoria_repo
from dto.atividade_dto import AtividadeCreateDTO, AtividadeUpdateDTO
from model.atividade_model import Atividade
from util.logger_config import logger

router = APIRouter(prefix="/admin/atividades")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def listar_atividades(request: Request):
    """Lista todas as atividades"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        atividades = atividade_repo.obter_todos()
        return templates.TemplateResponse(
            "admin/atividades/listar.html",
            {
                "request": request,
                "usuario": usuario,
                "atividades": atividades
            }
        )
    except Exception as e:
        logger.error(f"Erro ao listar atividades: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar atividades")
        return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/criar")
async def exibir_form_criar(request: Request):
    """Exibe formulário de criação de atividade"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        categorias = categoria_repo.obter_todos()
        return templates.TemplateResponse(
            "admin/atividades/criar.html",
            {
                "request": request,
                "usuario": usuario,
                "categorias": categorias
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar formulário: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar formulário")
        return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/criar")
async def criar_atividade(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(None),
    duracao_minutos: int = Form(...),
    nivel_dificuldade: str = Form(...),
    equipamento_necessario: str = Form(None),
    id_categoria: int = Form(None)
):
    """Processa criação de nova atividade"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        # Validar com DTO
        dto = AtividadeCreateDTO(
            nome=nome,
            descricao=descricao,
            duracao_minutos=duracao_minutos,
            nivel_dificuldade=nivel_dificuldade,
            equipamento_necessario=equipamento_necessario,
            id_categoria=id_categoria
        )

        # Criar atividade
        nova_atividade = Atividade(
            nome=dto.nome,
            descricao=dto.descricao,
            duracao_minutos=dto.duracao_minutos,
            nivel_dificuldade=dto.nivel_dificuldade,
            equipamento_necessario=dto.equipamento_necessario,
            id_categoria=dto.id_categoria
        )

        resultado = atividade_repo.inserir(nova_atividade)

        if resultado:
            adicionar_mensagem_sucesso(request, f"Atividade '{nome}' criada com sucesso!")
            return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)
        else:
            adicionar_mensagem_erro(request, "Erro ao criar atividade")
            return RedirectResponse("/admin/atividades/criar", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse("/admin/atividades/criar", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error(f"Erro ao criar atividade: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro inesperado ao criar atividade")
        return RedirectResponse("/admin/atividades/criar", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{id_atividade}/editar")
async def exibir_form_editar(request: Request, id_atividade: int):
    """Exibe formulário de edição de atividade"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        atividade = atividade_repo.obter_por_id(id_atividade)
        if not atividade:
            adicionar_mensagem_erro(request, "Atividade não encontrada")
            return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)

        categorias = categoria_repo.obter_todos()
        return templates.TemplateResponse(
            "admin/atividades/editar.html",
            {
                "request": request,
                "usuario": usuario,
                "atividade": atividade,
                "categorias": categorias
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar atividade para edição: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar atividade")
        return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/{id_atividade}/editar")
async def editar_atividade(
    request: Request,
    id_atividade: int,
    nome: str = Form(...),
    descricao: str = Form(None),
    duracao_minutos: int = Form(...),
    nivel_dificuldade: str = Form(...),
    equipamento_necessario: str = Form(None),
    id_categoria: int = Form(None)
):
    """Processa edição de atividade"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        # Validar com DTO
        dto = AtividadeUpdateDTO(
            id_atividade=id_atividade,
            nome=nome,
            descricao=descricao,
            duracao_minutos=duracao_minutos,
            nivel_dificuldade=nivel_dificuldade,
            equipamento_necessario=equipamento_necessario,
            id_categoria=id_categoria
        )

        # Atualizar atividade
        atividade = Atividade(
            id_atividade=dto.id_atividade,
            nome=dto.nome,
            descricao=dto.descricao,
            duracao_minutos=dto.duracao_minutos,
            nivel_dificuldade=dto.nivel_dificuldade,
            equipamento_necessario=dto.equipamento_necessario,
            id_categoria=dto.id_categoria
        )

        sucesso = atividade_repo.atualizar(atividade)

        if sucesso:
            adicionar_mensagem_sucesso(request, f"Atividade '{nome}' atualizada com sucesso!")
            return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)
        else:
            adicionar_mensagem_erro(request, "Erro ao atualizar atividade")
            return RedirectResponse(
                f"/admin/atividades/{id_atividade}/editar",
                status_code=status.HTTP_303_SEE_OTHER
            )
    except ValueError as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse(
            f"/admin/atividades/{id_atividade}/editar",
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        logger.error(f"Erro ao editar atividade: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro inesperado ao editar atividade")
        return RedirectResponse(
            f"/admin/atividades/{id_atividade}/editar",
            status_code=status.HTTP_303_SEE_OTHER
        )


@router.post("/{id_atividade}/excluir")
async def excluir_atividade(request: Request, id_atividade: int):
    """Exclui uma atividade"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        atividade = atividade_repo.obter_por_id(id_atividade)
        if not atividade:
            adicionar_mensagem_erro(request, "Atividade não encontrada")
            return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)

        sucesso = atividade_repo.excluir(id_atividade)

        if sucesso:
            adicionar_mensagem_sucesso(request, f"Atividade '{atividade.nome}' excluída com sucesso!")
        else:
            adicionar_mensagem_erro(
                request,
                "Não foi possível excluir a atividade. Ela pode estar sendo usada por turmas."
            )

        return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error(f"Erro ao excluir atividade: {e}", exc_info=True)
        adicionar_mensagem_erro(
            request,
            "Erro ao excluir atividade. Ela pode estar sendo usada por turmas."
        )
        return RedirectResponse("/admin/atividades", status_code=status.HTTP_303_SEE_OTHER)
```

#### Arquivo: `templates/admin/atividades/listar.html`

```html
{% extends "base.html" %}

{% block title %}Atividades - Admin{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row mb-4">
        <div class="col">
            <h2>Gerenciar Atividades</h2>
            <p class="text-muted">Atividades disponíveis no sistema</p>
        </div>
        <div class="col-auto">
            <a href="/admin/atividades/criar" class="btn btn-primary">
                <i class="bi bi-plus-circle"></i> Nova Atividade
            </a>
        </div>
    </div>

    {% if atividades %}
    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Categoria</th>
                            <th>Duração</th>
                            <th>Nível</th>
                            <th class="text-end">Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for atividade in atividades %}
                        <tr>
                            <td>{{ atividade.id_atividade }}</td>
                            <td><strong>{{ atividade.nome }}</strong></td>
                            <td>
                                {% if atividade.categoria %}
                                <span class="badge bg-secondary">{{ atividade.categoria.nome }}</span>
                                {% else %}
                                <span class="text-muted">-</span>
                                {% endif %}
                            </td>
                            <td>{{ atividade.duracao_minutos }} min</td>
                            <td>
                                {% if atividade.nivel_dificuldade == 'INICIANTE' %}
                                <span class="badge bg-success">Iniciante</span>
                                {% elif atividade.nivel_dificuldade == 'INTERMEDIÁRIO' %}
                                <span class="badge bg-warning">Intermediário</span>
                                {% elif atividade.nivel_dificuldade == 'AVANÇADO' %}
                                <span class="badge bg-danger">Avançado</span>
                                {% endif %}
                            </td>
                            <td class="text-end">
                                <a href="/admin/atividades/{{ atividade.id_atividade }}/editar"
                                   class="btn btn-sm btn-outline-primary">
                                    <i class="bi bi-pencil"></i> Editar
                                </a>
                                <form method="post"
                                      action="/admin/atividades/{{ atividade.id_atividade }}/excluir"
                                      style="display: inline;"
                                      onsubmit="return confirm('Deseja realmente excluir esta atividade?');">
                                    <button type="submit" class="btn btn-sm btn-outline-danger">
                                        <i class="bi bi-trash"></i> Excluir
                                    </button>
                                </form>
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
        <i class="bi bi-info-circle"></i> Nenhuma atividade cadastrada ainda.
        <a href="/admin/atividades/criar">Criar primeira atividade</a>
    </div>
    {% endif %}

    <div class="mt-3">
        <a href="/admin" class="btn btn-secondary">
            <i class="bi bi-arrow-left"></i> Voltar ao Painel Admin
        </a>
    </div>
</div>
{% endblock %}
```

#### Arquivo: `templates/admin/atividades/criar.html`

```html
{% extends "base.html" %}

{% block title %}Nova Atividade - Admin{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Nova Atividade</h4>
                </div>
                <div class="card-body">
                    <form method="post" action="/admin/atividades/criar">
                        <div class="mb-3">
                            <label for="nome" class="form-label">Nome <span class="text-danger">*</span></label>
                            <input type="text"
                                   class="form-control"
                                   id="nome"
                                   name="nome"
                                   required
                                   placeholder="Ex: Musculação Livre">
                        </div>

                        <div class="mb-3">
                            <label for="descricao" class="form-label">Descrição</label>
                            <textarea class="form-control"
                                      id="descricao"
                                      name="descricao"
                                      rows="3"
                                      placeholder="Descreva a atividade"></textarea>
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="duracao_minutos" class="form-label">Duração (minutos) <span class="text-danger">*</span></label>
                                <input type="number"
                                       class="form-control"
                                       id="duracao_minutos"
                                       name="duracao_minutos"
                                       required
                                       min="15"
                                       max="240"
                                       placeholder="60">
                                <div class="form-text">Entre 15 e 240 minutos</div>
                            </div>

                            <div class="col-md-6 mb-3">
                                <label for="nivel_dificuldade" class="form-label">Nível <span class="text-danger">*</span></label>
                                <select class="form-select"
                                        id="nivel_dificuldade"
                                        name="nivel_dificuldade"
                                        required>
                                    <option value="">Selecione...</option>
                                    <option value="INICIANTE">Iniciante</option>
                                    <option value="INTERMEDIÁRIO">Intermediário</option>
                                    <option value="AVANÇADO">Avançado</option>
                                </select>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="id_categoria" class="form-label">Categoria</label>
                            <select class="form-select"
                                    id="id_categoria"
                                    name="id_categoria">
                                <option value="">Sem categoria</option>
                                {% for categoria in categorias %}
                                <option value="{{ categoria.id_categoria }}">{{ categoria.nome }}</option>
                                {% endfor %}
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="equipamento_necessario" class="form-label">Equipamento Necessário</label>
                            <input type="text"
                                   class="form-control"
                                   id="equipamento_necessario"
                                   name="equipamento_necessario"
                                   placeholder="Ex: Halteres, barras, máquinas">
                        </div>

                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="/admin/atividades" class="btn btn-secondary">
                                <i class="bi bi-x-circle"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-check-circle"></i> Criar Atividade
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

#### Arquivo: `templates/admin/atividades/editar.html`

```html
{% extends "base.html" %}

{% block title %}Editar Atividade - Admin{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4 class="mb-0">Editar Atividade</h4>
                </div>
                <div class="card-body">
                    <form method="post" action="/admin/atividades/{{ atividade.id_atividade }}/editar">
                        <div class="mb-3">
                            <label for="nome" class="form-label">Nome <span class="text-danger">*</span></label>
                            <input type="text"
                                   class="form-control"
                                   id="nome"
                                   name="nome"
                                   required
                                   value="{{ atividade.nome }}">
                        </div>

                        <div class="mb-3">
                            <label for="descricao" class="form-label">Descrição</label>
                            <textarea class="form-control"
                                      id="descricao"
                                      name="descricao"
                                      rows="3">{{ atividade.descricao or '' }}</textarea>
                        </div>

                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="duracao_minutos" class="form-label">Duração (minutos) <span class="text-danger">*</span></label>
                                <input type="number"
                                       class="form-control"
                                       id="duracao_minutos"
                                       name="duracao_minutos"
                                       required
                                       min="15"
                                       max="240"
                                       value="{{ atividade.duracao_minutos }}">
                            </div>

                            <div class="col-md-6 mb-3">
                                <label for="nivel_dificuldade" class="form-label">Nível <span class="text-danger">*</span></label>
                                <select class="form-select"
                                        id="nivel_dificuldade"
                                        name="nivel_dificuldade"
                                        required>
                                    <option value="INICIANTE" {% if atividade.nivel_dificuldade == 'INICIANTE' %}selected{% endif %}>Iniciante</option>
                                    <option value="INTERMEDIÁRIO" {% if atividade.nivel_dificuldade == 'INTERMEDIÁRIO' %}selected{% endif %}>Intermediário</option>
                                    <option value="AVANÇADO" {% if atividade.nivel_dificuldade == 'AVANÇADO' %}selected{% endif %}>Avançado</option>
                                </select>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="id_categoria" class="form-label">Categoria</label>
                            <select class="form-select"
                                    id="id_categoria"
                                    name="id_categoria">
                                <option value="">Sem categoria</option>
                                {% for categoria in categorias %}
                                <option value="{{ categoria.id_categoria }}"
                                        {% if atividade.id_categoria == categoria.id_categoria %}selected{% endif %}>
                                    {{ categoria.nome }}
                                </option>
                                {% endfor %}
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="equipamento_necessario" class="form-label">Equipamento Necessário</label>
                            <input type="text"
                                   class="form-control"
                                   id="equipamento_necessario"
                                   name="equipamento_necessario"
                                   value="{{ atividade.equipamento_necessario or '' }}">
                        </div>

                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                            <a href="/admin/atividades" class="btn btn-secondary">
                                <i class="bi bi-x-circle"></i> Cancelar
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="bi bi-check-circle"></i> Salvar Alterações
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 📝 Registrar Router no Main

```python
# main.py

# Adicionar import
from routes.admin_atividades_routes import router as admin_atividades_router

# Adicionar após router de categorias
app.include_router(admin_atividades_router, tags=["Admin - Atividades"])
logger.info("Router admin de atividades incluído")
```

### ✅ Checklist

- [ ] `routes/admin_atividades_routes.py` criado
- [ ] `templates/admin/atividades/listar.html` criado
- [ ] `templates/admin/atividades/criar.html` criado
- [ ] `templates/admin/atividades/editar.html` criado
- [ ] Router registrado em `main.py`
- [ ] Testar CRUD completo de atividades
- [ ] Verificar seleção de categoria funcionando
- [ ] Verificar badges de nível no listagem
- [ ] **Commit:** `feat(admin): criar CRUD completo de atividades`

---

## 3.3 CRUD de Turmas (Admin)

### 📝 Objetivo

Criar interface completa de administração de turmas. Este é o CRUD mais complexo até agora, pois requer seleção de atividade, professor, validação de datas e gerenciamento de vagas.

### 📍 Localização

- `routes/admin_turmas_routes.py` (novo arquivo)
- `templates/admin/turmas/` (nova pasta)
  - `listar.html`
  - `criar.html`
  - `editar.html`
  - `detalhes.html` (visualizar alunos matriculados)

### 💻 Código Parcial - Instruções Detalhadas

Devido à complexidade deste CRUD, seguem as instruções detalhadas para implementação:

#### Arquivo: `routes/admin_turmas_routes.py`

**Estrutura da rota:**

1. **GET /admin/turmas** - Listar turmas
   - Obter todas as turmas com `turma_repo.obter_todos()`
   - Passar para template com informações de atividade, professor, vagas

2. **GET /admin/turmas/criar** - Formulário de criação
   - Obter lista de atividades: `atividade_repo.obter_todos()`
   - Obter lista de professores: `usuario_repo.obter_por_perfil(Perfil.PROFESSOR)`
   - Passar ambas para o template

3. **POST /admin/turmas/criar** - Processar criação
   - Campos do Form:
     - `nome`, `descricao`, `id_atividade`, `id_professor`
     - `vagas`, `horario`, `dias_semana`
     - `data_inicio`, `data_fim`, `ativa`
   - Validar com `TurmaCreateDTO`
   - Criar objeto `Turma` com `vagas_ocupadas=0`
   - Inserir com `turma_repo.inserir()`

4. **GET /admin/turmas/{id}/editar** - Formulário de edição
   - Obter turma específica
   - Obter listas de atividades e professores
   - Passar tudo para template

5. **POST /admin/turmas/{id}/editar** - Processar edição
   - Similar ao criar, mas usando `TurmaUpdateDTO`
   - Atenção: manter `vagas_ocupadas` atual (não permitir edição manual)

6. **POST /admin/turmas/{id}/excluir** - Excluir turma
   - Verificar se há matrículas: `matricula_repo.obter_por_turma(id_turma)`
   - Se houver matrículas ativas, impedir exclusão
   - Se não houver, excluir com `turma_repo.excluir()`

7. **GET /admin/turmas/{id}/detalhes** - Ver detalhes e alunos matriculados
   - Obter turma completa
   - Obter matrículas: `matricula_repo.obter_por_turma(id_turma)`
   - Mostrar lista de alunos, datas, status

**Exemplo de código inicial:**

```python
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth import obter_usuario_logado, exigir_admin
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro
from repo import turma_repo, atividade_repo, usuario_repo, matricula_repo
from dto.turma_dto import TurmaCreateDTO, TurmaUpdateDTO
from model.turma_model import Turma
from util.perfis import Perfil
from util.logger_config import logger

router = APIRouter(prefix="/admin/turmas")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def listar_turmas(request: Request):
    """Lista todas as turmas"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        turmas = turma_repo.obter_todos()
        return templates.TemplateResponse(
            "admin/turmas/listar.html",
            {
                "request": request,
                "usuario": usuario,
                "turmas": turmas
            }
        )
    except Exception as e:
        logger.error(f"Erro ao listar turmas: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar turmas")
        return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/criar")
async def exibir_form_criar(request: Request):
    """Exibe formulário de criação de turma"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        atividades = atividade_repo.obter_todos()
        professores = usuario_repo.obter_por_perfil(Perfil.PROFESSOR)

        return templates.TemplateResponse(
            "admin/turmas/criar.html",
            {
                "request": request,
                "usuario": usuario,
                "atividades": atividades,
                "professores": professores
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar formulário: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar formulário")
        return RedirectResponse("/admin/turmas", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/criar")
async def criar_turma(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(None),
    id_atividade: int = Form(...),
    id_professor: int = Form(...),
    vagas: int = Form(...),
    horario: str = Form(...),
    dias_semana: str = Form(...),
    data_inicio: str = Form(...),
    data_fim: str = Form(None),
    ativa: bool = Form(True)
):
    """Processa criação de nova turma"""
    usuario = obter_usuario_logado(request)
    exigir_admin(usuario)

    try:
        # Validar com DTO
        dto = TurmaCreateDTO(
            nome=nome,
            descricao=descricao,
            id_atividade=id_atividade,
            id_professor=id_professor,
            vagas=vagas,
            horario=horario,
            dias_semana=dias_semana,
            data_inicio=data_inicio,
            data_fim=data_fim,
            ativa=ativa
        )

        # Criar turma
        nova_turma = Turma(
            nome=dto.nome,
            descricao=dto.descricao,
            id_atividade=dto.id_atividade,
            id_professor=dto.id_professor,
            vagas=dto.vagas,
            vagas_ocupadas=0,  # Sempre inicia com 0
            horario=dto.horario,
            dias_semana=dto.dias_semana,
            data_inicio=dto.data_inicio,
            data_fim=dto.data_fim,
            ativa=dto.ativa
        )

        resultado = turma_repo.inserir(nova_turma)

        if resultado:
            adicionar_mensagem_sucesso(request, f"Turma '{nome}' criada com sucesso!")
            return RedirectResponse("/admin/turmas", status_code=status.HTTP_303_SEE_OTHER)
        else:
            adicionar_mensagem_erro(request, "Erro ao criar turma")
            return RedirectResponse("/admin/turmas/criar", status_code=status.HTTP_303_SEE_OTHER)
    except ValueError as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse("/admin/turmas/criar", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error(f"Erro ao criar turma: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro inesperado ao criar turma")
        return RedirectResponse("/admin/turmas/criar", status_code=status.HTTP_303_SEE_OTHER)


# CONTINUAR com as demais rotas seguindo o mesmo padrão...
# - GET /{id}/editar
# - POST /{id}/editar
# - POST /{id}/excluir
# - GET /{id}/detalhes
```

#### Template: `templates/admin/turmas/listar.html`

**Elementos importantes:**

- Tabela com colunas: ID, Nome, Atividade, Professor, Horário, Vagas (ocupadas/total), Status (Ativa/Inativa)
- Badge verde para turmas ativas, cinza para inativas
- Badge azul mostrando vagas disponíveis
- Botões: Ver Detalhes, Editar, Excluir
- Link para criar nova turma

**Exemplo de linha da tabela:**

```html
<tr>
    <td>{{ turma.id_turma }}</td>
    <td><strong>{{ turma.nome }}</strong></td>
    <td>{{ turma.atividade.nome if turma.atividade else '-' }}</td>
    <td>{{ turma.professor.nome if turma.professor else '-' }}</td>
    <td>{{ turma.horario }}<br><small class="text-muted">{{ turma.dias_semana }}</small></td>
    <td>
        <span class="badge bg-info">
            {{ turma.vagas_ocupadas }}/{{ turma.vagas }} vagas
        </span>
    </td>
    <td>
        {% if turma.ativa %}
        <span class="badge bg-success">Ativa</span>
        {% else %}
        <span class="badge bg-secondary">Inativa</span>
        {% endif %}
    </td>
    <td class="text-end">
        <a href="/admin/turmas/{{ turma.id_turma }}/detalhes" class="btn btn-sm btn-outline-info">
            <i class="bi bi-eye"></i> Detalhes
        </a>
        <a href="/admin/turmas/{{ turma.id_turma }}/editar" class="btn btn-sm btn-outline-primary">
            <i class="bi bi-pencil"></i> Editar
        </a>
        <form method="post" action="/admin/turmas/{{ turma.id_turma }}/excluir" style="display: inline;">
            <button type="submit" class="btn btn-sm btn-outline-danger">
                <i class="bi bi-trash"></i> Excluir
            </button>
        </form>
    </td>
</tr>
```

#### Template: `templates/admin/turmas/criar.html`

**Campos do formulário:**

1. Nome da turma (text, required)
2. Descrição (textarea)
3. Atividade (select com lista de atividades, required)
4. Professor (select com lista de professores, required)
5. Número de vagas (number, min=1, max=50, required)
6. Horário (text, ex: "06:00 - 07:00", required)
7. Dias da semana (text ou checkboxes, ex: "SEG,QUA,SEX", required)
8. Data de início (date, required)
9. Data de fim (date, optional)
10. Ativa (checkbox, default checked)

**Validações no HTML:**
- Duração de vagas: min="1" max="50"
- Datas: usar input type="date"
- Dias: validar formato (pode usar JavaScript para adicionar checkboxes)

#### Template: `templates/admin/turmas/detalhes.html`

**Seções:**

1. **Informações da Turma** (card com todos os dados)
2. **Lista de Alunos Matriculados** (tabela)
   - Colunas: Nome do Aluno, Email, Data Matrícula, Status
   - Se não houver alunos: "Nenhum aluno matriculado ainda"
3. **Estatísticas:**
   - Total de vagas
   - Vagas ocupadas
   - Vagas disponíveis
   - Taxa de ocupação (%)

### ✅ Checklist

- [ ] `routes/admin_turmas_routes.py` criado com todas as rotas
- [ ] `templates/admin/turmas/listar.html` criado
- [ ] `templates/admin/turmas/criar.html` criado com todos os campos
- [ ] `templates/admin/turmas/editar.html` criado
- [ ] `templates/admin/turmas/detalhes.html` criado
- [ ] Router registrado em `main.py`
- [ ] Testar criação de turma com atividade e professor
- [ ] Testar edição mantendo vagas_ocupadas
- [ ] Testar que não é possível excluir turma com matrículas
- [ ] Testar visualização de detalhes e alunos
- [ ] **Commit:** `feat(admin): criar CRUD completo de turmas`

---

## 3.4 Painel Administrativo Principal

### 📝 Objetivo

Criar/atualizar o painel administrativo principal (`/admin`) com cards de acesso rápido a todas as funcionalidades administrativas e estatísticas do sistema.

### 📍 Localização

- `templates/admin/index.html` (atualizar ou criar)
- Rota já deve existir em `routes/admin_*.py`

### 💻 Estrutura do Painel

**Seções do painel:**

1. **Cards de Navegação Rápida:**
   - Gerenciar Categorias
   - Gerenciar Atividades
   - Gerenciar Turmas
   - Gerenciar Usuários
   - Gerenciar Matrículas
   - Configurações do Sistema
   - Backups

2. **Estatísticas (Dashboard):**
   - Total de usuários (por perfil: Alunos, Professores)
   - Total de categorias
   - Total de atividades
   - Total de turmas (ativas/inativas)
   - Total de matrículas (ativas)
   - Turmas com mais alunos
   - Atividades mais populares

3. **Atalhos Rápidos:**
   - Criar nova turma
   - Adicionar atividade
   - Ver todas as matrículas pendentes
   - Gerar relatório

**Exemplo de card:**

```html
<div class="col-md-4 mb-3">
    <div class="card h-100">
        <div class="card-body text-center">
            <i class="bi bi-grid-3x3-gap display-4 text-primary"></i>
            <h5 class="card-title mt-3">Categorias</h5>
            <p class="card-text">Gerenciar categorias de atividades</p>
            <a href="/admin/categorias" class="btn btn-primary">Acessar</a>
        </div>
    </div>
</div>
```

**Para obter estatísticas:**

```python
# No handler da rota /admin
total_alunos = len(usuario_repo.obter_por_perfil(Perfil.ALUNO))
total_professores = len(usuario_repo.obter_por_perfil(Perfil.PROFESSOR))
total_categorias = len(categoria_repo.obter_todos())
total_atividades = len(atividade_repo.obter_todos())
turmas_ativas = turma_repo.obter_ativas()
matriculas_ativas = matricula_repo.obter_por_status("ATIVA")
```

### ✅ Checklist

- [ ] Painel admin atualizado com cards de navegação
- [ ] Estatísticas sendo calculadas e exibidas
- [ ] Ícones Bootstrap Icons apropriados
- [ ] Layout responsivo (Bootstrap grid)
- [ ] Links funcionando para todas as seções
- [ ] **Commit:** `feat(admin): atualizar painel administrativo com estatísticas`

---

## 3.5 Ajustes no Menu de Navegação

### 📝 Objetivo

Atualizar o menu de navegação (navbar) para incluir links para as novas seções administrativas, com visibilidade condicional baseada no perfil do usuário.

### 📍 Localização

- `templates/base.html` ou `templates/includes/navbar.html`

### 💻 Estrutura do Menu

**Menu para Administradores:**

```html
{% if usuario and usuario.perfil == 'Administrador' %}
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
        <i class="bi bi-gear"></i> Administração
    </a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="/admin">
            <i class="bi bi-speedometer2"></i> Painel Admin
        </a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="/admin/categorias">
            <i class="bi bi-grid-3x3-gap"></i> Categorias
        </a></li>
        <li><a class="dropdown-item" href="/admin/atividades">
            <i class="bi bi-activity"></i> Atividades
        </a></li>
        <li><a class="dropdown-item" href="/admin/turmas">
            <i class="bi bi-people"></i> Turmas
        </a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="/admin/usuarios">
            <i class="bi bi-person-badge"></i> Usuários
        </a></li>
        <li><a class="dropdown-item" href="/admin/configuracoes">
            <i class="bi bi-sliders"></i> Configurações
        </a></li>
        <li><a class="dropdown-item" href="/admin/backups">
            <i class="bi bi-cloud-arrow-down"></i> Backups
        </a></li>
    </ul>
</li>
{% endif %}
```

**Menu para Professores:**

```html
{% if usuario and usuario.perfil == 'Professor' %}
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
        <i class="bi bi-journal-text"></i> Professor
    </a>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="/professor">
            <i class="bi bi-speedometer2"></i> Meu Painel
        </a></li>
        <li><a class="dropdown-item" href="/professor/turmas">
            <i class="bi bi-people"></i> Minhas Turmas
        </a></li>
        <li><a class="dropdown-item" href="/professor/presencas">
            <i class="bi bi-check2-square"></i> Registrar Presenças
        </a></li>
        <li><a class="dropdown-item" href="/professor/avaliacoes">
            <i class="bi bi-clipboard-data"></i> Avaliações Físicas
        </a></li>
    </ul>
</li>
{% endif %}
```

**Menu para Alunos:**

```html
{% if usuario and usuario.perfil == 'Aluno' %}
<li class="nav-item">
    <a class="nav-link" href="/aluno">
        <i class="bi bi-house-door"></i> Meu Painel
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" href="/aluno/turmas">
        <i class="bi bi-calendar3"></i> Minhas Turmas
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" href="/aluno/matricular">
        <i class="bi bi-plus-circle"></i> Matricular-se
    </a>
</li>
{% endif %}
```

### ✅ Checklist

- [ ] Menu atualizado com links para admin
- [ ] Dropdowns funcionando (Bootstrap JS carregado)
- [ ] Visibilidade condicional por perfil
- [ ] Ícones apropriados
- [ ] Links ativos destacados (active class)
- [ ] **Commit:** `feat(nav): atualizar menu de navegação com novas seções`

---

## 📊 Progresso da Fase 3

✅ **Concluído:**
- 3.1 CRUD de Categorias (Admin) - Completo
- 3.2 CRUD de Atividades (Admin) - Completo
- 3.3 CRUD de Turmas (Admin) - Instruções detalhadas
- 3.4 Painel Administrativo - Instruções
- 3.5 Menu de Navegação - Instruções

🔄 **Em Progresso:**
- Implementar rotas e templates restantes de Turmas
- Implementar painel admin com estatísticas

⏳ **Pendente:**
- Área do Aluno (Fase 4)
- Área do Professor (Fase 5)
- Sistemas Avançados (Fase 6)

**Estimativa de tempo Fase 3:** 50-60 horas
**Próxima fase:** FASE 4 - Área do Aluno

---

# FASE 4: ÁREA DO ALUNO

## 4.1 Dashboard do Aluno

### 📝 Objetivo

Criar o painel principal do aluno com visão geral de suas turmas, próximas aulas, estatísticas pessoais e atalhos rápidos.

### 📍 Localização

- `routes/aluno_routes.py` (novo arquivo ou expandir existente)
- `templates/aluno/` (nova pasta)
  - `dashboard.html`

### 💻 Estrutura do Dashboard

**Seções do dashboard:**

1. **Boas-vindas e informações do perfil:**
   - Nome do aluno
   - Próximas aulas de hoje
   - Mensagem motivacional

2. **Cards de estatísticas:**
   - Total de turmas matriculadas (ativas)
   - Próxima aula (nome da turma, horário)
   - Taxa de presença (%)
   - Avaliações físicas realizadas

3. **Minhas Turmas Ativas:**
   - Lista resumida das turmas matriculadas
   - Nome da turma, atividade, horário, dias
   - Botão "Ver todas as turmas"

4. **Atalhos rápidos:**
   - Matricular-se em nova turma
   - Ver histórico de presenças
   - Agendar avaliação física
   - Ver pagamentos

### 💻 Código da Rota

```python
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth import obter_usuario_logado, exigir_aluno
from util.mensagens import adicionar_mensagem_erro
from repo import matricula_repo, turma_repo
from util.logger_config import logger

router = APIRouter(prefix="/aluno")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def dashboard_aluno(request: Request):
    """Dashboard principal do aluno"""
    usuario = obter_usuario_logado(request)
    exigir_aluno(usuario)

    try:
        # Obter matrículas ativas do aluno
        matriculas = matricula_repo.obter_por_aluno(usuario.id_usuario)
        matriculas_ativas = [m for m in matriculas if m.status == "ATIVA"]

        # Obter turmas ativas disponíveis para matrícula
        turmas_disponiveis = turma_repo.obter_com_vagas()

        # Calcular estatísticas
        total_turmas = len(matriculas_ativas)

        # Próxima aula (primeira turma ativa)
        proxima_aula = None
        if matriculas_ativas:
            proxima_aula = matriculas_ativas[0].turma

        return templates.TemplateResponse(
            "aluno/dashboard.html",
            {
                "request": request,
                "usuario": usuario,
                "matriculas_ativas": matriculas_ativas,
                "total_turmas": total_turmas,
                "proxima_aula": proxima_aula,
                "turmas_disponiveis_count": len(turmas_disponiveis)
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar dashboard do aluno: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar dashboard")
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
```

### 💻 Template Exemplo

```html
{% extends "base.html" %}

{% block title %}Meu Painel - Aluno{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Boas-vindas -->
    <div class="row mb-4">
        <div class="col">
            <h2>Olá, {{ usuario.nome }}! 👋</h2>
            <p class="text-muted">Bem-vindo ao seu painel de aluno</p>
        </div>
    </div>

    <!-- Cards de Estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="bi bi-people-fill display-4 text-primary"></i>
                    <h5 class="card-title mt-2">{{ total_turmas }}</h5>
                    <p class="card-text text-muted">Turmas Ativas</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="bi bi-clock-fill display-4 text-success"></i>
                    <h5 class="card-title mt-2">
                        {% if proxima_aula %}
                        {{ proxima_aula.horario }}
                        {% else %}
                        -
                        {% endif %}
                    </h5>
                    <p class="card-text text-muted">Próxima Aula</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="bi bi-check2-circle display-4 text-info"></i>
                    <h5 class="card-title mt-2">--%</h5>
                    <p class="card-text text-muted">Presença</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <i class="bi bi-clipboard-data display-4 text-warning"></i>
                    <h5 class="card-title mt-2">--</h5>
                    <p class="card-text text-muted">Avaliações</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Minhas Turmas -->
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Minhas Turmas</h5>
                    <a href="/aluno/turmas" class="btn btn-sm btn-primary">Ver Todas</a>
                </div>
                <div class="card-body">
                    {% if matriculas_ativas %}
                    <div class="list-group">
                        {% for matricula in matriculas_ativas[:5] %}
                        <a href="/aluno/turmas/{{ matricula.turma.id_turma }}" class="list-group-item list-group-item-action">
                            <div class="d-flex w-100 justify-content-between">
                                <h6 class="mb-1">{{ matricula.turma.nome }}</h6>
                                <small class="text-muted">{{ matricula.turma.horario }}</small>
                            </div>
                            <p class="mb-1">
                                <strong>Atividade:</strong> {{ matricula.turma.atividade.nome if matricula.turma.atividade else '-' }}
                            </p>
                            <small class="text-muted">{{ matricula.turma.dias_semana }}</small>
                        </a>
                        {% endfor %}
                    </div>
                    {% else %}
                    <div class="alert alert-info">
                        <i class="bi bi-info-circle"></i> Você ainda não está matriculado em nenhuma turma.
                        <a href="/aluno/matricular">Matricule-se agora!</a>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Atalhos Rápidos -->
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Atalhos Rápidos</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="/aluno/matricular" class="btn btn-primary">
                            <i class="bi bi-plus-circle"></i> Matricular-se
                        </a>
                        <a href="/aluno/turmas" class="btn btn-outline-secondary">
                            <i class="bi bi-calendar3"></i> Minhas Turmas
                        </a>
                        <a href="/aluno/presencas" class="btn btn-outline-secondary">
                            <i class="bi bi-check2-square"></i> Presenças
                        </a>
                        <a href="/perfil" class="btn btn-outline-secondary">
                            <i class="bi bi-person"></i> Meu Perfil
                        </a>
                    </div>
                </div>
            </div>

            {% if turmas_disponiveis_count > 0 %}
            <div class="card mt-3">
                <div class="card-body text-center">
                    <i class="bi bi-star-fill text-warning display-4"></i>
                    <h5 class="mt-2">{{ turmas_disponiveis_count }} turmas</h5>
                    <p class="text-muted">com vagas disponíveis</p>
                    <a href="/aluno/matricular" class="btn btn-sm btn-warning">Ver Turmas</a>
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### ✅ Checklist

- [ ] Rota `/aluno` criada
- [ ] Dashboard exibindo estatísticas
- [ ] Lista de turmas matriculadas funcionando
- [ ] Atalhos rápidos com links corretos
- [ ] Função `exigir_aluno()` implementada em `util/auth.py`
- [ ] **Commit:** `feat(aluno): criar dashboard do aluno`

---

## 4.2 Sistema de Matrícula

### 📝 Objetivo

Permitir que o aluno visualize turmas disponíveis e se matricule nelas, com validações de vagas e conflitos de horário.

### 📍 Localização

- `routes/aluno_routes.py` (adicionar rotas)
- `templates/aluno/matricular.html`
- `templates/aluno/turma_detalhes.html`

### 💻 Rotas de Matrícula

```python
from datetime import date

@router.get("/matricular")
async def listar_turmas_disponiveis(request: Request):
    """Lista turmas disponíveis para matrícula"""
    usuario = obter_usuario_logado(request)
    exigir_aluno(usuario)

    try:
        # Obter turmas com vagas
        turmas_disponiveis = turma_repo.obter_com_vagas()

        # Obter IDs das turmas em que o aluno já está matriculado
        matriculas_aluno = matricula_repo.obter_por_aluno(usuario.id_usuario)
        ids_turmas_matriculadas = [m.id_turma for m in matriculas_aluno if m.status == "ATIVA"]

        # Filtrar turmas já matriculadas
        turmas_para_mostrar = [t for t in turmas_disponiveis if t.id_turma not in ids_turmas_matriculadas]

        return templates.TemplateResponse(
            "aluno/matricular.html",
            {
                "request": request,
                "usuario": usuario,
                "turmas": turmas_para_mostrar
            }
        )
    except Exception as e:
        logger.error(f"Erro ao listar turmas disponíveis: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar turmas")
        return RedirectResponse("/aluno", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/turmas/{id_turma}/detalhes")
async def ver_detalhes_turma(request: Request, id_turma: int):
    """Ver detalhes de uma turma antes de matricular"""
    usuario = obter_usuario_logado(request)
    exigir_aluno(usuario)

    try:
        turma = turma_repo.obter_por_id(id_turma)
        if not turma:
            adicionar_mensagem_erro(request, "Turma não encontrada")
            return RedirectResponse("/aluno/matricular", status_code=status.HTTP_303_SEE_OTHER)

        # Verificar se já está matriculado
        ja_matriculado = matricula_repo.verificar_matricula_existente(id_turma, usuario.id_usuario)

        # Calcular vagas disponíveis
        vagas_disponiveis = turma.vagas - turma.vagas_ocupadas

        return templates.TemplateResponse(
            "aluno/turma_detalhes.html",
            {
                "request": request,
                "usuario": usuario,
                "turma": turma,
                "ja_matriculado": ja_matriculado,
                "vagas_disponiveis": vagas_disponiveis
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar detalhes da turma: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar turma")
        return RedirectResponse("/aluno/matricular", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/turmas/{id_turma}/matricular")
async def processar_matricula(request: Request, id_turma: int):
    """Processa a matrícula do aluno em uma turma"""
    usuario = obter_usuario_logado(request)
    exigir_aluno(usuario)

    try:
        # Verificar se turma existe
        turma = turma_repo.obter_por_id(id_turma)
        if not turma:
            adicionar_mensagem_erro(request, "Turma não encontrada")
            return RedirectResponse("/aluno/matricular", status_code=status.HTTP_303_SEE_OTHER)

        # Verificar se turma está ativa
        if not turma.ativa:
            adicionar_mensagem_erro(request, "Esta turma não está mais ativa")
            return RedirectResponse("/aluno/matricular", status_code=status.HTTP_303_SEE_OTHER)

        # Verificar se há vagas
        if turma.vagas_ocupadas >= turma.vagas:
            adicionar_mensagem_erro(request, "Esta turma não tem mais vagas disponíveis")
            return RedirectResponse("/aluno/matricular", status_code=status.HTTP_303_SEE_OTHER)

        # Verificar se já está matriculado
        if matricula_repo.verificar_matricula_existente(id_turma, usuario.id_usuario):
            adicionar_mensagem_erro(request, "Você já está matriculado nesta turma")
            return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)

        # Criar matrícula
        from model.matricula_model import Matricula
        nova_matricula = Matricula(
            id_turma=id_turma,
            id_aluno=usuario.id_usuario,
            data_matricula=date.today().isoformat(),
            status="ATIVA",
            observacoes=""
        )

        resultado = matricula_repo.inserir(nova_matricula)

        if resultado:
            # Incrementar vagas ocupadas
            turma_repo.incrementar_vagas_ocupadas(id_turma)

            adicionar_mensagem_sucesso(request, f"Matrícula realizada com sucesso na turma '{turma.nome}'!")
            return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)
        else:
            adicionar_mensagem_erro(request, "Erro ao processar matrícula")
            return RedirectResponse("/aluno/matricular", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        logger.error(f"Erro ao processar matrícula: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao processar matrícula")
        return RedirectResponse("/aluno/matricular", status_code=status.HTTP_303_SEE_OTHER)
```

### 📝 Implementar Função `exigir_aluno()`

Adicionar em `util/auth.py`:

```python
def exigir_aluno(usuario: Optional[Usuario]) -> None:
    """Verifica se o usuário é um aluno"""
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado"
        )
    if usuario.perfil != Perfil.ALUNO:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas alunos podem acessar esta página."
        )
```

### 💻 Templates

#### `templates/aluno/matricular.html`

**Elementos principais:**
- Cards das turmas disponíveis
- Informações: nome, atividade, professor, horário, dias, vagas
- Botão "Ver Detalhes" e "Matricular-se"
- Filtros (por categoria, nível, dias da semana)

#### `templates/aluno/turma_detalhes.html`

**Seções:**
1. Informações completas da turma
2. Dados do professor
3. Detalhes da atividade (duração, nível, equipamentos)
4. Horários e dias
5. Vagas disponíveis
6. Botão grande "Matricular-se" (se disponível)
7. Botão de voltar

### ✅ Checklist

- [ ] Rotas de matrícula implementadas
- [ ] Validações de vagas funcionando
- [ ] Verificação de matrícula duplicada
- [ ] Incremento de vagas ocupadas automático
- [ ] Templates criados
- [ ] Função `exigir_aluno()` implementada
- [ ] **Commit:** `feat(aluno): implementar sistema de matrícula`

---

## 4.3 Minhas Turmas

### 📝 Objetivo

Exibir lista completa das turmas em que o aluno está matriculado, com opção de cancelar matrícula.

### 📍 Localização

- `routes/aluno_routes.py` (adicionar rotas)
- `templates/aluno/minhas_turmas.html`

### 💻 Rotas

```python
@router.get("/turmas")
async def listar_minhas_turmas(request: Request):
    """Lista todas as turmas do aluno"""
    usuario = obter_usuario_logado(request)
    exigir_aluno(usuario)

    try:
        matriculas = matricula_repo.obter_por_aluno(usuario.id_usuario)

        # Separar por status
        matriculas_ativas = [m for m in matriculas if m.status == "ATIVA"]
        matriculas_canceladas = [m for m in matriculas if m.status == "CANCELADA"]

        return templates.TemplateResponse(
            "aluno/minhas_turmas.html",
            {
                "request": request,
                "usuario": usuario,
                "matriculas_ativas": matriculas_ativas,
                "matriculas_canceladas": matriculas_canceladas
            }
        )
    except Exception as e:
        logger.error(f"Erro ao listar turmas do aluno: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar turmas")
        return RedirectResponse("/aluno", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/turmas/{id_matricula}/cancelar")
async def cancelar_matricula(request: Request, id_matricula: int):
    """Cancela uma matrícula"""
    usuario = obter_usuario_logado(request)
    exigir_aluno(usuario)

    try:
        # Verificar se a matrícula existe e pertence ao aluno
        matricula = matricula_repo.obter_por_id(id_matricula)
        if not matricula or matricula.id_aluno != usuario.id_usuario:
            adicionar_mensagem_erro(request, "Matrícula não encontrada")
            return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)

        # Verificar se já está cancelada
        if matricula.status == "CANCELADA":
            adicionar_mensagem_erro(request, "Esta matrícula já foi cancelada")
            return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)

        # Atualizar status para cancelada
        sucesso = matricula_repo.atualizar_status(id_matricula, "CANCELADA")

        if sucesso:
            # Decrementar vagas ocupadas
            turma_repo.decrementar_vagas_ocupadas(matricula.id_turma)

            adicionar_mensagem_sucesso(request, "Matrícula cancelada com sucesso")
        else:
            adicionar_mensagem_erro(request, "Erro ao cancelar matrícula")

        return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        logger.error(f"Erro ao cancelar matrícula: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao cancelar matrícula")
        return RedirectResponse("/aluno/turmas", status_code=status.HTTP_303_SEE_OTHER)
```

### 💻 Template `minhas_turmas.html`

**Estrutura:**

1. **Abas (Tabs):**
   - Turmas Ativas
   - Histórico (Canceladas/Concluídas)

2. **Card para cada turma:**
   - Nome da turma
   - Atividade, professor
   - Horário e dias
   - Data de matrícula
   - Status
   - Botão "Cancelar Matrícula" (com confirmação)

3. **Confirmação de cancelamento:**
   - Modal ou alert JavaScript
   - "Tem certeza que deseja cancelar sua matrícula?"

### ✅ Checklist

- [ ] Rota de listagem implementada
- [ ] Rota de cancelamento implementada
- [ ] Decremento de vagas ao cancelar
- [ ] Template com abas funcionando
- [ ] Confirmação de cancelamento
- [ ] **Commit:** `feat(aluno): implementar gestão de matrículas do aluno`

---

## 4.4 Registrar Router do Aluno

### 📝 Objetivo

Registrar o router do aluno no `main.py` para que todas as rotas fiquem disponíveis.

### 💻 Código

```python
# main.py

# Adicionar import
from routes.aluno_routes import router as aluno_router

# Adicionar após outros routers (antes de public_router)
app.include_router(aluno_router, tags=["Aluno"])
logger.info("Router de aluno incluído")
```

### ✅ Checklist

- [ ] Router registrado em `main.py`
- [ ] Testar acesso a `/aluno` como aluno
- [ ] Testar bloqueio de acesso para não-alunos
- [ ] Verificar logs de registro do router
- [ ] **Commit:** `feat(aluno): registrar router do aluno no main`

---

## 📊 Progresso da Fase 4

✅ **Concluído:**
- 4.1 Dashboard do Aluno
- 4.2 Sistema de Matrícula
- 4.3 Minhas Turmas
- 4.4 Registrar Router

**Estimativa de tempo Fase 4:** 25-30 horas
**Próxima fase:** FASE 5 - Área do Professor

---

# FASE 5: ÁREA DO PROFESSOR

## 5.1 Dashboard do Professor

### 📝 Objetivo

Criar painel principal para o professor com visão das suas turmas, próximas aulas e estatísticas.

### 📍 Localização

- `routes/professor_routes.py` (novo arquivo)
- `templates/professor/dashboard.html`

### 💻 Estrutura do Dashboard

**Seções:**

1. **Boas-vindas**
2. **Estatísticas:**
   - Total de turmas que leciona
   - Total de alunos (somando todas as turmas)
   - Próxima aula
3. **Minhas Turmas:**
   - Lista das turmas que o professor leciona
   - Link para detalhes de cada turma
4. **Atalhos:**
   - Registrar presença
   - Ver todas as turmas
   - Relatórios

### 💻 Código da Rota

```python
from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth import obter_usuario_logado, exigir_professor
from util.mensagens import adicionar_mensagem_erro
from repo import turma_repo, matricula_repo
from util.logger_config import logger

router = APIRouter(prefix="/professor")
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def dashboard_professor(request: Request):
    """Dashboard principal do professor"""
    usuario = obter_usuario_logado(request)
    exigir_professor(usuario)

    try:
        # Obter turmas do professor
        minhas_turmas = turma_repo.obter_por_professor(usuario.id_usuario)
        turmas_ativas = [t for t in minhas_turmas if t.ativa]

        # Calcular total de alunos
        total_alunos = 0
        for turma in turmas_ativas:
            total_alunos += turma.vagas_ocupadas

        # Próxima aula
        proxima_aula = turmas_ativas[0] if turmas_ativas else None

        return templates.TemplateResponse(
            "professor/dashboard.html",
            {
                "request": request,
                "usuario": usuario,
                "turmas_ativas": turmas_ativas,
                "total_turmas": len(turmas_ativas),
                "total_alunos": total_alunos,
                "proxima_aula": proxima_aula
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar dashboard do professor: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar dashboard")
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
```

### 📝 Implementar Função `exigir_professor()`

Adicionar em `util/auth.py`:

```python
def exigir_professor(usuario: Optional[Usuario]) -> None:
    """Verifica se o usuário é um professor"""
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado"
        )
    if usuario.perfil != Perfil.PROFESSOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas professores podem acessar esta página."
        )
```

### ✅ Checklist

- [ ] Rota `/professor` criada
- [ ] Dashboard exibindo turmas do professor
- [ ] Estatísticas calculadas corretamente
- [ ] Função `exigir_professor()` implementada
- [ ] Template criado
- [ ] **Commit:** `feat(professor): criar dashboard do professor`

---

## 5.2 Minhas Turmas (Professor)

### 📝 Objetivo

Listar todas as turmas que o professor leciona, com acesso aos alunos matriculados e frequência.

### 📍 Localização

- `routes/professor_routes.py`
- `templates/professor/minhas_turmas.html`
- `templates/professor/turma_detalhes.html`

### 💻 Rotas

```python
@router.get("/turmas")
async def listar_minhas_turmas(request: Request):
    """Lista turmas do professor"""
    usuario = obter_usuario_logado(request)
    exigir_professor(usuario)

    try:
        turmas = turma_repo.obter_por_professor(usuario.id_usuario)

        return templates.TemplateResponse(
            "professor/minhas_turmas.html",
            {
                "request": request,
                "usuario": usuario,
                "turmas": turmas
            }
        )
    except Exception as e:
        logger.error(f"Erro ao listar turmas: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar turmas")
        return RedirectResponse("/professor", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/turmas/{id_turma}")
async def ver_turma_detalhes(request: Request, id_turma: int):
    """Ver detalhes de uma turma e seus alunos"""
    usuario = obter_usuario_logado(request)
    exigir_professor(usuario)

    try:
        # Obter turma
        turma = turma_repo.obter_por_id(id_turma)
        if not turma or turma.id_professor != usuario.id_usuario:
            adicionar_mensagem_erro(request, "Turma não encontrada ou você não tem permissão")
            return RedirectResponse("/professor/turmas", status_code=status.HTTP_303_SEE_OTHER)

        # Obter matrículas (alunos)
        matriculas = matricula_repo.obter_por_turma(id_turma)
        matriculas_ativas = [m for m in matriculas if m.status == "ATIVA"]

        return templates.TemplateResponse(
            "professor/turma_detalhes.html",
            {
                "request": request,
                "usuario": usuario,
                "turma": turma,
                "matriculas": matriculas_ativas,
                "total_alunos": len(matriculas_ativas)
            }
        )
    except Exception as e:
        logger.error(f"Erro ao carregar detalhes da turma: {e}", exc_info=True)
        adicionar_mensagem_erro(request, "Erro ao carregar turma")
        return RedirectResponse("/professor/turmas", status_code=status.HTTP_303_SEE_OTHER)
```

### 💻 Template `turma_detalhes.html`

**Seções:**

1. **Informações da Turma:**
   - Nome, atividade, horário, dias
   - Vagas totais e ocupadas
   - Datas (início/fim)

2. **Lista de Alunos:**
   - Tabela com: Nome, Email, Data Matrícula
   - Se vazio: "Nenhum aluno matriculado"

3. **Ações:**
   - Registrar presença para esta turma
   - Exportar lista de alunos (futuro)

### ✅ Checklist

- [ ] Rotas implementadas
- [ ] Verificação de propriedade da turma
- [ ] Templates criados
- [ ] Lista de alunos exibida
- [ ] **Commit:** `feat(professor): implementar gestão de turmas do professor`

---

## 5.3 Registrar Router do Professor

### 💻 Código

```python
# main.py

# Adicionar import
from routes.professor_routes import router as professor_router

# Adicionar após router do aluno
app.include_router(professor_router, tags=["Professor"])
logger.info("Router de professor incluído")
```

### ✅ Checklist

- [ ] Router registrado em `main.py`
- [ ] Testar acesso como professor
- [ ] Verificar proteção de acesso
- [ ] **Commit:** `feat(professor): registrar router do professor`

---

## 📊 Progresso da Fase 5

✅ **Concluído:**
- 5.1 Dashboard do Professor
- 5.2 Minhas Turmas
- 5.3 Registrar Router

**Estimativa de tempo Fase 5:** 20-25 horas
**Próxima fase:** FASE 6 - Testes e Documentação Final

---

# FASE 6: TESTES E DOCUMENTAÇÃO FINAL

## 6.1 Testes End-to-End

### 📝 Objetivo

Testar todos os fluxos principais do sistema para garantir funcionamento completo.

### ✅ Roteiro de Testes

**Fluxo 1: Admin**
- [ ] Login como admin
- [ ] Criar categoria
- [ ] Criar atividade vinculada à categoria
- [ ] Criar turma vinculada à atividade e professor
- [ ] Editar turma
- [ ] Verificar que não pode excluir turma com alunos
- [ ] Visualizar dashboard com estatísticas

**Fluxo 2: Aluno**
- [ ] Criar conta de aluno (se necessário usar admin)
- [ ] Login como aluno
- [ ] Visualizar turmas disponíveis
- [ ] Matricular-se em uma turma
- [ ] Verificar turma aparece em "Minhas Turmas"
- [ ] Cancelar matrícula
- [ ] Verificar vaga liberada

**Fluxo 3: Professor**
- [ ] Login como professor
- [ ] Visualizar dashboard
- [ ] Acessar "Minhas Turmas"
- [ ] Ver detalhes de uma turma
- [ ] Visualizar lista de alunos

**Fluxo 4: Validações**
- [ ] Tentar acessar área admin como aluno (deve bloquear)
- [ ] Tentar acessar área professor como aluno (deve bloquear)
- [ ] Tentar matricular em turma sem vagas (deve bloquear)
- [ ] Tentar matricular duas vezes na mesma turma (deve bloquear)

---

## 6.2 Documentação do README

### 📝 Objetivo

Atualizar o README.md com instruções completas de uso do sistema.

### 💻 Estrutura Sugerida

```markdown
# AgendaFit

Sistema de gerenciamento de atividades físicas para academias.

## Funcionalidades

### Administrador
- Gerenciar categorias de atividades
- Gerenciar atividades
- Gerenciar turmas
- Gerenciar usuários
- Visualizar estatísticas do sistema

### Aluno
- Visualizar turmas disponíveis
- Matricular-se em turmas
- Gerenciar matrículas
- Acompanhar estatísticas pessoais

### Professor
- Visualizar turmas que leciona
- Ver alunos matriculados
- Acessar informações das turmas

## Instalação

1. Clone o repositório
2. Crie ambiente virtual: `python -m venv venv`
3. Ative: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows)
4. Instale dependências: `pip install -r requirements.txt`
5. Execute: `python main.py`
6. Acesse: http://localhost:8000

## Usuários Padrão

- **Admin:** admin@admin.com / senha: admin
- **Professor:** joao.professor@agendafit.com / senha: senha123

## Tecnologias

- Python 3.12
- FastAPI
- SQLite
- Bootstrap 5
- Jinja2

## Estrutura do Projeto

```
AgendaFit/
├── model/          # Modelos de dados
├── repo/           # Repositórios (acesso ao banco)
├── routes/         # Rotas da API
├── templates/      # Templates HTML
├── util/           # Utilitários
├── sql/            # Queries SQL
└── main.py         # Ponto de entrada
```
```

### ✅ Checklist

- [ ] README atualizado com funcionalidades
- [ ] Instruções de instalação claras
- [ ] Usuários padrão documentados
- [ ] Estrutura do projeto explicada
- [ ] **Commit:** `docs: atualizar README com documentação completa`

---

## 📊 Progresso Final

✅ **Fases Concluídas:**
1. ✅ Adaptações Base
2. ✅ Infraestrutura de Dados
3. ✅ CRUDs Administrativos
4. ✅ Área do Aluno
5. ✅ Área do Professor
6. ✅ Testes e Documentação

🎉 **Projeto AgendaFit Completo!**

**Total estimado:** 150-180 horas de desenvolvimento

---

# APÊNDICES

## A. Troubleshooting Comum

### Erro: "Table already exists"
- Solução: Deletar arquivo `database.sqlite` e reiniciar

### Erro: "No module named 'X'"
- Solução: `pip install -r requirements.txt`

### Erro: "Foreign key constraint failed"
- Solução: Verificar ordem de criação de tabelas em `main.py`

### Erro 403 ao acessar áreas restritas
- Solução: Verificar se está logado com perfil correto

---

## B. Melhorias Futuras

1. **Sistema de Presenças:** Permitir professor registrar presença dos alunos
2. **Avaliações Físicas:** Registro e acompanhamento de evolução
3. **Pagamentos:** Controle financeiro completo
4. **Notificações:** Email/SMS para lembretes de aulas
5. **Calendário:** Visualização de aulas em calendário
6. **Relatórios:** Exportação de dados em PDF/Excel
7. **API REST:** Endpoints JSON para integração mobile
8. **Testes Automatizados:** Suite completa de testes unitários

---

**FIM DO GUIA COMPLETO DE IMPLEMENTAÇÃO DO AGENDAFIT**

**Total:** ~6,200 linhas
**Versão:** 1.0
**Data:** 2025
