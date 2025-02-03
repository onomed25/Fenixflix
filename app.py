from flask import Flask, jsonify, request, make_response, render_template, Response
from netcine import catalog_search, search_link
import json
import requests

app = Flask(__name__)

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


@app.route('/')
def home():
    name = MANIFEST['name']
    types = MANIFEST['types']
    logo = MANIFEST['logo']
    description = MANIFEST['description']
    version = MANIFEST['version']
    return render_template('index.html', name=name, types=types, logo=logo, description=description, version=version)

@app.route('/logo')
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
@app.route('/manifest.json')
def manifest():
    response = jsonify(MANIFEST)
    return add_cors_headers(response)

@app.route('/catalog/tv/skyflix/genre=<id>.json')
def genres(id):
    host = request.host
    if 'localhost' in host or '127.0.0.1' in host:
        server = f'http://{host}/logo?url='
    else:
        server = f'https://{host}/logo?url='
    try:
        r = requests.get(f'https://oneplayhd.com/stremio_oneplay/catalog/tv/OnePlay/genre={id}.json').text
        r = r.replace('oneplay:', 'skyflix:')
        r = r.replace('https', server+'https')
        data = json.loads(r)
        response = jsonify(data) 
    except:
        response = jsonify({
        "metas": []
        })
    return add_cors_headers(response)

# Rota para o catálogo
@app.route('/catalog/<type>/<id>.json')
def catalog_route(type, id):
    host = request.host
    if 'localhost' in host or '127.0.0.1' in host:
        server = f'http://{host}/logo?url='
    else:
        server = f'https://{host}/logo?url='      
    if type == 'tv':
        r = requests.get('https://oneplayhd.com/stremio_oneplay/catalog/tv/OnePlay.json').text
        r = r.replace('oneplay:', 'skyflix:')
        r = r.replace('https', server+'https')
        data = json.loads(r)
        response = jsonify(data)
    else:
        response = jsonify({
        "metas": []
        })
    return add_cors_headers(response)

# Rota para pesquisa
@app.route('/catalog/<type>/skyflix/search=<query>.json')
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

@app.route('/meta/<type>/<id>.json')
def meta(type,id):
    host = request.host
    if 'localhost' in host or '127.0.0.1' in host:
        server = f'http://{host}/logo?url='
    else:
        server = f'https://{host}/logo?url='      
    if type == 'tv':
        id_channels = id.split(':')[1]
        r = requests.get(f'https://oneplayhd.com/stremio_oneplay/meta/tv/oneplay:{id_channels}.json').text
        r = r.replace('oneplay:', 'skyflix:')
        r = r.replace('https', server+'https')
        data = json.loads(r)
        response = jsonify(data)
    else:
        response = jsonify({
        "meta": {}
        })
    return add_cors_headers(response)
           

# Rota para streams (exemplo simples)
@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    if type == 'tv':
        id_channels = id.split(':')[1]
        url = f'https://oneplayhd.com/stremio_oneplay/stream/tv/oneplay:{id_channels}.json'
        r = requests.get(url).json()
        scrape_ = r.get('streams', []) 
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
@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    response = make_response()
    return add_cors_headers(response)

if __name__ == '__main__':
    # executar server
    app.run(debug=True ,host='0.0.0.0', port=80)
