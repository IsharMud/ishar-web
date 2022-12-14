#!/bin/bash
pylint --min-public-methods=1 --disable=C0103,E0401,W0703 $(git ls-files *.py)
echo "pylint: $?"
flake8 $(git ls-files *.py)
echo "flake8: $?"
