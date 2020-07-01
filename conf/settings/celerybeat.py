from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    # },
    # 'task-example': {
    #     'task': 'tasks.tasks.starters.run_archive_tasks_workload',
    #     'schedule': crontab(minute=0, hour=3),
    # },
}

CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
