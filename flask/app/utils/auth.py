import jwt
from flask import jsonify, request, current_app, g
from datetime import datetime, timedelta
from functools import wraps

import app.crud.user as crud
from app import db

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.authorization.token
        if not request.authorization.token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(
                jwt=token, 
                key=current_app.config['SECRET_KEY'],
                algorithms=["HS256"]
                )
            g.current_user_nick = data['user']
        except:
            return jsonify({"message": "Token is invalid!"}), 401
        
        return f(*args, **kwargs)
    return decorated

def get_current_user():
    user = crud.get_user_by_nick(db.session, g.current_user_nick)
    return user

def check_if_admin():
    user = get_current_user()
    if user.nick == "admin":
        return user
    return None

def check_if_admin_or_current_user(user_id: int):
    user = get_current_user()
    if user.nick == "admin" or user.id == int(user_id):
        return user
    return None

def get_token(nick: str):
    token = jwt.encode(
        {
            'user': nick, 
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, 
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
        )
    return token