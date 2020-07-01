import inspect
from structlog import get_logger
from functools import wraps
from django.db import OperationalError
from time import sleep

logger = get_logger(__name__)


def deadlock_retry(timeout=10, max_retries=5):
    """
    Отлавливает dead lock, выполняет оборачиваемую
    функцию повторно с таймаутом @timeout
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for try_i in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except OperationalError as exc:
                    if 'deadlock detected' in str(exc).lower():

                        path = inspect.getmodule(func).__name__ + '.' + func.__qualname__
                        logger.warning('deadlock_detected', function=path,
                                       try_i=try_i, max_retries=max_retries, timeout=timeout)

                        if try_i == max_retries:
                            raise

                        sleep(timeout)
                    else:
                        raise
        return wrapper
    return decorator
