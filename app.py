from flask import Flask, render_template, request, jsonify
from flask_assets import Environment, Bundle

from spacy_pl_demo import (
    search as search_demo,
    similarity as similarity_demo,
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
        # filters='jsmin'  # TODO: This does not handle template strings properly (whitespace is squashed)
    )
}
assets.register(bundles)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search-demo', methods=['POST'])
def search_demo_handler():
    """
    Request schema: {'query': <list of words to search: str>}
    Response schema: [{'token_text': str, 'direct_match': bool, 'lemma_match': bool}]
    """
    if not request.is_json:
        return jsonify({}), 400
    query = request.json.get('query', '')
    print(f"query={repr(query)}")
    sp = search_demo.SearchProcessor()
    search_results = sp.process_query(query)
    search_results_json = jsonify([sr._asdict() for sr in search_results])
    return search_results_json, 200


@app.route('/similarity-demo', methods=['POST'])
def similarity_demo_handler():
    """
    Request schema: {'words': <list of words to search: str>}
    Response schema: {'td' <list of rows:<list of column values>>, 'th': <list of table column names>}
    """
    if not request.is_json:
        return jsonify({}), 400
    words = request.json.get('words', [])
    sc = similarity_demo.SimilarityCalculator()
    similarities = sc.calculate_pairwise_similarity(words)
    table_headers = ['word'] + sc.used_words  # 1st column and header will contain words
    table_rows = [
        [word] + [f"{sim_val:0.2f}" for sim_val in similarity_row]
        for word, similarity_row in zip(sc.used_words, similarities)
    ]
    return jsonify({
        'td': table_rows,
        'th': table_headers
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
