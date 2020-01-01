# Release guideline
This document describes what steps are taken before a new
model version is released.

## bump version
- update version info in `_version.py`

## run tests locally in develop branch 
```
git checkout develop
(exsimo) pytests
```
## execute analysis (updates results)
```
execute 
```
## execute analysis in docker
- build docker container
Build image from `Dockerfile`
```
$EXSIMO_VERSION
docker build -t matthiaskoenig/exsimo:${EXSIMO_VERSION} .
```
- run tests in docker container
```bash
docker container exec <container name/ID> pytest
```
- execute analysis in docker container
```bash
docker container exec <container name/ID> pytest
```

## push results and code
```
git add -u
git push
```
## make a pull request against master
- merge branch in master (after checks passed)

## make a new release
- github release from master branch (creates updated zenodo)
- update zenodo links

## update container
- push container to dockerhub (with new version tag)

The images can be pushed to the hub via
```
docker push matthiaskoenig/dmod:latest
```

## update develop branch
```
git checkout master
git pull
git checkout develop
git merge master
```
- bump version
- push changes
