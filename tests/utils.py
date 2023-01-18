import secrets
import requests
from hashlib import sha1
from uuid import uuid4
from models import db, User
from hashing import hash_mp_additionally


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


def add_new_user_to_db(new_user, is_admin=False):
    additionaly_hashed_mp = hash_mp_additionally(password_hash=new_user["master_password_hash"], 
                                                    salt=new_user["email"])

    
    new_user_db_model_object = User(id=new_user["id"], email=new_user["email"], 
                                master_password_hash=additionaly_hashed_mp, hint=new_user["hint"], is_admin=is_admin)
    db.session.add(new_user_db_model_object)
    db.session.commit()

