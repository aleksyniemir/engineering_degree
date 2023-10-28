import json
import jwt

def test_login_missing_fields(client):
    response = client.post('/auth/login', json={})
    assert response.status_code == 401
    assert response.json['message'] == "Could not verify!"
    assert response.json['WWW-Authenticate'] == "Basic auth='Login required'"

def test_login_wrong_credentials(client):
    wrong_data = {
        'username': 'wrong',
        'password': 'wrong'
    }
    response = client.post('/auth/login', json=wrong_data)
    assert response.status_code == 401
    assert response.json['message'] == "Could not verify!"

def test_login_correct_credentials(client, app):
    correct_data = {
        'username': 'test',
        'password': 'test'
    }
    response = client.post('/auth/login', json=correct_data)
    assert response.status_code == 200
    
    token_data = json.loads(response.data)
    assert 'token' in token_data
    
    decoded_token = jwt.decode(token_data['token'], app.config['SECRET_KEY'], algorithms=["HS256"])
    assert decoded_token['user'] == 'test'
