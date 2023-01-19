import jwt
import api
import models
import datetime
import secrets
import requests
from hashlib import sha1
from uuid import uuid4
from models import db
from hashing import hash_mp_additionally


def add_new_user_to_mock_db(new_user, is_admin=False):
    """
    Adds new_user to mock db for tests
    """
    additionaly_hashed_mp = hash_mp_additionally(password_hash=new_user["master_password_hash"], 
                                                    salt=new_user["email"])

    
    new_user_db_model_object = models.User(id=new_user["id"], email=new_user["email"], 
                                master_password_hash=additionaly_hashed_mp, hint=new_user["hint"], is_admin=is_admin)
    db.session.add(new_user_db_model_object)
    db.session.commit()


def add_new_record_to_mock_db(new_user, new_record):
    """
    Adds new_record to mock db for tests
    """
    
    new_record_db_model_object = models.Record(id=new_record["id"], name=new_record["name"], login=new_record["login"], 
                                encrypted_password=new_record["encrypted_password"], user_id=new_user["id"], creation_time=datetime.datetime.now(), 
                                update_time=datetime.datetime.now(), nonce=new_record["nonce"])
    
    db.session.add(new_record_db_model_object)
    db.session.commit()


def add_new_note_to_mock_db(new_user, new_note):
    """
    Adds new_note to mock db for tests
    """
    
    new_note_db_model_object = models.Note(id=new_note["id"], name=new_note["name"], content=new_note["content"], user_id=new_user["id"], creation_time=datetime.datetime.now(), 
                                update_time=datetime.datetime.now(), nonce=new_note["nonce"])
    
    db.session.add(new_note_db_model_object)
    db.session.commit()


def add_new_additional_field_to_mock_db(new_record, new_additional_field):
    """
    Adds new_note to mock db for tests
    """
    
    new_additional_field_db_model_object = models.AdditionalField(id=new_additional_field["id"], field_name=new_additional_field["field_name"], value=new_additional_field["value"], 
                                record_id=new_record["id"], nonce=new_additional_field["nonce"])
    
    db.session.add(new_additional_field_db_model_object)
    db.session.commit()


def get_mock_token(new_user):
    """
    Mocks new_user's auth token for tests
    """
    data = {'id': new_user["id"], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=api.TOKEN_TTL)}
    token = jwt.encode(payload=data, key=api.app.config['SECRET_KEY'], algorithm="HS256")
    return token


#-------------GENERATES NEW MOCK DATA FOR TESTS-----------------------------

WORD_SITE = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(WORD_SITE)
words = response.content.splitlines()


def get_random_word():
    return secrets.choice(words).decode()


def get_random_email():
    return f"{get_random_word()}@gmail.com"


def get_random_word_hash():
    return sha1(secrets.choice(words)).hexdigest()


def get_random_id():
    return str(uuid4())

