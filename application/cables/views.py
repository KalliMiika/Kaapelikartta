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

#Kuunnellaan osoitteeseen /cables/ tulevia POST-Pyyntöjä
#Syötteestä kerätään kaapelille nimi, viesti, alku ja loppu 
#risteyskojeet, sekä säikeiden lukumäärä ja lisätään se 
# lopuksi tietokantaan  ja uudelleenohjataan käyttäjä 
# osoitteeseen /cables
@app.route("/cables/", methods=["POST"])
def cables_create():
    form = CableForm(request.form)
    #Validoidaan CableFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan cables/new.html sivu
    #virheviestin kera.
    form.setupChoices()
    if not form.validate():
        return render_template("cables/new.html", form = form)
    if not form.validate2():
        return render_template("cables/new.html", form = form)
    
    c = Cable(form.controller_a_id.data, form.controller_b_id.data, form.size.data, form.name.data, form.note.data)   
    
    #c = form.size.data.split('x')
    #a = int(c[0])
    #b = int(c[1])

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("cables_index"))