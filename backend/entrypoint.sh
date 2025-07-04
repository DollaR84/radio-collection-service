#!/bin/bash
set -e

chown -R appuser:appgroup /app/data 2>/dev/null || true

graceful_shutdown() {
  echo "Shutting down..."
  exit 0
}
trap graceful_shutdown SIGTERM SIGINT

echo "Applying database migrations..."
for i in {1..5}; do
    alembic upgrade head && break
    sleep $i
done

echo "Starting application..."
exec uvicorn main:app --lifespan on --host 0.0.0.0 --port 8000 "$@"
