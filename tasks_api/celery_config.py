import os
from celery import Celery
# from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "tasks_api",
    backend=os.getenv('CELERY_RESULT_BACKEND'),
    broker=os.getenv('CELERY_BROKER_URL'),
    CELERY_TASK_SERIALIZER='json'
)

celery_app.conf.imports = [
    'tasks_api.task.tasks',
    'tasks_api.sub_task.tasks',
]

celery_app.conf.beat_schedule = {
    'task1_every_5_min': {
        'task': 'before_deadline_task_notification',
        'schedule': 300,  # Every 5 minutes (in seconds)
    },
    'task2_every_1_min': {
        'task': 'current_task_notification',
        'schedule': 60,  # Every 1 minute (in seconds)
    },
    'task3_every_15_min': {
        'task': 'after_deadline_task_notification',
        'schedule': 900,  # Every 15 minutes (in seconds)
    },
    'sub_task1_every_5_min': {
        'task': 'before_deadline_sub_task_notification',
        'schedule': 300,  # Every 5 minutes (in seconds)
    },
    'sub_task2_every_1_min': {
        'task': 'current_sub_task_notification',
        'schedule': 60,  # Every 1 minute (in seconds)
    },
    'sub_task3_every_15_min': {
        'task': 'after_deadline_sub_task_notification',
        'schedule': 900,  # Every 15 minutes (in seconds)
    },
}

celery_app.conf.timezone = 'UTC'
celery_app.conf.update(task_track_started=True)
