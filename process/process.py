# coding: utf-8
import json
import spacy
from nltk.probability import FreqDist
import redis
from tqdm import tqdm

MINIMAL_TERMS_NUMBER = 5
MODEL_PATH = 'pl_model'
CHOOSEN_POS = 'ADJ'
LABELS = ['PERSON']
r = redis.Redis(host='ner_storage', port=6379, db=0, decode_responses=True)

def generate_terms_dict(docs):
    all_entities = set()
    terms = dict()
    termcount=0
    for doc in docs:
        ents = doc.ents
        for ent in ents:
            if ent.label_ in LABELS:
                normalized_ent = ent.lemma_
                if normalized_ent not in all_entities:
                    all_entities.add(normalized_ent)
                    terms[normalized_ent]=[]

                sentence = ent.sent
                for token in sentence:
                    if token.pos_ == CHOOSEN_POS:
                        termcount += 1
                        terms[normalized_ent].append(token.lemma_)        
                        r.lpush('sents:{}:{}'.format(ent.lemma_, token.lemma_), sentence.text)

    print("Extracted " + str(termcount) + " terms.")
    final_terms=dict()
    for ent, terms_list in terms.items():
        if len(set(terms_list))>=MINIMAL_TERMS_NUMBER:
            final_terms[ent] = terms[ent]
            print("Adding entity:",ent)
        else:
            all_entities.remove(ent)
            print("Passing entity:", ent, ", not enough terms ({})".format(len(set(terms[ent]))))
    return all_entities, final_terms

arts = json.load(open('articles.json'))

if r.lrange('ners', 0, -1) == []:
    print("Processing data...")
    nlp = spacy.load(MODEL_PATH)

    docs = [nlp(art) for art in tqdm(arts) if len(art) != 0]
    ents, terms = generate_terms_dict(docs)

    stats = dict()

    for ent in terms:
        stats[ent] = FreqDist(terms[ent]).most_common()
    
    ents = sorted(ents, key=lambda ent: len(stats[ent]))

    for ner in tqdm(ents):
        r.lpush('ners', ner)
        for word, count in stats[ner]:
            r.hset('ner_stats:{}'.format(ner), word, count)
    print("Data processed!")
else:
    print("Data already in cache")

