from application import db
from application.controllers.models import Controller
from sqlalchemy.sql import text

#Kaapelin models.py
class Cable(db.Model):

    #Kaapelin pääavain id
    id = db.Column(db.Integer, primary_key=True)
    
    #Kaapelin päässä oleva Risteyskoje 'A'
    controller_a_id = db.Column(db.Integer, db.ForeignKey('controller.id'), nullable=False)
    #Kaapelin toisessa päässä oleva Risteyskoje 'B'
    controller_b_id = db.Column(db.Integer, db.ForeignKey('controller.id'), nullable=False)
    #Kaapelin kapasiteetti
    size = db.Column(db.String(144), nullable=False)

    #Kaapelin nimi
    name = db.Column(db.String(144), nullable=False)
    #Kaapelin vapaamuotoinen viesti
    note = db.Column(db.String(144), nullable=False)

    threads = db.relationship("Thread", backref='cable', lazy=True)

    def __init__(self, controller_a_id, controller_b_id, size, name, note):
        self.controller_a_id = controller_a_id
        self.controller_b_id = controller_b_id
        self.size = size
        self.name = name
        self.note = note

    @staticmethod
    def findThreadsByControllerId(controller_id):
        stmt = text("SELECT Cable.name AS cable_name, Thread.socket_a AS thread_socket, Thread.id AS thread_id FROM Cable, Thread "
                    "WHERE (Cable.controller_a_id = :controller_id OR Cable.controller_b_id = :controller_id) "
                    "AND Thread.cable_id = cable.id").params(controller_id=controller_id)
        res = db.engine.execute(stmt)
        return res

#Kaapeleiden listaamista varten olio, jolle annetaan kaapeliin
#kytkettyjen Risteyskojeiden nimet
class CableListModel():
    cable = None
    controller_a_name = None
    controller_b_name = None

    def __init__(self, cable):
        self.cable = cable
        self.controller_a_name = Controller.query.filter_by(id = cable.controller_a_id).first().name
        self.controller_b_name = Controller.query.filter_by(id = cable.controller_b_id).first().name
