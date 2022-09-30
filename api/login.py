import jwt
import database
import datetime
from api import app
from flask import Blueprint
from flask import request, make_response, jsonify


login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, 
        {'WWW-Authenticate': 'Basic realm="Login required!"'})


    user = database.User.query.filter_by(login=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, 
        {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if user.master_password_hash == auth.password:
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})


    return  make_response('Could not verify', 401, 
        {'WWW-Authenticate': 'Basic realm="Login required!"'})

    




    