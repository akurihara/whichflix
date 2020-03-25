import dj_database_url
import django_heroku

from whichflix.settings.base import *  # noqa

#
# django settings
#

ADMINS = [("Alex", "alex.kurihara@gmail.com")]

# Activate Django-Heroku.
django_heroku.settings(locals())

db_from_environment = dj_database_url.config()
DATABASES = {"default": db_from_environment}
