from flask import jsonify
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User

def get_users(session: Session):
    stmt = select(User)
    users = session.scalars(stmt).all()
    return users

def get_user_by_id(session: Session, id: int):
    stmt = select(User).where(User.id==id)
    user = session.scalar(stmt)
    return user

def get_user_by_nick(session: Session, nick: str):
    stmt = select(User).where(User.nick==nick)
    user = session.scalar(stmt)
    return user

def get_user_by_email(session: Session, email: str):
    stmt = select(User).where(User.email==email)
    user = session.scalar(stmt)
    return user

def add_user(session: Session, user_dict: dict):
    user = User(
        nick=user_dict["nick"], 
        email=user_dict["email"], 
        password=user_dict["password"]
    )
    session.add(user)
    session.commit()
    return user

def update_user(session: Session, id: int, user_dict: dict):
    user = get_user_by_id(session, id)
    if user is None:
        return None
    
    if "nick" in user_dict:
        user.nick = user_dict["nick"]
    if "email" in user_dict:
        user.email = user_dict["email"]
    if "password" in user_dict:
        user.password = user_dict["password"]

    session.add(user)
    session.commit()
    return user

def delete_user(session: Session, id: int):
    user = get_user_by_id(session, id)
    session.delete(user)
    session.commit()
    return jsonify({'message': 'User deleted'})

