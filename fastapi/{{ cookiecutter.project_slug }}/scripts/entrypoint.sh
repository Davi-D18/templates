#!/usr/bin/env sh
set -e

echo "Aplicando migrations..."
alembic upgrade head

echo "Iniciando Uvicorn..."
exec uvicorn {{ cookiecutter.project_slug }}.app.main:app --host 0.0.0.0 --port 8000
