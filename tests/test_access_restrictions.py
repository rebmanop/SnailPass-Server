import models
from models import db
from tests.utils import add_new_user_to_mock_db, get_mock_token


def test_access_restrictions_invalid_token(client, new_user):
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    token += "x"

    response = client.get("/users", headers={"x-access-token": f"{token}"})
    response = client.delete("/users", headers={"x-access-token": f"{token}"})
    assert response.status_code == 401
    assert b"Token is invalid" in response.data



def test_access_restrictions_token_expired(client, new_user):
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    
    token = get_mock_token(new_user, token_ttl_minutes=0.001)

    response = client.get("/users", headers={"x-access-token": f"{token}"})
    response = client.delete("/users", headers={"x-access-token": f"{token}"})

    assert response.status_code == 401
    assert b"Token already expired" in response.data



def test_access_restrictions_token_missing(client, new_user):
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    

    response = client.get("/users")
    response = client.delete("/users")
    assert response.status_code == 400
    assert b"Token is missing" in response.data


def test_access_restrictions_admin_only_function(client, new_user):
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    
    response = client.delete("/users", headers={"x-access-token": f"{token}"})
    assert response.status_code == 403
    assert b"Admin only function" in response.data





