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

#--------------------------Kirjautuminen---------------------------

#Tuodaan randomgeneraattori käyttöön?
from os import urandom

#Randomgeneroidaan salaiset avaimet?
app.config["SECRET_KEY"] = urandom(32)

#Tuodaan flask_loginin tarjoama LoginManager käyttöön
from flask_login import LoginManager, current_user

#Luodaan LoginManager olio
login_manager = LoginManager()
login_manager.setup_app(app)

#Määritetään login_managerille login näkymä
# auth/views.py metodi def auth_login():
login_manager.login_view = "auth_login"

#Määritellään login_managerille virheviesti kirjautumisen vaatimiselle
login_manager.login_message = "Please login to use this functionality."

# roles in login_required
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()
            try:
                if not current_user.is_authenticated():
                    return login_manager.unauthorized()
            except:
                return login_manager.unauthorized()
                
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

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

#Luetaan kansiosta application/crossconnections tiedostojen sisältö
from application.crossconnections import models
from application.crossconnections import views

#Luetaan kansiosta application/auth tiedostojen sisältö
from application.auth import models
from application.auth import views

#Luetaan kansiosta application/changelog tiedostojen sisältö
from application.changelog import models
from application.changelog import views

#Luetaan kansiosta application/routes tiedostojen sisältö
from application.routes import views

#Luetaan kansiosta application/auth/models tietokantaolio User
from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

#------------------------------------------------------------------

#Luodaan tarvittavat tietokantataulut
try:
    db.create_all()
except:
    pass