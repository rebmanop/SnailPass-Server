import models
import hashing
from models import db
from nameof import nameof
from flask import current_app
from api.validator import Validator
from api.errors import APIResourceAlreadyExistsError
from api.access_restrictions import token_required
from flask_restful import Resource, reqparse, marshal
from api.resource_fields import USER_RESOURCE_FIELDS
from api.core import MISSING_ARGUMENT_RESPONSE, create_successful_response


class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument(
            nameof(models.User.id),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.User.email),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(
            nameof(models.User.master_password_hash),
            type=str,
            help=MISSING_ARGUMENT_RESPONSE,
            required=True,
            nullable=False,
        )

        self.parser.add_argument(nameof(models.User.hint), type=str, nullable=False)

        self.validator = Validator(all_not_encrypted=True)

    def post(self):
        """Signup procedure"""
        args = self.parser.parse_args()
        self.validator.validate_args(args)

        additionaly_hashed_master_password = hashing.hash_mp_additionally(
            password_hash=args[nameof(models.User.master_password_hash)],
            salt=args[nameof(models.User.email)],
        )

        if db.session.query(models.User).get(args[nameof(models.User.id)]):
            raise APIResourceAlreadyExistsError(
                f"User with id {args[nameof(models.User.id)]} already exists"
            )

        if (
            db.session.query(models.User)
            .filter_by(email=args[nameof(models.User.email)])
            .first()
        ):
            raise APIResourceAlreadyExistsError(f"User with this email already exists")

        new_user = models.User(
            id=args[nameof(models.User.id)],
            email=args[nameof(models.User.email)],
            master_password_hash=additionaly_hashed_master_password,
            hint=args[nameof(models.User.hint)],
        )

        db.session.add(new_user)
        db.session.commit()

        return create_successful_response(
            f"User created successfully {new_user.id}", 201
        )

    @token_required
    def get(self, current_user):
        """
        Returns current user
        """
        return marshal(current_user, USER_RESOURCE_FIELDS), 200
