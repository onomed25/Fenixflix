# Use a imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o conteúdo da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta em que a aplicação irá rodar
EXPOSE 80

# Comando para rodar a aplicação usando Gunicorn
# render
#CMD ["gunicorn", "app:app_", "--bind", "0.0.0.0:80", "--log-level", "debug", "--access-logfile", "-"]
# beamup cli
#CMD ["sh", "-c", "gunicorn app:app_ --bind 0.0.0.0:${PORT} --log-level debug --access-logfile -"]
CMD ["python", "app.py"]