# Guia de Troubleshooting - Jenkins + Docker

## Problema: ModuleNotFoundError no container

### Passo 1: Verificar se o código está atualizado no VPS

```bash
# No servidor VPS, entre no diretório do projeto
cd /caminho/do/projeto/AgendaFit

# Execute o script de diagnóstico
chmod +x diagnose.sh
./diagnose.sh
```

### Passo 2: Verificar configuração do Jenkins

1. **Acesse o Jenkins**: http://seu-jenkins.com
2. **Vá no seu Job**: AgendaFit ou nome similar
3. **Clique em "Configure"**
4. **Verifique a seção "Build"**

#### O que verificar:

**a) Source Code Management (Git)**
```bash
# Deve ter algo como:
Repository URL: https://github.com/seu-usuario/AgendaFit
Branch: */main (ou a branch correta)
```

**b) Build Steps**

Verifique se os comandos estão assim:

```bash
# ERRADO - sem --no-cache
docker-compose build
docker-compose up -d

# CORRETO - com --no-cache
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Passo 3: Limpar cache do Docker no VPS

```bash
# No VPS, execute:
cd /caminho/do/projeto/AgendaFit

# Para containers
docker-compose down

# Remove TODAS as imagens do projeto (cuidado!)
docker images | grep agendafit | awk '{print $3}' | xargs docker rmi -f

# Limpa builder cache
docker builder prune -a -f

# Rebuild completo
docker-compose build --no-cache
docker-compose up -d
```

### Passo 4: Verificar logs

```bash
# Ver logs do container
docker-compose logs -f

# OU se estiver usando Portainer
# Vá em Containers > agendafit.cachoeiro.es > Logs
```

### Passo 5: Testar manualmente no VPS

```bash
# No VPS
cd /caminho/do/projeto/AgendaFit

# Teste se o Dockerfile está correto
docker build -t agendafit-manual --no-cache .

# Teste o import
docker run --rm agendafit-manual python -c "from model.atividade_model import Atividade; print('OK')"

# Se retornar "OK", a imagem está correta!
```

### Passo 6: Atualizar configuração do Jenkins

**Opção A: Via interface web**

1. Vá em Configure > Build
2. Adicione antes do build:
```bash
git pull origin main
docker builder prune -f
```

3. Modifique o comando de build:
```bash
docker-compose build --no-cache
```

**Opção B: Criar um script de build**

Crie `build.sh` no projeto:
```bash
#!/bin/bash
set -e

echo "Limpando cache..."
docker builder prune -f

echo "Parando containers..."
docker-compose down

echo "Removendo imagens antigas..."
docker images | grep agendafit | awk '{print $3}' | xargs docker rmi -f || true

echo "Build sem cache..."
docker-compose build --no-cache

echo "Iniciando containers..."
docker-compose up -d

echo "Logs:"
docker-compose logs --tail=50
```

No Jenkins, apenas execute:
```bash
chmod +x build.sh
./build.sh
```

## Checklist Final

- [ ] Código atualizado no VPS (`git pull`)
- [ ] Dockerfile contém `WORKDIR /app`
- [ ] Dockerfile contém `PYTHONPATH=/app`
- [ ] Jenkins faz `git pull` antes do build
- [ ] Jenkins usa `--no-cache` no build
- [ ] Cache do Docker foi limpo no VPS
- [ ] Container inicia sem erros

## Comandos Úteis

```bash
# Ver todas as imagens
docker images

# Ver todos os containers
docker ps -a

# Logs em tempo real
docker-compose logs -f

# Rebuild total (script automático)
./rebuild.sh

# Diagnóstico
./diagnose.sh

# Entrar no container (debug)
docker exec -it agendafit.cachoeiro.es /bin/bash

# Dentro do container, teste:
cd /app
python -c "from model.atividade_model import Atividade; print('OK')"
```
