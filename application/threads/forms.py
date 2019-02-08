from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class ThreadForm(FlaskForm):
    #Säikeen "alkupään" number_a kenttä
    number_a = IntegerField("Number_a")
    #Säikeen "loppupään" number_b kenttä
    number_b = IntegerField("Number_b")
    #Säikeen "alkupään" socket_a kenttä
    socket_a = IntegerField("Socket_a")
    #Säikeen "loppupään" socket_b kenttä
    socket_b = IntegerField("Socket_b")
    #Säikeen data kenttä
    data = StringField("Data", [validators.optional()])
    #Säikeen vapaamuotoinen viesti kenttä
    note = StringField("Note", [validators.optional()])
 
    class Meta:
        #toistaiseksi csrf = false, millä turvautuminen 
        # cross-site request forgery -hyökkäyksiä 
        # vastaan kytketään pois päältä.
        csrf = False