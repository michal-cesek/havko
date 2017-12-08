#!/usr/bin/env bash
set -e
set -a
. ./.env
set +a

python3 monitor.py >> log.txt