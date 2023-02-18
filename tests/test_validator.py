from tests.utils import add_new_user_to_mock_db, get_mock_token
from api.core import WRONG_FORMAT_ARGUMENT_RESPONSE, EMPTY_STRING_ARGUMENT_RESPONSE
import models
from models import db


def test_validator_fail(client, new_user, new_record):
    """
    Check validation exception handling
    """

    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None

    token = get_mock_token(new_user)
    new_record["login"] = "wrong_format_string"
    new_record["password"] = ""

    response = client.post(
        "/records", headers={"x-access-token": f"{token}"}, json=new_record
    )

    assert response.status_code == 400
    assert WRONG_FORMAT_ARGUMENT_RESPONSE.encode() in response.data
    assert EMPTY_STRING_ARGUMENT_RESPONSE.encode() in response.data
