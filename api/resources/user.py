import uuid
import hashlib
import models
import random
from api import db  
from api.access_restrictions import admin_only_function
from flask_restful import Resource, reqparse, request, fields, marshal_with


user_resource_fields = {
                        'id': fields.String, 
                        'email': fields.String,
                        'master_password_hash': fields.String,
                        'is_admin': fields.Boolean
                       }


class User(Resource):
    def post(self):
        """Signup procedure"""

        parser = reqparse.RequestParser()

        parser.add_argument("id", type=str, help="User id is required", required=True)
        parser.add_argument("email", type=str, help="Email is required", required=True)
        parser.add_argument("master_password_hash", type=str, help="Master password hash is required", required=True)
        parser.add_argument("hint", type=str)
        parser.add_argument("nonce", type=str, help="Nonce is required", required=True)
        args = parser.parse_args()

        new_user = models.User(id=args["id"], email=args["email"], 
                                 master_password_hash=args["master_password_hash"], hint=args["hint"], nonce=args["nonce"])
        
        db.session.add(new_user)
        db.session.commit()

        return {"message": f"User '{new_user.email}' created successfully"}, 201 

    
    @admin_only_function
    def delete(self): 
        """Delete user (admin only function)"""
        
        user_id = request.args.get("id")
        user = models.User.query.get(user_id)
        
        if not user:
            return {"message": "User with that id doesn't exist"}, 404

        db.session.delete(user)
        db.session.commit()

        return {"message": f"User '{user.email}' deleted successfully"}, 200


    @admin_only_function
    @marshal_with(user_resource_fields)
    def get(self):
        
        "Returns  all users"
        users = models.User.query.all()

        if len(users) == 0:
            return {"message: No users in the database"}, 404

        return users, 200



        













