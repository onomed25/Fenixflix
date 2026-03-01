FROM python:3.9-slim

WORKDIR /app

COPY . .

# Sem necessidade de apt-get install wget gnupg ou playwright install
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium --with-deps

CMD uvicorn app:app --host 0.0.0.0 --port $PORT
