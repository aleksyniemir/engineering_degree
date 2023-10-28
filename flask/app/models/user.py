from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column


from app import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nick: Mapped[str] = mapped_column(String(31), nullable=False)
    email: Mapped[str] = mapped_column(String(63), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # games = db.relationship('Game', back_populates='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    