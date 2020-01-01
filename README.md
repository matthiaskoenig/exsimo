<h1><img alt="EXSIMO logo" src="./docs/images/exsimo_logo_200.png" height="100" /> EXSIMO: EXecutable SImulation MOdel</h1>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3596068.svg)](https://doi.org/10.5281/zenodo.3596068)
[![Build Status](https://travis-ci.org/matthiaskoenig/exsimo.svg?branch=develop)](https://travis-ci.org/matthiaskoenig/exsimo)
[![GitHub version](https://badge.fury.io/gh/matthiaskoenig%2Fexsimo.svg)](https://badge.fury.io/gh/matthiaskoenig%2Fexsimo)
[![codecov](https://codecov.io/gh/matthiaskoenig/exsimo/branch/develop/graph/badge.svg)](https://codecov.io/gh/matthiaskoenig/exsimo)
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/matthiaskoenig/exsimo)
![Docker Pulls](https://img.shields.io/docker/pulls/matthiaskoenig/exsimo)

<b><a href="https://orcid.org/0000-0003-1725-179X" title="https://orcid.org/0000-0003-1725-179X"><img src="./docs/images/orcid.png" height="15"/></a> Matthias König</b>

Data, model and code for executable simulation model of hepatic glucose metabolism.

* `data` - data sets
* `docs` - documentation, results, report, models
* `docs/models` - SBML model and model report
* `pyexsimo` - python package (model generation, simulation experiments, tests, ...)

Results of the executed model are available from https://matthiaskoenig.github.io/exsimo/ 

Docker images available from https://hub.docker.com/repository/docker/matthiaskoenig/exsimo

## Setup local environment
To run the analysis locally create a python virtual environment and install `pyexsimo`. 

Create virtual environment with `python3.6`, e.g., with `virtualenv` & `virtualenvwrapper` via
```
mkvirtualenv exsimo --python=python3.6
```
Install the dependencies in the virtualenv
```
git clone https://github.com/matthiaskoenig/exsimo.git
cd exsimo
(exsimo) pip install -r requirements.txt
(exsimo) pip install -e . --upgrade
```
To run the tests use `pytest`, to execute the analysis use `execute`.

## Setup docker container
For the master branch docker containers are built automatically. To start the respective execution environment use

```bash
docker run -it matthiaskoenig/exsimo:latest
```
To run a specific model version use the respective tag
```bash
docker run -it matthiaskoenig/exsimo:0.3.0
```
To run the tests use `pytest`, to execute the analysis use `execute`.

## Run tests
All tests can be run via
```
pytest
```

## Run analysis
The complete analysis can be run via
```
(exsimo) execute
```
which updates the results in the `./docs/` folder.

----
&copy; 2019 Matthias König.