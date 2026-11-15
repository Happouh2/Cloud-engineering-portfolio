#!/usr/bin/env bash
# Run the same checks as GitHub Actions, inside a throwaway Python container.
# The project is mounted read-only (:ro), so nothing gets written into your folder.
set -euo pipefail
cd "$(dirname "$0")/.."
docker run --rm -v "$PWD":/src:ro -w /src \
  -e PYTHONDONTWRITEBYTECODE=1 -e PIP_ROOT_USER_ACTION=ignore -e PIP_DISABLE_PIP_VERSION_CHECK=1 \
  python:3.12-slim sh -c '
    echo "== installing" && pip install -q -r app/requirements.txt -r requirements-dev.txt &&
    echo "== lint (ruff)" && ruff check --no-cache . &&
    echo "== tests (pytest)" && pytest -q -p no:cacheprovider &&
    echo "== known-vulnerable packages (pip-audit)" && pip-audit -r app/requirements.txt --progress-spinner off &&
    echo "ALL CHECKS PASSED"'
