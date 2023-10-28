import pytest
import jwt
from datetime import datetime, timedelta
from flask import current_app

from app import create_app, db

@pytest.fixture()
def app():
    app = create_app(test_config=True)
    with app.app_context():
        db.create_all()  
        yield app
        db.session.remove()

    
@pytest.fixture()
def client(app):
    return app.test_client()

# conftest.py

@pytest.fixture()
def headers():
    token = jwt.encode(
        {
            'user': "test_user", 
            'exp': datetime.utcnow() + timedelta(minutes=100000000)
        }, 
        current_app.config['SECRET_KEY']
        )
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    return headers
