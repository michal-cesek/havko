#!/usr/bin/env bash
set -e
set -a
. ./.env
set +a

source python3_venv/bin/activate
python3 monitor.py >> log.txt