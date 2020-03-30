# whichflix

Whichflix makes the toughest part of movie night quick and efficient - choosing a movie. Suggest a movie, or vote on the suggestions of others. The movie with the most votes wins!

## Set Up (Locally)

1. Create a virtual environment and install dependencies.
   ```
   $ brew install pyenv
   $ pyenv install 3.7.4
   $ pyenv local 3.7.4
   $ brew install pipenv
   $ pipenv install
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

## Running the Server (Locally)

```
source .env && python whichflix/manage.py runserver
```

## Runnings Tests (Locally)

```
source .env && python whichflix/manage.py test test/.
```

## Running the Server (Docker)

1. Build the Docker image.
   ```
   $ docker build -t alexkurihara/whatshouldwewatch .
   ```

2. Run the server in a container.
   ```
   $ docker run -p 8000:8000 --env-file .env.docker alexkurihara/whatshouldwewatch
   ```

## Runnings Tests (Docker)

1. If you haven't already, build the Docker image.
   ```
   $ docker build -t alexkurihara/whatshouldwewatch .
   ```

2. Run a container in interactive mode.
   ```
   $ docker run -it alexkurihara/whatshouldwewatch sh
   ```

3. Run the tests using Django.
   ```
   # python whatshouldwewatch/manage.py test test/.
   ```
