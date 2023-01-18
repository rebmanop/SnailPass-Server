import models
import hashing
from models import db
from api.access_restrictions import admin_only_function, token_required
from flask_restful import Resource, reqparse, request, fields, marshal
from api.resource_fields import USER_RESOURCE_FIELDS




class User(Resource):
    def post(self):
        """Signup procedure"""

        parser = reqparse.RequestParser()

        parser.add_argument("id", type=str, help="User id is missing", required=True)
        parser.add_argument("email", type=str, help="Email is missing", required=True)
        parser.add_argument("master_password_hash", type=str, help="Master password hash is missing", required=True)
        parser.add_argument("hint", type=str)
        args = parser.parse_args()

        additionaly_hashed_master_password = hashing.hash_mp_additionally(password_hash=args["master_password_hash"], 
                                                salt=args["email"])

        if models.User.query.get(args["id"]):
            return {"message": f"User with received id '{args['id']}' already exists"}, 409
        elif models.User.query.filter_by(email=args["email"]).all():
            return {"message": f"User with received email '{args['email']}' already exists"}, 409

        new_user = models.User(id=args["id"], email=args["email"], 
                                master_password_hash=additionaly_hashed_master_password, hint=args["hint"])
        
        db.session.add(new_user)
        db.session.commit()

        return {"message": f"User '{new_user.email}' created successfully"}, 201 

    
    @admin_only_function
    def delete(self): 
        """Delete user (admin only function)"""
           
        user_id = request.args.get("id")
        
        if not user_id:
            return {"message": "User id not found in the url params"}, 400

        
        user = models.User.query.get(user_id)
        
        if not user:
            return {"message": "User with that id doesn't exist"}, 404


        db.session.delete(user)
        db.session.commit()

        return {"message": f"User '{user.email}' deleted successfully"}, 200


    @token_required
    def get(self, current_user):
        
        "Returns current user"
        user = models.User.query.get(current_user.id)

        if not user:
            return {"message": f"Current user wasn't found in the database"}, 404

        return marshal(user, USER_RESOURCE_FIELDS), 200



        













