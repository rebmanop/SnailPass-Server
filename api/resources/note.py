import models
import datetime
from models import db
from api.access_restrictions import token_required
from api.resource_fields import NOTE_RESOURCE_FIELDS
from flask_restful import Resource, reqparse, request
from flask_restful import Resource, marshal, reqparse
from api.core import MISSING_PARAMETER_RESPONSE


class Note(Resource):
    @token_required
    def post(self, current_user):
        
        """Create new note"""

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Record id" + MISSING_PARAMETER_RESPONSE, required=True, nullable=False)
        parser.add_argument("name", type=str, help="Record name" + MISSING_PARAMETER_RESPONSE, required=True, nullable=False)
        parser.add_argument("content", type=str, help="Record content" + MISSING_PARAMETER_RESPONSE, required=True, nullable=False)
        args = parser.parse_args()


        if db.session.query(models.Note).get(args["id"]):
            return {"message": f"Note with id '{args['id']}' already exist"}, 409
        elif db.session.query(models.Note).filter_by(user_id=current_user.id, name=args["name"]).all():
            return {"message": f"Note with name '{args['name']}' already exist in current user's vault"}, 409


        note = models.Note(id=args["id"], name=args["name"], content=args["content"], user_id=current_user.id, creation_time=datetime.datetime.now(), 
                                update_time=datetime.datetime.now())

                                
        db.session.add(note)
        db.session.commit()
        return {"message": f"Note '{args['name']}' created successfully (user = '{current_user.email}')"}, 201


    @token_required
    def patch(self, current_user):

        """Edit existing note"""
        
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Note id" + MISSING_PARAMETER_RESPONSE, required=True, nullable=False)
        parser.add_argument("name", type=str, help="Note name" + MISSING_PARAMETER_RESPONSE, required=True, nullable=False)
        parser.add_argument("content", type=str, help="Note content" + MISSING_PARAMETER_RESPONSE, required=True, nullable=False)
        parser.add_argument("is_favorite", type=bool, help="Note 'is_favorite' status" + MISSING_PARAMETER_RESPONSE, required=True, nullable=False)
        parser.add_argument("is_deleted", type=bool, help="Note 'is_deleted' status" + MISSING_PARAMETER_RESPONSE, required=True, nullable=False)
        args = parser.parse_args()

        note = db.session.query(models.Note).get(args["id"])

        if not note:
            return {"message": f"Note with id '{args['id']}' doesn't exist "}, 404
        
        if current_user.id != note.user_id:
            return {"message": f"Note with id '{note.id}' doesn't belong to the current user"}, 403


        if db.session.query(models.Note).filter(models.Note.id != args["id"],models.Note.name == args["name"]).first():
            return {"message": f"Note with name '{args['name']}' already exists in current user's vault"}, 409

        note.name = args["name"]
        note.content = args["content"]
        note.is_favorite = args["is_favorite"]
        note.is_deleted = args["is_deleted"]
        note.update_time = datetime.datetime.now()

        db.session.commit()
     
        return {"message": f"Changes for the note '{args['id']}' were successfully made"}, 200
       
    
    @token_required
    def delete(self, current_user):

        "Delete note"

        note_id = request.args.get("id")

        if not note_id:
            return {"message": f"Note id is missing in uri args"}, 400

        note = db.session.query(models.Note).get(note_id)

        if not note:
            return {"message": "Note with that id doesn't exist"}, 404

        if current_user.id != note.user_id:
            return {"message": f"Note with id '{note.id}' doesn't belong to the current user"}, 403

        
        db.session.delete(note)
        db.session.commit()

        return {"message": f"Note '{note.name}' deleted successfully (user = '{current_user.email}')"}, 200


    @token_required
    def get(self, current_user):

        """Get user notes"""

        if len(current_user.notes) == 0:
            return {"message": f"User '{current_user.email}' has no notes"}, 404
        else:
            return [marshal(note, NOTE_RESOURCE_FIELDS) for note in current_user.notes], 200


        

