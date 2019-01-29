from application import db

#Käyttäjän models.py
class User(db.Model):

    __tablename__ = "account"

    #Käyttäjän pääavain id
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    #Käyttäjän etu- ja sukunimi
    name = db.Column(db.String(144), nullable=False)
    #Käyttäjän käyttäjätunnus
    username = db.Column(db.String(144), nullable=False)
    #Käyttäjän salasana
    password = db.Column(db.String(144), nullable=False)
    #Käyttäjän rooli (moderator / user)
    role = db.Column(db.String(144), nullable=False)

    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password = password
        self.role = role
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        return self.role