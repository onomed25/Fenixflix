from flask import Flask, jsonify, abort, render_template
from scrape import movie_frembed, serie_frembed

app = Flask(__name__)

MANIFEST = {
    'id': 'com.skyflix',
    'version': '1.0.0',
    'name': 'SKY FLIX',
    'description': 'SKYFLIX offers streaming of movies and series',
    'logo': 'https://i.imgur.com/qVgkbYn.png',
    'resources': ['stream'],
    'types': ['movie', 'series'],
    'idPrefixes': ['tt'],
    'catalogs': []  # Sem catálogos por enquanto
}

def respond_with(data):
    resp = jsonify(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

@app.route('/')
def home():
    name = MANIFEST['name']
    types = MANIFEST['types']
    logo = MANIFEST['logo']
    description = MANIFEST['description']
    version = MANIFEST['version']
    return render_template('index.html', name=name, types=types, logo=logo, description=description, version=version)


@app.route('/manifest.json')
def addon_manifest():
    return respond_with(MANIFEST)

@app.route('/stream/<type>/<id>.json')
def addon_stream(type, id):
    if type not in MANIFEST['types']:
        abort(404)

    streams = {'streams': []}
    if type == 'movie':
        streams['streams'] = movie_frembed(id)
    elif type == 'series':
        streams['streams'] = serie_frembed(id)
    return respond_with(streams)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
