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

# Copia o script de entrypoint primeiro
COPY entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh

# Copia o restante do código
COPY . .

# Porta interna onde o Uvicorn escutará
EXPOSE 8000

# Usa o entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
