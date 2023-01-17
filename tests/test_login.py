import models
from base64 import b64encode

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