import sentry_sdk
from decouple import config
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import ignore_logger


ENVIRONMENT = config('ENVIRONMENT')
SENTRY_DSN = config('SENTRY_DSN')

if SENTRY_DSN and ENVIRONMENT in ('stage', 'prod'):
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        environment=ENVIRONMENT
    )
    ignore_logger('elasticapm.transport')
