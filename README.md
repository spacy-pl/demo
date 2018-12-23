# spacy-pl-demo
Demonstration of polish language support in spaCy.

## How it works
Flask application defined in `app.py` assembles `templates` and bundles `static` files 
into a single-page application. Navigation and demo functionalities are handled 
by `static/src/main.js` on the front end, and the `app.py` with 
a help of the `spacy_pl_demo` python package on the backend.

Application requires specific version of spacy that is included 
in the `spacy_install` submodule. It also requires some preprocessing of 
the included data, which is automated in the `Makefile`.

## Dev setup
Execute these to install dependencies, preprocess data and run a 
Flask development server on `localhost:5000`:
```bash
conda create -n spacy-demo  # only for the 1st time
source activate spacy-demo
source install-spacy  # has to be done manually every time demo branch changes
make  # setup & start server, this can take a few minutes
```

## Deployment
TODO
