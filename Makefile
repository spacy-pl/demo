all: env-warn install preprocess run-server

env-warn:
	@echo "Make sure to run all of the scripts in a virtual environemnt"

install:
	@echo "If some imports fail, you should probably source install-spacy before continuing"
	pip install -r requirements.txt
	pip install -e .

preprocess:
	spacy-pl-demo-preprocess

run-server:
	-export FLASK_ENV=development && export FLASK_APP=app.py && flask run --host=0.0.0.0

clean:
	rm data/*
