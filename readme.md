## FastAPI backend project  

A site with recipes for various dishes

1) FastApi
2) PostgeSQL+asycpg
3) Alembic

Starting the app:

1) install Git, Docker, Docker-compose and all docker requirements
2) clone repo
   ```commandline
   git clone https://github.com/RautaruukkiPalich/recipes_portal
   ```
3) create .env file in . with parameters
    ```bash
    DB_NAME= #enter database name 
    DB_HOST= #enter database host # database
    DB_PORT= #enter database port
    DB_USER= #enter database user
    DB_PASS= #enter database password
    JWT_SECRET= #enter jwt secret
    RESET_PASS_SECRET= #enter reset_pass secret
    VERIFICATION_SECRET= #enter verification_pass secret
    COOKIE_LIFETIME= #enter cookie lifetime in seconds
    ```
