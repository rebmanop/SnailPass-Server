import models
from models import db
from tests.utils import add_new_user_to_mock_db, get_mock_token, add_new_note_to_mock_db
from api.resource_fields import NOTE_RESOURCE_FIELDS

#-------------------------------------ADD NEW NOTE TESTS (POST REQUEST)---------------

def test_add_new_note_success(client, new_user, new_note):
    """
    Successful note creation
    """

    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    response = client.post("/notes", headers={"x-access-token": f"{token}"}, json=new_note)

    expected_response_message = f"Note {new_note['id']} created"
    assert response.status_code == 201
    assert expected_response_message.encode() in response.data and b"success" in response.data


def test_add_new_note_fail_1(client, new_user, new_note):
    """
    Note creation fail, note with recieved id already exists
    """

    add_new_user_to_mock_db(new_user)
    assert db.session.query(models.User).get(new_user["id"]) != None
    
    token = get_mock_token(new_user)
    response = client.post("/notes", headers={"x-access-token": f"{token}"}, json=new_note)
    assert response.status_code == 201
    
    #Sending second POST with same note to get 'note with that id already exists' error"
    response = client.post("/notes", headers={"x-access-token": f"{token}"}, json=new_note)
    
    expected_response_message = f"Note with id {new_note['id']} already exists"
    response.status_code == 409
    assert expected_response_message.encode() in response.data and b"error" in response.data
 


#-------------------------------------DELETE NOTE TESTS (DELETE REQUEST)---------------


def test_delete_note_success(client, new_user, new_note):
    """
    Successful delete note request
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None


    add_new_note_to_mock_db(new_user, new_note)
    assert db.session.query(models.Note).get(new_note["id"]) != None

    token = get_mock_token(new_user)

    #Sending delete request with note id as uri argument 
    response = client.delete("/notes", headers={"x-access-token": f"{token}"}, 
                            query_string={'id': new_note["id"]})
    
    expected_response_message = f"Note {new_note['id']} deleted successfully"
    assert response.status_code == 200
    assert expected_response_message.encode() in response.data and b"success" in response.data


def test_delete_note_fail_1(client, new_user):
    """
    Note delete fail, note id is missing in uri args
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None
    token = get_mock_token(new_user)

    #Sending delete request without note id as uri argument 
    response = client.delete("/notes", headers={"x-access-token": f"{token}"})
    
    assert response.status_code == 400
    assert b"Note id is missing in URI arguments" in response.data and b"error"


def test_delete_note_fail_2(client, new_user, new_note):
    """
    Note delete fail, not existing note id
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None

    token = get_mock_token(new_user)

    #Sending delete request with not existing note
    response = client.delete("/notes", headers={"x-access-token": f"{token}"}, 
                            query_string={'id': new_note["id"]})
    
    expected_response_message =f"Note with id {new_note['id']} doesn't exist"
    assert response.status_code == 404
    assert expected_response_message.encode() in response.data and b"error" in response.data


def test_delete_note_fail_3(client, new_user, new_note):
    """
    Note delete fail, note doesn't belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None

    add_new_note_to_mock_db(new_user, new_note)
    new_note_got_from_db = db.session.query(models.Note).get(new_note["id"])
    assert new_note_got_from_db != None

    token = get_mock_token(new_user)

    new_note_got_from_db.user_id += "x"
    db.session.commit()

    #Sending delete request, where notes's user id changed so it doesn't belong to current user
    response = client.delete("/notes", headers={"x-access-token": f"{token}"}, 
                            query_string={'id': new_note["id"]})
    
    expected_response_message = f"Note {new_note['id']} doesn't belong to the current user {new_user['id']}"
    assert response.status_code == 403
    assert expected_response_message.encode() in response.data and b"error" in response.data


#-------------------------------------GET CURRENT USER NOTES TESTS (GET REQUEST)---------------
def test_get_records_success(client, new_user, new_note):
    """
    Successful get user notes request
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = db.session.query(models.User).get(new_user["id"]) 
    assert  new_user_got_from_db != None

    add_new_note_to_mock_db(new_user, new_note)
    assert db.session.query(models.Note).get(new_note["id"]) != None

    new_note_2 = new_note.copy()
    new_note_2["id"] += "x"
    new_note_2["name"] += "x"
    add_new_note_to_mock_db(new_user, new_note_2)
    assert db.session.query(models.Note).get(new_note_2["id"]) != None

    token = get_mock_token(new_user)

    #Sending get user notes request
    response = client.get("/notes", headers={"x-access-token": f"{token}"})
    assert response.status_code == 200
    import json
    list_of_notes = json.loads(response.data.decode('utf-8'))
    assert len(list_of_notes) == 2
    assert len(NOTE_RESOURCE_FIELDS) == len(list_of_notes[0])


def test_get_note_fail(client, new_user):
    """
    Get user notes request fail, user has no notes
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = db.session.query(models.User).get(new_user["id"]) 
    assert  new_user_got_from_db != None

    token = get_mock_token(new_user)

    #Sending get user notes request, when user has no notes
    response = client.get("/notes", headers={"x-access-token": f"{token}"})
    expected_resoponse_message = f"Current user {new_user['id']} has no notes"
    assert response.status_code == 404
    assert expected_resoponse_message.encode() in response.data and b"error" in response.data


#-------------------------------------EDIT NOTE TESTS (PATCH REQUEST)---------------
def test_edit_note_success(client, new_user, new_note):
    """
    Successful edit note request (PATCH)
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = db.session.query(models.User).get(new_user["id"]) 
    assert  new_user_got_from_db != None

    add_new_note_to_mock_db(new_user, new_note)
    new_note_got_from_db = db.session.query(models.Note).get(new_note["id"])
    assert new_note_got_from_db != None

    token = get_mock_token(new_user)

    #Sending put request with edited note
    edited_note = new_note.copy()
    
    edited_note["content"] += "x"
    edited_note["is_deleted"] = new_note_got_from_db.is_deleted
    edited_note["is_favorite"] =new_note_got_from_db.is_favorite

    response = client.put("/notes", headers={"x-access-token": f"{token}"}, json=edited_note)
    expected_respones_message = f"Note {new_note['id']} changed successfully"
    assert response.status_code == 200
    assert expected_respones_message.encode() in response.data and b"success" in response.data
    assert db.session.query(models.Note).get(new_note["id"]).content == edited_note["content"]


def test_edit_note_fail_1(client, new_user, new_note):
    """
    Edit note fail, note with requested id doesn't exist
    """
    add_new_user_to_mock_db(new_user)
    new_user_got_from_db = db.session.query(models.User).get(new_user["id"]) 
    assert  new_user_got_from_db != None

    token = get_mock_token(new_user)

    #Sending put request when user has notes, expecting unexisting note error
    new_note["is_favorite"] = False
    new_note["is_deleted"] = False
    response = client.put("/notes", headers={"x-access-token": f"{token}"}, json=new_note)
    expected_respones_message = f"Note with id {new_note['id']} doesn't exist"
    assert response.status_code == 404
    assert expected_respones_message.encode() in response.data and b"error" in response.data


def test_edit_note_fail_2(client, new_user, new_note):
    """
    Note edit fail, note doesn't belong to the current user
    """
    add_new_user_to_mock_db(new_user)
    assert  db.session.query(models.User).get(new_user["id"]) != None

    add_new_note_to_mock_db(new_user, new_note)
    new_note_got_from_db = db.session.query(models.Note).get(new_note["id"])
    assert new_note_got_from_db != None

    token = get_mock_token(new_user)

    new_note_got_from_db.user_id += "x"
    db.session.commit()

    #Sending delete request, where note's user id changed so it doesn't belong to current user
    new_note["is_favorite"] = False
    new_note["is_deleted"] = False
    response = client.put("/notes", headers={"x-access-token": f"{token}"}, 
                            json=new_note)

    expected_response_message = f"Note {new_note['id']} doesn't belong to the current user {new_user['id']}"
    assert response.status_code == 403
    assert expected_response_message.encode() in response.data and b"error" in response.data
