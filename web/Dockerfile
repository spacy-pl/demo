FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development
ENV FLASK_APP app.py

WORKDIR /code

ADD requirements.txt /code
RUN pip install -r requirements.txt

ADD dev /code/dev
ADD static /code/static
RUN python dev/download_static.py
RUN jupyter nbconvert --to html --template basic nbconvert dev/notebooks/*.ipynb

ADD templates /code/templates
RUN mv dev/notebooks/*.html templates/
RUN python dev/replace_lines.py

ADD app.py /code/app.py
