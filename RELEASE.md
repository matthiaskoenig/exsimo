# Release guideline
This document describes steps for releasing a new version

## checkout develop branch
```
git checkout develop
```
## bump version & requirements
- update version info in `pyexsimo/_version.py`
- check `sbmlsim` and `sbmlutils` hashes in `requirements.txt`

## run tests 
```
(exsimo) pytest
```
## execute analysis & update results
```
execute 
```
## push results and code
```
git add -u
git push
```
## make a pull request against master
Merge pull request in master. This triggers a zenodo update and the build of a new docker image with tag latest.

## make a new release
- github release from master branch (creates updated zenodo)
`exsimo-v{EXSIMO_VERSION} - EXecutable SImulation MOdels`

## check online report
[https://matthiaskoenig.github.io/exsimo/](https://matthiaskoenig.github.io/exsimo/)

## update develop branch
```
git checkout master
git pull
git checkout develop
git merge master
```
- bump version
- push changes

## upload tagged docker-container
Either build the container locally
```
docker build -t matthiaskoenig/exsimo:${EXSIMO_VERSION} .
```
or better use the auto build container (takes some time)
```
docker pull matthiaskoenig/exsimo:latest
docker tag matthiaskoenig/exsimo:latest matthiaskoenig/exsimo:${EXSIMO_VERSION} 
```
docker login
docker push matthiaskoenig/exsimo:${EXSIMO_VERSION}
```