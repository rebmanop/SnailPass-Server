import models
from models import db
from nameof import nameof
from tests.utils import add_new_user_to_mock_db, get_mock_token

# -------------------------------------SIGN UP PROCEDURE TESTS (POST REQUEST)---------------


def test_signup_new_user_success(client, new_user: dict):
    """
    Successful sign procedure
    """
    response = client.post("/users", json=new_user, follow_redirects=True)
    assert response.status_code == 201
    expected_response_message = (
        f"User created successfully {new_user[nameof(models.User.id)]}"
    )
    assert (
        expected_response_message.encode() in response.data
        and b"success" in response.data
    )
    assert db.session.query(models.User).get(new_user["id"]) != None


def test_signup_new_user_fail_1(client, new_user: dict):
    """
    Sign up fail, user with received id already exists
    """
    response = client.post("/users", json=new_user, follow_redirects=True)
    response = client.post("/users", json=new_user, follow_redirects=True)
    assert response.status_code == 409
    expected_response_message = (
        f"User with id {new_user[nameof(models.User.id)]} already exists"
    )
    assert (
        expected_response_message.encode() in response.data
        and b"error" in response.data
    )


def test_signup_new_user_fail_2(client, new_user):
    """
    Sign up fail, user with received email already exists
    """
    local_new_user = new_user.copy()
    response = client.post("/users", json=local_new_user, follow_redirects=True)
    local_new_user["id"] = "1234"
    response = client.post("/users", json=local_new_user, follow_redirects=True)
    assert response.status_code == 409
    expected_response_message = f"User with this email already exists"
    assert (
        expected_response_message.encode() in response.data
        and b"error" in response.data
    )


# ------------------------------------- GET CURRENT USER TEST (GET REQUEST)---------------
def test_get_current_user_success(client, new_user):
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None

    token = get_mock_token(new_user)

    response = client.get("/users", headers={"x-access-token": f"{token}"})

    assert response.status_code == 200
    assert new_user[nameof(models.User.id)].encode() in response.data
    assert new_user[nameof(models.User.email)].encode() in response.data
    assert new_user[nameof(models.User.hint)].encode() in response.data
