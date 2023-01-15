import models
from api import db

def test_add_new_user(app):

    client = app.test_client()

    new_user = {
        "id": "1c536854-e7b2-413b-b55g-321bc92k471s",
        "email": "test@email.com",
        "master_password_hash": "password_hash_test",
        "hint": "test"
    }

    #Successful sign up operation 
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    db.session.delete(models.User.query.get(new_user["id"]))
    db.session.commit()
    assert rv.status_code == 201
    successful_response_message = f"User '{new_user['email']}' created successfully"
    assert successful_response_message.encode() in rv.data

    
    #User with that id already exists
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    db.session.delete(models.User.query.get(new_user["id"]))
    db.session.commit()
    assert rv.status_code == 409
    user_exists_response_message = f"User with received id '{new_user['id']}' already exists"
    assert user_exists_response_message.encode() in rv.data

    #User with that email already exists
    user_id = new_user["id"]
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    new_user["id"] = "1234"
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    db.session.delete(models.User.query.get(user_id))
    db.session.commit()
    assert rv.status_code == 409
    user_exists_response_message = f"User with received email '{new_user['email']}' already exists"
    assert user_exists_response_message.encode() in rv.data


    #Required argument missing (id)
    new_user.pop("id")
    rv = client.post('/users',  json=new_user, follow_redirects=True)
    assert rv.status_code == 400
