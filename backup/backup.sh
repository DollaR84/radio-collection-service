#!/bin/bash
set -e

DB_NAME="radiocenter"
DB_USER="postgres"
BACKUP_DIR="./backup"
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y-%m-%d_%H-%M-%S).sql"

mkdir -p "$BACKUP_DIR"

echo "Creating a database backup $DB_NAME..."
docker compose exec db pg_dump -U "$DB_USER" -d "$DB_NAME" > "$BACKUP_FILE"

echo "Backup saved: $BACKUP_FILE"
