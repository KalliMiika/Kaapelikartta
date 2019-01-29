from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
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