from flask import Flask, render_template, request

from spacy_pl_demo import (
    web,
    lemmatizer as lemmatizer_demo
)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        'index.html',
        menu_items=web.menu_for_page()
    )

@app.route('/lemmatizer', methods=['GET', 'POST'])
def lemmatizer():
    menu = web.menu_for_page('Lemmatizer')
    query = request.form.get('query', default='')
    print(f"query={repr(query)}")
    sp = lemmatizer_demo.SearchProcessor()
    search_results = sp.process_query(query)
    return render_template(
        'lemmatizer.html',
        page_subtitle=' - lemmatizer demo',
        menu_items=menu,
        search_results=search_results,
        query=query
    )
