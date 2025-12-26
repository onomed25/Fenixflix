# Usa uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (Playwright)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos
COPY . .

# Instala as bibliotecas
RUN pip install --no-cache-dir -r requirements.txt

# Instala o Firefox
RUN playwright install --with-deps firefox

# --- CORREÇÃO AQUI ---
# Usa a variável de ambiente $PORT fornecida pelo Render
CMD uvicorn app:app --host 0.0.0.0 --port $PORT
