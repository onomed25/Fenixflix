# Estágio 1: Compilar o binário Go (Atualizado para 1.22)
FROM golang:1.22-bullseye AS go-builder
WORKDIR /app
COPY main.go .
# Cria o módulo e compila o extrator
RUN go mod init fenix-extractor && go mod tidy
RUN go build -o fenix-extractor main.go

# Estágio 2: Ambiente Python (Final)
FROM python:3.10-slim-bullseye
WORKDIR /app

# Instalar dependências de sistema necessárias
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar o binário do Go do estágio anterior
COPY --from=go-builder /app/fenix-extractor /app/fenix-extractor

# Copiar os ficheiros do projeto
COPY . .

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar navegadores e dependências do Playwright
RUN playwright install chromium --with-deps

# Garantir permissões de execução
RUN chmod +x start.sh /app/fenix-extractor

EXPOSE 8000

CMD ["./start.sh"]
