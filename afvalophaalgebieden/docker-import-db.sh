#!/usr/bin/env bash

set -u   # crash on missing environment variables
set -e   # stop on any error
set -x   # log every command.

source docker-wait.sh

python check_db.py

# download files
python download_files_data_catalog.py qji2W_HBpWUWyg /data

# load data in database
python run_import.py /data
