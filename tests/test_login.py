from models import *
from base64 import b64encode
from tests.utils import add_new_user_to_db


def test_login_success(client, new_user):
    add_new_user_to_db(new_user)
    
    assert User.query.get(new_user["id"]) != None

    auth_str = f"{new_user['email']}:{new_user['master_password_hash']}"
    credentials = b64encode(auth_str.encode()).decode('utf-8')
    response = client.get("/login", headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == 200
    assert b"token" in response.data


def test_login_fail_authorization_info_missing(client, new_user):
    add_new_user_to_db(new_user)
    
    assert User.query.get(new_user["id"]) != None

    response = client.get("/login")

    assert response.status_code == 400
    assert b"Authorization info missing or it's incomplete" in response.data


def test_login_fail_email_dont_exists(client, new_user):
    add_new_user_to_db(new_user)
    assert User.query.get(new_user["id"]) != None

    new_user["email"] += "x"
    auth_str = f"{new_user['email']}:{new_user['master_password_hash']}"

    credentials = b64encode(auth_str.encode()).decode('utf-8')
    response = client.get("/login", headers={"Authorization": f"Basic {credentials}"})

    expected_response_message = f"User with recieved email '{new_user['email']}' doesn't exist"

    assert response.status_code == 401
    assert expected_response_message.encode() in response.data


def test_login_fail_incorrect_password(client, new_user):
    add_new_user_to_db(new_user)
    assert User.query.get(new_user["id"]) != None

    new_user["master_password_hash"] += "x"
    auth_str = f"{new_user['email']}:{new_user['master_password_hash']}"

    credentials = b64encode(auth_str.encode()).decode('utf-8')
    response = client.get("/login", headers={"Authorization": f"Basic {credentials}"})

    assert response.status_code == 401
    assert b"Incorrect password" in response.data
    
    
