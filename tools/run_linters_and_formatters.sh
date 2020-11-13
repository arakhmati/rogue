#!/usr/bin/env bash

set -e

# Formatters
black --check .

# Type Checkers
mypy --config-file mypy.ini "rogue"

# Linters
MYPYPATH=/dev/null flake8 --config .flake8 --mypy-config mypy.ini "rogue"
pylint --rcfile .pylintrc "rogue"
