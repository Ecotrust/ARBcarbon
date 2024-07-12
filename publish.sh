#! /bin/bash

set -e
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $ROOT_DIR

PY_REG=https://us-python.pkg.dev/new-forests/nf-carbon/

rm -rf dist
python3 setup.py sdist

# Setup authentication first
# https://cloud.google.com/artifact-registry/docs/python/authentication

# make sure you have logged in with the default credentials... whatever that means
# gcloud auth application-default login 
python3 -m twine upload \
   --verbose \
  --repository-url $PY_REG \
  dist/*