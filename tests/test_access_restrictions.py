import models
from models import db
from tests.utils import add_new_user_to_mock_db, get_mock_token


def test_access_restrictions_invalid_token(client, new_user):
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    token += "x"

    response = client.get("/users", headers={"x-access-token": f"{token}"})
    assert response.status_code == 401
    assert b"Token is invalid" in response.data and b"error" in response.data



def test_access_restrictions_token_expired(client, new_user):
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    
    token = get_mock_token(new_user, token_ttl_minutes=0.0001)

    response = client.get("/users", headers={"x-access-token": f"{token}"})

    assert response.status_code == 401
    assert b"Token already expired" in response.data and b"error" in response.data



def test_access_restrictions_token_missing(client, new_user):
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    

    response = client.get("/users")
    assert response.status_code == 400
    assert b"Token is missing" in response.data


def test_access_restrictions_current_user_doesnt_exist(client, new_user):
    add_new_user_to_mock_db(new_user)
    new_user_model = db.session.query(models.User).get(new_user["id"])
    assert new_user_model != None
    
    token = get_mock_token(new_user)

    db.session.delete(new_user_model)
    db.session.commit()

    response = client.get("/users", headers={"x-access-token": f"{token}"})

    assert response.status_code == 404
    assert b"Current user does not exist" in response.data and b"error" in response.data







