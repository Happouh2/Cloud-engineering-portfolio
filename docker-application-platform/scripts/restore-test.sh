#!/usr/bin/env bash
# Prove the newest backup works: load it into a scratch database, count rows, drop it.
set -euo pipefail
cd "$(dirname "$0")/.."
latest=$(ls -1t "$HOME/backups/docker-application-platform"/*.dump | head -1)
echo "testing $latest"
docker compose exec -T db sh -c 'dropdb -U "$POSTGRES_USER" --if-exists restore_test && createdb -U "$POSTGRES_USER" restore_test && pg_restore -U "$POSTGRES_USER" -d restore_test --no-owner' < "$latest"
rows=$(docker compose exec -T db sh -c 'psql -U "$POSTGRES_USER" -d restore_test -tAc "SELECT count(*) FROM items"')
echo "rows in the restored copy: $rows"
docker compose exec -T db sh -c 'dropdb -U "$POSTGRES_USER" restore_test'
echo "restore test passed"
