from flask import Flask, jsonify, abort, request, render_template
from flask_assets import Environment, Bundle

import redis

import jinja2
import json
import logging
import os

#tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, static_folder='/app/backend/backend/static')
app.url_map.strict_slashes = False
app.jinja_loader = jinja2.FileSystemLoader('/app/backend/backend/templates')


logging.basicConfig(level=logging.DEBUG)
@app.before_request
def log_request_info():
    app.logger.debug('[RECEIVED REQUEST] Headers\n%s', request.headers)
    app.logger.debug('[RECEIVED REQUEST] Body\n%s', request.get_data())
@app.after_request
def after(response):
    app.logger.debug('[SEND RESPONSE] Status\n%s', response.status)
    app.logger.debug('[SEND RESPONSE] Headers\n%s', response.headers)
    if int(response.headers['Content-Length']) < 1000:
        app.logger.debug('[SEND RESPONSE] Body\n%s', response.get_data())
    return response


assets = Environment(app)
bundles = {
    'css': Bundle(
        'lib/uikit/css/uikit.css',
        output='build/styles.css',
        filters='cssmin'
    ),
    'js': Bundle(
        'lib/uikit/js/uikit.js',
        'lib/uikit/js/uikit-icons.js',
        'lib/axios/axios.js',
        'lib/wordcloud/wordcloud.js',
        'lib/navigator/navigator.js',
        'src/utils.js',
        'src/wordcloud.js',
        'src/main.js',
        output='build/bundle.js',
    )
}
assets.register(bundles)


r=redis.Redis(host='ner_storage', port=6379, db=0, decode_responses=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/NERs/<ner_name>', methods=['GET'])
def get_NER(ner_name):
    '''Getting NER statistics'''
    adj_freq=r.hgetall('ner_stats:{}'.format(ner_name))
    if adj_freq == {}:
        return abort(404)
    response=dict()
    for term in adj_freq:
        term_sents_keys = r.lrange('sents:{}:{}'.format(ner_name, term), 0, -1)
        term_sents = []
        for sent_key in term_sents_keys:
            #TODO: fetch all sentences in one batch
            sentence = r.hget('sentences', sent_key)
            term_sents.append(sentence)

        term_dict = {
            'count': adj_freq[term],
            'sents': term_sents
        }
        response[term]=term_dict
    return jsonify(response), 200


@app.route('/api/NERs', methods=['GET'])
def get_NERs_list():
    '''Getting NERs list'''
    ners=r.lrange('ners', 0, -1)
    if ners == []:
        return abort(404)

    return jsonify(ners), 200


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
