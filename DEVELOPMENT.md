## 

## Pylint

```
$ python3 -m pylint --rcfile=.pylintrc roadmapgen2d/*.py
$ python3 -m pylint --rcfile=.pylintrc tests/*.py
```

## Tests

```
$ cd tests
$ python3 -m pytest -rAs .
```

or just all tests and pylint

```
./ci/travis/run.sh
```

## Install/Uninstall from localdev dir

```
$ python3 setup.py sdist bdist_wheel
$ python3 -m pip install .
```

```
$ pip3 uninstall roadmapgen2d
```

Run
```
$ python3 -m roadmapgen2d .
```