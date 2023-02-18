from flask_restful import fields


ADDITIONAL_FIELD_RESOURCE_FIELDS = {
    "id": fields.String,
    "name": fields.String,
    "value": fields.String,
    "record_id": fields.String,
}


NOTE_RESOURCE_FIELDS = {
    "id": fields.String,
    "name": fields.String,
    "content": fields.String,
    "user_id": fields.String,
    "is_favorite": fields.Boolean,
    "is_deleted": fields.Boolean,
    "creation_time": fields.DateTime,
    "update_time": fields.DateTime,
}


RECORD_RESOURCE_FIELDS = {
    "id": fields.String,
    "name": fields.String,
    "login": fields.String,
    "password": fields.String,
    "user_id": fields.String,
    "is_favorite": fields.Boolean,
    "is_deleted": fields.Boolean,
    "creation_time": fields.DateTime,
    "update_time": fields.DateTime,
}


USER_RESOURCE_FIELDS = {
    "id": fields.String,
    "email": fields.String,
    "hint": fields.String,
}
