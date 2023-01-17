import models
from base64 import b64encode

def test_add_new_user_success(client, new_user):
    #Successful sign up operation 
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    assert rv.status_code == 201
    successful_response_message = f"User '{new_user['email']}' created successfully"
    assert successful_response_message.encode() in rv.data
    assert models.User.query.get(new_user["id"]) != None


def test_add_new_user_fail_exists_id(client, new_user):
    #User with that id already exists
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    assert rv.status_code == 409
    user_exists_response_message = f"User with received id '{new_user['id']}' already exists"
    assert user_exists_response_message.encode() in rv.data


def test_add_new_user_fail_exists_email(client, new_user):
    #User with that email already exists
    local_new_user = new_user.copy()
    rv = client.post('/users',  json=local_new_user, follow_redirects=True)
    local_new_user["id"] = "1234"
    rv = client.post('/users',  json=local_new_user, follow_redirects=True)
    assert rv.status_code == 409
    user_exists_response_message = f"User with received email '{local_new_user['email']}' already exists"
    assert user_exists_response_message.encode() in rv.data


def test_add_new_user_fail_argument_missing_id(client, new_user):
    local_new_user = new_user.copy()
    local_new_user.pop("id")
    rv = client.post('/users',  json=local_new_user, follow_redirects=True)
    assert rv.status_code == 400


def test_login(client, new_user):
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    assert rv.status_code == 201
    successful_response_message = f"User '{new_user['email']}' created successfully"
    assert successful_response_message.encode() in rv.data
    assert models.User.query.get(new_user["id"]) != None

    auth_str = f"{new_user['email']}:{new_user['master_password_hash']}"

    credentials = b64encode(bytes(auth_str.encode())).decode('utf-8')
    res = client.get("/login", headers={"Authorization": f"Basic {credentials}"})

    assert res.status_code == 200
    


