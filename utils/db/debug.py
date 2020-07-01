from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.utils import CursorDebugWrapper
from utils.helpers.functions import calc_duration


class ShowSQLCursorDebugWrapper(CursorDebugWrapper):
    def execute(self, sql, params=()):
        sql = self.cursor.mogrify(sql, params).decode()

        with calc_duration() as duration:
            try:
                print(sql)
                return super().execute(sql, params)
            finally:
                print(f'finished: {duration}')


def show_sql():
    fn = BaseDatabaseWrapper.cursor

    BaseDatabaseWrapper.cursor = lambda self: ShowSQLCursorDebugWrapper(fn(self), self)
