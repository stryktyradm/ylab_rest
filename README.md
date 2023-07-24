**Project requirements**:

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).

The project is launched with test environment variables that can be found in the file .env in the root directory of the project

[.env](./.env)

Example:

```shell
# Backend
PROJECT_NAME=name_project

# Postgres
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=pass
POSTGRES_DB=app
```

## Run in docker compose.

*[INFO] for docker compose v1, use the commands below with the following syntax*

```shell
docker-compose build
docker-compose up -d
docker-compose down
```

*see: [https://stackoverflow.com/questions/66514436/difference-between-docker-compose-and-docker-compose](https://stackoverflow.com/questions/66514436/difference-between-docker-compose-and-docker-compose)*

If you are using docker compose v2:

#### 1) To build images:
```shell
docker compose build
```

#### 2) To launch all services
```shell
docker compose up -d
```

#### 3) After launching all the services to demonstrate the work and interaction with the API service, you can open the following address in the browser window:

[127.0.0.1:8000](127.0.0.1:8000)
or
[localhost:8000](localhost:8000)


#### 4) Stop previously running services
```shell
docker compose down
```