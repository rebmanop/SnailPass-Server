import os
import pytest
from tests import utils
from models import db
from api import create_app
from config import TestingConfig


@pytest.fixture()
def client():
    testing_config = TestingConfig()
    app = create_app(testing_config)
    
    with app.app_context():
        db.create_all()
        yield app.test_client()   
        db.drop_all()
    
    os.close(testing_config.db_fd)
    os.unlink(testing_config.db_filename)


@pytest.fixture
def new_user():
    
    new_user = {
    "id": utils.get_random_id(),
    "email": utils.get_random_email(),
    "master_password_hash": utils.get_random_word_hash(),
    "hint": utils.get_random_word()
    }

    return new_user


@pytest.fixture
def new_record():
    
    new_record = {
    "id": utils.get_random_id(),
    "name": utils.get_random_word(),
    "login": utils.get_random_email(),
    "encrypted_password": utils.get_random_word_hash(),
    }

    return new_record


@pytest.fixture
def new_note():
    
    new_note = {
    "id": utils.get_random_id(),
    "name": utils.get_random_word(),
    "content": utils.get_random_word() + " " + utils.get_random_word(),
    }

    return new_note


@pytest.fixture
def new_additional_field():
    
    additional_field = {
    "id": utils.get_random_id(),
    "field_name": utils.get_random_word(),
    "value": utils.get_random_word(),
    }

    return additional_field








     