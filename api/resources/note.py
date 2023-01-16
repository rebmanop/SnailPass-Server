import models
import datetime
from models import db
from flask_restful import Resource, marshal, reqparse
from api.access_restrictions import token_required
from flask_restful import Resource, reqparse, request, fields

note_resource_fields = {
                        'id': fields.String, 
                        'name': fields.String,
                        'content': fields.String,
                        'user_id': fields.String,
                        'is_favorite': fields.Boolean,
                        'is_deleted': fields.Boolean,
                        'creation_time': fields.DateTime,
                        'update_time': fields.DateTime,
                        'nonce': fields.String
                        }


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
        parser.add_argument("name", type=str)
        parser.add_argument("content", type=str)
        args = parser.parse_args()

        note = models.Note.query.get(args["id"])

        if not note:
            return {"message": f"Note with id '{args['id']}' doesn't exist "}, 404
        
        if current_user.id != note.user_id:
            return {"message": "You dont have access rights to edit this note"}, 403

        note_changed = False

        if args["name"]:
            note.name = args["name"]
            note_changed = True

        
        if args["content"]:
            note.content = args["content"]
            note_changed = True


        if note_changed:
            note.update_time = datetime.datetime.now()
            db.session.commit()
            return {"message": f"Changes for the note '{args['id']}' were successfully made"}, 200
        else:
            return {"message": f"Changes for the note '{args['id']}' weren't made because request body is empty"}, 400 

    
    @token_required
    def delete(self, current_user):

        "Delete note"

        parser = reqparse.RequestParser()
        parser.add_argument("id", type=str, help="Note id is missing", required=True)

        args = parser.parse_args()

        note = models.Note.query.get(args["id"])

        if not note:
            return {"message": "Note with that id doesn't exist"}, 404

        if current_user.id != note.user_id:
            return {"message": "You dont have access rights to delete this record"}, 403

        
        db.session.delete(note)
        db.session.commit()

        return {"message": f"Note '{note.name}' deleted successfully (user = '{current_user.email}')"}, 200



    @token_required
    def get(self, current_user):

        """Get user notes"""

        notes = models.Note.query.filter_by(user_id=current_user.id).all()

        if len(notes) == 0:
            return {"message": f"User '{current_user.email}' has no notes"}, 404

        
        return [marshal(note, note_resource_fields) for note in notes], 200

