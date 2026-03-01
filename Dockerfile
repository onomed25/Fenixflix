# Usa uma imagem do Python como base
FROM python:3.10-bullseye

# Instala git e wget (para baixar o Go moderno)
RUN apt-get update && apt-get install -y git wget

# Baixa e instala o Go mais recente (1.22) direto da fonte
RUN wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz && \
    rm go1.22.0.linux-amd64.tar.gz

# Diz para o Linux onde encontrar o Go que acabamos de instalar
ENV PATH="/usr/local/go/bin:${PATH}"

# Define o diretório de trabalho
WORKDIR /app

# Copia tudo para o servidor
COPY . .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Inicializa o projeto Go e instala o Playwright Go
RUN go mod init extrator || true
RUN go mod tidy || true
RUN go get github.com/playwright-community/playwright-go

# Instala o navegador Chromium dentro do Go
RUN go run github.com/playwright-community/playwright-go/cmd/playwright@latest install --with-deps chromium

# Dá permissão para rodar o script de inicialização
RUN chmod +x start.sh

# Libera a porta 8000 para a internet
EXPOSE 8000

# Comando para iniciar tudo
CMD ["./start.sh"]
