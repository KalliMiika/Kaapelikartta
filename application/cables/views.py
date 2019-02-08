from flask import redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db
from application.cables.models import Cable, CableListModel
from application.controllers.models import Controller
from application.cables.forms import CableForm

#Kuunnellaan osoitteeseen /cables tulevia GET-Pyyntöjä
#Palautetaan cables/list.html näkymä, 
#jolle annetaan "Select * from Cable"-kyselyn tulos
@app.route("/cables", methods=["GET"])
def cables_index():
    cables = []
    for cable in Cable.query.all():
        cables.append(CableListModel(cable))
    return render_template("cables/list.html", cables = cables)

#Kuunnellaan osoitteeseen /cables/new/ tulevia GET-Pyyntöjä
#Palautetaan cables/new.html sivu, parametriksi annetaan
#cables/forms.py määrittelemät elementit
@app.route("/cables/new/")
def cables_form():
    f = CableForm()
    f.setupChoices()
    return render_template("cables/new.html", form = f)

#Kuunnellaan osoitteeseen /cables/<cable_id>/ tulevia GET-Pyyntöjä
#Palautetaan <cable_id>:n määrittelemää kaapelia vastaava
#cables/edit.html sivu, parametriksi annetaan
#cables/forms.py määrittelemät elementit
@app.route("/cables/<cable_id>/", methods=["GET"])
#@login_required
def cables_view_one(cable_id):
    c = Cable.query.get(cable_id)
    f = CableForm()
    f.setupChoices()
    f.controller_a_id.default=c.controller_a_id
    f.controller_b_id.default=c.controller_b_id
    f.size.default=c.size
    f.process()
    return render_template("cables/edit.html", form = f, cable = c)

#Kuunnellaan osoitteeseen /cables/<controller_id>/ tulevia POST-Pyyntöjä
#Etsitään <cable_id>:tä vastaava kaapeli tietokannasta ja
#päivitetään sen tiedot POST-Pyynnön mukana tulleilla syötteillä.
#Päivitetään lopuksi muunneltu kaapeli tietokantaan ja
#uudelleenohjataan käyttäjä osoitteeseen /cables
@app.route("/cables/<cable_id>/", methods=["POST"])
#@login_required
def cables_edit_one(cable_id):
    f = CableForm(request.form)
    c = Cable.query.get(cable_id)

    #Validoidaan CableFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan cables/edit.html sivu
    #virheviestin kera.
    f.setupChoices()
    if not f.validate():
        return render_template("cables/edit.html", form = f, cable = c)
    if not f.validate2(True):
        return render_template("cables/edit.html", form = f, cable = c)

    c.name = f.name.data
    c.note = f.note.data
    c.controller_a_id = f.controller_a_id.data
    c.controller_b_id = f.controller_b_id.data
    c.size = f.size.data

    db.session().commit()

    return redirect(url_for("cables_index"))

#Kuunnellaan osoitteeseen /cables/ tulevia POST-Pyyntöjä
#Syötteestä kerätään kaapelille nimi, viesti, alku ja loppu 
#risteyskojeet, sekä säikeiden lukumäärä ja lisätään se 
#lopuksi tietokantaan  ja uudelleenohjataan käyttäjä 
#osoitteeseen /cables
@app.route("/cables/", methods=["POST"])
def cables_create():
    form = CableForm(request.form)
    #Validoidaan CableFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan cables/new.html sivu
    #virheviestin kera.
    form.setupChoices()
    if not form.validate():
        return render_template("cables/new.html", form = form)
    if not form.validate2(False):
        return render_template("cables/new.html", form = form)
    
    c = Cable(form.controller_a_id.data, form.controller_b_id.data, form.size.data, form.name.data, form.note.data)   
    
    #c = form.size.data.split('x')
    #a = int(c[0])
    #b = int(c[1])

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("cables_index"))