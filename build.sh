#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

pip3 install db-sqlite3

python3 manage.py collectstatic --no-input
python3 manage.py migrate