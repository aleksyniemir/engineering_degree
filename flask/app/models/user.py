from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy

from app import db

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nick: Mapped[str] = mapped_column(String(31), nullable=False)
    email: Mapped[str] = mapped_column(String(63), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # games = db.relationship('Game', back_populates='user')

    def __init__(self, nick, email, password):
        self.nick = nick
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f"<User {self.nick}>"