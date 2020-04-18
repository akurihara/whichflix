FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . /usr/src/app

# install dependencies
RUN pip install -r requirements.txt

# tell the port number the container should expose
EXPOSE 8000

# run the server
CMD gunicorn whichflix.wsgi:application -b 0.0.0.0:8000
