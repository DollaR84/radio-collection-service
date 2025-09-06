cat backup/backup.sql | docker compose exec db pg_dump -U postgres -d radiocenter
