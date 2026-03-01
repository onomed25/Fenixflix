#!/bin/bash

# Inicia o servidor Go (extrator) em segundo plano
go run main.go &

# Inicia o servidor Python (API principal) em primeiro plano
uvicorn app:app --host 0.0.0.0 --port 8000
