from application import db

#Säikeen models.py
class Thread(db.Model):

    #Säikeen pääavain id
    id = db.Column(db.Integer, primary_key=True)
    
    #Kaapeli, jonka sisällä säie kulkee
    cable_id = db.Column(db.Integer, db.ForeignKey('cable.id'), nullable=False)
    
    #Säikeen numero Kaapelin "Alkupäässä"
    number_a = db.Column(db.Integer, nullable=False)
    #Säikeen numero Kaapelin "Loppupäässä"
    number_b = db.Column(db.Integer, nullable=False)
    #Säikeen liittimen numero Kaapelin "Alkupäässä"
    #olevassa Risteyskojeessa
    socket_a = db.Column(db.Integer, nullable=False)
    #Säikeen liittimen numero Kaapelin "Loppupäässä"
    #olevassa Risteyskojeessa
    socket_b = db.Column(db.Integer, nullable=False)
    #Säikeen data
    data = db.Column(db.String(144), nullable=False)
    #Säikeen vapaamuotoinen viesti
    note = db.Column(db.String(144), nullable=False)

    def __init__(self, number_a, number_b, socket_a, socket_b, data, note):
        self.number_a = number_a
        self.number_b = number_b
        self.socket_a = socket_a
        self.socket_b = socket_b
        self.data = data
        self.note = note