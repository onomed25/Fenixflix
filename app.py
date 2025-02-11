from flask import Flask, jsonify, request, make_response, render_template, Response
from netcine import catalog_search, search_link
import json
import requests
import canais

app_ = Flask(__name__)

# Função para adicionar headers CORS
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # Permite todos os domínios
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Métodos permitidos
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Headers permitidos
    return response


MANIFEST = {
    "id": "com.skyflix",
    "version": "1.0.0",
    "name": "SKYFLIX",
    "description": "Tenha o melhor dos filmes e séries com Skyflix",
    "logo": "https://i.imgur.com/qVgkbYn.png",
    "resources": ["catalog", "meta", "stream"],
    "types": ["tv", "movie", "series"],
    "catalogs": [
        {
            "type": "tv",
            "id": "skyflix",
            "name": "SKYFLIX",
            "extra": [
                {
                    "name": "genre",
                    "options": [
                        "Canais Abertos",
                        "Variedades",
                        "Filmes e Series",
                        "Documentarios",
                        "Esportes",
                        "Infantil",
                        "Noticias",
                        "PLUTO TV",
                        "CANAL 24H"
                    ],
                    "isRequired": False
                }
            ]
        },
        {
            "type": "movie",
            "id": "skyflix",
            "name": "SKYFLIX",
            "extraSupported": ["search"]
        },
        {
            "type": "series",
            "id": "skyflix",
            "name": "SKYFLIX",
            "extraSupported": ["search"]
        }
    ],
    "idPrefixes": ["skyflix", "tt"]
}


@app_.route('/')
def home():
    name = MANIFEST['name']
    types = MANIFEST['types']
    logo = MANIFEST['logo']
    description = MANIFEST['description']
    version = MANIFEST['version']
    return render_template('index.html', name=name, types=types, logo=logo, description=description, version=version)

@app_.route('/logo')
def proxy_logo():
    image_url = request.args.get('url')

    if not image_url:
        return "Erro: Nenhuma URL fornecida", 400

    try:
        response = requests.get(image_url, stream=True)

        if response.status_code != 200:
            return f"Erro ao buscar a imagem: {response.status_code}", 400

        content_type = response.headers.get('Content-Type', 'image/jpeg')

        # Criar a resposta e adicionar os headers CORS manualmente
        resp = Response(response.content, content_type=content_type)
        resp.headers['Access-Control-Allow-Origin'] = '*'  # Permite acesso de qualquer origem
        resp.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'  # Métodos permitidos
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Permite cabeçalhos específicos

        return resp

    except requests.exceptions.RequestException as e:
        return f"Erro ao buscar a imagem: {str(e)}", 500

# Rota para o manifesto do addon
@app_.route('/manifest.json')
def manifest():
    response = jsonify(MANIFEST)
    return add_cors_headers(response)

@app_.route('/catalog/tv/skyflix/genre=<id>.json')
def genres(id):
    host = request.host
    if 'localhost' in host or '127.0.0.1' in host:
        server = f'http://{host}/logo?url='
    else:
        server = f'https://{host}/logo?url='
    canais_ = []
    if not 'skip' in id:
        list_canais = canais.canais_list(server)
        for canal in list_canais:
            canal.pop('streams')
            if id in canal['genres']:
                canais_.append(canal)      
    response = jsonify({
    "metas": canais_
    })
    return add_cors_headers(response)

# Rota para o catálogo
@app_.route('/catalog/<type>/<id>.json')
def catalog_route(type, id):
    host = request.host
    if 'localhost' in host or '127.0.0.1' in host:
        server = f'http://{host}/logo?url='
    else:
        server = f'https://{host}/logo?url='      
    if type == 'tv':
        canais_ = []
        list_canais = canais.canais_list(server)
        for canal in list_canais:
            canal.pop('streams')
            canais_.append(canal)
        response = jsonify({
        "metas": canais_  
            })      
    else:
        response = jsonify({
        "metas": []
    })  
    return add_cors_headers(response)

# Rota para pesquisa
@app_.route('/catalog/<type>/skyflix/search=<query>.json')
def search(type, query):
    catalog = catalog_search(query)
    if catalog:
        results = [item for item in catalog if item.get('type', '') == type]
    else:
        results = []
    response = jsonify({
        "metas": results
    })
    return add_cors_headers(response)

@app_.route('/meta/<type>/<id>.json')
def meta(type,id):
    host = request.host
    if 'localhost' in host or '127.0.0.1' in host:
        server = f'http://{host}/logo?url='
    else:
        server = f'https://{host}/logo?url='      
    if type == 'tv':
        meta = {}
        list_canais = canais.canais_list(server)
        for canal in list_canais:
            if canal['id'] == id:
                canal.pop('streams')
                meta['meta'] = canal
                break
        response = jsonify(meta)               

    else:
        response = jsonify({
        "meta": {}
        })
    return add_cors_headers(response)
           

# Rota para streams (exemplo simples)
@app_.route('/stream/<type>/<id>.json')
def stream(type, id):
    host = request.host
    if 'localhost' in host or '127.0.0.1' in host:
        server = f'http://{host}/logo?url='
    else:
        server = f'https://{host}/logo?url='      
    if type == 'tv':
        scrape_ = []
        list_canais = canais.canais_list(server)
        for canal in list_canais:
            if canal['id'] == id:
                streams_list = canal['streams']
                scrape_ = streams_list
                break
    elif type == 'movie' or type == 'series':
        try:
            stream_, headers = search_link(id)
            scrape_ = [{
                    "url": stream_,
                    "name": "SKYFLIX",
                    "description": "Netcine",
                    "behaviorHints": {
                        "notWebReady": True,
                        "proxyHeaders": {
                            "request": {
                                "User-Agent": headers['User-Agent'],
                                "Referer": headers['Referer'],
                                "Cookie": headers['Cookie']
                            }
                        }
                    }
                }]
        except:
            scrape_ = []
    else:
        scrape_ = []  
    response = jsonify({
        "streams": scrape_
    })
    return add_cors_headers(response)

# Rota para lidar com requisições OPTIONS (necessário para CORS)
@app_.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    response = make_response()
    return add_cors_headers(response)

# if __name__ == '__main__':
#     # executar server
#     app_.run(debug=True ,host='0.0.0.0', port=80)
