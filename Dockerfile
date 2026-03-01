# Estágio 1: Compilar o binário Go
FROM golang:1.21-bullseye AS go-builder
WORKDIR /app
COPY main.go .
# Instala as dependências do Go e compila
RUN go mod init fenix-extractor && go mod tidy
RUN go build -o fenix-extractor main.go

# Estágio 2: Ambiente final com Python e Playwright
FROM python:3.10-bullseye
WORKDIR /app

# Instalar dependências de sistema para o Playwright
RUN apt-get update && apt-get install -y \
    libicu-dev \
    libvpx-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar o binário compilado do Go do estágio anterior
COPY --from=go-builder /app/fenix-extractor /app/fenix-extractor

# Copiar os ficheiros do projeto Python
COPY . .

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar navegadores do Playwright
RUN playwright install chromium --with-deps

# Dar permissão de execução ao script e ao binário
RUN chmod +x start.sh /app/fenix-extractor

# Porta da API Python
EXPOSE 8000

# Usar o script de inicialização
CMD ["./start.sh"]
