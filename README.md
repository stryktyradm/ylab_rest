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

#### 1. To build images:
```shell
docker compose build
```

#### 2. To launch all services
```shell
docker compose up -d
```

#### 3. After launching all the services to demonstrate the work and interaction with the API service, you can open the following address in the browser window:

[127.0.0.1:8000](http://127.0.0.1:8000)
or
[localhost:8000](http://localhost:8000)


#### 4. Stop previously running services
```shell
docker compose down
```

## Run Tests.

#### 1. To run the tests, run the following command

```shell
docker compose -f docker-compose-tests.yml up -d
```

#### 2. To see the results of running in the console, you need to run the following command

```shell
docker logs tests_app
```

#### also, the test results are saved in an html file format, which after starting the container can be found in the following path:

*./app/tests-reports/report.html*

#### this file can be opened in the browser or in the IDE (the best option)

#### 3. After reviewing the test results, it is necessary to stop all previously started services using the command

```shell
docker compose down
```

#### 4. And also delete the container with tests

```shell
docker rm tests_app
```
