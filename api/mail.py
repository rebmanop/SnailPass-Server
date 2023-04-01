from flask_mail import Mail, Message

mail = Mail()

from api import celery


@celery.task
def send_email(to, subject, template, sender):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=sender,
    )
    mail.send(msg)
