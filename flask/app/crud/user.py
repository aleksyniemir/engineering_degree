from sqlalchemy import select
from app.models.user import User
from app.schemas.user import user_schema, user_schema_update, user_schema_create, users_schema, user_schema_private
from flask import jsonify
from app import db
import re

def get_users(session):
    stmt = select(User)
    users = session.scalars(stmt).all()
    #users_serialized = users_schema.dump(users_models)
    return users

def get_user_by_id(session, id):
    stmt = select(User).where(User.id==id)
    user = session.scalar(stmt)
    #user = user_schema.dump(user_model)
    return user

def get_user_by_id_with_password(session, id):
    stmt = select(User).where(User.id==id)
    user = session.scalar(stmt)
    # user = user_schema_private.dump(user_model)
    return user

def get_user_by_nick(session, nick):
    stmt = select(User).where(User.nick==nick)
    user = session.scalar(stmt)
    #user = user_schema.dump(user_model)
    return user

def get_user_by_email(session, email):
    stmt = select(User).where(User.email==email)
    user = session.scalar(stmt)
    # user = user_schema.dump(user_model)
    return user

def add_user(session, user_dict):
    user = User(**user_dict)
    session.add(user)
    session.commit()
    #user = user_schema_create.dump(user) 
    return user

def update_user(session, id, user_dict):
    user = get_user_by_id_with_password(session, id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if "nick" in user_dict:
        user.nick = user_dict["nick"]
    if "email" in user_dict:
        user.email = user_dict["email"]
    if "password" in user_dict:
        user.password = user_dict["password"]

    session.add(user)
    session.commit()
    return user

def delete_user(session, id):
    user = get_user_by_id(session, id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    session.delete(user)
    session.commit()
    return jsonify({'message': 'User deleted'})

