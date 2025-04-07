echo "Run migration with alembic"
alembic upgrade head

echo "Starting the server ..."
python3 /app/main.py
