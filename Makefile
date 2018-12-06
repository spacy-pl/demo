all: env-warn download-data install preprocess run-server

env-warn:
	@echo "Make sure to run all of the scripts in a virtual environemnt"

download-data:
	-mkdir data
# 	cd data && wget https://wolnelektury.pl/media/book/txt/pan-tadeusz.txt

install:
	pip install -r requirements.txt  # hotfix: add `from .tagger import PolishTagger` to lang.pl.__init__
	pip install -e .

preprocess:
	spacy-pl-demo-preprocess

run-server:
	-export FLASK_ENV=development && export FLASK_APP=app.py && flask run --host=0.0.0.0

clean:
	rm data/*
