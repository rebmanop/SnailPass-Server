from flask_mail import Mail, Message

mail = Mail()

from api import celery


@celery.task
def send_email(to: str, subject: str, template: str, sender: str) -> None:
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=sender,
    )
    mail.send(msg)
