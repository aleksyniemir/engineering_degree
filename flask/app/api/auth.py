from flask import jsonify, request, Blueprint
from app import db

import app.crud.user as crud
import app.utils.auth as auth
import app.utils.validators as validators

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route("/login", methods = ['POST'])
def login():
    user_dict = request.json
    if not user_dict or not user_dict['nick'] or not user_dict['password']:
       return jsonify({"message": "Could not verify!", "WWW-Authenticate": "Basic auth='Login required'"}), 401
    
    user = crud.get_user_by_nick(db.session, user_dict['nick'])
    if not user:
        return jsonify({"message": "Invalid user or password!"}), 401
    if not user.verify_password(user_dict['password']):
        return jsonify({"message": "Invalid user or password!"}), 401

    token = auth.get_token(user_dict["nick"])
    return jsonify({'token': token})


@bp.route("/sign_up", methods=['POST'])
def sign_up():
    user_dict = request.json
    if not user_dict or not user_dict['nick'] or not user_dict['password'] or not user_dict['email']:
        return jsonify({"message": "Missing required fields!"}), 400

    if not validators.check_email_regex(user_dict["email"]):
        return jsonify({"error": "Not a valid email address"}), 400
        
    if crud.get_user_by_email(db.session, user_dict["email"]):
        return jsonify({"error": "Email already in use"}), 400

    if crud.get_user_by_nick(db.session, user_dict["nick"]):
        return jsonify({"error": "Nickname already in use"}), 400
    
    crud.add_user(db.session, user_dict)
    token = auth.get_token(user_dict["nick"])
    return jsonify({'message': 'User registered successfully!', 'token': token}), 201
