import models
import datetime
from models import db
import api.errors as err
from nameof import nameof
from api.validator import Validator
from api.core import create_successful_response
from api.access_restrictions import token_required
from api.resource_fields import NOTE_RESOURCE_FIELDS
from flask_restful import Resource, reqparse, request
from flask_restful import Resource, marshal, reqparse
from api.core import MISSING_ARGUMENT_RESPONSE


class Note(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        
        self.parser.add_argument(nameof(models.Note.id), 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.parser.add_argument(nameof(models.Note.name), 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.parser.add_argument(nameof(models.Note.content), 
                                type=str, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.parser.add_argument(nameof(models.Note.is_favorite), 
                                type=bool, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.parser.add_argument(nameof(models.Note.is_deleted), 
                                type=bool, 
                                help=MISSING_ARGUMENT_RESPONSE, 
                                required=True, 
                                nullable=False)

        self.validator = Validator(not_encrypted_args=[nameof(models.Note.id), 
                                               nameof(models.Note.is_favorite), 
                                               nameof(models.Note.is_deleted)])

        self.class_name = {self.__class__.__name__}
        
        

    @token_required
    def post(self, current_user):
        """Create new note"""

        args = self.parser.parse_args()
        self.validator.validate_args(args)

        if db.session.query(models.Note).get(args[nameof(models.Note.id)]):
            raise err.APIResourceAlreadyExistsError(f"Note with id {args[nameof(models.Note.id)]} already exists")

        note = models.Note(id=args[nameof(models.Note.id)], 
                           name=args[nameof(models.Note.name)], 
                           content=args[nameof(models.Note.name)], 
                           user_id=current_user.id, 
                           creation_time=datetime.datetime.utcnow(), 
                           update_time=datetime.datetime.utcnow(),
                           is_favorite=args[nameof(models.Note.is_favorite)],
                           is_deleted=args[nameof(models.Note.is_deleted)])
                                 
        db.session.add(note)
        db.session.commit()
        return create_successful_response(f"Note {note.id} created", 201)


    @token_required
    def put(self, current_user):
        """Edit existing note"""
        
        args = self.parser.parse_args()
        self.validator.validate_args(args)

        note = db.session.query(models.Note).get(args[nameof(models.Note.id)])

        if not note:
            raise err.APIResourceNotFoundError(f"Note with id {args[nameof(models.Note.id)]} doesn't exist")
        
        if current_user.id != note.user_id:
            raise err.APIAccessDeniedError(f"Note {note.id} doesn't belong to the current user {current_user.id}")


        note.name = args[nameof(models.Note.name)]
        note.content = args[nameof(models.Note.content)]
        note.is_favorite = args[nameof(models.Note.is_favorite)]
        note.is_deleted = args[nameof(models.Note.is_deleted)]
        note.update_time = datetime.datetime.utcnow()

        db.session.commit()
     
        return create_successful_response(f"Note {note.id} changed successfully", 200)
       
    
    @token_required
    def delete(self, current_user):
        "Delete note"
        
        note_id = request.args.get(nameof(models.Note.id))

        if not note_id:
            raise err.APIMissingParameterError(f"Note id is missing in URI arguments")

        note = db.session.query(models.Note).get(note_id)

        if not note:
            raise err.APIResourceNotFoundError(f"Note with id {note_id} doesn't exist")

        if current_user.id != note.user_id:
            raise err.APIAccessDeniedError(f"Note {note.id} doesn't belong to the current user {current_user.id}")

        
        db.session.delete(note)
        db.session.commit()

        return create_successful_response(f"Note {note.id} deleted successfully", 200)


    @token_required
    def get(self, current_user):

        """Get user notes"""

        if len(current_user.notes) == 0:
            raise err.APIResourceNotFoundError(f"Current user {current_user.id} has no notes")
        else:
            return [marshal(note, NOTE_RESOURCE_FIELDS) for note in current_user.notes], 200


        

