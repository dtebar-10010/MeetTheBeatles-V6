#!/usr/bin/env bash
set -euo pipefail

# Safety: avoid accidental deploy with DEBUG enabled
if [ "${DJANGO_DEBUG:-True}" != "False" ]; then
  echo "ERROR: DJANGO_DEBUG is not 'False'. Aborting deploy to avoid exposing DEBUG in production."
  echo "Set DJANGO_DEBUG=False in the environment (or in PythonAnywhere Web > Environment variables) and retry."
  exit 1
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)

echo "Deploying branch: $BRANCH"

echo "Pulling latest changes..."
git pull origin "$BRANCH"

echo "Installing requirements..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "Applying migrations..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Deployment steps finished. Please reload the web app in the PythonAnywhere Web tab to apply changes."
