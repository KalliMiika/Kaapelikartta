from application import db

class Controller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    note = db.Column(db.String(144), nullable=False)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)

    def __init__(self, name, note, x, y):
        self.name = name
        self.note = note
        self.x = x
        self.y = y