from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db

class Game(db.Model): 
    __tablename__ = 'games'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str]

    user: Mapped["User"] = relationship("User", back_populates="games")

    # turns = db.relationship('Turn', back_populates='game')
from app.models.user import User