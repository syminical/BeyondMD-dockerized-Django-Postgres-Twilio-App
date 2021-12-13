# BeyondMD - Django/Postgres App

## Setup / Startup
## DB setup
I had to create a local volume for postgres persistence due to an issue with Docker for windows and postgres. The database may need to be manually intialized if running for the first time.  
```$ docker compose exec web sh```  
```# python manage.py makemigrations```  
```# python manage.py migrate notes```
## Startup
```$ docker compose up```  
* This may need to be terminated and re-ran if the volumes need to be created. (There was an option to use external volumes, but that seemed like more overhead.)