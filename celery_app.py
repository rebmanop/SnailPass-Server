import os
import smtplib, ssl
from celery import Celery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


celery_app = Celery("snailpass-server-celery")


class ProductionConfig:
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")


celery_app.config_from_object(ProductionConfig)


smtp_client = smtplib.SMTP_SSL(
    host=celery_app.conf.get("MAIL_SERVER"),
    port=celery_app.conf.get("MAIL_PORT"),
    context=ssl.create_default_context(),
)

smtp_client.login(
    user=celery_app.conf.get("MAIL_USERNAME"),
    password=celery_app.conf.get("MAIL_PASSWORD"),
)


@celery_app.task
def send_email(recipient_email: str, subject: str, html: str) -> None:
    message = MIMEMultipart()

    message["From"] = celery_app.conf.get("MAIL_DEFAULT_SENDER")
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(html, "html"))

    smtp_client.send_message(message)
