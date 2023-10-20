from datetime import datetime
import json
import base64
import os

def test_add_user(client):
    random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    data = {
        "nick": "test_user_" + random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",
        "password": "test_password"
    }

    response = client.post("/user/add_user", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json["nick"] == data["nick"]
    assert response.json["email"] == data["email"]
    # TODO make a hash of password
    assert response.json["password"] == data["password"]  

def test_add_user_with_invalid_email(client):
    random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    data = {
        "nick": "test_user_" + random_uid,
        "email": "invalid_email_" + random_uid,  # Missing domain part, making it an invalid email
        "password": "test_password"
    }

    response = client.post("/user/add_user", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {'error': 'Not a valid email address.'}

def test_add_user_with_existing_nick(client):
    random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    data = {
        "nick": "test_user_" + random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    client.post("/user/add_user", data=json.dumps(data), content_type='application/json')

    new_random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    new_data = {
        "nick": "test_user_" + random_uid,  # Using the same nickname
        "email": "new_test_email_" + new_random_uid + "@gmail.com",
        "password": "test_password"
    }

    response = client.post("/user/add_user", data=json.dumps(new_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {"error": "Nickname already in use"}  # Adjust the error message based on your actual API response

def test_add_user_with_existing_email(client):
    # Creating a user for the first time
    random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    data = {
        "nick": "test_user_" + random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    client.post("/user/add_user", data=json.dumps(data), content_type='application/json')

    # Trying to create another user with the same email
    new_random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    new_data = {
        "nick": "new_test_user_" + new_random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",  # Using the same email
        "password": "test_password"
    }

    response = client.post("/user/add_user", data=json.dumps(new_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {"error": "Email already in use"}  # Adjust the error message based on your actual API response
