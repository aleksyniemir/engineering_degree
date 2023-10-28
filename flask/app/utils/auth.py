from flask import jsonify, request, Blueprint, current_app, g
from datetime import datetime, timedelta
from functools import wraps
import jwt

from app import db
import app.crud.user as crud

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # TODO get token from header correctly
        token = request.args.get('token') 
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
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
    if user.nick == "admin" or user.id == user_id:
        return user
    return None