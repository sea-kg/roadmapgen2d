#!/bin/bash

# Tutorial: https://packaging.python.org/tutorials/packaging-projects/


# clean
rm -rf dist
rm -rf roadmapgen2d.egg-info

python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
