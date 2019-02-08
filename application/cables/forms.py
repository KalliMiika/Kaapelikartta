from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from application import db
from application.controllers.models import Controller
from application.cables.models import Cable

class CableForm(FlaskForm):

    #Kaapelin nimi kentän tulee olla vähintään 2 merkkiä pitkä
    name = StringField('Name', [validators.required()])
    #Kaapelin vapaamuotoinen viesti kenttä saa olla tyhjä
    note = StringField('Note', [validators.optional()])
    #Kaapelin päässä oleva Risteyskoje 'A'
    controller_a_id = SelectField('Controller A', [validators.optional()], coerce=int)
    #Kaapelin "toisessa päässä" oleva Risteyskoje 'B'
    controller_b_id = SelectField('Controller B', [validators.optional()], coerce=int)
    #Kaapelin koko. Kaapeleita on muutamia erilaisia, joista valitaan yksi
    size = SelectField('Size', [validators.required()])   
    #Mahdolliset koot:
    #100x4, 50x4, 25x4, 15x4, 10x4, 5x4
    #50x2, 20x2, 10x2
    choices = [('150x4', '150x4'), ('100x4', '100x4'), 
    ('50x4', '50x4'), ('25x4', '25x4'), ('15x4', '15x4'), 
    ('10x4', '10x4'), ('5x4', '5x4'), 
    ('50x2', '50x2'), ('20x2', '20x2'), ('10x2', '10x2')]

    def validate2(self):
        #Tarkistetaan että kaapelin nimi on uniikki
        c = Cable.query.filter_by(name = self.name.data).first()
        if not c is None:
            self.name.errors.append('Cable name already in use')
            return False
        #Tarkistetaan että kaapeli on molemmista päistä kiinni
        #eri risteyskojeessa 
        if self.controller_a_id.data == self.controller_b_id.data:
            self.controller_a_id.errors.append('Both ends of a cable cannot be connected to same Controller')
            return False

        return True

    #Alustetaan SelectFieldien sisältö
    def setupChoices(self):
        self.controller_a_id.choices = [(c.id, c.name) for c in Controller.query.order_by('name')]
        self.controller_b_id.choices = [(c.id, c.name) for c in Controller.query.order_by('name')]
        self.size.choices = self.choices

    class Meta:
        #toistaiseksi csrf = false, millä turvautuminen 
        # cross-site request forgery -hyökkäyksiä 
        # vastaan kytketään pois päältä.
        csrf = False