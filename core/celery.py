import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'core.settings')

app = Celery('wb_slots')
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'every_update_slots': {
        'task': 'wb.tasks.repeat_update_slots',
        'schedule': 10.0,
    },
    'every_update_whs': {
        'task': 'wb.tasks.repeat_update_warehouses',
        'schedule': 60.0,
    },
    'every_search_slots': {
        'task': 'orders.tasks.repeat_search_slots',
        'schedule': 15,
    }
}
