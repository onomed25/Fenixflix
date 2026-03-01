#!/bin/bash
# Inicia o extrator/proxy compilado em segundo plano
./fenix-extractor &

# Inicia o Python em primeiro plano
uvicorn app:app --host 0.0.0.0 --port 8000
