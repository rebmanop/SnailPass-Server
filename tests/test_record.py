import models
from models import db
from nameof import nameof
from tests.utils import add_new_user_to_mock_db, get_mock_token, add_new_record_to_mock_db
from api.resource_fields import RECORD_RESOURCE_FIELDS

#-------------------------------------ADD NEW RECORD TESTS (POST REQUEST)---------------

def test_add_new_record_success_1(client, new_user, new_record):
    """
    Successful record creation
    """

    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)

    expected_response_message = f"Record {new_record[nameof(models.Record.id)]} created"
    assert response.status_code == 201
    assert expected_response_message.encode() in response.data and b"success"


def test_add_new_record_fail_1(client, new_user, new_record):
    """
    Record creation fail, record with recieved id already exists
    """

    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)
    assert response.status_code == 201
    
    #Sending second POST with same record to get 'record with that id already exists' error"
    response = client.post("/records", headers={"x-access-token": f"{token}"}, json=new_record)
    
    expected_response_message = f"Record with id {new_record[nameof(models.Record.id)]} already exists"
    response.status_code == 409
    assert expected_response_message.encode() in response.data and b"error"


#-------------------------------------DELETE RECORD TESTS (DELETE REQUEST)---------------


def test_delete_record_success(client, new_user, new_record):
    """
    Successful delete record request
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None


    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"]) != None

    token = get_mock_token(new_user)

    #Sending delete request with record id as uri argument 
    response = client.delete("/records", headers={"x-access-token": f"{token}"}, 
                            query_string={'id': new_record["id"]})
    
    expected_response_message = f"Record {new_record[nameof(models.Record.id)]} deleted successfully"
    assert response.status_code == 200
    assert expected_response_message.encode() in response.data and b"success"


def test_delete_record_fail_1(client, new_user):
    """
    Record delete fail, record id is missing in uri args
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None
    token = get_mock_token(new_user)

    #Sending delete request without record id as uri argument 
    response = client.delete("/records", headers={"x-access-token": f"{token}"})
    
    assert response.status_code == 400
    assert b"Record id is missing in URI arguments" in response.data and b"error"


def test_delete_record_fail_2(client, new_user, new_record):
    """
    Record delete fail, not existing record id
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None

    token = get_mock_token(new_user)

    #Sending delete request with not existing record
    response = client.delete("/records", headers={"x-access-token": f"{token}"}, 
                            query_string={'id': new_record["id"]})
    
    assert response.status_code == 404
    expected_response_message = f"Record with id {new_record['id']} doesn't exist"
    assert expected_response_message.encode() in response.data and b"error"


def test_delete_record_fail_3(client, new_user, new_record):
    """
    Record delete fail, record doesn't belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None

    add_new_record_to_mock_db(new_user, new_record)
    new_record_got_from_db = db.session.query(models.Record).get(new_record["id"])
    assert new_record_got_from_db != None

    token = get_mock_token(new_user)

    new_record_got_from_db.user_id += "x"
    db.session.commit()

    #Sending delete request, where record's user id changed so it doesn't belong to current user
    response = client.delete("/records", headers={"x-access-token": f"{token}"}, 
                            query_string={'id': new_record["id"]})
    
    expected_response_message = f"Record {new_record['id']} doesn't belong to the current user {new_user['id']}"
    assert response.status_code == 403
    assert expected_response_message.encode() in response.data and b"error"


#-------------------------------------GET CURRENT USER RECORDS TESTS (GET REQUEST)---------------
def test_get_records_success(client, new_user, new_record):
    """
    Successful get user records request
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = db.session.query(models.User).get(new_user["id"]) 
    assert  new_user_got_from_db != None

    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"]) != None

    new_record_2 = new_record.copy()
    new_record_2["id"] += "x"
    new_record_2["name"] += "x"
    add_new_record_to_mock_db(new_user, new_record_2)
    assert db.session.query(models.Record).get(new_record_2["id"]) != None

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
    new_user_got_from_db = db.session.query(models.User).get(new_user["id"]) 
    assert  new_user_got_from_db != None

    token = get_mock_token(new_user)

    #Sending get user records request, when user has no records
    response = client.get("/records", headers={"x-access-token": f"{token}"})
    expected_resoponse_message = f"Current user {new_user['id']} has no records"
    assert response.status_code == 404
    assert expected_resoponse_message.encode() in response.data and b"error"


#-------------------------------------EDIT RECORD TESTS (PATCH REQUEST)---------------
def test_edit_record_success(client, new_user, new_record):
    """
    Successful edit record request (PATCH)
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = db.session.query(models.User).get(new_user["id"]) 
    assert  new_user_got_from_db != None

    add_new_record_to_mock_db(new_user, new_record)
    new_record_got_from_db = db.session.query(models.Record).get(new_record["id"])
    assert db.session.query(models.Record).get(new_record["id"]) != None

    token = get_mock_token(new_user)

    #Sending put request with edited record
    edited_record = new_record.copy()
    
    edited_record["password"] += "x"
    edited_record["is_deleted"] = new_record_got_from_db.is_deleted
    edited_record["is_favorite"] =new_record_got_from_db.is_favorite

    response = client.put("/records", headers={"x-access-token": f"{token}"}, json=edited_record)
    expected_respones_message = f"Record {new_record['id']} changed successfully"
    assert response.status_code == 200
    assert expected_respones_message.encode() in response.data and b"success" in response.data
    assert db.session.query(models.Record).get(new_record["id"]).password == edited_record["password"]


def test_edit_record_fail_1(client, new_user, new_record):
    """
    Edit record fail, record with requested id doesn't exist
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = db.session.query(models.User).get(new_user["id"]) 
    assert  new_user_got_from_db != None

    token = get_mock_token(new_user)

    #Sending put request when user has no records, expecting unexisting record error
    new_record["is_favorite"] = False
    new_record["is_deleted"] = False
    response = client.put("/records", headers={"x-access-token": f"{token}"}, json=new_record)
    expected_respones_message = f"Record with id {new_record['id']}"
    assert response.status_code == 404
    assert expected_respones_message.encode() in response.data and b"error" in response.data


def test_edit_record_fail_2(client, new_user, new_record):
    """
    Record edit fail, record doesn't belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None

    add_new_record_to_mock_db(new_user, new_record)
    new_record_got_from_db = db.session.query(models.Record).get(new_record["id"])
    assert new_record_got_from_db != None

    token = get_mock_token(new_user)

    new_record_got_from_db.user_id += "x"
    db.session.commit()

    #Sending delete request, where record's user id changed so it doesn't belong to current user
    new_record["is_favorite"] = False
    new_record["is_deleted"] = False
    response = client.put("/records", headers={"x-access-token": f"{token}"}, 
                            json=new_record)

    expected_response_message = f"Record {new_record['id']} doesn't belong to the current user {new_user['id']}"
    assert response.status_code == 403
    assert expected_response_message.encode() in response.data and b"error" in response.data




