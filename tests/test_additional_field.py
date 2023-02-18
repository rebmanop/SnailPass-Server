import models
from models import db
from tests.utils import add_new_user_to_mock_db, get_mock_token, add_new_record_to_mock_db, add_new_additional_field_to_mock_db
from api.resource_fields import ADDITIONAL_FIELD_RESOURCE_FIELDS


#-------------------------------------ADD NEW ADDITIONAL FIELD TESTS (POST REQUEST)---------------

def test_add_new_additional_field_success(client, new_user, new_record, new_additional_field):
    """
    Successful additional field creation
    """
    
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"])

    token = get_mock_token(new_user)
    
    #Sending post request with new additional field
    new_additional_field["record_id"] = new_record["id"]
    response = client.post("/additional_fields", headers={"x-access-token": f"{token}"}, json=new_additional_field)

    expected_response_message = f"Additional field {new_additional_field['id']} created"
    assert response.status_code == 201
    assert expected_response_message.encode() in response.data and b"success" in response.data


def test_add_new_additional_field_fail_1(client, new_user, new_record, new_additional_field):
    """
    Additional field creation fail, record of requested additional field doesn't exist
    """

    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"])

    token = get_mock_token(new_user)
    #Sending post request with new additional field and not existing record id in it
    new_additional_field["record_id"] = new_record["id"] + "x"
    response = client.post("/additional_fields", headers={"x-access-token": f"{token}"}, json=new_additional_field)
    expected_response_message = f"Record with id {new_additional_field['record_id']} doesn't exist"
    assert response.status_code == 404
    assert expected_response_message.encode() in response.data and b"error" in response.data


def test_add_new_additional_field_fail_2(client, new_user, new_record, new_additional_field):
    """
    Additional field creation fail, record id of requested additional field doesn't 
    belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    record_got_from_db = db.session.query(models.Record).get(new_record["id"])
    assert record_got_from_db != None

    record_got_from_db.user_id += "x"
    db.session.commit()

    token = get_mock_token(new_user)

    new_additional_field["record_id"] = new_record["id"] 
    response = client.post("/additional_fields", headers={"x-access-token": f"{token}"}, json=new_additional_field)

    expected_response_message = f"Record {new_record['id']} doesn't belong to the current user {new_user['id']}"

    assert response.status_code == 403
    assert expected_response_message.encode() in response.data and b"error" in response.data



def test_add_new_additional_field_fail_3(client, new_user, new_record, new_additional_field):
    """
    Additional field creation fail, af with that id already exists
    """
    
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"])

    token = get_mock_token(new_user)
    
    #Sending additional field post twice to get "af field with that id already exists error"
    new_additional_field["record_id"] = new_record["id"]
    response = client.post("/additional_fields", headers={"x-access-token": f"{token}"}, json=new_additional_field)
    response = client.post("/additional_fields", headers={"x-access-token": f"{token}"}, json=new_additional_field)

    expected_response_message = f"Additional field with id {new_additional_field['id']} already exists"
    assert response.status_code == 409
    assert expected_response_message.encode() in response.data and b"error" in response.data



#-------------------------------------DELETE ADDITIONAL FIELD TESTS (DELETE REQUEST)---------------

def test_delete_additional_field_success(client, new_user, new_record, new_additional_field):
    """
    Successful additional field delete
    """
    
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"])

    add_new_additional_field_to_mock_db(new_record, new_additional_field)
    assert db.session.query(models.AdditionalField).get(new_additional_field["id"])

    token = get_mock_token(new_user)
    
    #Sending delete request with new additional field id
    response = client.delete("/additional_fields", headers={"x-access-token": f"{token}"}, query_string={'id': new_additional_field["id"]})

    expected_response_message = f"Additional field {new_additional_field['id']} deleted successfully"
    assert response.status_code == 200
    assert expected_response_message.encode() in response.data and b"success" in response.data


def test_delete_additional_field_fail_1(client, new_user):
    """
    Additional field delete fail, id is missing in uri arguments
    """
    
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    token = get_mock_token(new_user)
    
    #Sending delete request without new additional field id
    response = client.delete("/additional_fields", headers={"x-access-token": f"{token}"})

    assert response.status_code == 400
    assert b"Additional field id is missing in URI arguments" in response.data and b"error" in response.data


def test_delete_additional_field_fail_2(client, new_user, new_additional_field):
    """
    Additional field delete fail, af with requested id doesn't exist
    """
    
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    token = get_mock_token(new_user)
    
    #Sending delete request with not existsing af id
    response = client.delete("/additional_fields", headers={"x-access-token": f"{token}"}, query_string={'id': new_additional_field["id"]})
    expected_response_message = f"Additional field with id {new_additional_field['id']} doesn't exist"
    assert response.status_code == 404
    assert expected_response_message.encode() in response.data and b"error" in response.data


def test_delete_additional_field_fail_3(client, new_user, new_record, new_additional_field):
    """
    Additional fields delete fail, af doesn't belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    record_got_from_db = db.session.query(models.Record).get(new_record["id"])
    assert record_got_from_db != None

    add_new_additional_field_to_mock_db(new_record, new_additional_field)
    assert db.session.query(models.AdditionalField).get(new_additional_field["id"])

    token = get_mock_token(new_user)

    record_got_from_db.user_id += "x"
    db.session.commit()
    
    #Sending put additional field request when af's record doesn't belong to the current user
    new_additional_field["record_id"] = new_record["id"] 
    response = client.delete("/additional_fields", headers={"x-access-token": f"{token}"}, query_string={'id': new_additional_field["id"]})
    expected_response_message = f"Additional field {new_additional_field['id']} doesn't belong to the current user {new_user['id']}"
    assert response.status_code == 403
    assert expected_response_message.encode() in response.data and b"error" in response.data


#-------------------------------------GET RECORDS ADDITIONAL FIELDS TESTS (GET REQUEST)---------------


def test_get_additional_fields_success(client, new_user, new_record, new_additional_field):
    """
    Successful additional fields get
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"])

    add_new_additional_field_to_mock_db(new_record, new_additional_field)
    assert db.session.query(models.AdditionalField).get(new_additional_field["id"])

    new_additional_field_2 = new_additional_field.copy()
    new_additional_field_2["id"] += "x"
    new_additional_field_2["name"] += "x"
    add_new_additional_field_to_mock_db(new_record, new_additional_field_2)
    assert db.session.query(models.AdditionalField).get(new_additional_field_2["id"]) != None

    token = get_mock_token(new_user)
    
    #Sending get user additional fields with record id as uri argument
    response = client.get("/additional_fields", headers={"x-access-token": f"{token}"}, query_string={"id": f"{new_record['id']}"})
    assert response.status_code == 200
    import json
    list_of_notes = json.loads(response.data.decode('utf-8'))
    assert len(list_of_notes) == 2
    assert len(ADDITIONAL_FIELD_RESOURCE_FIELDS) == len(list_of_notes[0])


def test_get_additional_fields_fail_1(client, new_user):
    """
    Additional fields get fail, record id is missing in uri args
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    token = get_mock_token(new_user)
    
    #Sending get user additional fields without record id as uri argument
    response = client.get("/additional_fields", headers={"x-access-token": f"{token}"})
    assert response.status_code == 400
    assert b"Record id is missing in URI arguments" in response.data and b"error" in response.data


def test_get_additional_fields_fail_2(client, new_user, new_record):
    """
    Additional fields get fail, not existing record id
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    token = get_mock_token(new_user)
    
    #Sending get user additional fields with not existing record id
    response = client.get("/additional_fields", headers={"x-access-token": f"{token}"}, query_string={"id": f"{new_record['id']}"})
    expected_response_message = f"Record with id {new_record['id']} doesn't exist"
    assert response.status_code == 404
    assert expected_response_message.encode() in response.data and b"error" in response.data


def test_get_additional_fields_fail_3(client, new_user, new_record):
    """
    Additional fields get fail, record doesnt't belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    record_got_from_db = db.session.query(models.Record).get(new_record["id"])
    assert record_got_from_db != None

    token = get_mock_token(new_user)

    record_got_from_db.user_id += "x"
    db.session.commit()
    
    #Sending get user additional fields when record of an af doesn't belong to the current user
    response = client.get("/additional_fields", headers={"x-access-token": f"{token}"}, query_string={"id": f"{new_record['id']}"})
    expected_response_message = f"Record {new_record['id']} doesn't belong to the current user {new_user['id']}"
    assert response.status_code == 403
    assert expected_response_message.encode() in response.data and b"error" in response.data


def test_get_additional_fields_fail_4(client, new_user, new_record, new_additional_field):
    """
    Additional fields get fail, record has no additional fields
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"])

    token = get_mock_token(new_user)
    
    #Sending get user additional fields when record has no afs
    response = client.get("/additional_fields", headers={"x-access-token": f"{token}"}, query_string={"id": f"{new_record['id']}"})
    expected_response_message = f"Current user's {new_user['id']} record {new_record['id']}  has no additional fields"
    assert response.status_code == 404
    assert expected_response_message.encode() in response.data and b"error" in response.data


#-------------------------------------PATCH ADDITIONAL FIELDS TESTS (GET REQUEST)---------------
def test_edit_additional_field_success(client, new_user, new_record, new_additional_field):
    """
    Successful additional fields edit (PATCH)
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"])

    add_new_additional_field_to_mock_db(new_record, new_additional_field)
    assert db.session.query(models.AdditionalField).get(new_additional_field["id"])

    edited_additional_field = new_additional_field.copy()
    edited_additional_field["record_id"] = new_record["id"]
    edited_additional_field["value"] += "x"

    token = get_mock_token(new_user)
    
    #Sending put additional field request 
    response = client.put("/additional_fields", headers={"x-access-token": f"{token}"}, json=edited_additional_field)
    expected_response_message = f"Additional field {new_additional_field['id']} changed successfully"
    assert response.status_code == 200
    assert expected_response_message.encode() in response.data and b"success" in response.data


def test_edit_additional_field_fail_1(client, new_user, new_record, new_additional_field):
    """
    Edit additional field fail, additional field with requested id doesn't exist
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    assert db.session.query(models.Record).get(new_record["id"])

    
    token = get_mock_token(new_user)
    
    #Sending put additional field request, when there is no af with that id in db 
    new_additional_field["record_id"] = new_record["id"]
    response = client.put("/additional_fields", headers={"x-access-token": f"{token}"}, json=new_additional_field)
    expected_response_message = f"Additional field with id {new_additional_field['id']} doesn't exist"
    assert response.status_code == 404
    assert expected_response_message.encode() in response.data and b"error" in response.data


def test_edit_additional_field_fail_3(client, new_user, new_record, new_additional_field):
    """
    Additional fields edit fail, af doesn't belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"])

    add_new_record_to_mock_db(new_user, new_record)
    record_got_from_db = db.session.query(models.Record).get(new_record["id"])
    assert record_got_from_db != None

    add_new_additional_field_to_mock_db(new_record, new_additional_field)
    assert db.session.query(models.AdditionalField).get(new_additional_field["id"])

    token = get_mock_token(new_user)

    record_got_from_db.user_id += "x"
    db.session.commit()
    
    #Sending put additional field request when af's record doesn't belong to the current user
    new_additional_field["record_id"] = new_record["id"] 
    response = client.put("/additional_fields", headers={"x-access-token": f"{token}"}, json=new_additional_field)
    expected_response_message = f"Additional field {new_additional_field['id']} doesn't belong to the current user {new_user['id']}"
    assert response.status_code == 403
    assert expected_response_message.encode() in response.data and b"error" in response.data