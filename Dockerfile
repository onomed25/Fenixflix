# Usa uma imagem do Python como base
FROM python:3.10-bullseye

# Instala o Go
COPY --from=golang:1.21-bullseye /usr/local/go/ /usr/local/go/
ENV PATH="/usr/local/go/bin:${PATH}"

# Define o diretório de trabalho
WORKDIR /app

# Copia todos os ficheiros
COPY . .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala o Playwright e as dependências do navegador
RUN playwright install chromium --with-deps

# Dá permissão de execução ao script de inicialização
RUN chmod +x start.sh

# Libera a porta 8000 (API Python)
EXPOSE 8000

# Inicia o processo através do script que roda Go e Python juntos
CMD ["./start.sh"]
