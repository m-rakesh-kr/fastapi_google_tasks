import asyncio
from celery import shared_task
from fastapi_mail import MessageSchema
from tasks_api import constants
from tasks_api.utils import MailConfig, Mail

@shared_task()
def send_user_creation_mail(email, username):
    # Logic to send the user creation email
    temp_body = {
        'username': username,
        'alert_msg': constants.USER_CREATION_EMAIL_ALERT_MSG,
    }

    message_schema = MessageSchema(
        subject=constants.USER_CREATION_EMAIL_ALERT_TITLE,
        recipients=email,  # Pass the email address as a string
        template_body=temp_body
    )
    mail_conf = MailConfig.connection_config()
    asyncio.run(Mail.send_mail(message_schema, mail_conf, "user_creation_mail.html"))
    print(f"User creation mail sent successfully! on .{email}")


@shared_task()
def send_reset_password_mail(email, username, reset_password_link):
    # Logic to send the user forget password email
    temp_body = {
        'username': username,
        'alert_msg': constants.FORGET_USER_PASSWORD_ALERT_MSG,
        'reset_password_link': reset_password_link,
    }

    message_schema = MessageSchema(
        subject=constants.FORGET_USER_PASSWORD_ALERT_TITLE,
        recipients=email,
        template_body=temp_body
    )
    mail_conf = MailConfig.connection_config()
    asyncio.run(Mail.send_mail(message_schema, mail_conf, "reset_password_mail.html"))
    print(f"User's Reset Password mail sent successfully! on .{email}")
