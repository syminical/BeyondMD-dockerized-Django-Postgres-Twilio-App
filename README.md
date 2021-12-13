# BeyondMD - Django/Postgres App

## Setup / Startup

## Docker Setup
### There's an issue with postgres and Docker for Windows (more info in DB setup).  

1. Make sure to modify `docker-compose.yml` to set the Authy variables!
2. Run ```$ docker compose up``` to set things up, but it will fail.
3. Run ```$ docker compose down```
4. Start up again with ```$ docker compose up```

## DB Setup
I had to create a local volume for postgres persistence due to an issue with Docker for windows and postgres. The database may need to be manually intialized if running for the first time.  
```$ docker compose exec web sh```  
```# python manage.py migrate notes```
___
## App
[http://localhost:8000](http://localhost:8000)  
- The app should work after following all of the above steps :)
  - The setup steps above only need to be done once per new db volume.