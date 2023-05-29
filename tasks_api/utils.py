# utils.py
import os
from fastapi_mail import FastMail, ConnectionConfig
from dotenv import load_dotenv

load_dotenv('.env')


class MailConfig:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME')

    @staticmethod
    def connection_config():
        """
        :return: connection config object.
        """
        return ConnectionConfig(
            MAIL_USERNAME=MailConfig.MAIL_USERNAME,
            MAIL_PASSWORD=MailConfig.MAIL_PASSWORD,
            MAIL_FROM=MailConfig.MAIL_FROM,
            MAIL_PORT=MailConfig.MAIL_PORT,
            MAIL_SERVER=MailConfig.MAIL_SERVER,
            MAIL_FROM_NAME=MailConfig.MAIL_FROM_NAME,
            MAIL_TLS=True,
            MAIL_SSL=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER="./templates/email"
        )


class Mail:
    def __init__(self, mail_conf):
        self.fm = FastMail(mail_conf)

    @staticmethod
    async def send_mail(message_schema, mail_conf, template_name):
        """
        Mail send functionality.
        :param message_schema: message schema
        :param mail_conf: mail configuration
        :param template_name: template name
        :return: send the mail
        """
        mail = Mail(mail_conf)
        await mail.fm.send_message(message_schema, template_name=template_name)
