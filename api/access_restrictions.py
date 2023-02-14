import jwt
import models
from functools import wraps
from models import db
from flask import request, current_app
from api.errors import APIAuthError, APIResourceNotFoundError, APIMissingRequestHeaderError


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            raise APIMissingRequestHeaderError("Token is missing in x-access-token header")

        try: 
            data = jwt.decode(token, key=current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.session.query(models.User).get(data['id'])
            if not current_user:
                raise TypeError

        except(jwt.ExpiredSignatureError): 
            raise APIAuthError("Token already expired")

        except(TypeError):
            raise APIResourceNotFoundError("Current user does not exist")
            
        except:
            raise APIAuthError("Token is invalid")

        return f(*args, current_user, **kwargs)

    return decorated

        

        

