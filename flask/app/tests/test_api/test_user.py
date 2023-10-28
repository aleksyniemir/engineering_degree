from app.models.user import User
from sqlalchemy import select
import json
import base64
import os
import pytest
from random import randint

from app import db

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

    random_uid = str(randint(0,999999))
    data = {
        "nick": "test_user_" + random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",
        "password": "test_password"
    }

    response = client.post("/user/add_user", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json["nick"] == data["nick"]
    assert response.json["email"] == data["email"]  
    assert isinstance(response.json["id"], int)

def test_add_user_with_invalid_email(client):
    random_uid = str(randint(0,999999))
    data = {
        "nick": "test_user_" + random_uid,
        "email": "invalid_email_" + random_uid,  
        "password": "test_password"
    }

    response = client.post("/user/add_user", data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert str(response.json) == "{'error': 'Not a valid email address'}"

def test_add_user(client):
    random_uid = str(randint(0,999999))
    user_data = {
    "nick": "test_user" + random_uid,
    "email": "test" + random_uid + "@example.com",
    "password": "test_password"
}
    response = client.post("/user/add_user", json=user_data)
    data = response.get_json()

    assert response.status_code == 200
    assert "email" in data and data["email"] == user_data["email"]
    assert "nick" in data and data["nick"] == user_data["nick"]


def test_add_user_with_existing_nick(client):
    random_uid = str(randint(0,999999))
    data = {
        "nick": "test_user_" + random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    client.post("/user/add_user", data=json.dumps(data), content_type='application/json')

    new_random_uid = str(randint(0,999999))
    new_data = {
        "nick": "test_user_" + random_uid, 
        "email": "new_test_email_" + new_random_uid + "@gmail.com",
        "password": "test_password"
    }

    response = client.post("/user/add_user", data=json.dumps(new_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {"error": "Nickname already in use"}  
    
def test_add_user_with_existing_email(client):
    random_uid = str(randint(0,999999))
    data = {
        "nick": "test_user_" + random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    client.post("/user/add_user", data=json.dumps(data), content_type='application/json')

    new_random_uid = str(randint(0,999999))
    new_data = {
        "nick": "new_test_user_" + new_random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",  
        "password": "test_password"
    }
    response = client.post("/user/add_user", data=json.dumps(new_data), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {"error": "Email already in use"} 


add_user_data = [
    ("user", "email@email.com", None, {'password': ['Password is required']}, 400),
    ("nick", None, "password",  {'email': ['Email is required']}, 400),
    ("nick", "email@email.com", "pass", {'password': ['Shorter than minimum length 8.']}, 400),
    ("", "email@email.com", "password", {'nick': ['Nickname is required']}, 400),
]
@pytest.mark.parametrize("nick,email,password,message,error_code", add_user_data)
def test_add_user_with_invalid_data(nick, email, password, message, error_code, client):
    data = {}
    if nick:
        data["nick"] = nick
    if email:
        data["email"] = email
    if password:
        data["password"] = password


    response = client.post("/user/add_user", data=json.dumps(data), content_type='application/json')
    assert response.status_code == error_code
    assert response.json == message



def test_update_existing_user(client):
    user_id = 2
    random_uid = str(randint(0,999999))
    update_data = {
        "nick": "updated_nick" + random_uid,
        "email": "updated_email@gmail.com",  
    }

    response = client.put(f"/user/update_user/{user_id}", data=json.dumps(update_data), content_type='application/json')

    assert response.status_code == 200
    assert response.json["nick"] == update_data["nick"]
    assert response.json["email"] == update_data["email"]


update_user_data = [
    (None, "email", None, 2, {'error': 'Not a valid email address'}, 400),
    ("nick", None, None, 999999, {'error': 'User not found'}, 404),
    (None, None, "short", 2, {'password': ['Shorter than minimum length 8.']}, 400),
]
@pytest.mark.parametrize("nick,email,password,user_id,message,error_code", update_user_data)
def test_update_user_with_invalid_data(nick, email, password, user_id, message, error_code, client):
    update_data = {}
    if nick:
        update_data["nick"] = nick
    if email:
        update_data["email"] = email
    if password:
        update_data["password"] = password

    response = client.put(f"/user/update_user/{user_id}", data=json.dumps(update_data), content_type='application/json')

    assert response.status_code == error_code
    assert response.json == message

def test_delete_existing_user(client):
    random_uid = str(randint(0,999999))
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
    deleted_user = db.session.scalar(stmt)
    assert deleted_user is None

def test_delete_non_existing_user(client):
    user_id = 9999999   

    response = client.delete(f"/user/delete_user/{user_id}")
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}