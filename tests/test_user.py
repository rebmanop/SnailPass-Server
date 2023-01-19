import jwt
import api
import models
import datetime
from models import db
from tests.utils import add_new_user_to_mock_db, get_mock_token

#-------------------------------------SIGN UP PROCEDURE TESTS (POST REQUEST)---------------

def test_signup_new_user_success(client, new_user):
    """
    Successful sign procedure
    """
    response = client.post('/users',  json=new_user, follow_redirects=True)
    assert response.status_code == 201
    expected_response_message = f"User '{new_user['email']}' created successfully"
    assert expected_response_message.encode() in response.data
    assert models.User.query.get(new_user["id"]) != None


def test_signup_new_user_fail_1(client, new_user):
    """
    Sign up fail, user with received id already exists
    """
    response = client.post('/users',  json=new_user, follow_redirects=True)
    response = client.post('/users',  json=new_user, follow_redirects=True)
    assert response.status_code == 409
    expected_response_message = f"User with received id '{new_user['id']}' already exists"
    assert expected_response_message.encode() in response.data


def test_signup_new_user_fail_2(client, new_user):
    """
    Sign up fail, user with received email already exists
    """
    local_new_user = new_user.copy()
    response = client.post('/users',  json=local_new_user, follow_redirects=True)
    local_new_user["id"] = "1234"
    response = client.post('/users',  json=local_new_user, follow_redirects=True)
    assert response.status_code == 409
    expected_response_message = f"User with received email '{local_new_user['email']}' already exists"
    assert expected_response_message.encode() in response.data


#------------------------------------- GET CURRENT USER TEST (GET REQUEST)---------------
def test_get_current_user_success(client, new_user):
    add_new_user_to_mock_db(new_user)
    assert models.User.query.get(new_user["id"]) != None
    
    token = get_mock_token(new_user)

    response = client.get("/users", headers={"x-access-token": f"{token}"})
    
    assert response.status_code == 200
    assert new_user["id"].encode() in response.data
    assert new_user["email"].encode() in response.data
    assert new_user["hint"].encode() in response.data
    assert b"is_admim" and b"false" in response.data



#------------------------------------- DELETE USER TESTS (DELETE REQUEST)---------------

def test_delete_user_success(client, new_user):
    """
    Successful delete user request
    """
    add_new_user_to_mock_db(new_user, is_admin=True)
    new_user_got_from_db = models.User.query.get(new_user["id"])
    assert  new_user_got_from_db != None
    assert new_user_got_from_db.is_admin == True

    token = get_mock_token(new_user)

    #Sending delete request where user deletes itself
    response = client.delete("/users", query_string={'id': new_user["id"]}, headers={"x-access-token": f"{token}"})
    
    expected_response_message = f"User '{new_user['email']}' deleted successfully"
    
    assert response.status_code == 200
    assert expected_response_message.encode() in response.data


def test_delete_user_fail_1(client, new_user):
    """
    Delete user request fail, user id not found in uri params
    """
    add_new_user_to_mock_db(new_user, is_admin=True)
    new_user_got_from_db = models.User.query.get(new_user["id"])
    assert  new_user_got_from_db != None
    assert new_user_got_from_db.is_admin == True

    token = get_mock_token(new_user)

    #Sending delete request without user id as uri argument 
    response = client.delete("/users", headers={"x-access-token": f"{token}"})
    
    assert response.status_code == 400
    assert b"User id not found in the url params" in response.data


def test_delete_user_fail_2(client, new_user):
    """
    Delete user request fail, user with recived id doesn't exist
    """
    add_new_user_to_mock_db(new_user, is_admin=True)
    new_user_got_from_db = models.User.query.get(new_user["id"])
    assert  new_user_got_from_db != None
    assert new_user_got_from_db.is_admin == True

    token = get_mock_token(new_user)

    #Sending delete request with not existing user id
    new_user["id"] += "x"
    response = client.delete("/users", query_string={'id': new_user["id"]}, headers={"x-access-token": f"{token}"})
    
    
    assert response.status_code == 404
    assert b"User with that id doesn't exist" in response.data

    








    



    





    


