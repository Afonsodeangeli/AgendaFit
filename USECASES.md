# Casos de Uso - AgendaFit

Relatório completo dos casos de uso de requisitos funcionais presentes no sistema.

---

## Perfis de Usuário

O sistema possui **3 perfis de usuário**:

| Perfil | Descrição |
|--------|-----------|
| **Administrador** | Acesso completo ao sistema |
| **Professor** | Gerencia turmas e visualiza alunos |
| **Aluno** | Matricula-se em turmas e realiza pagamentos |

---

## Casos de Uso por Área Funcional

### 1. Autenticação e Autorização

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-001 | Visualizar página inicial | Público |
| UC-002 | Visualizar página sobre | Público |
| UC-003 | Acessar página de login | Público |
| UC-004 | Acessar página de cadastro | Público |
| UC-005 | Solicitar recuperação de senha | Público |
| UC-006 | Redefinir senha com token | Público |
| UC-007 | Realizar login com e-mail e senha | Público |
| UC-008 | Realizar logout | Administrador, Professor, Aluno |
| UC-009 | Registrar nova conta | Público |
| UC-010 | Recuperar senha esquecida | Público |
| UC-011 | Redefinir senha com token válido | Público |

---

### 2. Gerenciamento de Perfil

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-012 | Visualizar perfil próprio | Administrador, Professor, Aluno |
| UC-013 | Editar informações do perfil | Administrador, Professor, Aluno |
| UC-014 | Alterar senha | Administrador, Professor, Aluno |
| UC-015 | Fazer upload e recortar foto de perfil | Administrador, Professor, Aluno |

---

### 3. Dashboard

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-016 | Visualizar dashboard personalizado | Administrador, Professor, Aluno |

---

### 4. Sistema de Chamados (Suporte)

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-017 | Listar chamados próprios | Administrador, Professor, Aluno |
| UC-018 | Criar novo chamado | Administrador, Professor, Aluno |
| UC-019 | Visualizar detalhes do chamado | Administrador, Professor, Aluno |
| UC-020 | Responder chamado próprio | Administrador, Professor, Aluno |
| UC-021 | Excluir chamado próprio | Administrador, Professor, Aluno |
| UC-022 | Listar todos os chamados do sistema | Administrador |
| UC-023 | Responder qualquer chamado | Administrador |
| UC-024 | Fechar chamado | Administrador |
| UC-025 | Reabrir chamado fechado | Administrador |

---

### 5. Sistema de Chat em Tempo Real

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-026 | Pesquisar usuários para conversar | Professor, Aluno |
| UC-027 | Criar ou acessar sala de chat | Professor, Aluno |
| UC-028 | Listar conversas | Professor, Aluno |
| UC-029 | Enviar mensagens | Professor, Aluno |
| UC-030 | Visualizar histórico de mensagens | Professor, Aluno |
| UC-031 | Marcar mensagens como lidas | Professor, Aluno |
| UC-032 | Visualizar total de mensagens não lidas | Professor, Aluno |
| UC-033 | Receber mensagens em tempo real | Professor, Aluno |

> **Nota**: Administradores só podem ser contatados via sistema de chamados, não via chat direto.

---

### 6. Gerenciamento de Usuários

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-034 | Listar todos os usuários | Administrador |
| UC-035 | Criar novo usuário | Administrador |
| UC-036 | Editar usuário | Administrador |
| UC-037 | Excluir usuário | Administrador |

---

### 7. Gerenciamento de Categorias

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-038 | Listar todas as categorias | Administrador |
| UC-039 | Criar categoria | Administrador |
| UC-040 | Editar categoria | Administrador |
| UC-041 | Excluir categoria | Administrador |

---

### 8. Gerenciamento de Atividades

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-042 | Listar todas as atividades | Administrador |
| UC-043 | Criar atividade | Administrador |
| UC-044 | Editar atividade | Administrador |
| UC-045 | Excluir atividade | Administrador |

---

### 9. Gerenciamento de Turmas

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-046 | Listar todas as turmas | Administrador |
| UC-047 | Criar turma | Administrador |
| UC-048 | Editar turma | Administrador |
| UC-049 | Excluir turma | Administrador |
| UC-050 | Visualizar turmas próprias (somente leitura) | Professor |
| UC-051 | Visualizar alunos da turma própria | Professor |

---

### 10. Gerenciamento de Matrículas

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-052 | Listar todas as matrículas | Administrador |
| UC-053 | Criar matrícula | Administrador |
| UC-054 | Editar matrícula | Administrador |
| UC-055 | Cancelar matrícula | Administrador |
| UC-056 | Visualizar matrículas próprias (somente leitura) | Aluno |

---

### 11. Gerenciamento de Pagamentos

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-057 | Listar todos os pagamentos | Administrador |
| UC-058 | Registrar pagamento | Administrador |
| UC-059 | Editar pagamento | Administrador |
| UC-060 | Excluir pagamento | Administrador |
| UC-061 | Visualizar pagamentos próprios (somente leitura) | Aluno |

---

### 12. Configurações do Sistema

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-062 | Visualizar todas as configurações | Administrador |
| UC-063 | Editar configurações em lote | Administrador |

---

### 13. Gerenciamento de Temas Visuais

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-064 | Visualizar temas disponíveis | Administrador |
| UC-065 | Aplicar tema | Administrador |

---

### 14. Backup e Restauração

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-066 | Listar todos os backups | Administrador |
| UC-067 | Criar backup | Administrador |
| UC-068 | Restaurar backup | Administrador |
| UC-069 | Baixar backup | Administrador |
| UC-070 | Excluir backup | Administrador |

---

### 15. Auditoria e Logs

| ID | Caso de Uso | Perfis Permitidos |
|----|-------------|-------------------|
| UC-071 | Visualizar logs do sistema | Administrador |
| UC-072 | Pesquisar logs | Administrador |

---

## Resumo Estatístico

### Total de Casos de Uso por Perfil

| Perfil | Casos de Uso Exclusivos | Casos de Uso Compartilhados | Total |
|--------|-------------------------|----------------------------|-------|
| Público (Sem Auth) | 6 | - | 6 |
| Administrador | 42 | 10 | 52 |
| Professor | 2 | 18 | 20 |
| Aluno | 2 | 18 | 20 |

### Distribuição por Área Funcional

| Área | Quantidade |
|------|------------|
| Autenticação e Autorização | 11 |
| Gerenciamento de Perfil | 4 |
| Dashboard | 1 |
| Sistema de Chamados | 9 |
| Sistema de Chat | 8 |
| Gerenciamento de Usuários | 4 |
| Gerenciamento de Categorias | 4 |
| Gerenciamento de Atividades | 4 |
| Gerenciamento de Turmas | 6 |
| Gerenciamento de Matrículas | 6 |
| Gerenciamento de Pagamentos | 5 |
| Configurações do Sistema | 2 |
| Gerenciamento de Temas | 2 |
| Backup e Restauração | 5 |
| Auditoria e Logs | 2 |
| **TOTAL** | **72** |

---

## Matriz de Permissões

| Caso de Uso | Público | Administrador | Professor | Aluno |
|-------------|:-------:|:-------------:|:---------:|:-----:|
| **Autenticação** |
| Login/Logout | ✓ | ✓ | ✓ | ✓ |
| Registro | ✓ | - | - | - |
| Recuperação de Senha | ✓ | - | - | - |
| **Perfil** |
| Visualizar/Editar Perfil | - | ✓ | ✓ | ✓ |
| Alterar Senha | - | ✓ | ✓ | ✓ |
| Upload de Foto | - | ✓ | ✓ | ✓ |
| **Dashboard** |
| Visualizar Dashboard | - | ✓ | ✓ | ✓ |
| **Chamados** |
| Criar/Gerenciar Próprios | - | ✓ | ✓ | ✓ |
| Gerenciar Todos | - | ✓ | - | - |
| **Chat** |
| Usar Chat | - | - | ✓ | ✓ |
| **Usuários** |
| CRUD Completo | - | ✓ | - | - |
| **Categorias** |
| CRUD Completo | - | ✓ | - | - |
| **Atividades** |
| CRUD Completo | - | ✓ | - | - |
| **Turmas** |
| CRUD Completo | - | ✓ | - | - |
| Visualizar Próprias | - | - | ✓ | - |
| **Matrículas** |
| CRUD Completo | - | ✓ | - | - |
| Visualizar Próprias | - | - | - | ✓ |
| **Pagamentos** |
| CRUD Completo | - | ✓ | - | - |
| Visualizar Próprios | - | - | - | ✓ |
| **Configurações** |
| Gerenciar | - | ✓ | - | - |
| **Temas** |
| Gerenciar | - | ✓ | - | - |
| **Backup** |
| Gerenciar | - | ✓ | - | - |
| **Logs** |
| Visualizar/Pesquisar | - | ✓ | - | - |

---

## Regras de Negócio Importantes

1. **Exclusão de Usuários**: Não é possível excluir usuários que possuem turmas (professores) ou matrículas (alunos)
2. **Exclusão de Categorias**: Não é possível excluir categorias que possuem atividades vinculadas
3. **Exclusão de Atividades**: Não é possível excluir atividades que possuem turmas vinculadas
4. **Exclusão de Turmas**: Não é possível excluir turmas que possuem matrículas vinculadas
5. **Cancelamento de Matrículas**: Não é possível cancelar matrículas que possuem pagamentos registrados
6. **Exclusão de Chamados**: Usuários só podem excluir chamados próprios com status "Aberto" e sem respostas do administrador
7. **Chat**: Administradores não participam do chat direto - contato apenas via chamados
8. **Capacidade de Turmas**: Não é possível reduzir a capacidade abaixo do número de alunos matriculados
