FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . /usr/src/app

# install dependencies
RUN pip3 install pipenv
RUN pipenv install

# tell the port number the container should expose
EXPOSE 8000

# run the server
CMD pipenv run gunicorn whichflix.wsgi:application -b 0.0.0.0:8000
