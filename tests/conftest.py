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
def new_user() -> dict:

    new_user = {
        "id": utils.get_random_id(),
        "email": utils.get_random_email(),
        "master_password_hash": utils.get_random_word_hash(),
        "hint": utils.get_random_word(),
    }

    return new_user


@pytest.fixture
def new_record() -> dict:

    new_record = {
        "id": utils.get_random_id(),
        "name": utils.MOCK_ENCRYPTED_DATA,
        "login": utils.MOCK_ENCRYPTED_DATA,
        "password": utils.MOCK_ENCRYPTED_DATA,
        "is_favorite": False,
        "is_deleted": False,
    }

    return new_record


@pytest.fixture
def new_note() -> dict:

    new_note = {
        "id": utils.get_random_id(),
        "name": utils.MOCK_ENCRYPTED_DATA,
        "content": utils.MOCK_ENCRYPTED_DATA,
        "is_favorite": False,
        "is_deleted": False,
    }

    return new_note


@pytest.fixture
def new_additional_field() -> dict:

    additional_field = {
        "id": utils.get_random_id(),
        "name": utils.MOCK_ENCRYPTED_DATA,
        "value": utils.MOCK_ENCRYPTED_DATA,
    }

    return additional_field
