# API School & Students

API for view schools and students

## Prerequisites

- Python 3.8
- Docker
- Docker-Compose
- Postgres (if want to run locally)

## Library & Framework

- Django 3.2
- Django Rest Framework 3.13.1
- Pytest

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


## INSTALLING

- Clone the project into a directory you've created on your machine

```sh
git clone https://github.com/switchell1990/manatal.git
```

- To get into the project directory from your terminal

```sh
cd manatal
```

- Open project into your editior (VS CODE)

```sh
code .
```

## ENVIRONMENT VARIABLES

- Create a file in the root and call it .env
- Add the following environments

```sh

ALLOWED_HOSTS=*
DATABASE_URL=postgres://postgres:postgres@postgres:5432/school_api (for docker)
DATABASE_URL=postgres://postgres:postgres@localhost:5432/school_api (for local)
POSTGRES_PASSWORD=postgres
POSTGRES_DB=school_api
DEBUG=True
SECRET_KEY=set_me

```


## GETTING STARTED

Once your project is up and running,you can access it from your access the api by going to - <http://localhost:8000/api/>

## Run with Docker

- Open a command terminal and run Docker-Compose (Postgres)

```sh
docker-compose up -d postgres
```

- Open a new terminal and Run Docker-Compose (Django) - This will also do your create migrations and migrations.

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

## Run with Pipenv

- Create a database with the following commands (reuqires postgres installed on local machine)

```sh
psql -U postgres
```

```sh
create database school_api;
```

- Create environemnt and install dependencies

```sh
pipenv install -r dependencies/requirements-dev.txt
```

- Activate the virtual enviornment

```sh
pipenv shell
```

- Migrate the migrations.

```sh
./manage.py migrate
```

-Run tests

```sh
pytest
```

- Run the server

```sh
./manage.py runserver
```

## API Documentation

- To access the API Document, visit - <http://localhost:8000/docs/>

## Step 1

- Time spend - 1 hour

## Step 2

- Time spent - 2 hours

## Step 3

- Time spent - 3 hours (including setting up tests)

## Further comments

I have decided to change how delete works, instead of deleting the record I have opted to change the is_active flag to false so the records can be kept in the database for a period of time. 