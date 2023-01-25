import jwt
import api
import models
from functools import wraps
from models import db
from flask import request, make_response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response({'message': 'Token is missing'}, 400)

        try: 
            data = jwt.decode(token, key=api.app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.session.query(models.User).get(data['id'])

        except(jwt.ExpiredSignatureError): 
            return make_response({'message': 'Token already expired'}, 401)
        
        except:
            return make_response({'message': 'Token is invalid'}, 401)

        return f(*args, current_user, **kwargs)

    return decorated


def admin_only_function(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return make_response({'message': 'Token is missing'}, 400)
        
        try: 
            data = jwt.decode(token, key=api.app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.session.query(models.User).get(data['id'])

        except(jwt.ExpiredSignatureError): 
            return make_response({'message': 'Token already expired'}, 401)

        except:
            return make_response({'message': 'Token is invalid'}, 401)

        if not current_user.is_admin:
            return make_response({'message': 'Admin only function'}, 403)

        return f(*args, **kwargs)

    return decorated
        

        

