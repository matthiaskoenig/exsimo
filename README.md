# `exsimo` - Executable simulation model of the liver
Data, model and code for model of hepatic glucose metabolism.

* `data` - data sets
* `docs` - documentation
* `models` - SBML model and model report
* `pyexsimo` - python package 

## Installation

### virtualenv
Create virtual environment with `python3.6`, e.g., with `virtualenv` & `virtualenvwrapper` via
```
mkvirtualenv exsimo --python=python3.6
```

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

To work with notebooks
```bash
(exsimo) pip install jupyterlab
(exsimo) python -m ipykernel install --user --name=exismo
```
----
&copy; 2019 Matthias König.