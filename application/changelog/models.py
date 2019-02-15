from application import db
from sqlalchemy.sql import text

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
    def findByUser(user_id):
        stmt = text("SELECT * FROM Changelog WHERE account_id = :user_id").params(user_id=user_id)
        res = db.engine.execute(stmt)
        result = []
        for row in res:
            result.append(row)
        return result

    @staticmethod
    def findByTable(table):
        stmt = text("SELECT * FROM Changelog WHERE modified_table = :table").params(table=table)
        res = db.engine.execute(stmt)
        result = []
        for row in res:
            result.append(row)
        return result

    @staticmethod
    def findByUserAndTable(user_id, table):
        stmt = text("SELECT * FROM Changelog WHERE modified_table = :table "
        "AND account_id = :user_id").params(table=table, user_id=user_id)
        res = db.engine.execute(stmt)
        result = []
        for row in res:
            result.append(row)
        return result

    @staticmethod
    def findByUserAndTableAndId(user_id, table, id):
        stmt = text("SELECT * FROM Changelog WHERE modified_table = "
                    ":table AND modified_id = :id AND "
                    "account_id = :user_id").params(table=table, user_id=user_id, id=id)
        res = db.engine.execute(stmt)
        result = []
        for row in res:
            result.append(row)
        return result