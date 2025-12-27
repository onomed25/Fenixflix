# Usa uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema básicas
# (O playwright install-deps cuidará das libs específicas do navegador depois)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos
COPY . .

# Instala as bibliotecas do Python
RUN pip install --no-cache-dir -r requirements.txt

# --- CORREÇÃO ---
# O erro anterior indicava que o Python busca o CHROMIUM.
# A flag --with-deps instala automaticamente as dependências do sistema operacional necessárias.
RUN playwright install --with-deps chromium

# Usa a variável de ambiente $PORT fornecida pelo Render
# Nota: Manter neste formato (sem colchetes []) é essencial para o $PORT funcionar
CMD uvicorn app:app --host 0.0.0.0 --port $PORT
