FROM python:3.5
ARG MODEL_URL="https://storage.googleapis.com/spacy-pl-public-models/pl_model-0.2.0.tar.gz"

ENV PYTHONUNBUFFERED 1
WORKDIR /code

ADD requirements.txt /code
RUN pip install -r requirements.txt
RUN wget ${MODEL_URL}
RUN pip install *model*

ADD . /code/
