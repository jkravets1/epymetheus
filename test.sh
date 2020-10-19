#!/bin/sh

python3 -m pytest --doctest-modules epymetheus
python3 -m pytest --doctest-modules tests

python3 -m flake8 epymetheus
python3 -m black --check epymetheus || read -p "Run formatter? (y/N): " yn; [[ $yn = [yY] ]] && python3 -m black epymetheus
python3 -m isort --check --force-single-line-imports epymetheus || read -p "Run formatter? (y/N): " yn; [[ $yn = [yY] ]] && python3 -m isort --force-single-line-imports epymetheus
