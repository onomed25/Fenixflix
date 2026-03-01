# Usa uma imagem do Python como base
FROM python:3.10-bullseye

# Instala o Go e ferramentas do sistema
RUN apt-get update && apt-get install -y golang git

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

# Instala o navegador Chromium dentro do Go (corrige aquele seu erro antigo!)
RUN go run github.com/playwright-community/playwright-go/cmd/playwright@latest install --with-deps chromium

# Dá permissão para rodar o script de inicialização
RUN chmod +x start.sh

# Libera a porta 8000 para a internet
EXPOSE 8000

# Comando para iniciar tudo
CMD ["./start.sh"]
