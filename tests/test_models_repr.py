import api.models as models
import datetime
from tests import utils


def test_user_repr():
    user = models.User(
        id=utils.get_random_id(),
        email=utils.get_random_email(),
        master_password_hash=utils.get_random_word_hash(),
        hint=utils.get_random_word(),
    )
    print(user)


def test_record_repr():
    record = models.Record(
        id=utils.get_random_id(),
        name=utils.get_random_word(),
        login=utils.get_random_email(),
        password=utils.get_random_word_hash(),
        user_id=utils.get_random_id(),
        creation_time=datetime.datetime.utcnow(),
        update_time=datetime.datetime.utcnow(),
    )
    print(record)


def test_note_repr():
    note = models.Note(
        id=utils.get_random_id(),
        name=utils.get_random_word(),
        content=utils.get_random_word() + utils.get_random_word(),
        user_id=utils.get_random_id(),
        creation_time=datetime.datetime.utcnow(),
        update_time=datetime.datetime.utcnow(),
    )
    print(note)


def test_additional_field_repr():
    additional_field = models.AdditionalField(
        id=utils.get_random_id(),
        name=utils.get_random_word(),
        value=utils.get_random_word(),
        record_id=utils.get_random_id(),
    )
    print(additional_field)
