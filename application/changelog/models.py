from application import db
from sqlalchemy.sql import text

from application.auth.models import User
from application.controllers.models import Controller
from application.cables.models import Cable
from application.threads.models import Thread

#Muutoslogin models.py
class Changelog(db.Model):

    #Muutoslogin pääavain id
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    
    #Muutoksen tehneen käyttäjän id
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    #Muutoksen kohde: taulu
    modified_table = db.Column(db.String(144), nullable=False)
    #Muutoksen kohde: sarake
    modified_column = db.Column(db.String(144), nullable=False)
    #Muutoksen kohde: rivi(haetaan id perusteella)
    modified_id = db.Column(db.Integer, nullable=False)

    #Muutoksen tyyppi
    action = db.Column(db.String(144), nullable=False)

    #Alkuperäinen arvo
    old_value = db.Column(db.String(144), nullable=False)
    #Uusi arvo
    new_value = db.Column(db.String(144), nullable=False)

    def __init__(self, account_id, modified_table, modified_column, modified_id, action, old_value, new_value):
        self.account_id = account_id
        self.modified_table = modified_table
        self.modified_column = modified_column
        self.modified_id = modified_id
        self.action = action
        self.old_value = old_value
        self.new_value = new_value

    @staticmethod
    def findAll():
        stmt = text("SELECT * FROM Changelog")
        res = db.engine.execute(stmt)
        return Changelog.parseRes(res)

    @staticmethod
    def findByUser(user_id):
        stmt = text("SELECT * FROM Changelog WHERE account_id = :user_id").params(user_id=user_id)
        res = db.engine.execute(stmt)
        return Changelog.parseRes(res)

    @staticmethod
    def findByTable(table):
        stmt = text("SELECT * FROM Changelog WHERE modified_table = :table").params(table=table)
        res = db.engine.execute(stmt)
        return Changelog.parseRes(res)

    @staticmethod
    def findByUserAndTable(user_id, table):
        stmt = text("SELECT * FROM Changelog WHERE modified_table = :table "
        "AND account_id = :user_id").params(table=table, user_id=user_id)
        res = db.engine.execute(stmt)
        return Changelog.parseRes(res)

    @staticmethod
    def findByUserAndTableAndId(user_id, table, target_id):
        stmt = text("SELECT * FROM Changelog WHERE modified_table = "
                    ":table AND modified_id = :id AND "
                    "account_id = :user_id").params(table=table, user_id=user_id, id=target_id)
        res = db.engine.execute(stmt)
        return Changelog.parseRes(res)

    def parseRes(res):
        result = []
        for row in res:
            target = None
            if row[4] == "Thread":
                t = Thread.query.get(row[6])
                target = Cable.query.get(t.cable_id).name + " / " + str(t.socket_a)
            elif row[4] == "Cable":
                target = Cable.query.get(row[6]).name
            elif row[4] == "Controller":
                target = Controller.query.get(row[6]).name
            elif row[4] == "Account":
                target = User.query.get(row[6]).name

            result.append({"modified_by":User.query.get(row[3]).name, "date":row[1], 
                        "target_table":row[4], "target_column":row[5], "target":target, 
                        "action":row[7], "old_value":row[8], "new_value":row[9]
                        })
        return result