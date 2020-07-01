import logging
from decouple import config
from django.core.serializers.json import DjangoJSONEncoder
from structlog import configure, stdlib, processors, dev
from structlog_sentry import SentryJsonProcessor

from utils.helpers.logging import (
    add_task_info, date_formatter, add_environment, add_request_info
)
from utils.db.debug import show_sql


CI_TESTS = config('CI_TESTS', cast=bool, default=False)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'required_prod_only': {
            '()': 'utils.helpers.logging.RequiredProdOnly',
        },
        'not_ci': {
            '()': 'utils.helpers.logging.NotCI',
        }
    },
    'formatters': {
        'plain_console': {
            '()': stdlib.ProcessorFormatter,
            'processor': dev.ConsoleRenderer(colors=not CI_TESTS),
        },
        'json': {
            '()': stdlib.ProcessorFormatter,
            'processor': processors.JSONRenderer(cls=DjangoJSONEncoder)
        }
    },
    'handlers': {
        # 'logstash': {
        #     'class': 'helpers.utils.logging.RedisHandler',
        #     'filters': ['required_prod_only'],
        #     'formatter': 'json',
        #     'redis_list': 'logstash_bfb',
        #     'redis_url': config('LOGSTASH_REDIS_URL'),
        #     'redis_timeout': config('LOGSTASH_TIMEOUT', default=30, cast=int)
        # },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'plain_console',
            'filters': ['not_ci']
        }
    },
    'loggers': {
        'django_structlog': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'utils': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'billing': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'butler_bot': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'chat': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'marketing': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'notifications': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'payouts': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'projects': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'reports': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'tasks': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'teams': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
        'users': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

dev_processors = [
    stdlib.add_log_level,
    processors.StackInfoRenderer(),
    dev.set_exc_info,
    processors.format_exc_info,
    date_formatter,
    add_request_info,
    stdlib.ProcessorFormatter.wrap_for_formatter
]

prod_processors = [
    stdlib.filter_by_level,
    stdlib.add_log_level,
    stdlib.add_logger_name,
    add_task_info,
    add_request_info,
    add_environment,
    processors.format_exc_info,
    processors.UnicodeDecoder(),
    processors.TimeStamper(fmt="ISO", utc=True, key='@timestamp'),
    SentryJsonProcessor(level=logging.ERROR, tag_keys=['environment']),
    stdlib.ProcessorFormatter.wrap_for_formatter
]

if config('ENVIRONMENT') in ('dev', 'test'):
    processors_list = dev_processors
else:
    processors_list = prod_processors

configure(
    processors=processors_list,
    logger_factory=stdlib.LoggerFactory(),
    wrapper_class=stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

if config('ENABLE_PRINT_SQL', cast=bool, default=False):
    show_sql()
