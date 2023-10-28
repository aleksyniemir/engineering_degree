import pytest
import jwt
from datetime import datetime, timedelta
from flask import current_app, g
from random import randint

import app.crud.user as crud
from app import create_app, db

@pytest.fixture()
def app():
    app = create_app(test_config=True)
    with app.app_context():
        db.create_all()
        # adding test user
        crud.add_user(
            db.session, 
            {   "nick":"test_user", 
                "email":"test_email@email.com", 
                "password":"test_password"}
            )
        # adding test admin
        crud.add_user(
            db.session, 
            {   "nick":"admin", 
                "email":"admin@admin.com", 
                "password":"test_password"}
            )
        yield app
        db.session.remove()
        db.drop_all()

    
@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def headers():
    random_uid = str(randint(0,999999))
    data = {
        "nick": "test_user_" + random_uid,
        "email": "test_email_" + random_uid + "@gmail.com",
        "password": "test_password"
    }
    user = crud.add_user(db.session, data)
    token = jwt.encode(
        {
            'user': user.nick, 
            'exp': datetime.utcnow() + timedelta(minutes=100000000)
        }, 
        current_app.config['SECRET_KEY']
        )
    g.current_user_nick = user.nick
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return headers

@pytest.fixture()
def admin_headers():
    token = jwt.encode(
        {
            'user': "admin", 
            'exp': datetime.utcnow() + timedelta(minutes=100000000)
        }, 
        current_app.config['SECRET_KEY']
        )
    g.current_user_nick = "admin"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return headers
