import models
import hashing
from models import db
from api.access_restrictions import token_required
from flask_restful import Resource, reqparse, request, fields, marshal
from api.resource_fields import USER_RESOURCE_FIELDS
from api.core import  MISSING_PARAMETER_RESPONSE


class User(Resource):
    def post(self):
        """Signup procedure"""

        parser = reqparse.RequestParser()

        parser.add_argument("id", type=str, help="User id" + MISSING_PARAMETER_RESPONSE, required=True, nullable=False)
        parser.add_argument("email", type=str, help="User email is missing at all, value is null or value is empty", required=True, nullable=False)
        parser.add_argument("master_password_hash", type=str, help="User's master password hash is missing at all, value is null or value is empty", required=True, nullable=False)
        parser.add_argument("hint", type=str, nullable=False)
        args = parser.parse_args()

        additionaly_hashed_master_password = hashing.hash_mp_additionally(password_hash=args["master_password_hash"], 
                                                salt=args["email"])

        if db.session.query(models.User).get(args["id"]):
            return {"message": f"User with received id '{args['id']}' already exists"}, 409
        elif db.session.query(models.User).filter_by(email=args["email"]).all():
            return {"message": f"User with received email '{args['email']}' already exists"}, 409

        new_user = models.User(id=args["id"], email=args["email"], 
                                master_password_hash=additionaly_hashed_master_password, hint=args["hint"])
        
        db.session.add(new_user)
        db.session.commit()

        return {"message": f"User '{new_user.email}' created successfully"}, 201 


    @token_required
    def get(self, current_user):
        """
        Returns current user
        """
        return marshal(current_user, USER_RESOURCE_FIELDS), 200



        













