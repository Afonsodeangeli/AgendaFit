#!/bin/bash
set -e

echo "========================================="
echo "=== AgendaFit Container Starting ==="
echo "========================================="
echo ""
echo "📁 Working directory: $(pwd)"
echo "🐍 Python version: $(python --version)"
echo "📦 PYTHONPATH: ${PYTHONPATH:-'(not set)'}"
echo ""

echo "🔍 Checking project structure..."
ls -la /app/ | head -20
echo ""

echo "🔍 Checking model directory..."
if [ -d "/app/model" ]; then
    ls -la /app/model/
    echo ""

    # Verifica se __init__.py existe
    if [ -f "/app/model/__init__.py" ]; then
        echo "✅ model/__init__.py exists"
    else
        echo "❌ WARNING: model/__init__.py NOT found!"
    fi

    # Verifica se atividade_model.py existe
    if [ -f "/app/model/atividade_model.py" ]; then
        echo "✅ model/atividade_model.py exists"
    else
        echo "❌ ERROR: model/atividade_model.py NOT found!"
        exit 1
    fi
else
    echo "❌ ERROR: /app/model directory NOT found!"
    echo "Directory contents:"
    find /app -type d | head -20
    exit 1
fi

echo ""
echo "🧪 Testing Python import..."
cd /app
export PYTHONPATH=/app:$PYTHONPATH

if python -c "from model.atividade_model import Atividade; print('✅ Import test SUCCESSFUL!')"; then
    echo ""
    echo "========================================="
    echo "🚀 Starting uvicorn server..."
    echo "========================================="
    exec uvicorn main:app --host 0.0.0.0 --port 8000
else
    echo ""
    echo "❌ Import test FAILED!"
    echo ""
    echo "Python sys.path:"
    python -c "import sys; print('\n'.join(sys.path))"
    echo ""
    echo "All .py files in /app:"
    find /app -name "*.py" -type f | head -30
    exit 1
fi
