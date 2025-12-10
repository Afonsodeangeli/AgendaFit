# Atividade Final - Projeto AgendaFit

Este documento contém 4 atividades independentes para os alunos do projeto AgendaFit. Cada atividade deve ser concluída em até 60 minutos.

---

## ATIVIDADE DO ALUNO 1: Criar Página de Contato

**Objetivo:** Criar uma nova página pública "Contato" com um formulário estilizado (apenas visual, sem funcionalidade de envio).

**Tempo estimado:** 45-60 minutos

### Passo 1: Criar sua branch

Abra o terminal na pasta do projeto e execute:

```bash
git checkout main
git pull origin main
git checkout -b aluno1
```

### Passo 2: Criar o arquivo do template

Crie o arquivo `templates/contato.html` com o seguinte conteúdo:

```html
{% extends "base_publica.html" %}

{% block titulo %}Contato{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="row mb-4">
    <div class="col-12">
        <div class="position-relative overflow-hidden rounded-4 shadow-lg hero-fitness"
             style="background: linear-gradient(135deg, #FF6B35 0%, #9B51E0 100%); min-height: 200px;">
            <div class="position-relative p-5 text-center" data-bs-theme="dark">
                <h1 class="display-5 fw-bold text-white mb-2" style="font-family: 'Montserrat', sans-serif;">
                    <i class="bi bi-envelope-heart me-2"></i>Entre em Contato
                </h1>
                <p class="lead text-white mb-0" style="opacity: 0.9;">
                    Estamos prontos para atender você!
                </p>
            </div>
        </div>
    </div>
</div>

<div class="row g-4">
    <!-- Formulário de Contato -->
    <div class="col-lg-8">
        <div class="card card-fitness shadow-sm border-0">
            <div class="card-body p-4">
                <h4 class="card-title fw-bold mb-4" style="color: var(--fitness-blue);">
                    <i class="bi bi-send me-2"></i>Envie sua Mensagem
                </h4>

                <form>
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label for="nome" class="form-label fw-semibold">Nome Completo</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-person"></i></span>
                                <input type="text" class="form-control" id="nome" placeholder="Seu nome completo" required>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <label for="email" class="form-label fw-semibold">E-mail</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                                <input type="email" class="form-control" id="email" placeholder="seu@email.com" required>
                            </div>
                        </div>

                        <div class="col-md-6">
                            <label for="telefone" class="form-label fw-semibold">Telefone</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-telephone"></i></span>
                                <input type="tel" class="form-control" id="telefone" placeholder="(00) 00000-0000">
                            </div>
                        </div>

                        <div class="col-md-6">
                            <label for="assunto" class="form-label fw-semibold">Assunto</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-tag"></i></span>
                                <select class="form-select" id="assunto" required>
                                    <option value="" selected disabled>Selecione um assunto</option>
                                    <option value="informacoes">Informações sobre planos</option>
                                    <option value="matricula">Dúvidas sobre matrícula</option>
                                    <option value="horarios">Horários das aulas</option>
                                    <option value="outros">Outros assuntos</option>
                                </select>
                            </div>
                        </div>

                        <div class="col-12">
                            <label for="mensagem" class="form-label fw-semibold">Mensagem</label>
                            <textarea class="form-control" id="mensagem" rows="5"
                                      placeholder="Digite sua mensagem aqui..." required></textarea>
                        </div>

                        <div class="col-12">
                            <button type="button" class="btn btn-fitness-primary btn-lg rounded-pill px-5"
                                    onclick="alert('Mensagem enviada com sucesso! (Demonstração)')">
                                <i class="bi bi-send me-2"></i>Enviar Mensagem
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Informações de Contato -->
    <div class="col-lg-4">
        <div class="card card-fitness shadow-sm border-0 mb-4">
            <div class="card-body p-4">
                <h5 class="card-title fw-bold mb-4" style="color: var(--fitness-green);">
                    <i class="bi bi-geo-alt me-2"></i>Localização
                </h5>
                <p class="text-body-secondary mb-0">
                    <i class="bi bi-pin-map me-2"></i>
                    Rua das Atividades Físicas, 123<br>
                    Centro - Cachoeiro de Itapemirim/ES<br>
                    CEP: 29300-000
                </p>
            </div>
        </div>

        <div class="card card-fitness shadow-sm border-0 mb-4">
            <div class="card-body p-4">
                <h5 class="card-title fw-bold mb-4" style="color: var(--fitness-orange);">
                    <i class="bi bi-telephone me-2"></i>Telefones
                </h5>
                <p class="text-body-secondary mb-2">
                    <i class="bi bi-phone me-2"></i>(28) 99999-9999
                </p>
                <p class="text-body-secondary mb-0">
                    <i class="bi bi-whatsapp me-2"></i>(28) 98888-8888
                </p>
            </div>
        </div>

        <div class="card card-fitness shadow-sm border-0">
            <div class="card-body p-4">
                <h5 class="card-title fw-bold mb-4" style="color: var(--fitness-blue);">
                    <i class="bi bi-envelope me-2"></i>E-mail
                </h5>
                <p class="text-body-secondary mb-0">
                    <i class="bi bi-at me-2"></i>contato@agendafit.com.br
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Passo 3: Adicionar a rota no backend

Abra o arquivo `routes/public_routes.py` e adicione a seguinte rota **antes da última linha do arquivo**:

```python
@router.get("/contato")
async def contato(request: Request):
    """
    Página de Contato
    """
    # Rate limiting por IP
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

    return templates_public.TemplateResponse(
        "contato.html",
        {"request": request}
    )
```

### Passo 4: Adicionar link no menu

Abra o arquivo `templates/base_publica.html` e procure pela linha 53-58 (seção do menu de navegação). Encontre onde está o link "Sobre":

```html
                    <li class="nav-item">
                        <a class="nav-link px-3 rounded-pill {{ 'active bg-white bg-opacity-10' if request.path == '/sobre' else '' }}"
                            href="/sobre">
                            <i class="bi bi-info-circle me-1"></i>Sobre
                        </a>
                    </li>
```

**Logo após** esse `</li>` (linha 58), adicione:

```html
                    <li class="nav-item">
                        <a class="nav-link px-3 rounded-pill {{ 'active bg-white bg-opacity-10' if request.path == '/contato' else '' }}"
                            href="/contato">
                            <i class="bi bi-envelope me-1"></i>Contato
                        </a>
                    </li>
```

### Passo 5: Testar a página

1. Inicie o servidor (se não estiver rodando): `python main.py`
2. Acesse no navegador: `http://localhost:8405/contato`
3. Verifique se a página está exibindo corretamente

### Passo 6: Commitar as alterações

```bash
git add .
git commit -m "feat: adicionar página de contato

- Criar template contato.html com formulário estilizado
- Adicionar rota /contato em public_routes.py
- Adicionar link no menu de navegação"
```

---

## ATIVIDADE DO ALUNO 2: Adicionar Seção de Horário de Funcionamento

**Objetivo:** Adicionar uma nova seção na página inicial mostrando os horários de funcionamento da academia.

**Tempo estimado:** 30-45 minutos

### Passo 1: Criar sua branch

Abra o terminal na pasta do projeto e execute:

```bash
git checkout main
git pull origin main
git checkout -b aluno2
```

### Passo 2: Editar a página inicial

Abra o arquivo `templates/index.html` e procure pela seção de FAQ (procure por `<!-- FAQ Section`). **Antes** dessa seção, adicione o seguinte código:

```html
<!-- Horário de Funcionamento Section -->
<div class="mb-5" id="horarios">
    <div class="text-center mb-5">
        <span class="badge-fitness-green rounded-pill px-3 py-2 mb-2" style="display: inline-block;">
            <i class="bi bi-clock me-1"></i>Funcionamento
        </span>
        <h2 class="fw-bold display-6" style="font-family: 'Montserrat', sans-serif;">Horário de Funcionamento</h2>
        <p class="text-body-secondary col-lg-6 mx-auto">
            Confira nossos horários e venha treinar no melhor momento para você
        </p>
    </div>

    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="card card-fitness shadow-sm border-0">
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-hover mb-0">
                            <thead style="background: linear-gradient(135deg, #FF6B35 0%, #9B51E0 100%);">
                                <tr>
                                    <th class="text-white py-3 ps-4">
                                        <i class="bi bi-calendar3 me-2"></i>Dia
                                    </th>
                                    <th class="text-white py-3 text-center">
                                        <i class="bi bi-clock me-2"></i>Horário
                                    </th>
                                    <th class="text-white py-3 pe-4 text-end">
                                        <i class="bi bi-info-circle me-2"></i>Status
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td class="py-3 ps-4 fw-semibold">
                                        <i class="bi bi-calendar-day icon-blue me-2"></i>Segunda-feira
                                    </td>
                                    <td class="py-3 text-center">06:00 às 22:00</td>
                                    <td class="py-3 pe-4 text-end">
                                        <span class="badge bg-success rounded-pill">Aberto</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="py-3 ps-4 fw-semibold">
                                        <i class="bi bi-calendar-day icon-blue me-2"></i>Terça-feira
                                    </td>
                                    <td class="py-3 text-center">06:00 às 22:00</td>
                                    <td class="py-3 pe-4 text-end">
                                        <span class="badge bg-success rounded-pill">Aberto</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="py-3 ps-4 fw-semibold">
                                        <i class="bi bi-calendar-day icon-blue me-2"></i>Quarta-feira
                                    </td>
                                    <td class="py-3 text-center">06:00 às 22:00</td>
                                    <td class="py-3 pe-4 text-end">
                                        <span class="badge bg-success rounded-pill">Aberto</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="py-3 ps-4 fw-semibold">
                                        <i class="bi bi-calendar-day icon-blue me-2"></i>Quinta-feira
                                    </td>
                                    <td class="py-3 text-center">06:00 às 22:00</td>
                                    <td class="py-3 pe-4 text-end">
                                        <span class="badge bg-success rounded-pill">Aberto</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="py-3 ps-4 fw-semibold">
                                        <i class="bi bi-calendar-day icon-blue me-2"></i>Sexta-feira
                                    </td>
                                    <td class="py-3 text-center">06:00 às 22:00</td>
                                    <td class="py-3 pe-4 text-end">
                                        <span class="badge bg-success rounded-pill">Aberto</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="py-3 ps-4 fw-semibold">
                                        <i class="bi bi-calendar-day icon-orange me-2"></i>Sábado
                                    </td>
                                    <td class="py-3 text-center">08:00 às 18:00</td>
                                    <td class="py-3 pe-4 text-end">
                                        <span class="badge bg-warning text-dark rounded-pill">Horário Reduzido</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="py-3 ps-4 fw-semibold">
                                        <i class="bi bi-calendar-day icon-orange me-2"></i>Domingo
                                    </td>
                                    <td class="py-3 text-center">08:00 às 12:00</td>
                                    <td class="py-3 pe-4 text-end">
                                        <span class="badge bg-warning text-dark rounded-pill">Horário Reduzido</span>
                                    </td>
                                </tr>
                                <tr class="table-light">
                                    <td class="py-3 ps-4 fw-semibold text-danger">
                                        <i class="bi bi-calendar-x icon-orange me-2"></i>Feriados
                                    </td>
                                    <td class="py-3 text-center text-danger">Fechado</td>
                                    <td class="py-3 pe-4 text-end">
                                        <span class="badge bg-danger rounded-pill">Fechado</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Observação -->
            <div class="alert border-0 rounded-4 shadow-sm mt-4" role="alert"
                 style="background: linear-gradient(135deg, var(--bs-warning-bg-subtle) 0%, var(--bs-orange-bg-subtle) 100%);">
                <div class="d-flex align-items-start gap-3">
                    <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-warning bg-opacity-10 p-2">
                        <i class="bi bi-exclamation-triangle-fill text-warning fs-4"></i>
                    </div>
                    <div class="flex-fill">
                        <h6 class="alert-heading fw-bold mb-1">
                            <i class="bi bi-info-circle me-1"></i>Atenção
                        </h6>
                        <p class="mb-0 text-body-secondary">
                            Os horários podem sofrer alterações em datas comemorativas.
                            Consulte nossa equipe para mais informações.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

### Passo 3: Testar a página

1. Inicie o servidor (se não estiver rodando): `python main.py`
2. Acesse no navegador: `http://localhost:8405/`
3. Role a página para ver a nova seção de horários

### Passo 4: Commitar as alterações

```bash
git add .
git commit -m "feat: adicionar seção de horário de funcionamento na página inicial

- Criar tabela estilizada com dias e horários
- Adicionar badges de status (Aberto, Horário Reduzido, Fechado)
- Incluir alerta informativo sobre feriados"
```

---

## ATIVIDADE DO ALUNO 3: Criar Página de Política de Privacidade

**Objetivo:** Criar uma página de Política de Privacidade seguindo o padrão visual do projeto.

**Tempo estimado:** 40-50 minutos

### Passo 1: Criar sua branch

Abra o terminal na pasta do projeto e execute:

```bash
git checkout main
git pull origin main
git checkout -b aluno3
```

### Passo 2: Criar o arquivo do template

Crie o arquivo `templates/privacidade.html` com o seguinte conteúdo:

```html
{% extends "base_publica.html" %}

{% block titulo %}Política de Privacidade{% endblock %}

{% block content %}
<!-- Hero Section -->
<div class="row mb-4">
    <div class="col-12">
        <div class="position-relative overflow-hidden rounded-4 shadow-lg hero-fitness"
             style="background: linear-gradient(135deg, #1AA260 0%, #00BCD4 100%); min-height: 200px;">
            <div class="position-relative p-5 text-center" data-bs-theme="dark">
                <h1 class="display-5 fw-bold text-white mb-2" style="font-family: 'Montserrat', sans-serif;">
                    <i class="bi bi-shield-check me-2"></i>Política de Privacidade
                </h1>
                <p class="lead text-white mb-0" style="opacity: 0.9;">
                    Sua privacidade é importante para nós
                </p>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-lg-10 mx-auto">
        <!-- Última atualização -->
        <div class="alert alert-info border-0 rounded-4 shadow-sm mb-4">
            <i class="bi bi-calendar-check me-2"></i>
            <strong>Última atualização:</strong> Dezembro de 2025
        </div>

        <!-- Seção 1 -->
        <div class="card card-fitness shadow-sm border-0 mb-4">
            <div class="card-body p-4">
                <h4 class="card-title fw-bold mb-3" style="color: var(--fitness-blue);">
                    <i class="bi bi-1-circle me-2"></i>Informações que Coletamos
                </h4>
                <p class="text-body-secondary">
                    Coletamos informações que você nos fornece diretamente, incluindo:
                </p>
                <ul class="text-body-secondary">
                    <li><strong>Dados de cadastro:</strong> nome, e-mail, telefone e data de nascimento</li>
                    <li><strong>Dados de pagamento:</strong> informações necessárias para processamento de mensalidades</li>
                    <li><strong>Dados de uso:</strong> informações sobre sua interação com nosso sistema</li>
                    <li><strong>Comunicações:</strong> mensagens enviadas através do sistema de chamados e chat</li>
                </ul>
            </div>
        </div>

        <!-- Seção 2 -->
        <div class="card card-fitness shadow-sm border-0 mb-4">
            <div class="card-body p-4">
                <h4 class="card-title fw-bold mb-3" style="color: var(--fitness-green);">
                    <i class="bi bi-2-circle me-2"></i>Como Usamos suas Informações
                </h4>
                <p class="text-body-secondary">
                    Utilizamos as informações coletadas para:
                </p>
                <ul class="text-body-secondary">
                    <li>Gerenciar sua conta e matrículas</li>
                    <li>Processar pagamentos e enviar notificações</li>
                    <li>Melhorar nossos serviços e experiência do usuário</li>
                    <li>Comunicar sobre atualizações, promoções e novidades</li>
                    <li>Garantir a segurança do sistema</li>
                </ul>
            </div>
        </div>

        <!-- Seção 3 -->
        <div class="card card-fitness shadow-sm border-0 mb-4">
            <div class="card-body p-4">
                <h4 class="card-title fw-bold mb-3" style="color: var(--fitness-orange);">
                    <i class="bi bi-3-circle me-2"></i>Compartilhamento de Dados
                </h4>
                <p class="text-body-secondary">
                    <strong>Não vendemos suas informações pessoais.</strong> Podemos compartilhar dados apenas:
                </p>
                <ul class="text-body-secondary">
                    <li>Com prestadores de serviço que auxiliam nossa operação</li>
                    <li>Quando exigido por lei ou ordem judicial</li>
                    <li>Para proteger nossos direitos e segurança</li>
                </ul>
            </div>
        </div>

        <!-- Seção 4 -->
        <div class="card card-fitness shadow-sm border-0 mb-4">
            <div class="card-body p-4">
                <h4 class="card-title fw-bold mb-3" style="color: var(--fitness-blue);">
                    <i class="bi bi-4-circle me-2"></i>Segurança dos Dados
                </h4>
                <p class="text-body-secondary">
                    Implementamos medidas de segurança para proteger suas informações:
                </p>
                <ul class="text-body-secondary">
                    <li><i class="bi bi-check-circle text-success me-1"></i> Criptografia de senhas com algoritmos seguros</li>
                    <li><i class="bi bi-check-circle text-success me-1"></i> Proteção contra ataques (CSRF, XSS, SQL Injection)</li>
                    <li><i class="bi bi-check-circle text-success me-1"></i> Controle de acesso baseado em perfis</li>
                    <li><i class="bi bi-check-circle text-success me-1"></i> Monitoramento e auditoria de acessos</li>
                </ul>
            </div>
        </div>

        <!-- Seção 5 -->
        <div class="card card-fitness shadow-sm border-0 mb-4">
            <div class="card-body p-4">
                <h4 class="card-title fw-bold mb-3" style="color: var(--fitness-green);">
                    <i class="bi bi-5-circle me-2"></i>Seus Direitos
                </h4>
                <p class="text-body-secondary">
                    De acordo com a LGPD (Lei Geral de Proteção de Dados), você tem direito a:
                </p>
                <div class="row g-3">
                    <div class="col-md-6">
                        <div class="d-flex align-items-start">
                            <i class="bi bi-arrow-right-circle icon-green me-2 mt-1"></i>
                            <span class="text-body-secondary">Acessar seus dados pessoais</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="d-flex align-items-start">
                            <i class="bi bi-arrow-right-circle icon-green me-2 mt-1"></i>
                            <span class="text-body-secondary">Corrigir dados incompletos ou incorretos</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="d-flex align-items-start">
                            <i class="bi bi-arrow-right-circle icon-green me-2 mt-1"></i>
                            <span class="text-body-secondary">Solicitar a exclusão de seus dados</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="d-flex align-items-start">
                            <i class="bi bi-arrow-right-circle icon-green me-2 mt-1"></i>
                            <span class="text-body-secondary">Revogar consentimentos concedidos</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Seção 6 -->
        <div class="card card-fitness shadow-sm border-0 mb-4">
            <div class="card-body p-4">
                <h4 class="card-title fw-bold mb-3" style="color: var(--fitness-orange);">
                    <i class="bi bi-6-circle me-2"></i>Contato
                </h4>
                <p class="text-body-secondary">
                    Para exercer seus direitos ou esclarecer dúvidas sobre esta política, entre em contato:
                </p>
                <div class="row g-3 mt-2">
                    <div class="col-md-6">
                        <div class="d-flex align-items-center">
                            <i class="bi bi-envelope icon-blue me-2 fs-5"></i>
                            <span class="text-body-secondary">privacidade@agendafit.com.br</span>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="d-flex align-items-center">
                            <i class="bi bi-headset icon-orange me-2 fs-5"></i>
                            <span class="text-body-secondary">Sistema de Chamados (após login)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Botão Voltar -->
        <div class="text-center">
            <a href="/" class="btn btn-fitness-primary rounded-pill px-5">
                <i class="bi bi-arrow-left me-2"></i>Voltar para Início
            </a>
        </div>
    </div>
</div>
{% endblock %}
```

### Passo 3: Adicionar a rota no backend

Abra o arquivo `routes/public_routes.py` e adicione a seguinte rota **antes da última linha do arquivo**:

```python
@router.get("/privacidade")
async def privacidade(request: Request):
    """
    Página de Política de Privacidade
    """
    # Rate limiting por IP
    ip = obter_identificador_cliente(request)
    if not public_limiter.verificar(ip):
        informar_erro(request, "Muitas requisições. Aguarde alguns minutos.")
        logger.warning(f"Rate limit excedido para página pública - IP: {ip}")
        return templates_public.TemplateResponse(
            "errors/429.html",
            {"request": request},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

    return templates_public.TemplateResponse(
        "privacidade.html",
        {"request": request}
    )
```

### Passo 4: Adicionar link no rodapé

Abra o arquivo `templates/base_publica.html` e procure pela linha 116-134 (seção de links do rodapé). Encontre a lista de links no rodapé:

```html
                    <ul class="list-inline mb-0">
                        <li class="list-inline-item">
                            <a href="/" class="link-fitness text-decoration-none">
                                Início
                            </a>
                        </li>
                        <li class="list-inline-item text-body-tertiary">•</li>
                        <li class="list-inline-item">
                            <a href="/sobre" class="link-fitness text-decoration-none">
                                Sobre
                            </a>
                        </li>
                        <li class="list-inline-item text-body-tertiary">•</li>
                        <li class="list-inline-item">
                            <a href="/login" class="link-fitness text-decoration-none">
                                Login
                            </a>
                        </li>
                    </ul>
```

**Antes do `</ul>`** (linha 134), adicione:

```html
                        <li class="list-inline-item text-body-tertiary">•</li>
                        <li class="list-inline-item">
                            <a href="/privacidade" class="link-fitness text-decoration-none">
                                Privacidade
                            </a>
                        </li>
```

### Passo 5: Testar a página

1. Inicie o servidor (se não estiver rodando): `python main.py`
2. Acesse no navegador: `http://localhost:8405/privacidade`
3. Verifique se a página está exibindo corretamente

### Passo 6: Commitar as alterações

```bash
git add .
git commit -m "feat: adicionar página de política de privacidade

- Criar template privacidade.html com seções informativas
- Adicionar rota /privacidade em public_routes.py
- Adicionar link no rodapé do site"
```

---

## ATIVIDADE DO ALUNO 4: Adicionar Seção de Depoimentos na Página Inicial

**Objetivo:** Criar uma seção de depoimentos/testemunhos de alunos na página inicial.

**Tempo estimado:** 40-50 minutos

### Passo 1: Criar sua branch

Abra o terminal na pasta do projeto e execute:

```bash
git checkout main
git pull origin main
git checkout -b aluno4
```

### Passo 2: Editar a página inicial

Abra o arquivo `templates/index.html` e procure pela seção de CTA (procure por `<!-- CTA Section`). **Antes** dessa seção, adicione o seguinte código:

```html
<!-- Depoimentos Section -->
<div class="mb-5" id="depoimentos">
    <div class="text-center mb-5">
        <span class="badge-fitness-orange rounded-pill px-3 py-2 mb-2" style="display: inline-block;">
            <i class="bi bi-chat-quote me-1"></i>Depoimentos
        </span>
        <h2 class="fw-bold display-6" style="font-family: 'Montserrat', sans-serif;">O que nossos alunos dizem</h2>
        <p class="text-body-secondary col-lg-6 mx-auto">
            Veja o que nossos alunos têm a dizer sobre a experiência com o AgendaFit
        </p>
    </div>

    <div class="row g-4">
        <!-- Depoimento 1 -->
        <div class="col-md-6 col-lg-4">
            <div class="card card-fitness h-100 bg-body border-0 shadow-sm">
                <div class="card-body p-4">
                    <div class="d-flex mb-3">
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                    </div>
                    <p class="card-text text-body-secondary mb-4" style="font-style: italic;">
                        "O sistema de agendamento facilitou muito minha rotina de treinos.
                        Agora consigo me organizar melhor e nunca perco uma aula!"
                    </p>
                    <div class="d-flex align-items-center">
                        <div class="d-inline-flex align-items-center justify-content-center rounded-circle me-3"
                             style="width: 50px; height: 50px; background: linear-gradient(135deg, #FF6B35 0%, #9B51E0 100%);">
                            <span class="text-white fw-bold">MA</span>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-semibold">Maria Almeida</h6>
                            <small class="text-body-secondary">Aluna há 8 meses</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Depoimento 2 -->
        <div class="col-md-6 col-lg-4">
            <div class="card card-fitness h-100 bg-body border-0 shadow-sm">
                <div class="card-body p-4">
                    <div class="d-flex mb-3">
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                    </div>
                    <p class="card-text text-body-secondary mb-4" style="font-style: italic;">
                        "Excelente plataforma! O controle de pagamentos e a comunicação
                        com os professores ficaram muito mais práticos."
                    </p>
                    <div class="d-flex align-items-center">
                        <div class="d-inline-flex align-items-center justify-content-center rounded-circle me-3"
                             style="width: 50px; height: 50px; background: linear-gradient(135deg, #1AA260 0%, #00BCD4 100%);">
                            <span class="text-white fw-bold">CS</span>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-semibold">Carlos Silva</h6>
                            <small class="text-body-secondary">Aluno há 1 ano</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Depoimento 3 -->
        <div class="col-md-6 col-lg-4">
            <div class="card card-fitness h-100 bg-body border-0 shadow-sm">
                <div class="card-body p-4">
                    <div class="d-flex mb-3">
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-half text-warning"></i>
                    </div>
                    <p class="card-text text-body-secondary mb-4" style="font-style: italic;">
                        "Como professora, o sistema me ajuda a gerenciar todas as minhas turmas
                        de forma organizada. Recomendo muito!"
                    </p>
                    <div class="d-flex align-items-center">
                        <div class="d-inline-flex align-items-center justify-content-center rounded-circle me-3"
                             style="width: 50px; height: 50px; background: linear-gradient(135deg, #004E89 0%, #9B51E0 100%);">
                            <span class="text-white fw-bold">JO</span>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-semibold">Juliana Oliveira</h6>
                            <small class="text-body-secondary">Professora de Pilates</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Depoimento 4 -->
        <div class="col-md-6 col-lg-4">
            <div class="card card-fitness h-100 bg-body border-0 shadow-sm">
                <div class="card-body p-4">
                    <div class="d-flex mb-3">
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                    </div>
                    <p class="card-text text-body-secondary mb-4" style="font-style: italic;">
                        "A interface é muito intuitiva e bonita. Mesmo não sendo muito
                        familiarizado com tecnologia, consigo usar sem problemas."
                    </p>
                    <div class="d-flex align-items-center">
                        <div class="d-inline-flex align-items-center justify-content-center rounded-circle me-3"
                             style="width: 50px; height: 50px; background: linear-gradient(135deg, #FF6B35 0%, #1AA260 100%);">
                            <span class="text-white fw-bold">RF</span>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-semibold">Roberto Ferreira</h6>
                            <small class="text-body-secondary">Aluno há 3 meses</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Depoimento 5 -->
        <div class="col-md-6 col-lg-4">
            <div class="card card-fitness h-100 bg-body border-0 shadow-sm">
                <div class="card-body p-4">
                    <div class="d-flex mb-3">
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                    </div>
                    <p class="card-text text-body-secondary mb-4" style="font-style: italic;">
                        "O chat com os professores é muito útil para tirar dúvidas rapidamente.
                        Adoro a praticidade do sistema!"
                    </p>
                    <div class="d-flex align-items-center">
                        <div class="d-inline-flex align-items-center justify-content-center rounded-circle me-3"
                             style="width: 50px; height: 50px; background: linear-gradient(135deg, #9B51E0 0%, #00BCD4 100%);">
                            <span class="text-white fw-bold">AC</span>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-semibold">Amanda Costa</h6>
                            <small class="text-body-secondary">Aluna há 6 meses</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Depoimento 6 -->
        <div class="col-md-6 col-lg-4">
            <div class="card card-fitness h-100 bg-body border-0 shadow-sm">
                <div class="card-body p-4">
                    <div class="d-flex mb-3">
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                        <i class="bi bi-star-fill text-warning"></i>
                    </div>
                    <p class="card-text text-body-secondary mb-4" style="font-style: italic;">
                        "Finalmente um sistema que funciona! Acompanho meus pagamentos e
                        horários de aula sem nenhuma complicação."
                    </p>
                    <div class="d-flex align-items-center">
                        <div class="d-inline-flex align-items-center justify-content-center rounded-circle me-3"
                             style="width: 50px; height: 50px; background: linear-gradient(135deg, #1AA260 0%, #FF6B35 100%);">
                            <span class="text-white fw-bold">PS</span>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-semibold">Pedro Santos</h6>
                            <small class="text-body-secondary">Aluno há 4 meses</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

### Passo 3: Testar a página

1. Inicie o servidor (se não estiver rodando): `python main.py`
2. Acesse no navegador: `http://localhost:8405/`
3. Role a página para ver a nova seção de depoimentos

### Passo 4: Commitar as alterações

```bash
git add .
git commit -m "feat: adicionar seção de depoimentos na página inicial

- Criar 6 cards de depoimentos com avaliações em estrelas
- Adicionar avatares estilizados com iniciais
- Incluir informações de tempo como aluno/professor"
```

---

## Resumo das Atividades

| Aluno | Atividade | Arquivos Modificados/Criados |
|-------|-----------|------------------------------|
| Aluno 1 | Página de Contato | `templates/contato.html`, `routes/public_routes.py`, `templates/base_publica.html` |
| Aluno 2 | Seção de Horário de Funcionamento | `templates/index.html` |
| Aluno 3 | Página de Política de Privacidade | `templates/privacidade.html`, `routes/public_routes.py`, `templates/base_publica.html` |
| Aluno 4 | Seção de Depoimentos | `templates/index.html` |

## Observações Importantes

1. **Cada aluno deve trabalhar em sua própria branch** para evitar conflitos
2. **Não façam merge** das branches até que o professor revise
3. **Testem as alterações** antes de commitar
4. Em caso de dúvidas, consultem o professor
