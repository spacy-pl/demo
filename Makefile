develop: env-warn install preprocess run-server

env-warn:
	@echo "Make sure to run all of the scripts in a virtual environemnt"

install:
	@echo "If some imports fail, you should probably source install-spacy before continuing"
	pip install -r requirements.txt
	pip install -r spacy_pl_utils/requirements.txt
	pip install -e .

preprocess:
	cd spacy_pl_utils && dvc pull && dvc repro vectors_300.txt.dvc
	spacy-pl-preprocess-search
	spacy-pl-preprocess-similarity


run-server:
	-export FLASK_ENV=development && export FLASK_APP=app.py && flask run --host=0.0.0.0

deploy: deploy-install deploy-setup deploy-enable-demo deploy-enable-nginx

deploy-install: env-warn
	sudo apt update
	sudo apt install build-essential libssl-dev libffi-dev
	conda install -c conda-forge uwsgi
	pip install ./spacy_install  # TODO: might need `pip install .` as well
	python -m pip install "msgpack==0.5.6"  # TODO: Rebase spacy, remove this hotfix

deploy-setup:
	-sudo systemctl disable spacy-pl-demo && sudo systemctl stop spacy-pl-demo
	sudo cp deployment/spacy-pl-demo.service /etc/systemd/system/
	-sudo mkdir /etc/nginx/sites-available
	-sudo mkdir /etc/nginx/sites-enabled
	sudo cp deployment/spacy-pl-demo /etc/nginx/sites-available/

deploy-enable-demo:
	sudo systemctl daemon-reload
	sudo systemctl start spacy-pl-demo
	sudo systemctl enable spacy-pl-demo
	@echo "to check for errors:"
	@echo "sudo systemctl status spacy-pl-demo"
	@echo "to disable demo:"
	@echo "sudo systemctl disable spacy-pl-demo && sudo systemctl stop spacy-pl-demo"

deploy-enable-nginx:
	-sudo rm /etc/nginx/sites-enabled/spacy-pl-demo
	sudo ln -s /etc/nginx/sites-available/spacy-pl-demo /etc/nginx/sites-enabled/spacy-pl-demo
	sudo service nginx restart
	@echo "to disable nginx usage of demo:"
	@echo "sudo rm /etc/nginx/sites-enabled/spacy-pl-demo && sudo service nginx restart"
	@echo "to disable nginx:"
	@echo "sudo service nginx stop"

clean:
	rm data/*
