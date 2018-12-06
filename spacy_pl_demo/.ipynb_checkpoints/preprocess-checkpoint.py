import click
import requests

from spacy_pl_demo import lemmatizer


@click.command("Generates necessary files for the web app demo to run.")
def preprocess():
    print("Preprocessing data...")
    lemmatizer.preprocess()
    print("Preprocessing complete.")
