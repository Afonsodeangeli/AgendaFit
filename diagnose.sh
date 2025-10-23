#!/bin/bash

echo "========================================="
echo "AgendaFit - Script de Diagnóstico"
echo "========================================="
echo ""

# Verifica se está no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ ERRO: Execute este script no diretório raiz do projeto!"
    exit 1
fi

echo "1. Verificando Dockerfile..."
if grep -q "WORKDIR /app" Dockerfile; then
    echo "✅ WORKDIR /app encontrado"
else
    echo "❌ WORKDIR /app NÃO encontrado no Dockerfile!"
fi

if grep -q "PYTHONPATH=/app" Dockerfile; then
    echo "✅ PYTHONPATH=/app encontrado"
else
    echo "❌ PYTHONPATH=/app NÃO encontrado no Dockerfile!"
fi

echo ""
echo "2. Verificando estrutura de arquivos..."
if [ -f "model/__init__.py" ]; then
    echo "✅ model/__init__.py existe"
else
    echo "❌ model/__init__.py NÃO existe!"
fi

if [ -f "model/atividade_model.py" ]; then
    echo "✅ model/atividade_model.py existe"
else
    echo "❌ model/atividade_model.py NÃO existe!"
fi

if [ -f "repo/__init__.py" ]; then
    echo "✅ repo/__init__.py existe"
else
    echo "❌ repo/__init__.py NÃO existe!"
fi

echo ""
echo "3. Mostrando conteúdo do Dockerfile:"
echo "========================================="
cat Dockerfile
echo "========================================="

echo ""
echo "4. Verificando último commit:"
git log -1 --oneline

echo ""
echo "5. Verificando branch:"
git branch --show-current

echo ""
echo "========================================="
echo "Diagnóstico concluído!"
echo "========================================="
