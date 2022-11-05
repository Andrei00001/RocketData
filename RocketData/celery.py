import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RocketData.settings')

celery_app = Celery('RocketData')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    from app.tasks import (
        sync_bods,
    )
    sender.add_periodic_task(3 * 60 * 60, sync_bods.s())


celery_app.conf.beat_schedule = {
    # Executes every dey morning at 6:30 a.m.
    'every-dey': {
        'task': 'app.tasks.sync_bods2',
        'schedule': crontab(minute=30, hour=6),
    },
}
