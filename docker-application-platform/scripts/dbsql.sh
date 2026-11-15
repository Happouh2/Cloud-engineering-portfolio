#!/usr/bin/env bash
# Run psql inside the db container as the database owner.
# Usage: ./scripts/dbsql.sh -c "SELECT 1;"   or   ./scripts/dbsql.sh < file.sql
cd "$(dirname "$0")/.."
exec docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" "$@"' psql "$@"
