from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, validators
from application import db
from application.auth.models import User
  
class LoginForm(FlaskForm):
    #Käyttäjän käyttäjänimi -kenttä ei saa olla tyhjä
    username = StringField("Username", [validators.required()])
    #Käyttäjän salasana -kenttä ei saa olla tyhjä
    password = PasswordField("Password", [validators.required()])
  
    class Meta:
        #toistaiseksi csrf = false, millä turvautuminen 
        # cross-site request forgery -hyökkäyksiä 
        # vastaan kytketään pois päältä.
        csrf = False

class RegisterForm(FlaskForm):
    #Käyttäjän nimen täytyy olla vähintään 2 merkkiä pitkä
    name = StringField("Name", [validators.Length(min=2)])
    #Käyttäjän käyttäjänimen täytyy olla vähintään 2 merkkiä pitkä
    username = StringField("Username", [
        validators.Length(min=2)
        ])
    #Käyttäjän salasanan täytyy olla vähintään 2 merkkiä pitkä
    #Ja sen täytyy täsmätä salasanan varmistus kenttään
    password = PasswordField("Password", [
        validators.Length(min=2), 
        validators.Required(), 
        validators.EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField("Repeat password", [
        validators.Length(min=2), 
        validators.Required()
        ])
    role = SelectField("Role", choices=[("USER", "User"), ("ADMIN", "Admin")])
  
    #Etsitään tietokannasta käyttäjää syötetyn käyttäjätunnuksen 
    #perusteella. Jos käyttäjätunnuksella löydetään käyttäjä,
    #todetaan käyttäjätunnus varatuksi
    def validateUsername(self):
        user = User.query.filter_by(username=self.username.data).first()
        if not user is None:
            self.username.errors.append('Username already in use.')
            return False

        self.user = user
        return True
    
    class Meta:
        #toistaiseksi csrf = false, millä turvautuminen 
        # cross-site request forgery -hyökkäyksiä 
        # vastaan kytketään pois päältä.
        csrf = False
