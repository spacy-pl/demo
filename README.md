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
Make sure you have aws cli installed and configured for reading the remote server specified in `spacy_pl_utils/.dvc/config` 
as well as python 3.7 or newer (dev setup and deployment were tested on conda python 3.7.1 distribution).

## Dev setup
Execute these to install dependencies, preprocess data and run a 
Flask development server on `localhost:5000`:
```bash
git submodule init  # only for the 1st time
git submodule update --recursive  # only for the 1st time
conda create -n spacy-demo  # only for the 1st time
source activate spacy-demo
make develop  # setup & start server, this can take a few minutes
```
Server is set up to autoreload whenever app or its dependencies change.
Develop is a long process that can be divided into smaller automated steps if necessary 
- see `Makefile` for more details.

### Docker (WIP)
The Docker container can be built using docker compose.
This works, but is not yet as efficient as I would like it to be.

1. In order for dvc to work, place your google cloud json key in `dev/`, its protected from adding to git via `.gitignore`
2. `docker-compose build` installs as much as possible, this is only done once
3. `docker-compose up` currently not only runs the app, but also some preprocessing
which in the future will likely be moved to build (but is now impossible due to demo's directory structure)

Docker volume is mounted so that demo package and app itself auto-reloads on any change in source files.
Note that changes to spacy or utils directories will **NOT** result in a reload.

## Deployment
In addition to prerequisites described earlier, this requires 
a machine with nginx installed and running as a service.

Also, make sure that nginx is configured to restart automatically in case of system failure.
The easiest way to do this is to modify `/lib/systemd/system/nginx.service`, adding the following line below the `[Service]` tag:
```
Restart=always
```

To perform full deployment, execute this on a server after cloning the repo:
```
git submodule init  # only for the 1st time
git submodule update --recursive  # only for the 1st time
conda create -n spacy-demo python=3.7.2 pip=18.1  # only for the 1st time
source activate spacy-demo
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
