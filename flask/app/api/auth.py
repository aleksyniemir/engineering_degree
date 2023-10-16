from flask import Flask, jsonify, request, make_response, Blueprint
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from marshmallow import fields, ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime, timedelta
from dotenv import load_dotenv
from functools import wraps
import jwt
import os 
from flask_sqlalchemy import SQLAlchemy

from app.models.user import User
from app.schemas.user import user_schema, users_schema

bp = Blueprint('auth', __name__, url_prefix='/auth')
db = SQLAlchemy()  

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # TODO get token from header correctly
        token = request.args.get('token') 
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({"message": "Token is invalid!"}), 401
        
        return f(*args, **kwargs)
    return decorated

@bp.route("/login", methods = ['POST'])
def login():
    auth = request.json
    if not auth or not auth['username'] or not auth['password']:
       return jsonify({"message": "Could not verify!", "WWW-Authenticate": "Basic auth='Login required'"}), 401
    
    if auth['username'] != 'test' or auth['password'] != 'test':
        return jsonify({"message": "Could not verify!", "WWW-Authenticate": "Basic auth='Login required'"}), 401
    token = jwt.encode({
        'user': auth['username'], 
        'exp': datetime.utcnow() + timedelta(minutes=100000000)}, 
        app.config['SECRET_KEY'
    ])
    return jsonify({'token': token})