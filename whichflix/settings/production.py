import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from whichflix.settings.base import *  # noqa

#
# django settings
#

ADMINS = [("Alex", "alex.kurihara@gmail.com")]

db_from_environment = dj_database_url.config()
DATABASES = {"default": db_from_environment}


#
# Sentry
#

sentry_sdk.init(
    dsn="https://f49134b3cdbe4161a339f4df212ff731@o380398.ingest.sentry.io/5206143",
    integrations=[DjangoIntegration()],
    send_default_pii=True,
)
