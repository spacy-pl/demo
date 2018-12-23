from flask import Flask, render_template, request, jsonify
from flask_assets import Environment, Bundle

from spacy_pl_demo import (
    web,
    lemmatizer as lemmatizer_demo
)

app = Flask('spacy-pl-demo', static_folder='static')
assets = Environment(app)
bundles = {
    'css': Bundle(
        'src/uikit/css/uikit.css',
        output='build/styles.css',
        filters='cssmin'
    ),
    'js': Bundle(
        'src/uikit/js/uikit.js',
        'src/uikit/js/uikit-icons.js',
        'src/axios/axios.js',
        'src/main.js',
        output='build/bundle.js',
        filters='jsmin'
    )
}
assets.register(bundles)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lemmatizer', methods=['POST'])
def lemmatizer():
    if not request.is_json:
        return jsonify({}), 400
    query = request.json.get('query', '')
    print(f"query={repr(query)}")
    sp = lemmatizer_demo.SearchProcessor()
    search_results = sp.process_query(query)
    json_results = jsonify([sr._asdict() for sr in search_results])
    return json_results, 200
