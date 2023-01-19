import models
from models import db
from tests.utils import add_new_user_to_mock_db, get_mock_token, add_new_record_to_mock_db
from api.resource_fields import RECORD_RESOURCE_FIELDS

#-------------------------------------ADD NEW RECORD TESTS (POST REQUEST)---------------

def test_add_new_record_success_1(client, new_user, new_record):
    """
    Successful record creation
    """

    add_new_user_to_mock_db(new_user)
    assert models.User.query.get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)

    expected_response_message = f"Record '{new_record['name']}' created successfully (user = '{new_user['email']}')"
    assert response.status_code == 201
    assert expected_response_message.encode() in response.data


def test_add_new_record_success_2(client, new_user, new_record):
    """
    Successful record creation, with already existing record name but unique login
    """

    add_new_user_to_mock_db(new_user)
    assert models.User.query.get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)
    assert response.status_code == 201

    #Sending second POST with different record id and login but same name
    new_record["id"] += "x"
    new_record["login"] += "x"

    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)


    expected_response_message = f"Record '{new_record['name']}' created successfully (user = '{new_user['email']}')"
    assert response.status_code == 201
    assert expected_response_message.encode() in response.data


def test_add_new_record_fail_1(client, new_user, new_record):
    """
    Record creation fail, record with recieved id already exists
    """

    add_new_user_to_mock_db(new_user)
    assert models.User.query.get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)
    assert response.status_code == 201
    
    #Sending second POST with same record to get 'record with that id already exists' error"
    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)
    
    expected_response_message = f"Record with id '{new_record['id']}' already exist"
    response.status_code == 409
    assert expected_response_message.encode() in response.data


def test_add_new_record_fail_2(client, new_user, new_record):
    """
    Record creation fail, record with recieved name and login already exists
    """

    add_new_user_to_mock_db(new_user)
    assert models.User.query.get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)
    assert response.status_code == 201
    
    #Sending second POST with new record id but same name and login"
    new_record["id"] += "x"
    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)
    
    expected_response_message = f"Record with name '{new_record['name']}' and with login '{new_record['login']}' already exist in current user's vault"
    response.status_code == 409
    assert expected_response_message.encode() in response.data


#-------------------------------------DELETE RECORD TESTS (DELETE REQUEST)---------------


def test_delete_record_success(client, new_user, new_record):
    """
    Successful delete record request
    """
    add_new_user_to_mock_db(new_user)
    assert  models.User.query.get(new_user["id"]) != None


    add_new_record_to_mock_db(new_user, new_record)
    assert models.Record.query.get(new_record["id"]) != None

    token = get_mock_token(new_user)

    #Sending delete request with record id as uri argument 
    response = client.delete("/records", headers={"x-access-token": f"{token}"}, 
                            query_string={'id': new_record["id"]})
    
    expected_response_message = f"Record '{new_record['name']}' deleted successfully (user = '{new_user['email']}')"
    assert response.status_code == 200
    assert expected_response_message.encode() in response.data


def test_delete_record_fail_1(client, new_user):
    """
    Record delete fail, record id is missing in uri args
    """
    add_new_user_to_mock_db(new_user)
    assert  models.User.query.get(new_user["id"]) != None
    token = get_mock_token(new_user)

    #Sending delete request without record id as uri argument 
    response = client.delete("/records", headers={"x-access-token": f"{token}"})
    
    assert response.status_code == 400
    assert b"Record id is missing in uri args" in response.data


def test_delete_record_fail_2(client, new_user, new_record):
    """
    Record delete fail, not existing record id
    """
    add_new_user_to_mock_db(new_user)
    assert  models.User.query.get(new_user["id"]) != None

    token = get_mock_token(new_user)

    #Sending delete request with not existing record
    response = client.delete("/records", headers={"x-access-token": f"{token}"}, 
                            query_string={'id': new_record["id"]})
    
    assert response.status_code == 404
    assert b"Record with that id doesn't exist" in response.data


def test_delete_record_fail_3(client, new_user, new_record):
    """
    Record delete fail, record doesn't belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert  models.User.query.get(new_user["id"]) != None

    add_new_record_to_mock_db(new_user, new_record)
    new_record_got_from_db = models.Record.query.get(new_record["id"])
    assert new_record_got_from_db != None

    token = get_mock_token(new_user)

    new_record_got_from_db.user_id += "x"
    db.session.commit()

    #Sending delete request, where record's user id changed so it doesn't belong to current user
    response = client.delete("/records", headers={"x-access-token": f"{token}"}, 
                            query_string={'id': new_record["id"]})
    
    expected_response_message = f"Record with id '{new_record['id']}' doesn't belong to the current user"
    assert response.status_code == 403
    assert expected_response_message.encode() in response.data


#-------------------------------------GET CURRENT USER RECORDS TESTS (GET REQUEST)---------------
def test_get_records_success(client, new_user, new_record):
    """
    Successful get user records request
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = models.User.query.get(new_user["id"]) 
    assert  new_user_got_from_db != None

    add_new_record_to_mock_db(new_user, new_record)
    assert models.Record.query.get(new_record["id"]) != None

    new_record_2 = new_record.copy()
    new_record_2["id"] += "x"
    new_record_2["name"] += "x"
    add_new_record_to_mock_db(new_user, new_record_2)
    assert models.Record.query.get(new_record_2["id"]) != None

    token = get_mock_token(new_user)

    #Sending get user records request
    response = client.get("/records", headers={"x-access-token": f"{token}"})
    assert response.status_code == 200
    import json
    list_of_records = json.loads(response.data.decode('utf-8'))
    assert len(list_of_records) == 2
    assert len(RECORD_RESOURCE_FIELDS) == len(list_of_records[0])


def test_get_records_fail(client, new_user):
    """
    Get user records request fail, user has no records
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = models.User.query.get(new_user["id"]) 
    assert  new_user_got_from_db != None

    token = get_mock_token(new_user)

    #Sending get user records request, when user has no records
    response = client.get("/records", headers={"x-access-token": f"{token}"})
    expected_resoponse_message = f"User '{new_user['email']}' has no records"
    assert response.status_code == 404
    assert expected_resoponse_message.encode() in response.data


#-------------------------------------EDIT RECORD TESTS (PATCH REQUEST)---------------
def test_edit_record_success(client, new_user, new_record):
    """
    Successful edit record request (PATCH)
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = models.User.query.get(new_user["id"]) 
    assert  new_user_got_from_db != None

    add_new_record_to_mock_db(new_user, new_record)
    new_record_got_from_db = models.Record.query.get(new_record["id"])
    assert models.Record.query.get(new_record["id"]) != None

    token = get_mock_token(new_user)

    #Sending patch request with edited record
    edited_record = new_record.copy()
    
    edited_record["encrypted_password"] += "x"
    edited_record["is_deleted"] = new_record_got_from_db.is_deleted
    edited_record["is_favorite"] =new_record_got_from_db.is_favorite

    response = client.patch("/records", headers={"x-access-token": f"{token}"}, json=edited_record)
    expected_respones_message = f"Changes for the record '{new_record['id']}' were successfully made"
    assert response.status_code == 200
    assert expected_respones_message.encode() in response.data
    assert models.Record.query.get(new_record["id"]).encrypted_password == edited_record["encrypted_password"]


def test_edit_record_fail_1(client, new_user, new_record):
    """
    Edit record fail, record with requested id doesn't exist
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = models.User.query.get(new_user["id"]) 
    assert  new_user_got_from_db != None

    token = get_mock_token(new_user)

    #Sending patch request when user has no records, expecting unexisting record error
    new_record["is_favorite"] = False
    new_record["is_deleted"] = False
    response = client.patch("/records", headers={"x-access-token": f"{token}"}, json=new_record)
    expected_respones_message = f"Record with id '{new_record['id']}' doesn't exist"
    assert response.status_code == 404
    assert expected_respones_message.encode() in response.data


def test_edit_record_fail_2(client, new_user, new_record):
    """
    Record edit fail, record doesn't belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert  models.User.query.get(new_user["id"]) != None

    add_new_record_to_mock_db(new_user, new_record)
    new_record_got_from_db = models.Record.query.get(new_record["id"])
    assert new_record_got_from_db != None

    token = get_mock_token(new_user)

    new_record_got_from_db.user_id += "x"
    db.session.commit()

    #Sending delete request, where record's user id changed so it doesn't belong to current user
    new_record["is_favorite"] = False
    new_record["is_deleted"] = False
    response = client.patch("/records", headers={"x-access-token": f"{token}"}, 
                            json=new_record)

    expected_response_message = f"Record with id '{new_record['id']}' doesn't belong to the current user"
    assert response.status_code == 403
    assert expected_response_message.encode() in response.data


def test_edit_record_fail_3(client, new_user, new_record):
    """
    Record edit fail, record with requested name and login already exists
    """
    add_new_user_to_mock_db(new_user)
    assert  models.User.query.get(new_user["id"]) != None

    add_new_record_to_mock_db(new_user, new_record)
    new_record_got_from_db = models.Record.query.get(new_record["id"])
    assert new_record_got_from_db != None

    new_record_2 = new_record.copy()
    new_record_2["id"] += "x"
    new_record_2["name"] += "x"
    add_new_record_to_mock_db(new_user, new_record_2)
    new_record_got_from_db_2 = models.Record.query.get(new_record_2["id"])
    assert new_record_got_from_db_2 != None


    token = get_mock_token(new_user)

    """"
    Sending delete request, where record's records name and login are changed to 
    already existing record's name and login
    """
    new_record_2["name"] = new_record["name"]
    new_record_2["login"] = new_record["login"]
    new_record_2["is_favorite"] = False
    new_record_2["is_deleted"] = False
    response = client.patch("/records", headers={"x-access-token": f"{token}"}, 
                            json=new_record_2)

    expected_response_message = f"Record with name '{new_record_2['name']}' and with login '{new_record_2['login']}' already exist in current user's vault"
    assert response.status_code == 409
    assert expected_response_message.encode() in response.data




