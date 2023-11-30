# from sqlalchemy import Integer, String, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column

# from app import db

# class Game(db.Model): 
#     __tablename__ = 'games'
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey())
#     #db.Column(db.Integer, primary_key = True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     title = db.Column(db.String(255), nullable=False)

#     user = db.relationship('User', back_populates='games')

#     # turns = db.relationship('Turn', back_populates='game')