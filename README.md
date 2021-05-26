# EOSC Marketplace OMS JIRA Adapter

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

OMS Jira adapter allows interaction between [Marketplace](https://github.com/cyfronet-fid/marketplace) and JIRA in order to fulfill users' orders.

## Architecture
OMS JIRA Adapter works as a microservice and exposes API to the Marketplace.

The inner structure can be described as two elements:
- thin web service part based on `Celery` and `Flask` 

## Development environment

### Requirements
- [git](https://git-scm.com/)
- [Python 3.9.x](https://www.python.org/downloads/release/python-390/)
- [Pipenv](https://pypi.org/project/pipenv/)
- [postgres](https://www.mongodb.com/)
- [redis](https://redis.io/)


All required project packages are listed in the pipfile. For their installation look at the setup section.

### Setup
1. Install git, python and pipenv
2. Clone this repository and go to its root directory
```bash
git clone https://github.com/cyfronet-fid/oms-adapter-jira.git
```
3. Install all required project packages by executing
```bash
pipenv --dev install
```

4. To open project virtual environment shell, type:
```bash
pipenv shell
```

### DB Migrations

Application uses sqlalchemy as an orm wrapper and alembic (wrapped in flask-migrations) as a migration engine.

Check documentation for the above libraries for details, but here's a short version:

Migrate database to the newest version:

```
flask db upgrade
```

Create new migration based on the changes in the models:

```
flask db migrate -m "name_of_migration"
```

### Server

Launch OMS Jira adapter server by executing in the project root directory:
```
export FLASK_ENV=development
export FLASK_APP=app.py
pipenv run flask run
```

NOTE: You can customize flask host and flask port by using `FLASK_RUN_HOST` and `FLASK_RUN_PORT` [env](#env-variables) variables accordingly.

### Celery
To run background tasks you also need a celery worker running alongside your server. To run the worker:
```bash
export FLASK_ENV=development
pipenv run celery -A worker:app worker --loglevel=info
```

NOTE: Celery needs a running [redis](#redis) broker server in the background.

### Redis
NOTE: It is recommended for the developers to use docker-compose to run all the background servers
(see [docker](#Docker) section below).

OMS Jira adapter is running celery to execute background tasks in a queue.
In the development environment we are assuming that
the redis is running on `redis://localhost:36379`.

NOTE: You can customize your redis host url using `REDIS_HOST` [env](#env-variables) variable.

### Postgres
NOTE: It is recommended for the developers to use docker-compose to run all the background servers
(see [docker](#Docker) section below).

Install and start the postgres server. It is expected to be available on 
url `mongodb://localhost:35432`.

NOTE: You can customize your postgresql host path in `OMS_DB_HOST` [env](#env-variables) variable.

### API
You can interact with OMS Jira adapter microservice using API available (by default) here: http://localhost:9000/

### Docker
To run all background servers needed for development (redis, postgresql) it is recommended that you use Docker:
```bash
docker-compose up
```
Postgresql will be exposed and available on your host on `127.0.0.1:35432`, and redis on `127.0.0.1:36379`, although
you can change them using `OMS_DB_HOST` and `REDIS_HOST` [env](#env-variables) variables accordingly.

NOTE: You still need to set up Flask server and celery worker as shown above. This is advantageous over the next option
because you can run pytest from your IDE, easily debug the application, easily restart the broken flask server and 
additionally you don't need to rebuild your docker image if your dependencies change.

For full-stack local development deployment use:
```bash
docker-compose -f docker-compose.yml -f development.yml up
```
This will build application images and run base flask development server on `127.0.0.1:9000` 
(you can customize flask port and host using [env](#env-variables) variables).
This command will also run celery worker, mongo and redis.
You can immediately change the server code without restarting the containers.


### Tests
To run all the tests in our app run:
```bash
export FLASK_ENV=testing
pipenv run pytest ./tests
```
...or you can run them using docker:
```bash
docker-compose -f docker-compose.testing.yml up && docker-compose -f docker-compose.testing.yml down
```

### ENV variables
We are using .env to store instance specific constants or secrets. This file is not tracked by git and it needs to be 
present in the project root directory. Details:
- `OMS_ID` - OMS ID as defined in the marketplace
- `OMS_MP_TOKEN` - User authentication token for the MP (required for API auth) 
- `OMS_MP_URL` - URL to the root of the marketplace with which adapter instance should communicate 
- `OMS_DB_HOST` - url and port of your running database server (example: postgresql://postgres:postgres@127.0.0.1:35432/oms_jira) or desired url and port of your database
  server when ran using docker-compose (recommended)
- `OMS_REDIS_HOST` - url and port of your running redis server (example: `127.0.0.1:36379`) or desired url and port of your redis
  server when ran using docker-compose (recommended)
- `FLASK_RUN_HOST` - desired url of your application server (example: `127.0.0.1`)
- `FLASK_RUN_PORT` - desired port of your application server (example: `9000`)
- `CELERY_LOG_LEVEL` - log level of your celery worker when ran using docker (one of: `CRITICAL`, `ERROR`, `WARN`, `INFO` or `DEBUG`)
- `SENTRY_DSN` -  The DSN tells the sentry where to send the events (example: `https://16f35998712a415f9354a9d6c7d096e6@o556478.ingest.sentry.io/7284791`). If that variable does not exist, sentry will just not send any events.
- `SENTRY_ENVIRONMENT` - environment name - it's optional and it can be a free-form string. If not specified and using docker, it is set to `development`/`testing`/`production` respectively to the docker environment.
- `SENTRY_RELEASE` - human readable release name - it's optional and it can be a free-form string. If not specified, sentry automatically set it based on commit revision number.

NOTE: All the above variables have reasonable defaults, so if you want you can just have your .env file empty.

### PyCharm Integrations
#### .env
Install [EnvFile plugin](https://plugins.jetbrains.com/plugin/7861-envfile). Go to the run configuration of your choice, switch to `EnvFile` tab, check `Enable EnvFile`, click `+` button below, select `.env` file and click `Apply` (Details on the plugin's page)

#### PyTest
In Pycharm, go to `Settings` -> `Tools` -> `Python Integrated Tools` -> `Testing` and choose `pytest`
Remember to put FLASK_ENV=testing env variable in the configuration.

### External tools integration

#### Sentry
`Sentry` is integrated with the `flask` server and the `celery` task queue manager so all unhandled exceptions from these entities will be tracked and sent to the sentry.
Customization of the sentry ntegration can be done vie environmental variables (look into [ENV variables](#env-variables) section) - more about them [here](https://docs.sentry.io/platforms/python/configuration/options/)