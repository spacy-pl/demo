import click

from spacy_pl_demo import lemmatizer, vectors


@click.command("Generates necessary files for the web app demo to run.")
def preprocess():
    print("Preprocessing data...")
    lemmatizer.preprocess()
    vectors.preprocess()
    print("Preprocessing complete.")
