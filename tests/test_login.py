import api.models as models
from api.models import db
from base64 import b64encode
from tests.utils import add_new_user_to_mock_db


def test_login_success(client, new_user):
    add_new_user_to_mock_db(new_user)

    assert db.session.query(models.User).get(new_user["id"]) != None

    auth_str = f"{new_user['email']}:{new_user['master_password_hash']}"
    credentials = b64encode(auth_str.encode()).decode("utf-8")
    response = client.get("/login", headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == 200
    assert b"token" in response.data


def test_login_fail_1(client, new_user):
    """
    Login request fail, authorization info missing or it's incomplete
    """

    add_new_user_to_mock_db(new_user)

    assert db.session.query(models.User).get(new_user["id"]) != None

    response = client.get("/login")

    assert response.status_code == 401
    assert (
        b"Authentication info missing or it's incomplete" in response.data
        and b"error" in response.data
    )


def test_login_fail_2(client, new_user):
    """
    Login request fail, email doesn't exist
    """

    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None

    new_user["email"] += "x"
    auth_str = f"{new_user['email']}:{new_user['master_password_hash']}"

    credentials = b64encode(auth_str.encode()).decode("utf-8")
    response = client.get("/login", headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == 401
    assert b"Incorrect credentials" in response.data and b"error" in response.data


def test_login_fail_3(client, new_user):
    """
    Login request fail, incorrect password
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None

    new_user["master_password_hash"] += "x"
    auth_str = f"{new_user['email']}:{new_user['master_password_hash']}"

    credentials = b64encode(auth_str.encode()).decode("utf-8")
    response = client.get("/login", headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == 401
    assert b"Incorrect credentials" in response.data and b"error" in response.data
