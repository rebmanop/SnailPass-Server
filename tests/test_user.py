import jwt
import api
import models
import datetime
from models import db
from tests.utils import add_new_user_to_db

#-------------------------------------SIGN UP PROCEDURE TESTS (POST REQUEST)---------------

def test_signup_new_user_success(client, new_user):
    #Successful sign up operation 
    response = client.post('/users',  json=new_user, follow_redirects=True)
    assert response.status_code == 201
    expected_response_message = f"User '{new_user['email']}' created successfully"
    assert expected_response_message.encode() in response.data
    assert models.User.query.get(new_user["id"]) != None


def test_signup_new_user_fail_exists_id(client, new_user):
    #User with that id already exists
    response = client.post('/users',  json=new_user, follow_redirects=True)
    response = client.post('/users',  json=new_user, follow_redirects=True)
    assert response.status_code == 409
    expected_response_message = f"User with received id '{new_user['id']}' already exists"
    assert expected_response_message.encode() in response.data


def test_signup_new_user_fail_exists_email(client, new_user):
    #User with that email already exists
    local_new_user = new_user.copy()
    response = client.post('/users',  json=local_new_user, follow_redirects=True)
    local_new_user["id"] = "1234"
    response = client.post('/users',  json=local_new_user, follow_redirects=True)
    assert response.status_code == 409
    expected_response_message = f"User with received email '{local_new_user['email']}' already exists"
    assert expected_response_message.encode() in response.data


#------------------------------------- GET CURRENT USER TESTS (GET REQUEST)---------------
def test_get_current_user_success(client, new_user):
    add_new_user_to_db(new_user)
    assert models.User.query.get(new_user["id"]) != None
    
    #Mocking new_user's token
    data = {'id': new_user["id"], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=api.TOKEN_TTL)}
    token = jwt.encode(payload=data, key=api.app.config['SECRET_KEY'], algorithm="HS256")

    response = client.get("/users", headers={"x-access-token": f"{token}"})
    
    assert response.status_code == 200
    assert new_user["id"].encode() in response.data
    assert new_user["email"].encode() in response.data
    assert new_user["hint"].encode() in response.data
    assert b"is_admim" and b"false" in response.data



#------------------------------------- DELETE USER TESTS (DELETE REQUEST)---------------

def test_delete_user_success(client, new_user):
    add_new_user_to_db(new_user, is_admin=True)
    new_user_got_from_db = models.User.query.get(new_user["id"])
    assert  new_user_got_from_db != None
    assert new_user_got_from_db.is_admin == True

    #Mocking new_user's token
    data = {'id': new_user["id"], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=api.TOKEN_TTL)}
    token = jwt.encode(payload=data, key=api.app.config['SECRET_KEY'], algorithm="HS256")

    #User deletes itself
    response = client.delete("/users", query_string={'id': new_user["id"]}, headers={"x-access-token": f"{token}"})
    
    expected_response_message = f"User '{new_user['email']}' deleted successfully"
    
    assert response.status_code == 200
    assert expected_response_message.encode() in response.data








    



    





    


