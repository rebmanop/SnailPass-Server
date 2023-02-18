import jwt
import api
import models
import datetime
from flask import current_app
import secrets
from hashlib import sha1
from uuid import uuid4
from models import db
from hashing import hash_mp_additionally
from nameof import nameof


MOCK_ENCRYPTED_DATA = "9EVyUnWNQDH6vHHLE6yJMw==:yfNpDOxbKqTLVoggLnWNIw=="


def add_new_user_to_mock_db(new_user: dict) -> None:
    """
    Adds new_user to mock db for tests
    """
    additionaly_hashed_mp = hash_mp_additionally(
        password_hash=new_user[nameof(models.User.master_password_hash)],
        salt=new_user[nameof(models.User.email)],
    )

    new_user_model = models.User(
        id=new_user[nameof(models.User.id)],
        email=new_user[nameof(models.User.email)],
        master_password_hash=additionaly_hashed_mp,
        hint=new_user[nameof(models.User.hint)],
    )
    db.session.add(new_user_model)
    db.session.commit()


def add_new_record_to_mock_db(new_user: dict, new_record: dict) -> None:
    """
    Adds new_record to mock db for tests
    """

    new_record_model = models.Record(
        id=new_record[nameof(models.Record.id)],
        name=new_record[nameof(models.Record.name)],
        login=new_record[nameof(models.Record.login)],
        password=new_record[nameof(models.Record.password)],
        user_id=new_user[nameof(models.User.id)],
        creation_time=datetime.datetime.utcnow(),
        update_time=datetime.datetime.utcnow(),
        is_favorite=new_record[nameof(models.Record.is_favorite)],
        is_deleted=new_record[nameof(models.Record.is_deleted)],
    )

    db.session.add(new_record_model)
    db.session.commit()


def add_new_note_to_mock_db(new_user: dict, new_note: dict) -> None:
    """
    Adds new_note to mock db for tests
    """

    new_note_model = models.Note(
        id=new_note[nameof(models.Note.id)],
        name=new_note[nameof(models.Note.name)],
        content=new_note[nameof(models.Note.content)],
        user_id=new_user[nameof(models.User.id)],
        creation_time=datetime.datetime.utcnow(),
        update_time=datetime.datetime.utcnow(),
        is_favorite=new_note[nameof(models.Note.is_favorite)],
        is_deleted=new_note[nameof(models.Note.is_deleted)],
    )

    db.session.add(new_note_model)
    db.session.commit()


def add_new_additional_field_to_mock_db(
    new_record: dict, new_additional_field: dict
) -> None:
    """
    Adds new_note to mock db for tests
    """

    new_additional_field_model = models.AdditionalField(
        id=new_additional_field[nameof(models.AdditionalField.id)],
        name=new_additional_field[nameof(models.AdditionalField.name)],
        value=new_additional_field[nameof(models.AdditionalField.value)],
        record_id=new_record[nameof(models.Record.id)],
    )

    db.session.add(new_additional_field_model)
    db.session.commit()


def get_mock_token(new_user: dict, token_ttl_minutes=api.TOKEN_TTL):
    """
    Mocks new_user's auth token for tests
    """
    data = {
        "id": new_user[nameof(models.User.id)],
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=token_ttl_minutes),
    }
    token = jwt.encode(
        payload=data, key=current_app.config["SECRET_KEY"], algorithm="HS256"
    )
    return token


# -------------GENERATES NEW MOCK DATA FOR TESTS-----------------------------

words = []

with open("tests/mockdata/wordlist.txt") as file:
    while line := file.readline().rstrip():
        words.append(line)


def get_random_word():
    return secrets.choice(words)


def get_random_email():
    return f"{get_random_word()}@gmail.com"


def get_random_word_hash():
    return sha1((secrets.choice(words)).encode()).hexdigest()


def get_random_id():
    return str(uuid4())
