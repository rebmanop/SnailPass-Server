import jwt
import database
from api import app
from functools import wraps
from flask import request, jsonify



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'})

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = database.User.query.filter_by(id=data['id']).first()

        except: 
            return jsonify({'message': 'Token is invalid!'})

        return f(current_user, *args, **kwargs)

    return decorated

        

