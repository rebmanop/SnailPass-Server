import api
import jwt
import models
import datetime
import hashing
from flask import Blueprint
from flask import request, make_response, jsonify


login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login')
def login():
    """Login procedure"""
    """Returns authorization token if login is approved"""

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response({'message': f"Authorization info missing or it's incomplete"}, 400)

    user = models.User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response({'message': f"User with recieved email '{auth.username}' doesn't exist"}, 401) 


    if user.master_password_hash == hashing.hash_mp_additionally(auth.password, auth.username):
        data = {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=api.TOKEN_TTL)}
        token = jwt.encode(payload=data, key=api.app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})


    return  make_response({'message': 'Incorrect password'}, 401)

    




    