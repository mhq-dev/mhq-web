# MHQ-Web

MHQ-Web is a backend service using Django REST framework for a web application that aims to combine Integromat and Postman. It is developed by MHQ team.

## Description

MHQ-Web allows users to create custom APIs and use them in automation pipelines. It mimics the functionality of Integromat, which is a automation platform that connects apps and services together, and Postman, which is an API platform for developers to design, build, test and iterate their APIs. It uses PostgreSQL as database and Celery for scheduling purpose.

## Usage

- First you need to install [Docker](https://docs.docker.com/get-docker/)

- Then clone the repository and run server on your localhost
    
```shell script
$ docker-compose -f docker-compose.dev.yml up -d --build
```
 
## Deployment

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
