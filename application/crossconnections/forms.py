from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from application import db

from application.cables.models import Cable
from application.threads.models import Thread

class CrossconnectionForm(FlaskForm):

    #Risteyskojeeseen "saapuva" säie 'A'
    thread_a_id = SelectField('Thread A', [validators.optional()], coerce=int)
    #Risteyskojeesta "lähtevä" säie 'B'
    thread_b_id = SelectField('Thread B', [validators.optional()], coerce=int)
    #Risteyskojeen laite a johon säie 'A' päätetään
    device_a = StringField('Device A', [validators.optional()])
    #Risteyskojeen laite b josta säie 'B' alkaa
    device_b = StringField('Device B', [validators.optional()])

    def validate2(self, edit):
        #Tarkistetaan että kaapeli on molemmista päistä kiinni
        #eri risteyskojeessa 
        if self.thread_a_id.data == self.thread_b_id.data:
            self.thread_a_id.errors.append('Thread cannot be connected to itself')
            return False

        return True

    #Alustetaan SelectFieldien sisältö
    def setupChoices(self):
        choices = [(t.id, Cable.query.get(t.cable_id).name + "/" + str(t.socket_a)) for t in Thread.query.all()]
        self.thread_a_id.choices = choices
        self.thread_b_id.choices = choices

    class Meta:
        #toistaiseksi csrf = false, millä turvautuminen 
        # cross-site request forgery -hyökkäyksiä 
        # vastaan kytketään pois päältä.
        csrf = False