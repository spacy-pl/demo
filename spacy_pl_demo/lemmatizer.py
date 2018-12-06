from typing import List, NamedTuple
import pickle

from tqdm import tqdm
import spacy
from spacy.lang.pl import Polish
from spacy.lang.pl.tagger import PolishTagger  # hotfix for getting lemmatizer to work


DOC_TEXT_PATH = 'data/pan-tadeusz.txt'
DOC_PICKLE_PATH = 'data/pan-tadeusz.pkl'

MAX_RETURNED_TOKENS = 5000


nlp = Polish()
tagger = PolishTagger(nlp.vocab)  # hotfix for getting lemmatizer to work
nlp.add_pipe(tagger, first=True, name='polish_tagger')


class SearchProcessor(object):
    def __init__(
            self, 
            processed_doc_path: str=DOC_PICKLE_PATH,
            max_returned_tokens: int=MAX_RETURNED_TOKENS
        ):
        with open(processed_doc_path, 'rb') as file:
            self.doc = pickle.load(file)
        self.max_returned_tokens = max_returned_tokens

    def process_query(self, query: str):
        finder = Finder(self.doc, query)
        return finder.find_results[:self.max_returned_tokens]


class DemoToken(NamedTuple):
    """ Compatible with spacy's token without lazy evaluation. """
    text: str
    lemma_: str
    text_with_ws: str


class DemoDoc(NamedTuple):
    """ 
    This removes unnecessary overhead from spacy's doc as well as 
    forces all tokens to be computed during preprocessing.
    """
    tokens: List[DemoToken]
    
    def __iter__(self):
        for token in self.tokens:
            yield token


class FindResult(NamedTuple):
    token_text: str
    lemma_match: bool=False
    direct_match: bool=False


class Finder(object):
    def __init__(self, processed_doc: DemoDoc, query: str):
        self.doc = processed_doc
        processed_query = nlp(query)
        self.query_words = {token.text for token in processed_query if token.is_alpha}
        self.query_lemmas = {token.lemma_ for token in processed_query if token.is_alpha}

    @property
    def find_results(self) -> List[FindResult]:
        return [self._check_token(token) for token in tqdm(self.doc) if token.is_alpha or token.is_stop]

    def _check_token(self, token: DemoToken) -> FindResult:
        if not token.is_alpha:
            return FindResult(token.text_with_ws)
        else:
            lemma_match = token.lemma_ in self.query_lemmas
            direct_match = token.text in self.query_words
            return FindResult(token.text_with_ws, lemma_match, direct_match)


def preprocess(doc_text_path: str=DOC_TEXT_PATH, doc_pickle_path: str=DOC_PICKLE_PATH):
    print(f"Reading {doc_text_path}, this may take a while...")
    with open(doc_text_path, 'r') as text_file:
        processed_doc = nlp(text_file.read())
    with open(doc_pickle_path, 'wb') as pickle_file:
        pickle.dump(processed_doc, pickle_file)
