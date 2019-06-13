# spacy-pl-demo
Demonstration of Polish language support in spaCy, see it live on: http://spacypl.sigmoidal.io

## How it works
Demo contains a flask application which displays status of development process for each of the modules,
rendered jupyter notebooks with instructions and examples of how to use the latest Polish language version,
as well as an interactive demonstration - a simple application that allows you to select a famous person 
and visualize adjectives used to describe that person in a set of polish newspaper articles.

Aside from the flask application, we use rabbitmq to store processed documents, preprocessing container that
scrapes articles and performs all heavy data processing and an nginx server as a gateway.

## Interactive demonstration
SpaCy is a library that puts a high focus on efficiency - we wanted to demonstrate how it allowed us to build
the core demo application functionality within a few hours. To analyze the scraped articles and match
famous people names with adjectives relating to them, the following steps need to be taken:

1. Tokenization - parsing the text to separate it into tokens: words, punctuation, etc that we can use
later to separate sentences or vectorize tokens to use machine learning
2. Named Entity Recognition - spaCy uses deep learning models to classify spans of text (one or more tokens) into
various classes of named entities - we use that to select just the people mentioned in the text
3. Dependency Parsing - this also is a neural network, this time trained to build 
a tree of relationships between tokens in a sentence. Having already marked famous people in the previous step,
we can filter words that are connected to them in the sentence tree.
4. Part-of-Speech Tagging - now that we have a words connected to famous people, we just want to keep the adjectives,
and this is where POS Tagging comes along - this is also a neural network classifier, just like steps 2 and 3
5. Lemmatization - adjectives we currently have come in various forms - we need to unify their form, otherwise
each of the forms of an adjective would be counted as a separate adjective.

Our implementation of all these steps inside a single library is, at the moment of writing this, 
the only one that exisits for Polish language. This is extremely important, as it allows companies
using spaCy for other languages easily extend their work to Polish. For newcomers, spaCy also offers benefits,
such as the clear and easy interface: all steps mentioned above are computed automatically within 2-3 lines of code :)

## Deployment
Application exposes ports through a secure nginx server in a container. All you need is:
```
docker-compose build
docker-compose up
```
