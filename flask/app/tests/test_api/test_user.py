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
    assert response.status_code == 401