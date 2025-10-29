# Decisões de Design - Entidades Especiais

**Data:** 2025-10-28
**Versão:** 1.0
**Objetivo:** Documentar decisões arquiteturais para entidades que não seguem o padrão CRUD completo

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Matricula](#matricula)
3. [Pagamento](#pagamento)
4. [Endereco](#endereco)
5. [Chat (Sala, Mensagem, Participante)](#chat)
6. [Resumo de Decisões](#resumo-de-decisões)

---

## 🎯 VISÃO GERAL

Nem todas as entidades do AgendaFit seguem o padrão CRUD completo de 5 camadas (SQL, Model, Repo, DTO, Routes). Este documento explica **por que** algumas entidades têm estruturas diferentes e as **vantagens** dessas decisões.

### Padrão de Referência: Categoria

O padrão CRUD completo (Categoria) inclui:
- ✅ SQL com constraints completos
- ✅ Model com docstrings
- ✅ Repository com todas operações
- ✅ DTOs de validação (Criar, Alterar)
- ✅ Routes administrativas completas
- ✅ Timestamps de auditoria

**Quando usar:** Entidades independentes que precisam de CRUD completo pela UI administrativa.

---

## 💰 MATRICULA

### Características da Entidade

Matricula representa o vínculo entre **Aluno** e **Turma**, com informações financeiras (valor_mensalidade, data_vencimento).

### Decisões de Design

#### ✅ MANTIDO: Estrutura Padrão
- **SQL:** Completo com constraints
- **Model:** Com docstrings completos
- **Repository:** Operações completas
- **DTOs:** ❌ **NÃO CRIADOS** (decisão consciente)
- **Routes:** Gerenciadas como parte de Usuario/Turma

#### ❌ SEM DTOs Próprios

**Razão:** Matriculas são criadas através do contexto de **Turma** ou **Aluno**, não como entidade independente.

**Vantagens:**
1. **Menos código duplicado:** Validação feita nas rotas de contexto
2. **UX mais clara:** Usuário matricula em turma, não "cria matrícula"
3. **Acoplamento correto:** Matricula não existe sem turma + aluno

**Como é usado:**
```python
# Na rota de turma
POST /turma/{id}/matricular
{
  "aluno_id": 123,
  "valor_mensalidade": 150.00,
  "data_vencimento": 10
}
```

#### 🔒 Constraints Especiais

```sql
UNIQUE (id_turma, id_aluno)  -- Previne duplicação
ON DELETE RESTRICT           -- Não pode excluir turma/aluno com matriculas
```

**Razão:** Integridade referencial forte para dados financeiros.

#### 📊 Repository Especializado

```python
verificar_matricula_existente(id_turma, id_aluno) -> bool
obter_por_aluno(id_aluno) -> List[Matricula]
obter_por_turma(id_turma) -> List[Matricula]
```

**Razão:** Queries sempre contextuais (por aluno OU por turma), nunca "todas matriculas".

---

## 💳 PAGAMENTO

### Características da Entidade

Pagamento registra pagamentos de mensalidades, vinculado a **Matricula** e **Aluno**.

### Decisões de Design

#### ✅ MANTIDO: Estrutura Mínima
- **SQL:** Completo com constraints
- **Model:** Com docstrings completos
- **Repository:** ❌ **OPERAÇÕES LIMITADAS** (apenas inserir e consultar)
- **DTOs:** ❌ **NÃO CRIADOS**
- **Routes:** Gerenciadas como parte de Matricula

#### ❌ SEM Operações de UPDATE/DELETE

**Razão:** Pagamentos são **append-only** (histórico financeiro imutável).

**Vantagens:**
1. **Auditoria:** Histórico completo preservado
2. **Compliance:** Rastreamento financeiro confiável
3. **Simplicidade:** Sem lógica de edição/estorno

**Padrão:**
```python
# Apenas estas operações existem
inserir(pagamento: Pagamento) -> Optional[int]
obter_por_matricula(id_matricula: int) -> List[Pagamento]
obter_por_aluno(id_aluno: int) -> List[Pagamento]
```

#### 🚫 SEM Timestamps de Auditoria

**Razão:** `data_pagamento` já serve como timestamp único e suficiente.

**Diferença de outros:**
- ❌ Não tem `data_cadastro` (redundante com data_pagamento)
- ❌ Não tem `data_atualizacao` (pagamentos não são editados)

#### 🔒 Constraints Especiais

```sql
ON DELETE RESTRICT  -- Não pode excluir matricula/aluno com pagamentos
```

**Razão:** Preservar histórico financeiro completo.

---

## 🏠 ENDERECO

### Características da Entidade

Endereco armazena endereços de **Usuarios**. Um usuário pode ter múltiplos endereços.

### Decisões de Design

#### ✅ MANTIDO: Child Entity Pattern
- **SQL:** Completo com CASCADE
- **Model:** Com docstrings completos
- **Repository:** Operações completas
- **DTOs:** ✅ **CRIADOS NA FASE 2** (endereco_dto.py)
- **Routes:** ❌ **SEM ROTAS PRÓPRIAS**

#### 🔗 Pattern: Child Entity

**Razão:** Endereços são sub-recursos de Usuario, não entidades independentes.

**Como é acessado:**
```python
# Através de rotas de usuario
GET    /usuario/{id}/enderecos           # Listar
POST   /usuario/{id}/enderecos           # Criar
PUT    /usuario/{id}/enderecos/{end_id}  # Alterar
DELETE /usuario/{id}/enderecos/{end_id}  # Excluir
```

**Vantagens:**
1. **Segurança:** Usuario só vê seus próprios endereços
2. **Contexto claro:** Endereço sempre vinculado a usuario
3. **URLs RESTful:** Hierarquia correta de recursos

#### 🔒 Constraint: CASCADE

```sql
FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
```

**Razão:** Endereços não fazem sentido sem o usuário. Ao excluir usuario, endereços vão junto.

#### 🚫 SEM Timestamps

**Razão:** Endereços são dados relativamente estáticos que não precisam auditoria temporal.

**Quando seria necessário:**
- Se houvesse regras de negócio baseadas em "endereço antigo vs novo"
- Se precisasse rastrear mudanças de endereço ao longo do tempo

**Decisão atual:** Não necessário para o escopo do AgendaFit.

---

## 💬 CHAT

### Características do Subsistema

Chat é composto por 3 tabelas interdependentes:
- **chat_sala:** Sala entre 2 usuários
- **chat_mensagem:** Mensagens trocadas
- **chat_participante:** Usuários em cada sala

### Decisões de Design

#### ✅ MANTIDO: Subsistema Coeso Pattern
- **SQL:** 3 tabelas com CASCADE
- **Models:** 3 models com docstrings
- **Repositories:** 3 repositories especializados
- **DTOs:** ✅ **DTOs CONSOLIDADOS** (chat_dto.py)
- **Routes:** ✅ **ROTAS CONSOLIDADAS** (chat_routes.py)

#### 🎯 Pattern: Subsistema Coeso

**Razão:** As 3 tabelas são sempre usadas em conjunto, nunca isoladamente.

**Vantagens:**
1. **Menos endpoints:** 1 arquivo de rotas ao invés de 3
2. **Transações atômicas:** Criar sala + participantes + primeira mensagem
3. **DTOs simplificados:** Usuário não precisa saber da estrutura interna

**Como é usado:**
```python
POST /chat/criar
{
  "destinatario_id": 456,
  "mensagem_inicial": "Olá!"
}

# Internamente cria:
# - 1 chat_sala
# - 2 chat_participante (remetente + destinatário)
# - 1 chat_mensagem
```

#### 📊 Data Atualizacao (Fase 2)

**chat_mensagem:**
- ✅ **TEM data_atualizacao** (mensagens podem ser editadas)

**chat_sala:**
- ❌ **NÃO TEM data_atualizacao**
- ✅ **TEM ultima_atividade** (serve o mesmo propósito)

**Razão:** `ultima_atividade` é atualizada a cada mensagem, já rastreia mudanças na sala.

**chat_participante:**
- ❌ **SEM timestamps** (registro estático de quem está na sala)

#### 🔒 Constraints: CASCADE em cadeia

```sql
chat_mensagem → chat_sala (CASCADE)
chat_participante → chat_sala (CASCADE)
chat_sala → (independente)

Resultado: Excluir sala = excluir tudo
```

**Razão:** Ao deletar uma sala de chat, todas as mensagens e participantes devem ir junto.

---

## 📊 RESUMO DE DECISÕES

### Tabela Comparativa

| Entidade | SQL | Model | Repo | DTO | Routes | Timestamps | Pattern |
|----------|-----|-------|------|-----|--------|------------|---------|
| **Categoria** | ✅ | ✅ | ✅ | ✅ | ✅ | Completo | CRUD Completo |
| **Matricula** | ✅ | ✅ | ✅ | ❌ | Contexto | Completo | Relacional |
| **Pagamento** | ✅ | ✅ | Parcial | ❌ | Contexto | Apenas data_pagamento | Append-Only |
| **Endereco** | ✅ | ✅ | ✅ | ✅* | ❌ | Sem timestamps | Child Entity |
| **Chat*** | ✅ | ✅ | ✅ | ✅ | ✅ | Variado | Subsistema Coeso |

\* DTOs criados na Fase 2
\*\* Chat = 3 tabelas tratadas como uma

### Princípios Aplicados

1. **CRUD Completo NEM SEMPRE é melhor**
   - Adiciona complexidade desnecessária
   - Expõe detalhes de implementação

2. **Contexto importa**
   - Matricula e Pagamento são sempre acessados via Turma/Aluno
   - Endereço é sempre acessado via Usuario

3. **Imutabilidade quando apropriado**
   - Pagamentos são append-only
   - Chat_participante é estático

4. **Granularidade de timestamps**
   - Nem tudo precisa data_cadastro + data_atualizacao
   - Escolher o que faz sentido para cada entidade

5. **Subsistemas coesos**
   - Agrupar tabelas relacionadas
   - Simplificar API pública

---

## 🔮 QUANDO ADICIONAR CRUD COMPLETO

**Considere adicionar CRUD completo se:**

1. ✅ Entidade precisa ser gerenciada independentemente
2. ✅ Há UI administrativa para manipulação direta
3. ✅ Regras de negócio complexas de validação
4. ✅ Múltiplos contextos de acesso (não apenas um pai)

**Exemplos no AgendaFit:**
- Categoria: ✅ Gerenciada independentemente
- Atividade: ✅ Gerenciada independentemente
- Turma: ✅ Gerenciada independentemente
- Usuario: ✅ Gerenciada independentemente

**Contra-exemplos:**
- Matricula: ❌ Sempre através de Turma/Aluno
- Pagamento: ❌ Apenas inserção e consulta
- Endereco: ❌ Sempre através de Usuario
- Chat_participante: ❌ Parte de subsistema maior

---

## 📚 REFERÊNCIAS

- `docs/PADROES_ARQUITETURAIS.md` - Detalhamento de todos os padrões
- `docs/CHECKLIST_CONFORMIDADE.md` - Como decidir estrutura de novas entidades
- `docs/MELHORES_PRATICAS.md` - Princípios gerais de design

---

**Mantido por:** Equipe de Desenvolvimento AgendaFit
**Última revisão:** 2025-10-28
**Versão:** 1.0
