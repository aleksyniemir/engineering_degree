from sqlalchemy import Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db

class Game(db.Model): 
    __tablename__ = 'games'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str]
    photo: Mapped[LargeBinary] = mapped_column(LargeBinary)
    prompt: Mapped[str] = mapped_column(String(8191))
    description: Mapped[str] = mapped_column(String(1023))
    scene: Mapped[str] = mapped_column(String(1023))
    turn_number: Mapped[int]    
    possible_actions: Mapped[str] = mapped_column(String(1023))
    quests: Mapped[str] = mapped_column(String(1023))
    inventory: Mapped[str] = mapped_column(String(1023))
    location: Mapped[str] = mapped_column(String(1023))
    weather: Mapped[str] = mapped_column(String(1023))
    health: Mapped[str] = mapped_column(String(255))

    user: Mapped["User"] = relationship("User", back_populates="games")

from app.models.user import User