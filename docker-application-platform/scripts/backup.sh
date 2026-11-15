#!/usr/bin/env bash
# Save the database to one file with pg_dump, keep the newest 7 copies.
set -euo pipefail
cd "$(dirname "$0")/.."
dir="$HOME/backups/docker-application-platform"
mkdir -p "$dir"
file="$dir/items-$(date +%F-%H%M).dump"
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$file"
ls -1t "$dir"/*.dump | tail -n +8 | xargs -r rm --
echo "backup saved: $file ($(du -h "$file" | cut -f1))"
