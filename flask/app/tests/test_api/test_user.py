from datetime import datetime
from app.models.user import User
from sqlalchemy import select
import json
import base64
import os


def test_get_users(client):
    response = client.get("/user/get_users")

    assert response.status_code == 200
    users = response.json
    assert isinstance(users, list)
    if users: 
        assert "nick" in users[0]
        assert "email" in users[0]  

def test_get_existing_user_by_id(client):
    user_id = 1 
    response = client.get(f"/user/get_user/{user_id}")

    assert response.status_code == 200
    user_data = response.json
    assert 'nick' in user_data
    assert 'email' in user_data

def test_get_non_existing_user_by_id(client):
    user_id = 99999 
    response = client.get(f"/user/get_user/{user_id}")

    assert response.status_code == 404  
    assert response.json == {"error": "User not found"}

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
        "email": "invalid_email_" + random_uid,  
        "password": "test_password"
    }

    response = client.post("/user/add_user", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert str(response.json) == "{'error': 'Not a valid email address'}"

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
    random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    data = {
        "nick": "test_user_" + random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    client.post("/user/add_user", data=json.dumps(data), content_type='application/json')

    new_random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    new_data = {
        "nick": "new_test_user_" + new_random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",  
        "password": "test_password"
    }

    response = client.post("/user/add_user", data=json.dumps(new_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {"error": "Email already in use"} 

def test_update_existing_user(client):
    user_id = 2
    random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    update_data = {
        "nick": "updated_nick" + random_uid,
        "email": "updated_email@gmail.com",  
    }

    response = client.put(f"/user/update_user/{user_id}", data=json.dumps(update_data), content_type='application/json')

    assert response.status_code == 200
    assert response.json["nick"] == update_data["nick"]
    assert response.json["email"] == update_data["email"]

def test_update_non_existing_user(client):
    user_id = 99999  
    update_data = {
        "nick": "updated_nick",
        "email": "updated_email@gmail.com",
    }

    response = client.put(f"/user/update_user/{user_id}", data=json.dumps(update_data), content_type='application/json')

    assert response.status_code == 404
    assert response.json == {'error': 'User not found'}

def test_update_user_with_invalid_data(client):
    user_id = 1 
    update_data = {
        "nick": "", 
        "email": "invalid_email",  
    }

    response = client.put(f"/user/update_user/{user_id}", data=json.dumps(update_data), content_type='application/json')

    assert response.status_code == 400
    assert response.json == {'email': ['Not a valid email address.'], 'nick': ['Shorter than minimum length 1.'], 'password': ['Password is required']}


def test_delete_existing_user(client, app):
    random_uid = base64.b64encode(os.urandom(32))[:8].decode()
    data = {
        "nick": "test_user_" + random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    user = client.post("/user/add_user", data=json.dumps(data), content_type='application/json')
    user_id = user.json["id"]

    response = client.delete(f"/user/delete_user/{user_id}")
    assert response.status_code == 200
    stmt = select(User).where(user_id == User.id)
    deleted_user = app.db.session.scalar(stmt)
    assert deleted_user is None
