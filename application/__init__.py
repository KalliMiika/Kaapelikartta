# Tuodaan Flask käyttöön
from flask import Flask
app = Flask(__name__)

# Tuodaan SQLAlchemy käyttöön
from flask_sqlalchemy import SQLAlchemy
# Käytetään kaapelikartta.db-nimistä SQLite-tietokantaa.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kaapelikartta.db"
# Pyydetään SQLAlchemyä tulostamaan kaikki SQL-kyselyt
app.config["SQLALCHEMY_ECHO"] = True
# Luodaan db-olio, jota käytetään tietokannan käsittelyyn
db = SQLAlchemy(app)

# Luetaan kansiosta application tiedoston views sisältö
from application import views

#Luetaan kasiosta application/controller tiedoston sisältö
from application.controllers import models
from application.controllers import views

# Luodaan tarvittavat tietokantataulut
db.create_all()