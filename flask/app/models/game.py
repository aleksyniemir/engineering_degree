
# class Game(db.Model): 
    #__tablename__ = 'games'
    # id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # title = db.Column(db.String(255), nullable=False)

    # user = db.relationship('User', back_populates='games')

    # turns = db.relationship('Turn', back_populates='game')