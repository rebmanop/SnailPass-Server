import uuid
import hashlib
import models
from api import db  
from api.access_restrictions import admin_only_function
from flask_restful import Resource, reqparse, request, fields, marshal_with


user_resource_fields = {
                        'id': fields.String, 
                        'login': fields.String,
                        'master_password_hash': fields.String,
                        'is_admin': fields.Boolean
                       }


class User(Resource):
    
    def post(self):
        """Signup procedure"""

        parser = reqparse.RequestParser()

        parser.add_argument("id", type=str, help="User id is required", required=True)
        parser.add_argument("login", type=str, help="Login is required", required=True)
        parser.add_argument("master_password_hash", type=str, help="Master password hash is required", required=True)
        parser.add_argument("hint", type=str)
        args = parser.parse_args()

        new_user = models.User(id=args["id"], login=args["login"], 
                                 master_password_hash=args["master_password_hash"], hint=args["hint"])

        # parser.add_argument("login", type=str, help="Login is required", required=True)
        # parser.add_argument("hint", type=str)
        # args = parser.parse_args()
        # new_user = models.User(id=str(uuid.uuid4()), login=args["login"], 
        #                          master_password_hash=(hashlib.sha512(str(uuid.uuid4()).encode())).hexdigest(), hint=args["hint"])
        
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201 

    
    @admin_only_function
    def delete(self): 
        """Delete user (admin only function)"""
        
        user_id = request.args.get("id")
        user = models.User.query.get(user_id)
        
        if not user:
            return {"message": "User with that id doesn't exist"}, 404

        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted successfully"}, 200


    @admin_only_function
    @marshal_with(user_resource_fields)
    def get(self):
        
        "Returns  all users"
        users = models.User.query.all()

        if len(users) == 0:
            return {"message: No users in the database"}, 404

        return users, 200



        













