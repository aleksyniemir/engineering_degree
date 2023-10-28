import json
import jwt
from random import randint

def test_login_missing_fields(client):
    response = client.post('/auth/login', json={})
    assert response.status_code == 401
    assert response.json['message'] == "Could not verify!"
    assert response.json['WWW-Authenticate'] == "Basic auth='Login required'"

def test_login_no_credentials(client):
    response = client.post('/auth/login', json={})

    assert response.status_code == 401
    assert response.json['message'] == "Could not verify!"
    assert response.json['WWW-Authenticate'] == "Basic auth='Login required'"


def test_login_wrong_nick(client):
    wrong_data = {
        'nick': 'wrong',
        'password': 'wrong'
    }
    response = client.post('/auth/login', json=wrong_data)
    assert response.status_code == 401
    assert response.json['message'] == "Invalid user or password!"

def test_login_wrong_password(client):
    wrong_data = {
        'nick': 'test_user',
        'password': 'wrong'
    }
    response = client.post('/auth/login', json=wrong_data)
    assert response.status_code == 401
    assert response.json['message'] == "Invalid user or password!"

def test_login_correct_credentials(client, app):
    correct_data = {
        'nick': 'test_user',
        'password': 'test_password'
    }
    response = client.post('/auth/login', json=correct_data)
    assert response.status_code == 200
    
    token_data = json.loads(response.data)
    assert 'token' in token_data
    
    decoded_token = jwt.decode(token_data['token'], app.config['SECRET_KEY'], algorithms=["HS256"])
    assert decoded_token['user'] == 'test_user'

def test_sign_up_missing_fields(client):
    response = client.post('/auth/sign_up', json={})
    assert response.status_code == 400
    assert response.json['message'] == "Missing required fields!"

def test_sign_up_invalid_email(client):
    data = {
        'nick': 'test_user2',
        'password': 'test_password2',
        'email': 'invalidEmail'
    }
    response = client.post('/auth/sign_up', json=data)
    assert response.status_code == 400
    assert response.json['error'] == "Not a valid email address"

def test_sign_up_email_in_use(client):
    existing_user_data = {
        'nick': 'test_user',
        'password': 'test_password',
        'email': 'test_email@email.com'
    }
    response = client.post('/auth/sign_up', json=existing_user_data)
    assert response.status_code == 400
    assert response.json['error'] == "Email already in use"

def test_sign_up_nick_in_use(client):
    existing_user_data = {
        'nick': 'test_user',
        'password': 'test_password2',
        'email': 'test_user111111111@example.com'
    }
    response = client.post('/auth/sign_up', json=existing_user_data)
    assert response.status_code == 400
    assert response.json['error'] == "Nickname already in use"

def test_sign_up_successful(client, app):
    random_uid = str(randint(0,999999))
    new_user_data = {
        'nick': 'test_user' + random_uid,
        'password': 'new_test_password' + random_uid,
        'email': 'new_test_user'+ random_uid +'@example.com'
    }
    response = client.post('/auth/sign_up', json=new_user_data)
    assert response.status_code == 201
    assert response.json['message'] == "User registered successfully!"
    assert 'token' in response.json
    token_data = response.json['token']
    decoded_token = jwt.decode(token_data, app.config['SECRET_KEY'], algorithms=["HS256"])
    assert decoded_token['user'] == 'test_user' + random_uid

def test_logout_successful(client):
    #TODO after logout logic is implemented
    response = client.post('/auth/logout')
    assert response.status_code == 200
    assert response.json['message'] == "Logged out successfully!"
