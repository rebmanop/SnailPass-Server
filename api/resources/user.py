import models
import hashing
from models import db
from flask import current_app
from api.validator import Validator
from api.errors import APIResourceAlreadyExistsError
from api.access_restrictions import token_required
from flask_restful import Resource, reqparse, marshal
from api.resource_fields import USER_RESOURCE_FIELDS
from api.core import  MISSING_ARGUMENT_RESPONSE, create_successful_response



class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument("id", 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.parser.add_argument("email", 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.parser.add_argument("master_password_hash", 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)
        
        self.parser.add_argument("hint", 
                                type=str, 
                                nullable=False)
        
        self.validator = Validator(all_not_encrypted=True)


    def post(self):
        """Signup procedure"""
        args = self.parser.parse_args()
        self.validator.validate_args(args)

        additionaly_hashed_master_password = hashing.hash_mp_additionally(
                                                password_hash=args["master_password_hash"], 
                                                salt=args["email"])
        
        if db.session.query(models.User).get(args["id"]):
            raise APIResourceAlreadyExistsError("User with this id already exists")
        if db.session.query(models.User).filter_by(email=args["email"]).first():
            raise APIResourceAlreadyExistsError("User with this email already exists")

        new_user = models.User(id=args["id"], email=args["email"], 
                                master_password_hash=additionaly_hashed_master_password, 
                                hint=args["hint"])
        
        db.session.add(new_user)
        db.session.commit()

        current_app.logger.debug(f"User {new_user.email} created successfully")
        return create_successful_response(message="User created successfully", status_code=201) 


    @token_required
    def get(self, current_user):
        """
        Returns current user
        """
        current_app.logger.debug(f"Current user successfully returned: {current_user}")
        return marshal(current_user, USER_RESOURCE_FIELDS), 200



        













