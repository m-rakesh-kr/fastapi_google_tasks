from datetime import datetime
from datetime import timedelta
from fastapi_mail import MessageSchema
from tasks_api.celery_config import celery_app
from tasks_api.utils import MailConfig
from tasks_api.utils import Mail
from tasks_api import constants
import asyncio
from tasks_api.task.models import Task
from database import get_db

session = next(get_db())


@celery_app.task(name="before_deadline_task_notification")
def before_deadline_task_notification():
    current_time = datetime.utcnow() + timedelta(hours=5.5)
    tasks = session.query(Task).filter(Task.date_time > current_time,
                                       Task.date_time - current_time <= timedelta(minutes=15)).all()
    for t in tasks:
        mail = t.list.creator.email
        name = t.list.creator.name

        template = "alert_msg.html"
        temp_body = {'username': name,
                     'alert_msg': constants.TASK_ALERT_MSG_BEFORE,
                     'title': t.title,
                     'details': t.details,
                     'created_on': t.created_on,
                     'date_time': t.date_time
                     }
        message_schema = MessageSchema(subject=constants.TASK_ALERT_SUBJECT, recipients=[mail],
                                       template_body=temp_body)
        mail_conf = MailConfig.connection_config()
        asyncio.run(Mail.send_mail(message_schema, mail_conf, template))
        print(f"Task alert before mail sent successfully! on {mail}")


@celery_app.task(name="current_task_notification")
def current_task_notification():
    current_time = datetime.utcnow() + timedelta(hours=5.5)
    tasks = session.query(Task).filter(Task.date_time == current_time).all()
    for t in tasks:
        mail = t.list.creator.email
        name = t.list.creator.name

        template = "alert_msg.html"
        temp_body = {'username': name,
                     'alert_msg': constants.TASK_ALERT_MSG_CURRENT,
                     'title': t.title,
                     'details': t.details,
                     'created_on': t.created_on,
                     'date_time': t.date_time
                     }
        message_schema = MessageSchema(subject=constants.TASK_ALERT_SUBJECT, recipients=[mail],
                                       template_body=temp_body)
        mail_conf = MailConfig.connection_config()
        asyncio.run(Mail.send_mail(message_schema, mail_conf, template))
        print(f"Task alert Current mail sent successfully! on {mail}")


@celery_app.task(name="after_deadline_task_notification")
def after_deadline_task_notification():
    current_time = datetime.utcnow() + timedelta(hours=5.5)
    tasks = session.query(Task).filter(Task.date_time < current_time,
                                       current_time - Task.date_time <= timedelta(minutes=15)).all()
    for t in tasks:
        mail = t.list.creator.email
        name = t.list.creator.name

        template = "alert_msg.html"
        temp_body = {'username': name,
                     'alert_msg': constants.TASK_ALERT_DEADLINE_MSG,
                     'title': t.title,
                     'details': t.details,
                     'created_on': t.created_on,
                     'date_time': t.date_time
                     }

        message_schema = MessageSchema(subject=constants.TASK_ALERT_SUBJECT, recipients=[mail],
                                       template_body=temp_body)
        mail_conf = MailConfig.connection_config()
        asyncio.run(Mail.send_mail(message_schema, mail_conf, template))
        print(f"Task alert after deadline mail sent successfully! on {mail}")
