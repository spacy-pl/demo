from typing import List, NamedTuple
import pickle

import spacy
from spacy.lang.pl import Polish
import requests


DOC_TEXT_PATH = 'data/pan-tadeusz.txt'
DOC_PICKLE_PATH = 'data/pan-tadeusz.pkl'

nlp = spacy.load('xx')  # TODO: Use nlp = Polish() when our lemmatizer is implemented


class SearchProcessor(object):
    def __init__(self, processed_doc_path: str=DOC_PICKLE_PATH):
        with open(processed_doc_path, 'r') as file:
            self.doc = pickle.load(file)

    def process_query(self, query: str):
        finder = Finder(self.doc, query)
        return finder.find_results


class FindResult(NamedTuple):
    token_text: str
    lemma_match: bool=False
    direct_match: bool=False


class Finder(object):
    def __init__(self, processed_doc: spacy.tokens.doc.Doc, query: str):
        self.doc = processed_doc
        processed_query = nlp(query)
        self.query_words = {token.text for token in processed_query if token.is_alpha}
        self.query_lemmas = {token.lemma_ for token in processed_query if token.is_alpha}

    @property
    def find_results(self) -> List[FindResult]:
        return [self._check_token(token) for token in self.doc if token.is_alpha or token.is_stop]

    def _check_token(self, token: spacy.tokens.token.Token) -> FindResult:
        if not token.is_alpha:
            return FindResult(token.text_with_ws)
        else:
            lemma_match = token.lemma_ in self.query_lemmas
            direct_match = token.text in self.query_words
            return FindResult(token.text_with_ws, lemma_match, direct_match)


def preprocess(doc_text_path: str=DOC_TEXT_PATH, doc_pickle_path: str=DOC_PICKLE_PATH):
    with open(doc_text_path, 'r') as text_file:
        processed_doc = nlp(text_file.read())
    with open(doc_pickle_path, 'wb') as pickle_file:
        pickle.dump(processed_doc, pickle_file)
