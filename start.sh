#!/bin/bash
# Inicia o extrator em Go em segundo plano
go run main.go &

# Inicia o Python em primeiro plano (mantém o container vivo)
uvicorn app:app --host 0.0.0.0 --port 8000
