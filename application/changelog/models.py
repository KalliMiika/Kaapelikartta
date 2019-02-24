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

        
    @staticmethod
    def deleteByTableAndId(table, target_id):
        stmt = text("DELETE FROM Changelog WHERE modified_table = "
                    ":table AND modified_id = :id").params(table=table, id=target_id)
        res = db.engine.execute(stmt)

    def parseRes(res):
        result = []
        for change in res:
            target = None
            if change.modified_table == "Thread":
                t = Thread.query.get(change.modified_id)
                target = Cable.query.get(t.cable_id).name + " / " + str(t.socket_a)
            elif change.modified_table == "Cable":
                if change.action == "Delete":
                    target = change.old_value
                else:
                    target = Cable.query.get(change.modified_id).name
            elif change.modified_table == "Controller":
                if change.action == "Delete":
                    target = change.old_value
                else:
                    target = Controller.query.get(change.modified_id).name
            elif change.modified_table == "Account":
                target = User.query.get(change.modified_id).name

            result.append({"modified_by":User.query.get(change[3]).name, "date":change[1], 
                        "target_table":change[4], "target_column":change[5], "target":target, 
                        "action":change[7], "old_value":change[8], "new_value":change[9]
                        })
        return result