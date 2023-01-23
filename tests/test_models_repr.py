import models
from models import db
from tests import utils
import datetime

def test_user_repr():
    user = models.User(id=utils.get_random_id(), email=utils.get_random_email(), 
                                master_password_hash=utils.get_random_word_hash(), hint=utils.get_random_word(), is_admin=False)
    print(user)

def test_record_repr():
    record = models.Record(id=utils.get_random_id(), name=utils.get_random_word(), login=utils.get_random_email(), 
                                encrypted_password=utils.get_random_word_hash(), user_id=utils.get_random_id(), creation_time=datetime.datetime.now(), 
                                update_time=datetime.datetime.now(), nonce=utils.get_random_word_hash())
    print(record)

def test_note_repr():
    note = models.Note(id=utils.get_random_id(), name=utils.get_random_word(), content=utils.get_random_word() + utils.get_random_word(), user_id=utils.get_random_id(), creation_time=datetime.datetime.now(), 
                                update_time=datetime.datetime.now(), nonce=utils.get_random_word_hash())
    print(note)

def test_additional_field_repr():
    additional_field = models.AdditionalField(id=utils.get_random_id(), field_name=utils.get_random_word(), value=utils.get_random_word(), 
                                record_id=utils.get_random_id(), nonce=utils.get_random_word_hash())
    print(additional_field)
