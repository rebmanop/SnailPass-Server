import jwt
import models
import hashing
import datetime
from models import db
from api import TOKEN_TTL
from flask import request, jsonify
from api.errors import APIAuthError
from flask import Blueprint, current_app


login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login")
def login():
    """
    Authentication procedure. Returns session token if authentication is successful
    """

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        raise APIAuthError(f"Authentication info missing or it's incomplete")

    user = db.session.query(models.User).filter_by(email=auth.username).first()

    if not user or (
        user.master_password_hash
        != hashing.hash_mp_additionally(auth.password, auth.username)
    ):
        raise APIAuthError("Incorrect credentials")

    data = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_TTL),
    }
    token = jwt.encode(
        payload=data, key=current_app.config["SECRET_KEY"], algorithm="HS256"
    )
    return jsonify({"token": token})
