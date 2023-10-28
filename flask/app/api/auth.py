from flask import jsonify, request, Blueprint, current_app, g
from datetime import datetime, timedelta
from functools import wraps
import jwt

from app import db
import app.crud.user as crud

bp = Blueprint('auth', __name__, url_prefix='/auth')

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

@bp.route("/login", methods = ['POST'])
def login():
    auth = request.json
    if not auth or not auth['nick'] or not auth['password']:
       return jsonify({"message": "Could not verify!", "WWW-Authenticate": "Basic auth='Login required'"}), 401
    
    user = crud.get_user_by_nick(db.session, auth['nick'])
    if not user:
        return jsonify({"message": "Invalid user or password!"}), 401

    if not user.verify_password(auth['password']):
        return jsonify({"message": "Invalid user or password!"}), 401

    token = jwt.encode(
        {
            'user': auth['nick'], 
            'exp': datetime.utcnow() + timedelta(minutes=100000000)
        }, 
        current_app.config['SECRET_KEY']
        )
    return jsonify({'token': token})

bp.route("/sign_up")
def sign_up(): ...

@bp.route("/logout")
def logout(): ...