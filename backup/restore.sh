#!/usr/bin/bash
set -e

DB_NAME="radiocenter"
DB_USER="postgres"

if [ -n "$1" ]; then
  BACKUP_FILE="$1"
else
  BACKUP_FILE=$(ls -t ./backup/backup_*.sql | head -n 1)
fi

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Backup file not found: $BACKUP_FILE"
  exit 1
fi

echo "Restoring the database $DB_NAME from file $BACKUP_FILE..."

docker compose exec -T db psql -U "$DB_USER" -d "$DB_NAME" < "$BACKUP_FILE"

echo "Restoration completed!"
