# Usa uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para o Playwright e Python
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto
COPY . .

# Instala as bibliotecas do Python
RUN pip install --no-cache-dir -r requirements.txt

# --- AQUI ESTÁ O COMANDO MÁGICO ---
# Instala o Firefox e as dependências do sistema dele
RUN playwright install --with-deps firefox

# Comando para iniciar o site
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
