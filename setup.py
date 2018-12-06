from setuptools import setup, find_packages

setup(
    name='spacy_pl_demo',
    version='0.1',
    packages=find_packages(include=['spacy_pl_demo']),
    entry_points={
        'console_scripts': [
            'spacy-pl-demo-preprocess = spacy_pl_demo.preprocess:preprocess'
        ]
    }
)
