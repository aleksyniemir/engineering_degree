# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import Integer, String, ForeignKey

# from app import db

# class Turn(db.Model):
#     __tablename__ = 'turns'
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    

#     game: Mapped["Game"] = relationship("Game", back_populates="turns")

# from app.models.game import Game