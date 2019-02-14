from application import db

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
