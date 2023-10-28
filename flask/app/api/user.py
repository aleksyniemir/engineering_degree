from flask import jsonify, request, Blueprint
from marshmallow import ValidationError

from app import db
import app.crud.user as crud
import app.utils.validators as validators
import app.utils.auth as auth
from app.schemas.user import *
from app.utils.auth import token_required

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route("/get_users", methods = ['GET'])
@token_required
def get_users():
    if not auth.check_if_admin():
        return jsonify({"error": "You do not have enough permissions"}), 401
    users = crud.get_users(db.session)
    return users_schema.jsonify(users)

@token_required
@bp.route("/get_user/<id>", methods = ['GET'])
def get_user(id: int):
    if not auth.check_if_admin_or_current_user(id):
        return jsonify({"error": "You do not have enough permissions"}), 401
    user = crud.get_user_by_id(db.session, id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return user_schema.jsonify(user)

@token_required
@bp.route("/add_user", methods = ['POST'])
def add_user():
    if not auth.check_if_admin():
        return jsonify({"error": "You do not have enough permissions"}), 401
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

@token_required
@bp.route("/update_user/<id>", methods = ['PUT'])
def update_user(id: int):
    if not auth.check_if_admin_or_current_user(id):
        return jsonify({"error": "You do not have enough permissions"}), 401
    
    user = crud.get_user_by_id(db.session, id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        user_dict = user_schema_update.load(request.json)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return jsonify(err.messages), 400
    
    if "email" in user_dict:
        if not validators.check_email_regex(user_dict["email"]):
            return jsonify({"error": "Not a valid email address"}), 400
            
        if crud.get_user_by_email(db.session, user_dict["email"]):
            return jsonify({"error": "Email already in use"}), 400

    if "nick" in user_dict:
        if crud.get_user_by_nick(db.session, user_dict["nick"]):
            return jsonify({"error": "Nickname already in use"}), 400
        
    user = crud.update_user(db.session, id, user_dict)
    return user_schema_update.jsonify(user)

@token_required
@bp.route("/delete_user/<id>", methods = ['DELETE'])
def delete_user(id: int):
    if not auth.check_if_admin_or_current_user(id):
        return jsonify({"error": "You do not have enough permissions"}), 401
    
    user = crud.get_user_by_id(db.session, id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    message = crud.delete_user(db.session, id)
    return message
