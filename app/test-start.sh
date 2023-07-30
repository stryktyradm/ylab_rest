#! /usr/bin/env bash

set -e
set -x

# Delete the directory and files with reports.
rm -rf tests-reports/*

# Let the DB start.
python src/backend_prestart.py

# Run tests.
pytest src/tests

# Change access rights to report files.
chmod -R 777 tests-reports/*
