import jwt
import models
import datetime
from flask import Blueprint
from api import app, TOKEN_TTL
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

    received_password_hash = auth.password
    
    if user.master_password_hash == received_password_hash:
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(TOKEN_TTL)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode("UTF-8")})


    return  make_response({'message': 'Incorrect password'}, 401)

    




    