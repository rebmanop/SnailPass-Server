import jwt
import datetime
from api.models import db
import api.models as models
from flask import flash, current_app
from api import EMAIL_CONFIRMATION_TTL
from flask import Blueprint, current_app, render_template, url_for
from api.mail import send_email_async
from email_validator import validate_email, EmailNotValidError
from api.errors import APIUnprocessableEntityError
from threading import Thread


email_confirmation_blueprint = Blueprint("email_confirmation", __name__)


@email_confirmation_blueprint.route("/confirm/<token>")
def confirm_email(token: str):
    try:
        user = verify_confirmation_token(token)
    except jwt.ExpiredSignatureError:
        return render_template("email_confirmation_link_has_expired.html")
    except TypeError:
        return render_template("user_does_not_exists.html")
    except:
        return render_template("email_confirmation_link_is_invalid.html")

    if user.email_confirmed:
        return render_template("email_already_confirmed.html")
    else:
        user.email_confirmed = True
        db.session.add(user)
        db.session.commit()
        return render_template("email_confirmation_success.html")


def generate_confirmation_token(user: models.User) -> str:
    data = {
        "id": user.id,
        "email": user.email,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=EMAIL_CONFIRMATION_TTL),
    }
    token = jwt.encode(
        payload=data,
        key=current_app.config["SECRET_KEY"],
        algorithm="HS256",
    )

    return token


def verify_confirmation_token(token: str) -> models.User:
    data = jwt.decode(token, key=current_app.config["SECRET_KEY"], algorithms=["HS256"])
    user = db.session.query(models.User).get(data["id"])
    if not user:
        raise TypeError
    return user


def send_email_confirmation_letter(recipient: models.User) -> None:
    token = generate_confirmation_token(recipient)
    confirm_url = url_for(
        "email_confirmation.confirm_email", token=token, _external=True
    )
    html = render_template("email_confirmation_letter.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    try:
        validate_email(recipient.email)
    except EmailNotValidError:
        raise APIUnprocessableEntityError(
            "Error while sending an email. The recipient address is not valid"
        )

    Thread(target=send_email_async, args=(recipient.email, subject, html)).start()
