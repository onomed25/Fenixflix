# Usa uma imagem do Python como base (Debian Bullseye)
FROM python:3.10-bullseye

# Instala git e wget (necessários para transferir o Go moderno)
RUN apt-get update && apt-get install -y git wget

# Transfere e instala a versão mais recente do Go (1.22) direto da fonte oficial
RUN wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz && \
    rm go1.22.0.linux-amd64.tar.gz

# Diz ao sistema Linux onde encontrar o Go que acabámos de instalar
ENV PATH="/usr/local/go/bin:${PATH}"

# Define o diretório de trabalho no servidor
WORKDIR /app

# Copia todos os ficheiros do seu projeto para dentro do servidor
COPY . .

# Instala as dependências do Python (FastAPI, httpx, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Inicializa o projeto Go e instala a biblioteca do Playwright
RUN go mod init extrator || true
RUN go mod tidy || true
RUN go get github.com/playwright-community/playwright-go

# Instala o driver do Playwright e o navegador Chromium com todas as dependências do sistema
RUN go run github.com/playwright-community/playwright-go/cmd/playwright@latest install --with-deps chromium

# Dá permissão de execução ao script de arranque
RUN chmod +x start.sh

# Libera a porta 8000 para a internet
EXPOSE 8000

# Comando final que executa o ficheiro start.sh (que liga o Go e o Python)
CMD ["./start.sh"]
