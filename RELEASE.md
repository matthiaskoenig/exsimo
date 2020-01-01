# Release guideline
This document describes steps for releasing a new version

## bump version
Update version info in `_version.py` and set environment variable
```bash
EXSIMO_VERSION=0.3.0a2
```
## run tests 
```
git checkout develop
(exsimo) pytests
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
Merge branch in master (after checks passed).
This triggers a zenodo update and the build of the docker image.

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
