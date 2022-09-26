import database
from api import db  
from flask_restful import Resource, reqparse


class User(Resource):
    
    def post(self):
        """Sign up procedure"""

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="User id is required", required=True)
        parser.add_argument("login", type=str, help="Login is required", required=True)
        parser.add_argument("master_password_hash", type=str, help="Master password hash is required", required=True)
        parser.add_argument("hint", type=str)
        args = parser.parse_args()

        new_user = database.User(id=args["id"], login=args["login"], 
                                master_password_hash=args["master_password_hash"], hint=args["hint"])
        
        db.session.add(new_user)
        db.session.commit()

        return 201 


    def get(self):
        """Log in procedure"""

        parser = reqparse.RequestParser()
        parser.add_argument("login", type=str, help="Login is required", required=True)
        parser.add_argument("master_password_hash", type=str, help="Master password hash is required", required=True)
        args = parser.parse_args()

        records = database.User.query.filter_by(login=args["login"]).all()

        return records, 200










