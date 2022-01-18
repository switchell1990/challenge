# API School & Students

API for view school and students

## Prerequisites

- Python 3.8
- Docker
- Docker-Compose
- Postgres (if want to run locally)

## Library & Framework

- Django 3.2
- Django Rest Framework 3.13.1
- Pytest

## ENVIRONMENT VARIABLES

- Create a file in the root and call it .env
- Add the following environments

```sh

ALLOWED_HOSTS=*
DATABASE_URL=set_me
POSTGRES_PASSWORD=postgres
POSTGRES_DB=school_api
DEBUG=True
SECRET_KEY=set_me

```

## GETTING STARTED

- Run Docker-Compose (Postgres)

```sh
docker-compose up -d postgres
```

- Run Docker-Compose (Django) - This will also do your create migrations and migrations.

```sh
docker-compose up -d django
```

- Add initial data

```sh
docker-compose exec django ./manage.py createdata
```

## Running Tests

```sh
docker-compose exec django pytest
```

## Models

<p align="center">
  <img width="380" src="Model Design.png">
</p>

## Endpoints

- api/v1/students/ (GET, POST)
- api/v1//schools/ (GET, POST)
- api/v1/schools/:id (GET, PUT, PATCH, DELETE)
- api/v1/students/:id (GET, PUT, PATCH, DELETE)
- api/v1//schools/:id/students (GET, POST)
- api/v1/schools/:id/students/:id (GET, PUT, PATCH, DELETE)

## API Documentation

- To access the API Document, visit - <http://localhost:8000/docs/>

## Step 1

- Time spend - 1 hour

## Step 2

- Time spent - 2 hours

## Step 3

- Time spent - 3 hours (including setting up tests)

## LEFT TO DO

- Review one more time and then submit to recruiter!

<!-- pipenv lock -r > requirements.txt -->
