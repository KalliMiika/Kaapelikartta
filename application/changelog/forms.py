from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from application import db

from application.auth.models import User
from application.threads.models import Thread
from application.controllers.models import Controller
from application.cables.models import Cable

class SearchForm(FlaskForm):

    modified_by = SelectField("Search by user")
    targetTable = SelectField("Search by type")
    target = SelectField("Search by object", choices=[("", "")])

    table_choices = [("", ""), ("Account", "Account"), ("Controller", "Controller"), 
                    ("Cable", "Cable"), ("Thread", "Thread")]

    #Alustetaan SelectFieldien sisältö
    def setupChoices(self):
        self.modified_by.choices = [(("", ""))]
        self.modified_by.default = ""
        for u in User.query.order_by('name'):
            self.modified_by.choices.append((u.id, u.name))
            
        self.targetTable.choices = self.table_choices
        self.targetTable.default = ""

    def setupTarget(self, table):
        self.target.choices = [(("", ""))]
        self.target.default = ""
        if table == "Thread":
            for t in Thread.query.order_by('cable_id'):
                self.target.choices.append((t.id, Cable.query.get(t.cable_id).name + " / " + str(t.socket_a)))
        elif table == "Account":
            for u in User.query.order_by('name'):
                self.target.choices.append((u.id, u.name))
        elif table == "Controller":
            for c in Controller.query.order_by('name'):
                self.target.choices.append((c.id, c.name))
        elif table == "Cable":
            for c in Cable.query.order_by('name'):
                self.target.choices.append((c.name, c.name))


class Meta:
#toistaiseksi csrf = false, millä turvautuminen 
# cross-site request forgery -hyökkäyksiä 
# vastaan kytketään pois päältä.
    csrf = False