#! /usr/bin/env bash

# Let the DB start.
python src/backend_prestart.py

# Run migrations.
alembic upgrade head

# Create initial data in DB.
python src/initial_data.py
