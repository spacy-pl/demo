# spacy-pl-demo
Demonstration of polish language support in spaCy.

## How it works
Flask application defined in `app.py` assembles `templates` and bundles `static` files 
into a single-page application. Navigation and demo functionalities are handled 
by `static/src/main.js` on the front end, and the `app.py` with 
a help of the `spacy_pl_demo` python package on the backend.

Application requires specific version of spacy (located in the `spacy_install` directory) as well as `spacy_pl_utils` demo branch, both of which are included as git submodules. It also requires some preprocessing of 
the included data, most of which is automated in the `Makefile`.

## Prerequisites
Make sure you have access to pull `kowaalczyk/spacy_pl` and `Gizzio/spacy_pl_utils`, 
aws cli installed and configured for reading `s3://spacy.pl` 
as well as python 3.7 or newer 
(dev setup and deployment were tested on conda python 3.7.1 distribution).

## Dev setup
Execute these to install dependencies, preprocess data and run a 
Flask development server on `localhost:5000`:
```bash
conda create -n spacy-demo  # only for the 1st time
source activate spacy-demo
source install-spacy
make develop # setup & start server, this can take a few minutes
```
Server is set up to autoreload whenever app or its dependencies change.

## Deployment
In addition to prerequisites described earlier, this requires 
a machine with nginx installed and running as a service.

To perform full deployment:
```
conda create -n spacy-demo  # only for the 1st time
source activate spacy-demo
make install
make preprocess
make deploy
```
Expect to be prompted for password muliple times - 
sudo is required to access nginx and service config files.

Deployment steps based on:
- https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04
- https://peteris.rocks/blog/deploy-flask-apps-using-anaconda-on-ubuntu-server/
- https://stackoverflow.com/questions/17413526/nginx-missing-sites-available-directory
- https://stackoverflow.com/a/40041214

## Common problems

##### `ValueError: 143478 exceeds max_map_len(32768)`
Due to `msgpack` update, `spacy.load` breaks when trying to read our custom vocab. In order to fix this, install older version of `msgpack` and re-start the server:
```
# in a virtual env:
python -m pip install "msgpack==0.5.6"
make run-server
```
Suggested by: https://github.com/explosion/spaCy/issues/3053
