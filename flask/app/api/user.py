from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import re

from app import db

from app.models.user import User
import app.crud.user as crud
from app.schemas.user import *
import app.utils.validators as validators

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route("/get_users", methods = ['GET'])
def get_users():
    users = crud.get_users(db.session)
    return users_schema.jsonify(users)

@bp.route("/get_user/<id>", methods = ['GET'])
def get_user(id):
    user = crud.get_user_by_id(db.session, id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return user_schema.jsonify(user)

@bp.route("/add_user", methods = ['POST'])
def add_user():
    try:
        user_dict = user_schema_create.load(request.json)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return jsonify(err.messages), 400
    
    if not validators.check_email_regex(user_dict["email"]):
        return jsonify({"error": "Not a valid email address"}), 400
        
    if crud.get_user_by_email(db.session, user_dict["email"]):
        return jsonify({"error": "Email already in use"}), 400

    if crud.get_user_by_nick(db.session, user_dict["nick"]):
        return jsonify({"error": "Nickname already in use"}), 400

    user = crud.add_user(db.session, user_dict)
    return user_schema.jsonify(user)

@bp.route("/update_user/<id>", methods = ['PUT'])
def update_user(id):
    user = crud.get_user_by_id(db.session, id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        user_dict = user_schema_update.load(request.json)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return jsonify(err.messages), 400
    
    user = crud.update_user(db.session, id, user_dict)
    return user_schema_update.jsonify(user)

@bp.route("/delete_user/<id>", methods = ['DELETE'])
def delete_user(id):
    message = crud.delete_user(db.session, id)
    return message
