import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'hotelmanagementsystem.settings')

app = Celery('hotelmanagementsystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.beat_schedule = {
    'is_active_check_task': {
        'task': 'accounts.tasks.daily_check_task',
        'schedule': crontab(minute=59,hour=23),
    },
    'notification_task': {
        'task': 'accounts.tasks.reservation_defore_end',
        'schedule': crontab(minute=59,hour=23),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
