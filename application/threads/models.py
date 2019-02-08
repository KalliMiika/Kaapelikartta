from application import db
from sqlalchemy.sql import text

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

    @staticmethod
    def find_routes():
        stmt = text("SELECT DISTINCT data FROM thread where LENGTH(data) > 0")
        res = db.engine.execute(stmt)
        result = []
        for row in res:
            result.append({"name":row[0], "length":Thread.route_length(row[0])})
        return result

    @staticmethod
    def route_length(route):
        stmt = text("SELECT COUNT(DISTINCT Controller.id) FROM Controller, Cable, Thread"
                    " WHERE Thread.data = :route AND Thread.cable_id = Cable.id AND"
                    " (Cable.controller_a_id = Controller.id OR Cable.controller_b_id = Controller.id)").params(route=route)
        res = db.engine.execute(stmt)
        result = []
        for row in res:
            result.append(row[0])
        return result[0]

    #Saa parametriksi merkkijonon route jonka perusteella etsitään se reitti 
    #jota pitkin tietty data liikkuu kaapeliverkostossa.
    #palautetaan lista joka sisältää askeleen verkossa / rivi
    @staticmethod
    def get_route(route):
        stmt = text("select controller.name, cable.name, thread.socket_a, thread.socket_b"
                    " from controller inner join cable on (cable.controller_a_id = controller.id"
                    " or cable.controller_b_id = controller.id) inner join thread on"
                    " thread.cable_id = cable.id and thread.data = :route").params(route=route)
        res = db.engine.execute(stmt)
        result = []
        tmp = []
            
        for row in res:
            tmp.append(row)

        prevType = None
        prevName = None

        while(len(tmp) > 0):
            if prevType is None:
                result.append({"type":"Controller", "name":tmp[0][0]})
                result.append({"type":"Cable", "name":tmp[0][1], "socket_a":tmp[0][2], "socket_b":tmp[0][3]})
                prevType = "cab"
                prevName = tmp[0][1]
                tmp.pop(0)
            boo = False
            for i in range(len(tmp)):
                if prevType == "cab" and prevName == tmp[i][1]:
                    result.append({"type":"Controller", "name":tmp[i][0]})
                    prevType = "con"
                    prevName = tmp[i][0]
                    tmp.pop(i)
                    boo = False
                    break
                elif prevType == "con" and prevName == tmp[i][0]:
                    result.append({"type":"Cable", "name":tmp[0][1], "socket_a":tmp[0][2], "socket_b":tmp[0][3]})
                    prevType = "cab"
                    prevName = tmp[0][1]
                    tmp.pop(i)
                    boo = False
                    break
            if boo:
                break
        return result