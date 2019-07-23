#!/usr/bin/env bash
set -u
set -e

# download files
python download_files_from_dcatd.py qji2W_HBpWUWyg /data  || echo "Could not retrieve the files from the dcat catalog, stopping."

python check_db.py /data || echo "Could not migrate, ignoring"

exec uwsgi
