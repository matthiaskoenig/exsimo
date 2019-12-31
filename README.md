

<h1><img alt="EXSIMO logo" src="./docs/images/exsimo_logo_200.png" height="100" /> EXSIMO: EXecutable SImulation MOdel</h1>

[![Build Status](https://travis-ci.org/matthiaskoenig/exsimo.svg?branch=develop)](https://travis-ci.org/matthiaskoenig/exsimo)
[![GitHub version](https://badge.fury.io/gh/matthiaskoenig%2Fexsimo.svg)](https://badge.fury.io/gh/matthiaskoenig%2Fexsimo)
[![DOI](https://zenodo.org/badge/230637955.svg)](https://zenodo.org/badge/latestdoi/230637955)
[![codecov](https://codecov.io/gh/matthiaskoenig/exsimo/branch/develop/graph/badge.svg)](https://codecov.io/gh/matthiaskoenig/exsimo)

<b><a href="https://orcid.org/0000-0003-1725-179X" title="https://orcid.org/0000-0003-1725-179X"><img src="./docs/images/orcid.png" height="15"/></a> Matthias König</b>

Data, model and code for executable simulation model of hepatic glucose metabolism.

* `data` - data sets
* `docs` - documentation
* `models` - SBML model and model report
* `pyexsimo` - python package (model generation, simulation experiments, tests, ...)
* `results` - results of simulation experiments 


## Installation

### virtualenv
Create virtual environment with `python3.6`, e.g., with `virtualenv` & `virtualenvwrapper` via
```
mkvirtualenv exsimo --python=python3.6
```

### dependencies
Install latest `sbmlutils` and `sbmlsim`
```bash
git clone https://github.com/matthiaskoenig/sbmlutils.git
cd sbmlutils
(exsimo) pip install -e . --upgrade

# install latest sbmlsim
git clone https://github.com/matthiaskoenig/sbmlsim.git
cd sbmlsim
(exsimo) pip install -e . --upgrade

# install latest pyexsimo
git clone https://github.com/matthiaskoenig/exsimo.git
cd exsimo
(exsimo) pip install -e . --upgrade
```
## Testing
Tests can be run via
```
cd exsimo
(exsimo) pytest
```
## Run analysis
The complete analysis, i.e.,
- generation of SBML models
- execution of simulation experiments
- creating all figures
can be run via
```
cd exsimo
(exsimo) execute
```

----
&copy; 2019 Matthias König.