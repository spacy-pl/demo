FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development
ENV FLASK_APP app.py

WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt
#copying static files and utilities scripts
ADD dev /app/dev
ADD static /app/backend/backend/static
RUN python dev/download_static.py

RUN jupyter nbconvert --to html --template basic nbconvert dev/notebooks/*.ipynb
#
ADD templates /app/backend/backend/templates
RUN mv dev/notebooks/*.html /app/backend/backend/templates/
RUN python dev/replace_lines.py

ADD uwsgi.ini /app/
ADD backend /app/backend

RUN pip install /app/backend
