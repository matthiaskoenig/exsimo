# exesimo
Python package for executable simulation model of the liver.

* `data` - data sets
* `docs` - documentation
* `models` - latest model versions
* `notebooks` - Jupyter notebooks
* `pyexesimo` - python package for executable simulation models 

## Installation

### virtualenv
Create virtual environment with `virtualenv` & `virtualenvwrapper`.
```
mkvirtualenv exsimo --python=python3.6
```
If this is not working use
```
which python3.6
```
to find the path to python and use it in the command above.

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

----
&copy; 2019 Matthias König.