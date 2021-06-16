<b><i> MHQ WEB SERVER </i></b>

# Instructions For Use

#### First you need to install [Docker](https://docs.docker.com/get-docker/)

- Clone the repository

    ```shell script
    $ git clone https://github.com/mhq-dev/mhq-web.git
    ```
- Run server on your localhost
    
    ```shell script
    $ docker-compose -f docker-compose.dev.yml up -d --build
    ```
 
## Deploy

- Make .env.prod file like the .env.dev file with your own settings

- Make .env.prod.db file
   
    ```shell script
    POSTGRES_USER={YOUR_DATABASE_USERNAME}
    POSTGRES_PASSWORD={YOUR_DATABASE_PASSWORD}
    POSTGRES_DB={YOUR_DATABASE_NAMW}
    ```
- Move to the nginx directory and clone mhq front repository
    
    ```shell script
    $ cd nginx
    $ git clone https://github.com/mhq-dev/mhq-front.git
    ``` 
- Back to the root directory and run server

    ```shell script
    $ cd ..
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

- Create your super user for administrative tasks
    
    ```shell script
    $ docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
    ```

#### Database Management at '/api/admin/'

#### API Document and Management at '/api/swagger/'
