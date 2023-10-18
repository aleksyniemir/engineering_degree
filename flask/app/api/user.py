from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
from flask_sqlalchemy import SQLAlchemy

from app import db

from app.models.user import User
from app.schemas.user import user_schema, users_schema

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route("/get_users", methods = ['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@bp.route("/get_user/<id>", methods = ['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@bp.route("/add_user", methods = ['POST'])
def add_user():
    try:
        user_dict = user_schema.load(request.json)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return jsonify(err.messages), 400
        
        
    # TODO check if nick and email exists


    user = User(**user_dict)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

@bp.route("/update_user/<id>", methods = ['PUT'])
def update_user(id):
    user = User.query.get(id)

    try:
        user_dict = user_schema.load(request.json)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        return jsonify(err.messages), 400
    
    for key, value in user_dict.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.session.commit()
    return user_schema.jsonify(user)

@bp.route("/delete_user/<id>", methods = ['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)