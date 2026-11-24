#!/usr/bin/env bash
# Daily pg_dump of the soulsle database (runs pg_dump inside the postgres container).
# Restore: docker exec -i postgresql-osnn-postgresql-1 sh -c 'pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --clean --if-exists' < <dump>
set -euo pipefail

CONTAINER="${PG_CONTAINER:-postgresql-osnn-postgresql-1}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/backups/soulsle}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"

mkdir -p "$BACKUP_DIR"
out="$BACKUP_DIR/soulsle-$(date -u +%Y%m%dT%H%M%SZ).dump"

docker exec "$CONTAINER" sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$out.tmp"
mv "$out.tmp" "$out"

find "$BACKUP_DIR" -name 'soulsle-*.dump' -mtime +"$RETENTION_DAYS" -delete
echo "backup written: $out ($(du -h "$out" | cut -f1))"
