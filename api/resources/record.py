import models
import datetime
from models import db
from flask import current_app
from api.validator import Validator
from api.access_restrictions import token_required
from flask_restful import Resource, marshal, reqparse
from flask_restful import Resource, reqparse, request
from api.resource_fields import RECORD_RESOURCE_FIELDS
from api.core import MISSING_ARGUMENT_RESPONSE, create_successful_response
from api.errors import APIResourceAlreadyExistsError, APIResourceNotFoundError, APIAccessDeniedError, APIMissingParameterError


class Record(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        
        self.parser.add_argument("id", 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)
        
        self.parser.add_argument("name", 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.parser.add_argument("login", 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE,
                                required=True, 
                                nullable=False)

        self.parser.add_argument("password", 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.parser.add_argument("is_favorite", 
                                type=bool, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.parser.add_argument("is_deleted", 
                                type=bool, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)
        
        self.validator = Validator(not_encrypted_args=["id", "is_favorite", "is_deleted"])


    @token_required
    def post(self, current_user):
        """Create new record"""
        
        args = self.parser.parse_args()
        self.validator.validate_args(args)

        if db.session.query(models.Record).get(args["id"]):
            raise APIResourceAlreadyExistsError("Record with this id already exists")
                
        record = models.Record(id=args["id"], name=args["name"], login=args["login"], 
                                password=args["password"], user_id=current_user.id, creation_time=datetime.datetime.now(), 
                                update_time=datetime.datetime.now(), is_favorite=args["is_favorite"], is_deleted=args["is_deleted"])

        db.session.add(record)
        db.session.commit()

        current_app.logger.debug(f"Record created successfully: {record}")
        return create_successful_response("Record created", 201)
        


    @token_required
    def patch(self, current_user):
        """Edit existing record"""
        
        args = self.parser.parse_args()
        self.validator.validate_args()

        record = db.session.query(models.Record).get(args["id"])

        if not record:
            raise APIResourceNotFoundError("Record with that id doesn't exist")
        
        if current_user.id != record.user_id:
            raise APIAccessDeniedError("Record with that id doesn't belong to the current user")

        record.name = args["name"]
        record.login = args["login"]
        record.password = args["password"]
        record.is_favorite = args["is_favorite"]
        record.is_deleted = args["is_deleted"]
        record.update_time = datetime.datetime.now()
        
        db.session.commit()
        current_app.logger.debug(f"Record changed successfully: {record}")
        return create_successful_response("Changes for the record were successfully made", 200)

    
    @token_required
    def delete(self, current_user):
        "Delete record"

        record_id = request.args.get("id")

        if not record_id:
            raise APIMissingParameterError("Record id is missing in uri args")

        record = db.session.query(models.Record).get(record_id)

        if not record:
            raise APIResourceNotFoundError("Record with that id doesn't exist")

        if current_user.id != record.user_id:
            raise APIAccessDeniedError("Record with that id doesn't belong to the current user")

        
        db.session.delete(record)
        db.session.commit()
        
        current_app.logger.debug(f"Record deleted successfully: {record}")
        return create_successful_response("Record deleted successfully", 200)


    @token_required
    def get(self, current_user):

        """Get user records"""

        if len(current_user.records) == 0:
            current_app.logger.debug(f"Current user {current_user} has no records")
            raise APIResourceNotFoundError("Current user has no records")
        else:
            current_app.logger.debug("Current user's records return")
            return [marshal(record, RECORD_RESOURCE_FIELDS) for record in current_user.records], 200
            

        
