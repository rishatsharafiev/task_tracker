from django.conf import settings
from kombu.utils import symbol_by_name


class EnvRouter(object):
    def route_for_task(self, task, args=None, kwargs=None):
        if settings.ENVIRONMENT in ['stage', 'dev', 'prod']:
            return {'exchange': 'default', 'routing_key': 'default'}
        else:
            return getattr(symbol_by_name(task), 'queue', None)
