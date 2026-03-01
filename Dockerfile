# Estágio 1: Compilar o binário Go de forma simples
FROM golang:1.21-bullseye AS go-builder
WORKDIR /app
COPY main.go .
# Cria o módulo e compila o extrator
RUN go mod init fenix-extractor && go mod tidy
RUN go build -o fenix-extractor main.go

# Estágio 2: Ambiente Python (Final)
FROM python:3.10-slim-bullseye
WORKDIR /app

# Instalar apenas o necessário para o Playwright rodar
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar o binário do Go
COPY --from=go-builder /app/fenix-extractor /app/fenix-extractor

# Copiar os ficheiros do projeto
COPY . .

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar o Chromium e as dependências de sistema do navegador
# O comando --with-deps instala as bibliotecas que faltavam (libicu, libvpx, etc)
RUN playwright install chromium --with-deps

# Garantir permissões
RUN chmod +x start.sh /app/fenix-extractor

EXPOSE 8000

CMD ["./start.sh"]
