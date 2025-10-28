#!/bin/bash

echo "========================================="
echo "AgendaFit - Rebuild e Deploy"
echo "========================================="

# Para os containers
echo "1. Parando containers..."
docker-compose down

# Remove imagens antigas (força rebuild completo)
echo "2. Removendo imagens antigas..."
docker-compose down --rmi all

# Remove volumes órfãos e cache
echo "3. Limpando cache do Docker..."
docker builder prune -f

# Rebuild sem cache
echo "4. Reconstruindo imagem (sem cache)..."
docker-compose build --no-cache

# Inicia os containers
echo "5. Iniciando containers..."
docker-compose up -d

# Aguarda um momento para o container iniciar
echo "6. Aguardando inicialização..."
sleep 3

# Mostra os logs
echo "7. Logs do container:"
echo "========================================="
docker-compose logs --tail=50

echo ""
echo "========================================="
echo "Deploy concluído!"
echo "Para ver os logs em tempo real: docker-compose logs -f"
echo "Para verificar status: docker-compose ps"
echo "========================================="
