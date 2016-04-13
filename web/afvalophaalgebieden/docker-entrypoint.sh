#!/usr/bin/env bash

set -u
set -e

cd /app

# run uwsgi
exec uwsgi --ini /app/uwsgi.ini
