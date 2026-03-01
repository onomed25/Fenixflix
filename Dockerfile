# Usa uma imagem do Python como base
FROM python:3.10-bullseye

# Define o diretório de trabalho no servidor
WORKDIR /app

# Copia todos os ficheiros do seu projeto para dentro do servidor
COPY . .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala o navegador Chromium do Playwright para o Python
RUN playwright install chromium --with-deps

# Libera a porta 8000 para a internet
EXPOSE 8000

# Inicia o servidor Python diretamente
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
