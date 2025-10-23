#!/bin/bash
set -e

echo "========================================="
echo "AgendaFit - Fix completo no VPS"
echo "========================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se está no diretório correto
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ ERRO: Execute este script no diretório raiz do projeto!${NC}"
    exit 1
fi

echo -e "${YELLOW}1. Atualizando código do repositório...${NC}"
git fetch --all
git pull origin main

echo ""
echo -e "${YELLOW}2. Parando containers...${NC}"
docker-compose down || true

echo ""
echo -e "${YELLOW}3. Removendo imagens antigas do AgendaFit...${NC}"
docker images | grep -E 'agendafit|agendafit.cachoeiro.es' | awk '{print $3}' | xargs docker rmi -f || true

echo ""
echo -e "${YELLOW}4. Limpando cache do builder...${NC}"
docker builder prune -a -f

echo ""
echo -e "${YELLOW}5. Verificando Dockerfile...${NC}"
if grep -q "WORKDIR /app" Dockerfile && grep -q "PYTHONPATH=/app" Dockerfile; then
    echo -e "${GREEN}✅ Dockerfile está correto!${NC}"
else
    echo -e "${RED}❌ ERRO: Dockerfile não está correto!${NC}"
    echo "Execute 'cat Dockerfile' e verifique se contém:"
    echo "  - WORKDIR /app"
    echo "  - PYTHONPATH=/app"
    exit 1
fi

echo ""
echo -e "${YELLOW}6. Fazendo rebuild completo (sem cache)...${NC}"
docker-compose build --no-cache

echo ""
echo -e "${YELLOW}7. Testando import dentro da imagem...${NC}"
IMAGE_NAME=$(docker images --format '{{.Repository}}:{{.Tag}}' | grep agendafit | head -1)
if docker run --rm "$IMAGE_NAME" python -c "from model.atividade_model import Atividade; print('✅ Import OK')" 2>&1 | grep -q "Import OK"; then
    echo -e "${GREEN}✅ Teste de import passou!${NC}"
else
    echo -e "${RED}❌ ERRO: Teste de import falhou!${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}8. Iniciando containers...${NC}"
docker-compose up -d

echo ""
echo -e "${YELLOW}9. Aguardando inicialização (5s)...${NC}"
sleep 5

echo ""
echo -e "${YELLOW}10. Verificando status dos containers...${NC}"
docker-compose ps

echo ""
echo -e "${YELLOW}11. Últimas 30 linhas de log:${NC}"
echo "========================================="
docker-compose logs --tail=30

echo ""
echo "========================================="
echo -e "${GREEN}✅ Fix concluído!${NC}"
echo ""
echo "Comandos úteis:"
echo "  - Ver logs: docker-compose logs -f"
echo "  - Ver status: docker-compose ps"
echo "  - Reiniciar: docker-compose restart"
echo "========================================="
