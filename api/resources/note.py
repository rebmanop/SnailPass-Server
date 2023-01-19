import models
import datetime
from models import db
from api.access_restrictions import token_required
from api.resource_fields import NOTE_RESOURCE_FIELDS
from flask_restful import Resource, reqparse, request
from flask_restful import Resource, marshal, reqparse


class Note(Resource):
    @token_required
    def post(self, current_user):
        
        """Create new note"""

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Record id is missing", required=True)
        parser.add_argument("name", type=str, help="Record name is missing", required=True)
        parser.add_argument("content", type=str, help="Record content is missing", required=True)
        parser.add_argument("nonce", type=str, help="Nonce is missing", required=True)
        args = parser.parse_args()


        if models.Note.query.get(args["id"]):
            return {"message": f"Note with id '{args['id']}' already exist"}, 409
        elif models.Note.query.filter_by(user_id=current_user.id, name=args["name"]).all():
            return {"message": f"Note with name '{args['name']}' already exist in current user's vault"}, 409


        note = models.Note(id=args["id"], name=args["name"], content=args["content"], user_id=current_user.id, creation_time=datetime.datetime.now(), 
                                update_time=datetime.datetime.now(), nonce=args["nonce"])

                                
        db.session.add(note)
        db.session.commit()
        return {"message": f"Note '{args['name']}' created successfully (user = '{current_user.email}')"}, 201


    @token_required
    def patch(self, current_user):

        """Edit existing note"""
        
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Note id is missing", required=True)
        parser.add_argument("name", type=str, help="Note name is missing", required=True)
        parser.add_argument("content", type=str, help="Note content is missing", required=True)
        parser.add_argument("is_favorite", type=bool, help="Note 'is_favorite' status is missing", required=True)
        parser.add_argument("is_deleted", type=bool, help="Note 'is_deleted' status is missing", required=True)
        parser.add_argument("nonce", type=str, help="Note nonce is missing", required=True)
        args = parser.parse_args()

        note = models.Note.query.get(args["id"])

        if not note:
            return {"message": f"Note with id '{args['id']}' doesn't exist "}, 404
        
        if current_user.id != note.user_id:
            return {"message": f"Note with id '{note.id}' doesn't belong to the current user"}, 403


        if db.session.query(models.Note).filter(models.Note.id != args["id"],models.Note.name == args["name"]).first():
            return {"message": f"Note with name '{args['name']}' already exists in current user's vault"}, 409

        note.name = args["name"]
        note.content = args["content"]
        note.nonce = args["nonce"]
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

        note = models.Note.query.get(note_id)

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

        notes = models.Note.query.filter_by(user_id=current_user.id).all()

        if len(notes) == 0:
            return {"message": f"User '{current_user.email}' has no notes"}, 404

        
        return [marshal(note, NOTE_RESOURCE_FIELDS) for note in notes], 200

