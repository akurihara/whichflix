import dj_database_url

from whatshouldwewatch.settings.base import *  # noqa

#
# django settings
#

DEBUG = True

db_from_environment = dj_database_url.config()
DATABASES = {"default": db_from_environment}
