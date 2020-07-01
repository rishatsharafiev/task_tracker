import os
import time
import types
from contextlib import contextmanager

import dateutil.parser as parser

from functools import wraps
from datetime import datetime, date, timedelta
from math import floor

from django.conf import settings


def chunked_items(items, size=100):
    if isinstance(items, set):
        items = tuple(items)

    if isinstance(items, types.GeneratorType):
        chunk = []
        for item in items:
            chunk.append(item)

            if len(chunk) == size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk
    else:
        for index in range(0, len(items), size):
            yield items[index:index + size]


def environ(*envs):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if settings.ENVIRONMENT in envs:
                return func(*args, **kwargs)
        return wrapper
    return inner


def to_date(d):
    if isinstance(d, str):
        return parser.parse(d).date()
    elif isinstance(d, datetime):
        return d.date()
    elif isinstance(d, date):
        return d
    else:
        raise Exception("Bad date")


def date_range(date1, date2):
    for n in range(int((to_date(date2) - to_date(date1)).days) + 1):
        yield date1 + timedelta(n)


def human_time(*args, **kwargs):
    secs = float(timedelta(*args, **kwargs).total_seconds())
    units = [("day", 86400), ("hour", 3600), ("minute", 60), ("second", 1)]
    parts = []
    for unit, mul in units:
        if secs / mul >= 1 or mul == 1:
            if mul > 1:
                n = int(floor(secs / mul))
                secs -= n * mul
            else:
                n = round(secs, 3) if secs != int(secs) else int(secs)
            parts.append("%s %s%s" % (n, unit, "" if n == 1 else "s"))
    return ", ".join(parts)


@contextmanager
def calc_duration():
    class Duration:
        def __init__(self):
            self._start_ts = time.time()
            self._dlt_ts = None
            self._finish_ts = None

        @property
        def ms(self):
            return (self._finish_ts or time.time()) - self._start_ts

        def freeze(self):
            if not self._finish_ts:
                self._finish_ts = time.time()

        def delta(self):
            dlt = self._dlt_ts or self._start_ts
            self._dlt_ts = time.time()
            return human_time(seconds=time.time() - dlt)

        def __repr__(self):
            return human_time(seconds=self.ms)

        def __str__(self):
            return human_time(seconds=self.ms)

    duration = Duration()
    try:
        yield duration
    finally:
        duration.freeze()
