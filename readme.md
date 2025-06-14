# RadioCollectionService  
* version: 1.0


This service provides information about radio station audio streams.  
Parses these links in open sources, tests them for functionality, provides search by country, genre or other information.  
Users will have preferences saved, based on which recommendations will be offered.  

## Initializing the Project:  
First of all, need to fill the environment variables with configuration data in the file: '.env'

## Build project:  
```
    docker-compose build
```

## Running the Project:  
```
    docker-compose up -d
```

### Notes:  
If everything is done correctly, the project should automatically apply migrations and start.

## Manual apply migrations and start:  
### When there is a problem with the missing database in postgresql:
```
    docker compose exec db psql -U {your-db-user} -c "CREATE DATABASE {your-db-name};"
```
Where:
  your-db-user: your db user for database login;
  your-db-name: your db name in postgresql;

## Development:  
To manually create migrations and apply them:
```
    docker compose exec api alembic revision --autogenerate -m "your comment for migration"
    docker compose exec api alembic upgrade head
```

### Access:
for backend api:
```
    http://127.0.0.1:8000
```

for frontend web:
'''
    http://127.0.0.1
    http://127.0.0.1:80
    http://127.0.0.1:3000
'''
