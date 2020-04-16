import dj_database_url

from whichflix.settings.base import *  # noqa

#
# django settings
#

ADMINS = [("Alex", "alex.kurihara@gmail.com")]

db_from_environment = dj_database_url.config()
DATABASES = {"default": db_from_environment}
