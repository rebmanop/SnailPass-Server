new_user = {
    "id": "1c536854-e7b2-413b-b55g-321bc92k471s",
    "email": "test@email.com",
    "master_password_hash": "password_hash_test",
    "hint": "test"
}

def test_add_new_user_success(client):
    #Successful sign up operation 
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    print(rv.data)
    assert rv.status_code == 201
    successful_response_message = f"User '{new_user['email']}' created successfully"
    assert successful_response_message.encode() in rv.data


def test_add_new_user_fail_exists_id(client):
    #User with that id already exists
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    assert rv.status_code == 409
    user_exists_response_message = f"User with received id '{new_user['id']}' already exists"
    assert user_exists_response_message.encode() in rv.data


def test_add_new_user_fail_exists_email(client):
    #User with that email already exists
    local_new_user = new_user.copy()
    rv = client.post('/users',  json=local_new_user, follow_redirects=True)
    local_new_user["id"] = "1234"
    rv = client.post('/users',  json=local_new_user, follow_redirects=True)
    assert rv.status_code == 409
    user_exists_response_message = f"User with received email '{local_new_user['email']}' already exists"
    assert user_exists_response_message.encode() in rv.data


def test_add_new_user_fail_argument_missing_id(client):
    local_new_user = new_user.copy()
    local_new_user.pop("id")
    rv = client.post('/users',  json=local_new_user, follow_redirects=True)
    assert rv.status_code == 400



