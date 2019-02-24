from application import db
from sqlalchemy.sql import text
from application.controllers.models import Controller
from application.cables.models import Cable
from application.threads.models import Thread

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

    @staticmethod
    def find_routes():
        stmt = text("SELECT DISTINCT(Thread.data) FROM Thread, Crossconnection "
                    "WHERE Crossconnection.thread_b_id = Thread.id AND "
                    "Crossconnection.thread_a_id = 0")
        res = db.engine.execute(stmt)
        result = []
        for row in res:
            result.append({"name":row[0]})
        return result

    #Haetaan säikeiden data kenttien perusteella route hakusanaa
    #vastaava reitti
    @staticmethod
    def get_route(route):
        #Etsitään reitin alku, eli se ristikytkentä reitillä, joka alkaa
        #Risteyskojeesta ilman että signaali saapuu risteyskojeeseen ensin.
        stmt = text("SELECT Crossconnection.id, Crossconnection.thread_b_id FROM Crossconnection, Thread "
                    "WHERE Thread.data = :route AND Crossconnection.thread_a_id = 0 AND Crossconnection.thread_b_id = Thread.id").params(route=route)
        res = db.engine.execute(stmt)
        current = res.first()
        result = []
        while True:
            end = True
            crossConnection = Crossconnection.query.get(current.id)
            controller = Controller.query.get(crossConnection.controller_id)
            if not crossConnection.thread_b_id == 0:
                end = False
            cable = None
            thread = None
            socket_a = None
            socket_b = None
            if not end:
                thread = Thread.query.get(current.thread_b_id)
                cable = Cable.query.get(thread.cable_id)
                #Ristikytkennät eivät ota kantaa siihen miten päin kaapelit ovat,
                #joten syncataan socketit oikein päin
                if controller.id == cable.controller_a_id:
                    socket_a = thread.socket_a
                    socket_b = thread.socket_b
                else:
                    socket_b = thread.socket_a
                    socket_a = thread.socket_b
            #Otetaan nykyisen iteraation tulokset talteen
            result.append({
                "type":"Controller",
                "name":controller.name
            })
            if not end:
                result.append({
                    "type":"Cable",
                    "name":cable.name,
                    "socket_a":thread.socket_a,
                    "socket_b":thread.socket_b
                })
            if end:
                return result
            #Etsitään seuraava ristikytkentä seuraavaa iteraatiota varten
            stmt = text("SELECT Crossconnection.id, Crossconnection.thread_b_id FROM Crossconnection, Thread WHERE "
                        "Crossconnection.thread_a_id = :thread_id").params(thread_id=thread.id)
            nxt = db.engine.execute(stmt)
            hasnext = False
            for cc in nxt:
                current = nxt.first()
                hasnext = True
                break
            if not hasnext:
                break
                
        return result

        
