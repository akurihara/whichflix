[![CircleCI](https://circleci.com/gh/akurihara/whichflix/tree/master.svg?style=svg)](https://circleci.com/gh/akurihara/whichflix/tree/master)

# whichflix

Whichflix makes the toughest part of movie night quick and efficient - choosing a movie. Suggest a movie, or vote on the suggestions of others. The movie with the most votes wins!

## Documentation

This project uses Redoc to serve OpenAPI 2.0 documentation defined in each `views.py` file. See the documentation [here](https://warm-wave-23838.herokuapp.com/redoc).

## Set Up (Locally)

1. Create a virtual environment and install dependencies.
   ```
   $ brew install pyenv
   $ brew install pyenv-virtualenv
   $ pyenv install 3.7.4
   $ pyenv virtualenv 3.7.4 whichflix
   $ pyenv activate whichflix
   $ (whichflix) pip install -r requirements.txt
   ```

2. Set up environmental variables.
   ```
   cp .env.sample .env
   ```

   Add the following variables to the .env file:
   - `TMDB_API_KEY` - Your API key for The Movie Database, which can be obtained by following [these instructions](https://developers.themoviedb.org/3/getting-started/introduction).
   - `DATABASE_URL` - Database URL specifying which SQL database to connect to locally (e.g. `postgres://:@localhost:5432/whichflix`).

3. Install Postgres, create a new database, and initialize tables.
   ```
   $ brew install postgresql
   $ brew services start postgresql
   $ createdb whichflix
   $ source .env && python whichflix/manage.py migrate
   ```

## Running the Server

```
$ (whichflix) source .env && python whichflix/manage.py runserver
```

## Runnings Tests

```
$ (whichflix) source .env && python whichflix/manage.py test test/.
```

## Developing with Docker

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).

2. Run the server using `docker-compose`.
   ```
   $ docker-compose --env-file /dev/null up
   ```

3. Run the tests using `docker-compose`.
   ```
   $ docker-compose --env-file /dev/null run whichflix python whichflix/manage.py test
   ```
