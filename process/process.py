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
    entities_terms_sentence_lists = dict()
    termcount = 0
    for i, doc in enumerate(docs):
        if i % (len(docs)//100) == 0:
            print(i/len(docs)*100, "% processed.")
        ents = doc.ents
        print("Entities in doc:", len(ents))

        for ent in ents:
            if ent.label_ in LABELS:
                entity_orth = ent.orth_
                if entity_orth not in all_entities:
                    all_entities.add(entity_orth)
                    terms[entity_orth]=[]

                sentence = ent.sent
                sentence_key = hash(sentence.orth_)
                for token in sentence:
                    if token.pos_ == CHOOSEN_POS and not token.is_stop:
                        termcount += 1
                        lemmatized_term = token.lemma_
                        terms[entity_orth].append(token.lemma_)
                        l = entities_terms_sentence_lists.get((entity_orth, lemmatized_term))
                        if l:
                            entities_terms_sentence_lists[(entity_orth, lemmatized_term)].append(sentence_key)
                        else:
                            entities_terms_sentence_lists[(entity_orth, lemmatized_term)]=[sentence_key]

    print("Extracted " + str(termcount) + " terms.")
    final_terms=dict()
    for ent, terms_list in terms.items():
        if len(set(terms_list))>=MINIMAL_TERMS_NUMBER:
            final_terms[ent] = terms[ent]
            print("Adding entity:",ent)
        else:
            all_entities.remove(ent)
            print("Passing entity:", ent, ", not enough terms ({})".format(len(set(terms[ent]))))
    return all_entities, final_terms, entities_terms_sentence_lists

def push_sentence_dict(docs):
    pipe = r.pipeline()
    for doc in docs:
        for sentence in doc.sents:
            sent_value = sentence.orth_
            sent_key = hash(sent_value)
            pipe.hset('sentences', sent_key, sent_value)
    pipe.execute()
            

arts = json.load(open('articles.json'))

if r.lrange('ners', 0, -1) == []:
    print("Preprocessing text data...")
    nlp = spacy.load(MODEL_PATH)
    docs = [nlp(art) for art in tqdm(arts) if len(art) != 0]
    print("Processing docs...")

    ents, terms, entities_terms_sentence_lists = generate_terms_dict(docs)

    stats = dict()

    for ent in terms:
        stats[ent] = FreqDist(terms[ent]).most_common()

    ents = sorted(ents, key=lambda ent: len(stats[ent]))
    print("Storing entities and term counts in Redis...")
    pipe = r.pipeline()
    for ner in tqdm(ents):
        pipe.lpush('ners', ner)
        for word, count in stats[ner]:
            pipe.hset('ner_stats:{}'.format(ner), word, count)
    pipe.execute()

    print("Storing references to sentences in Redis...")
    pipe = r.pipeline()
    for key, value in tqdm(entities_terms_sentence_lists.items()):
        pipe.lpush('sents:{}:{}'.format(key[0], key[1]), *value)
    pipe.execute()

    print("Storing sentence dict in Redis...")
    push_sentence_dict(docs)

    print("Data processed!")
else:
    print("Data already in cache")

