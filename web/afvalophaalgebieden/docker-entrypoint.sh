#!/usr/bin/env bash

set -u
set -e

cd /app

PYTHON=$(which python3 || which python)

echo checking tables
${PYTHON} check_db.py

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini
