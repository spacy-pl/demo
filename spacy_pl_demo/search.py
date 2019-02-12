from typing import List
from dataclasses import dataclass, asdict
import json

import click
from spacy.lang.pl import Polish, PolishTagger  # hotfix for getting lemmatizer to work

DOC_RAW_PATH = 'data/pan-tadeusz.txt'
DOC_PROCESSED_PATH = 'data/pan-tadeusz.json'

MAX_RETURNED_TOKENS = 5000

nlp = Polish()
tagger = PolishTagger(nlp.vocab)  # hotfix for getting lemmatizer to work
nlp.add_pipe(tagger, first=True, name='polish_tagger')


class SearchProcessor(object):
    def __init__(
            self,
            processed_doc_path: str = DOC_PROCESSED_PATH,
            max_returned_tokens: int = MAX_RETURNED_TOKENS
    ):
        with open(processed_doc_path, 'r') as file:
            doc_as_dicts = json.load(file)
        self.doc = [DemoToken(**token_dict) for token_dict in doc_as_dicts]
        self.max_returned_tokens = max_returned_tokens

    def process_query(self, query: str) -> List[dict]:
        finder = Finder(self.doc, query)
        results = finder.find_results[:self.max_returned_tokens]
        return list(map(asdict, results))


@dataclass
class DemoToken(object):
    """ Compatible with spacy's token, but without lazy evaluation. """
    text: str
    lemma_: str
    text_with_ws: str
    is_alpha: str
    is_stop: str

    @classmethod
    def from_spacy(cls, spacy_token):
        return cls(
            spacy_token.text,
            spacy_token.lemma_,
            spacy_token.text_with_ws,
            spacy_token.is_alpha,
            spacy_token.is_stop
        )


@dataclass
class SearchResult(object):
    token_text: str
    lemma_match: bool = False
    direct_match: bool = False


class Finder(object):
    def __init__(self, processed_doc: List[DemoToken], query: str):
        self.doc = processed_doc
        processed_query = nlp(query)
        self.query_words = {token.text for token in processed_query if token.is_alpha}
        self.query_lemmas = {token.lemma_ for token in processed_query if token.is_alpha}

    @property
    def find_results(self) -> List[SearchResult]:
        return [self._check_token(token) for token in self.doc]

    def _check_token(self, token: DemoToken) -> SearchResult:
        if not token.is_alpha:
            return SearchResult(token.text_with_ws)
        else:
            lemma_match = token.lemma_ in self.query_lemmas
            direct_match = token.text in self.query_words
            return SearchResult(token.text_with_ws, lemma_match, direct_match)


@click.command("Processes provided document, saving it as an array of tokens with preserved lemma information.")
def preprocess(doc_text_path: str = DOC_RAW_PATH, doc_json_path: str = DOC_PROCESSED_PATH):
    print(f"Reading {doc_text_path}, this may take a while...")
    with open(doc_text_path, 'r') as text_file:
        doc = nlp(text_file.read())
    processed_doc = [asdict(DemoToken.from_spacy(token)) for token in doc]
    with open(doc_json_path, 'w') as json_file:
        json.dump(processed_doc, json_file)
