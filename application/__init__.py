# Tuodaan Flask käyttöön
from flask import Flask
app = Flask(__name__)

#----------------------------SQLAlchemy----------------------------

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy

import os

#Määritetään SQLAlchemylle käytettävä tietokanta
#Herokussa käytetään Herokun omaa Postgresql kantaa
#Muutoin käytetään omaa sqlite tietokantaa.
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kaapelikartta.db"
    # Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
    app.config["SQLALCHEMY_ECHO"] = True

# Luodaan db-olio, jota käytetään tietokannan käsittelyyn
db = SQLAlchemy(app)

#---------------Oman sovelluksen toiminnallisuudet-----------------

# Luetaan kansiosta application tiedoston views sisältö
from application import views

#Luetaan kansiosta application/controllers tiedostojen sisältö
from application.controllers import models
from application.controllers import views

#Luetaan kansiosta application/cables tiedostojen sisältö
from application.cables import models
from application.cables import views

#Luetaan kansiosta application/thread tiedostojen sisältö
from application.threads import models
from application.threads import views

#Luetaan kansiosta application/auth tiedostojen sisältö
from application.auth import models
from application.auth import views

#Luetaan kansiosta application/routes tiedostojen sisältö
from application.routes import views

#--------------------------Kirjautuminen---------------------------

#Luetaan kansiosta application/models tietokantaolio User
from application.auth.models import User

#Tuodaan randomgeneraattori käyttöön?
from os import urandom

#Randomgeneroidaan salaiset avaimet?
app.config["SECRET_KEY"] = urandom(32)

#Tuodaan flask_loginin tarjoama LoginManager käyttöön
from flask_login import LoginManager

#Luodaan LoginManager olio
login_manager = LoginManager()
login_manager.init_app(app)

#Määritetään login_managerille login näkymä
# auth/views.py metodi def auth_login():
login_manager.login_view = "auth_login"

#Määritellään login_managerille virheviesti kirjautumisen vaatimiselle
login_manager.login_message = "Please login to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#------------------------------------------------------------------

#Luodaan tarvittavat tietokantataulut
try:
    db.create_all()
except:
    pass