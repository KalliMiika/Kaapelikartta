from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class ControllerForm(FlaskForm):
    #Risteyskojeen nimi kentän tulee olla vähintään 2 merkkiä pitkä
    name = StringField("Name", [validators.Length(min=2)])
    #Risteyskojeen vapaamuotoinen viesti kenttä saa olla tyhjä.
    note = StringField("Note", [validators.optional()])
    #Risteyskojeen x/y-koordinaatti kenttä ei saa olla tyhjä ja sen
    #sisällön täytyy olla numero. IntegerField toteuttaa tämän
    #tarkistuksen automaattisesti
    x = IntegerField("X-Coordinate")
    y = IntegerField("Y-Coordinate")
 
    class Meta:
        #toistaiseksi csrf = false, millä turvautuminen 
        # cross-site request forgery -hyökkäyksiä 
        # vastaan kytketään pois päältä.
        csrf = False