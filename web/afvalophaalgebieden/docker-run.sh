#!/usr/bin/env bash
set -u
set -e

python check_db.py || echo "Could not migrate, ignoring"

exec uwsgi --ini /app/uwsgi.ini
