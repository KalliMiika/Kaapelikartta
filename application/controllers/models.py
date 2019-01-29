from application import db

#Risteyskojeen models.py
class Controller(db.Model):

    #Risteyskojeen pääavain id
    id = db.Column(db.Integer, primary_key=True)
    
    #Risteyskojeen nimi
    name = db.Column(db.String(144), nullable=False)
    #Risteyskojeen vapaamuotoinen viesti
    note = db.Column(db.String(144), nullable=False)
    #Risteyskojeen X-koordinaatti, 
    # jonka perusteella se asetetaan karttanäkymään
    x = db.Column(db.Integer, nullable=False)
    #Risteyskojeen Y-koordinaatti, 
    # jonka perusteella se asetetaan karttanäkymään
    y = db.Column(db.Integer, nullable=False)

    def __init__(self, name, note, x, y):
        self.name = name
        self.note = note
        self.x = x
        self.y = y