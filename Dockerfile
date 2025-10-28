# Usa a imagem oficial do Python como imagem base
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Evita geração de .pyc e buffer no stdout
# Define PYTHONPATH para /app para resolver imports
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Instala dependências do projeto
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Verifica estrutura de diretórios e testa import antes de iniciar
# Não usa script separado - faz tudo direto no CMD
EXPOSE 8000

CMD ["sh", "-c", "\
echo '=========================================' && \
echo '=== AgendaFit Container Starting ===' && \
echo '=========================================' && \
echo '' && \
echo 'Working directory:' && pwd && \
echo 'Python version:' && python --version && \
echo 'PYTHONPATH:' $PYTHONPATH && \
echo '' && \
echo 'Checking project structure...' && \
ls -la /app/ | head -20 && \
echo '' && \
echo 'Checking model directory...' && \
ls -la /app/model/ && \
echo '' && \
echo 'Testing Python import...' && \
cd /app && \
python -c 'from model.atividade_model import Atividade; print(\"Import test SUCCESSFUL!\")' && \
echo '' && \
echo '=========================================' && \
echo 'Starting uvicorn server...' && \
echo '=========================================' && \
exec uvicorn main:app --host 0.0.0.0 --port 8000 \
"]
