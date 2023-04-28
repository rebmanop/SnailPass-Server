import jwt
import api.models as models
from api.hashing import hash_mp_additionally
import datetime
from api.models import db
from api import TOKEN_TTL
from flask import request, jsonify
from api.errors import APIAuthError, APIAccessDeniedError
from flask import Blueprint, current_app, Response
from api.email_confirmation import send_email_confirmation_letter


login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login")
def login():
    """
    Authentication procedure. Returns session token if authentication is successful
    """

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        raise APIAuthError(f"Authentication info missing or it's incomplete")

    email = auth.username.lower()
    master_password = auth.password

    user = db.session.query(models.User).filter_by(email=email).first()

    if not user or (
        user.master_password_hash != hash_mp_additionally(master_password, salt=email)
    ):
        raise APIAuthError("Incorrect credentials")

    if not user.email_confirmed:
        send_email_confirmation_letter(user)
        raise APIAccessDeniedError(
            f"Email isn't confirmed. Resending email confirmation letter..."
        )

    data = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_TTL),
    }
    token = jwt.encode(
        payload=data, key=current_app.config["SECRET_KEY"], algorithm="HS256"
    )
    return jsonify({"token": token})
