#!/usr/bin/env bash

set -u   # crash on missing environment variables
set -e   # stop on any error
set -x   # log every command.

source docker-wait.sh

# download files
python download_files_from_dcatd.py qji2W_HBpWUWyg /data

python check_db.py /data

# load data in database
python run_import.py /data
