from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORS

app = FastAPI()

# Configurar CORS (opcional, caso precise de suporte a cross-origin)
app.add_middleware(
    CORS,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL de destino para o redirecionamento
TARGET_URL = "https://zoreu-skyflix.hf.space"

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def redirect_all(request: Request, path: str):
    # Constrói a URL completa com o path original
    redirect_url = f"{TARGET_URL}/{path}"
    
    # Preserva os query parameters, se houver
    if request.query_params:
        redirect_url += f"?{request.query_params}"
    
    return RedirectResponse(url=redirect_url, status_code=307)