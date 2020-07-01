import socket
import os
import logging
import redis

from datetime import date, datetime
from celery import current_task
from celery.utils.log import current_process_index

from django.conf import settings
from .structlog import get_current_request


def add_task_info(_, __, event_dict):
    try:
        if current_task and current_task.request:
            event_dict['task_name'] = current_task.name
            event_dict['task_id'] = current_task.request.id
    except AttributeError:
        pass

    return event_dict


def add_request_info(_, __, event_dict):
    request = get_current_request()
    if not request:
        return event_dict

    event_dict.update(getattr(request, '_event_dict', {}))

    return event_dict


def date_formatter(_, __, event_dict):
    for key in event_dict.keys():
        if isinstance(event_dict[key], (date, datetime)):
            event_dict[key] = str(event_dict[key])
    return event_dict


def add_environment(_, __, event_dict):
    event_dict['@version'] = 1
    event_dict['environment'] = settings.ENVIRONMENT
    event_dict['hostname'] = socket.gethostname()
    event_dict['proc_pid'] = os.getpid()
    event_dict['proc_index'] = current_process_index()

    return event_dict


class RedisHandler(logging.Handler):
    def __init__(self, redis_list, redis_url=None, redis_timeout=30, level=logging.NOTSET):
        super().__init__(level)
        self.redis_list = redis_list
        self.redis_client = redis.StrictRedis.from_url(redis_url, socket_timeout=redis_timeout)

    def emit(self, record):
        try:
            self.redis_client.lpush(self.redis_list, self.format(record))
        except redis.RedisError:
            pass


class RequireProdOrStage(logging.Filter):
    def filter(self, record):
        return settings.ENVIRONMENT in ('prod', 'stage')


class RequiredProdOnly(logging.Filter):
    def filter(self, record):
        return settings.ENVIRONMENT == 'prod'


class NotCI(logging.Filter):
    def filter(self, record):
        return settings.CI_TESTS is False
