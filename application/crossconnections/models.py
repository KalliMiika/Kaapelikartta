from application import db

#Risteyskojeen models.py
class Crossconnection(db.Model):

    #Ristikyteknnän pääavain id
    id = db.Column(db.Integer, primary_key=True)
    
    #Risteyskojeen id, jonka sisällä kytkentä tapahtuu
    controller_id = db.Column(db.Integer, db.ForeignKey('controller.id'), nullable=False)

    #"Vasemmalta tuleva" säie a
    thread_a_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    #"Oikealle lähtevä" säie b
    thread_b_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    
    #"Vasemmalta tulevan" säikeen a päättävä laite device_a
    device_a = db.Column(db.String(144), nullable=False)
    #"Oikealle lähtevän" säikeen b aloittava laite device_b
    device_b = db.Column(db.String(144), nullable=False)

    def __init__(self, controller_id, thread_a_id, thread_b_id, device_a, device_b):
        self.controller_id = controller_id
        self.thread_a_id = thread_a_id
        self.thread_b_id = thread_b_id
        self.device_a = device_a
        self.device_b = device_b
