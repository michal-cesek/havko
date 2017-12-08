#!/usr/bin/env bash
set -e
export $(cat .env | xargs)

apt update
apt install python-pip -y
pip install virtualenv
virtualenv -p python3 python3_venv
source python3_venv/bin/activate
pip install --trusted-host pypi.python.org -r requirements.txt

python3 monitor.py >> log.txt