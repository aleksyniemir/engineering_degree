# class Turn(db.Model):
#     __tablename__ = 'turns'
#     id = db.Column(db.Integer, primary_key = True, autoincrement=True)
#     game_id = db.column(db.Integer, db.ForeignKey('games.id'), nullable=False)
#     body = db.Column(db.String(1023), nullable=False)
#     picture = db.Column(db.LargeBinary, nullable=True)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     game = db.relationship('Game', back_populates='turns')
