import api.models as models
import datetime
from api.models import db
import api.errors as err
from nameof import nameof
from flask import current_app
from api.validator import Validator
from api.access_restrictions import token_required
from flask_restful import Resource, marshal, reqparse
from flask_restful import Resource, reqparse, request
from api.resource_fields import RECORD_RESOURCE_FIELDS, ADDITIONAL_FIELD_RESOURCE_FIELDS
from api.core import MISSING_ARGUMENT_RESPONSE, create_successful_response


class Record(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument(
            nameof(models.Record.id),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.Record.name),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.Record.login),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.Record.password),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.Record.is_favorite),
            type=bool,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.Record.is_deleted),
            type=bool,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.validator = Validator(
            not_encrypted_args=[
                nameof(models.Record.id),
                nameof(models.Record.is_favorite),
                nameof(models.Record.is_deleted),
            ]
        )

    @token_required
    def post(self, current_user):
        """Create new record"""

        args = self.parser.parse_args()
        self.validator.validate_args(args)

        if db.session.query(models.Record).get(args[nameof(models.Record.id)]):
            raise err.APIResourceAlreadyExistsError(
                f"Record with id {args[nameof(models.Record.id)]} already exists"
            )

        record = models.Record(
            id=args[nameof(models.Record.id)],
            name=args[nameof(models.Record.name)],
            login=args[nameof(models.Record.login)],
            password=args[nameof(models.Record.password)],
            is_favorite=args[nameof(models.Record.is_favorite)],
            is_deleted=args[nameof(models.Record.is_deleted)],
            creation_time=datetime.datetime.utcnow(),
            update_time=datetime.datetime.utcnow(),
            user_id=current_user.id,
        )

        db.session.add(record)
        db.session.commit()

        return create_successful_response(f"Record {record.id} created", 201)

    @token_required
    def put(self, current_user):
        """Edit existing record"""

        args = self.parser.parse_args()
        self.validator.validate_args(args)

        record = db.session.query(models.Record).get(args[nameof(models.Record.id)])

        if not record:
            raise err.APIResourceNotFoundError(
                f"Record with id {args[nameof(models.Record.id)]} doesn't exist"
            )

        if current_user.id != record.user_id:
            raise err.APIAccessDeniedError(
                f"Record {record.id} doesn't belong to the current user {current_user.id}"
            )

        record.name = args[nameof(models.Record.name)]
        record.login = args[nameof(models.Record.login)]
        record.password = args[nameof(models.Record.password)]
        record.is_favorite = args[nameof(models.Record.is_favorite)]
        record.is_deleted = args[nameof(models.Record.is_deleted)]
        record.update_time = datetime.datetime.utcnow()

        db.session.commit()
        return create_successful_response(
            f"Record {record.id} changed successfully", 200
        )

    @token_required
    def delete(self, current_user):
        "Delete record"

        record_id = request.args.get(nameof(models.Record.id))

        if not record_id:
            raise err.APIMissingParameterError(f"Record id is missing in URI arguments")

        record = db.session.query(models.Record).get(record_id)

        if not record:
            raise err.APIResourceNotFoundError(
                f"Record with id {record_id} doesn't exist"
            )

        if current_user.id != record.user_id:
            raise err.APIAccessDeniedError(
                f"Record {record.id} doesn't belong to the current user {current_user.id}"
            )

        if record.is_deleted == False:
            record.is_deleted = True
            db.session.commit()
            return create_successful_response(
                f"Record {record.id} successfully marked as deleted", 200
            )
        else:
            db.session.delete(record)
            db.session.commit()
            return create_successful_response(
                f"Record {record.id} successfully permanently deleted", 200
            )

    @token_required
    def get(self, current_user):
        """
        Get user records with corresponding additional fields
        """

        if len(current_user.records) == 0:
            raise err.APIResourceNotFoundError(
                f"Current user {current_user.id} has no records"
            )
        else:
            serialized_records = [
                marshal(record, RECORD_RESOURCE_FIELDS)
                for record in current_user.records
            ]
            for record, serialized_record in zip(
                current_user.records, serialized_records
            ):
                serialized_record[nameof(models.Record.additional_fields)] = [
                    marshal(additional_field, ADDITIONAL_FIELD_RESOURCE_FIELDS)
                    for additional_field in record.additional_fields
                ]
            return serialized_records, 200
