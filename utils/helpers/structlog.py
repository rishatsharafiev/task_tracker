import uuid
import structlog
import traceback

from threading import local
from django.http import Http404
from django_structlog.celery import receivers
from celery import bootsteps
from celery.signals import (
    after_task_publish, task_prerun, task_retry, task_success, task_failure, task_revoked
)
from .functions import calc_duration


logger = structlog.getLogger(__name__)

_thread_locals = local()


def get_current_request():
    return getattr(_thread_locals, "request", None)


def receiver_after_task_publish(sender=None, headers=None, body=None, **kwargs):
    if body:
        receivers.logger.info("task_enqueued", task_id=headers['id'], task_name=headers['task'])
    else:
        receivers.logger.info("task_enqueued")


def receiver_task_pre_run(task_id, task, *args, **kwargs):
    receivers.logger.info('task_received', task_id=task_id, task_name=task.name)


def receiver_task_retry(request=None, reason=None, einfo=None, **kwargs):
    logger.warning("task_retrying", reason=reason)


def receiver_task_success(result=None, **kwargs):
    logger.info("task_succeed", result=str(result))


def receiver_task_failure(task_id=None, exception=None, traceback=None, einfo=None, *args, **kwargs):
    logger.exception("task_failed", error=str(exception), exception=exception)


def receiver_task_revoked(request=None, terminated=None, signum=None, expired=None, **kwargs):
    logger.warning("task_revoked", terminated=terminated, signum=signum, expired=expired)


def get_request_header(request, header_key, meta_key):
    if hasattr(request, "headers"):
        return request.headers.get(header_key)

    return request.META.get(meta_key)


class StructlogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        after_task_publish.connect(receiver_after_task_publish)

        self._raised_exception = False

    def get_event_dict(self, request):
        from ipware import get_client_ip

        correlation_id = get_request_header(request, "x-correlation-id", "HTTP_X_CORRELATION_ID")
        request_id = get_request_header(request, "x-request-id", "HTTP_X_REQUEST_ID") or str(uuid.uuid4())
        ip, _ = get_client_ip(request)

        _event_dict = {'request_id': request_id, 'ip': ip}

        if correlation_id:
            _event_dict['correlation_id'] = correlation_id

        if hasattr(request, "user"):
            _event_dict['user_id'] = request.user.pk

        _event_dict['request'] = f"{request.method} {request.path}"

        return _event_dict

    def __call__(self, request):

        setattr(request, '_event_dict', self.get_event_dict(request))

        _thread_locals.request = request

        logger.info("request_started", user_agent=request.META.get("HTTP_USER_AGENT"))

        self._raised_exception = False

        with calc_duration() as duration:
            response = self.get_response(request)

        if not self._raised_exception:
            logger.info("request_finished", code=response.status_code, duration=duration.ms,
                        duration_human=duration)

        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request

        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            # We don't log an exception here, and we don't set that we handled
            # an error as we want the standard `request_finished` log message
            # to be emitted.
            return

        self._raised_exception = True

        traceback_object = exception.__traceback__
        formatted_traceback = traceback.format_tb(traceback_object)
        logger.exception("request_failed", code=500, error=exception, error_traceback=formatted_traceback)

        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request


class StructlogInitStep(bootsteps.Step):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        after_task_publish.connect(receiver_after_task_publish)
        task_prerun.connect(receiver_task_pre_run)
        task_retry.connect(receiver_task_retry)
        task_success.connect(receiver_task_success)
        task_failure.connect(receiver_task_failure)
        task_revoked.connect(receiver_task_revoked)
