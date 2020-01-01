<h1><img alt="EXSIMO logo" src="./docs/images/exsimo_logo_200.png" height="100" /> EXSIMO: EXecutable SImulation MOdel</h1>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3596068.svg)](https://doi.org/10.5281/zenodo.3596068)
[![Build Status](https://travis-ci.org/matthiaskoenig/exsimo.svg?branch=develop)](https://travis-ci.org/matthiaskoenig/exsimo)
[![GitHub version](https://badge.fury.io/gh/matthiaskoenig%2Fexsimo.svg)](https://badge.fury.io/gh/matthiaskoenig%2Fexsimo)
[![codecov](https://codecov.io/gh/matthiaskoenig/exsimo/branch/develop/graph/badge.svg)](https://codecov.io/gh/matthiaskoenig/exsimo)

<b><a href="https://orcid.org/0000-0003-1725-179X" title="https://orcid.org/0000-0003-1725-179X"><img src="./docs/images/orcid.png" height="15"/></a> Matthias König</b>

Data, model and code for executable simulation model of hepatic glucose metabolism.

* `data` - data sets
* `docs` - documentation, results, report, models
* `docs/models` - SBML model and model report
* `pyexsimo` - python package (model generation, simulation experiments, tests, ...)

Results of the executed model are available from https://matthiaskoenig.github.io/exsimo/ 
Docker images at https://hub.docker.com/repository/docker/matthiaskoenig/exsimo


## Run locally
To run the analysis locally create a python virtual environment and install `pyexsimo` 

### virtualenv
Create virtual environment with `python3.6`, e.g., with `virtualenv` & `virtualenvwrapper` via
```
mkvirtualenv exsimo --python=python3.6
```

### install latest version
```
git clone https://github.com/matthiaskoenig/exsimo.git
cd exsimo
(exsimo) pip install -r requirements.txt
(exsimo) pip install -e . --upgrade
```
## Tests
All tests can be run via
```
(exsimo) pytest
```
## Run analysis
The complete analysis can be run via
```
(exsimo) execute
```
which updates the results in the `./docs/` folder.

## Run in docker container
For the releases on the master branch docker containers are provided.
These allow to run the tests or execute the workflow via

TODO: link volume
- run tests in docker container
```bash
docker run -it matthiaskoenig/exsimo:0.3.0a2

docker container exec <container name/ID> pytest
```
- execute analysis in docker container
```bash
docker container exec <container name/ID> execute

----
&copy; 2019 Matthias König.