from random import randint

import app.crud.user as crud
from app import db

def test_get_users():
    users = crud.get_users(db.session)
    assert isinstance(users, list)

def test_get_user_by_id():
    random_uid = str(randint(0,999999))
    user_data = {
        "nick": "unique_nick" + random_uid,
        "email": "unique_email" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    created_user = crud.add_user(db.session, user_data)
    
    user = crud.get_user_by_id(db.session, created_user.id)
    assert user.id == created_user.id
    assert user.nick == user_data["nick"]

def test_get_user_by_nick():
    random_uid = str(randint(0,999999))
    user_data = {
        "nick": "unique_nick" + random_uid,
        "email": "unique_email" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    crud.add_user(db.session, user_data)

    user = crud.get_user_by_nick(db.session, user_data["nick"])
    assert user.nick == user_data["nick"]

def test_get_user_by_email():
    random_uid = str(randint(0,999999))
    user_data = {
        "nick": "unique_nick" + random_uid,
        "email": "unique_email" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    crud.add_user(db.session, user_data)

    user = crud.get_user_by_email(db.session, user_data["email"])
    assert user.email == user_data["email"]

def test_add_user():
    random_uid = str(randint(0,999999))
    user_data = {
        "nick": "unique_nick" + random_uid,
        "email": "unique_email" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    added_user = crud.add_user(db.session, user_data)
    assert added_user.nick == user_data["nick"]
    assert added_user.email == user_data["email"]

def test_update_user():
    random_uid = str(randint(0,999999))
    user_data = {
        "nick": "unique_nick" + random_uid,
        "email": "unique_email" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    original_user = crud.add_user(db.session, user_data)

    new_random_uid = str(randint(0,999999))
    updated_data = {
        "nick": "unique_nick" + new_random_uid,
        "email": "unique_email" + new_random_uid + "@gmail.com",
        "password": "test_password" + new_random_uid
    }
    updated_user = crud.update_user(db.session, original_user.id, updated_data)

    assert updated_user.nick == updated_data["nick"]
    assert updated_user.email == updated_data["email"]

def test_delete_user():
    user_data = {
        "nick": "to_be_deleted",
        "email": "to_be_deleted@gmail.com",
        "password": "test_password"
    }
    user_to_delete = crud.add_user(db.session, user_data)
    crud.delete_user(db.session, user_to_delete.id)

    assert crud.get_user_by_id(db.session, user_to_delete.id) is None
