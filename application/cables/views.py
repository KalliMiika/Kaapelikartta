from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.cables.models import Cable, CableListModel
from application.threads.models import Thread
from application.cables.forms import CableForm
from application.changelog.models import Changelog

#Kuunnellaan osoitteeseen /cables tulevia GET-Pyyntöjä
#Palautetaan cables/list.html näkymä, 
#jolle annetaan "Select * from Cable"-kyselyn tulos
@app.route("/cables", methods=["GET"])
def cables_index():
    cables = []
    for cable in Cable.query.all():
        cables.append(CableListModel(cable))
    return render_template("cables/list.html", cables = cables)

#Kuunnellaan osoitteeseen /cables/<cable_id>/view/ tulevia GET-Pyyntöjä
#Palautetaan <cable_id>:n määrittelemää kaapelia vastaava
#cables/view.html sivu, parametriksi annetaan
#cables/models.py CableListModel
@app.route("/cables/<cable_id>/view/", methods=["GET"])
def cables_view_one(cable_id):
    c = CableListModel(Cable.query.get(cable_id))
    return render_template("cables/view.html", cable = c)

#Kuunnellaan osoitteeseen /cables/new/ tulevia GET- ja POST-Pyyntöjä
#GET-Pyynnöille:
#   Palautetaan cables/new.html sivu, parametriksi annetaan
#   cables/forms.py määrittelemät elementit
#POST-Pyynnöille:
#   Syötteestä kerätään kaapelille nimi, viesti, alku ja loppu 
#   risteyskojeet, sekä säikeiden lukumäärä ja lisätään se 
#   lopuksi tietokantaan  ja uudelleenohjataan käyttäjä 
#   osoitteeseen /cables
@app.route("/cables/new/", methods=["GET", "POST"])
@login_required(role="USER")
def cables_create():
    if request.method == "GET":
        f = CableForm()
        f.setupChoices()
        return render_template("cables/new.html", form = f)

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

    #Kerätään kaapelin size kentästä (esim 5x4) kaapelin säikeiden
    #lukumäärä ja luodaan sen mukaan kaapelin sisällä kulkevat
    #säikeet tietokantaan.
    tmp = form.size.data.split('x')
    n = int(tmp[0])*int(tmp[1])
    for i in range(n):
        c.threads.append(Thread(i+1, i+1, i+1, i+1, "", ""))

    db.session().add(c)
    db.session().commit()

    log = Changelog(current_user.id, "Cable", "", c.id, "Create", "", "")
    db.session().add(log)
    db.session().commit()

    return redirect(url_for("cables_index"))

#Kuunnellaan osoitteeseen /cables/<cable_id>/edit/ tulevia GET- ja POST-Pyyntöjä
#GET-Pyynnöille:
#   Palautetaan <cable_id>:n määrittelemää kaapelia vastaava
#   cables/edit.html sivu, parametriksi annetaan
#   cables/forms.py määrittelemät elementit
#POST-Pyynnöille:
#   Etsitään <cable_id>:tä vastaava kaapeli tietokannasta ja
#   päivitetään sen tiedot POST-Pyynnön mukana tulleilla syötteillä.
#   Päivitetään lopuksi muunneltu kaapeli tietokantaan ja
#   uudelleenohjataan käyttäjä osoitteeseen /cables
@app.route("/cables/<cable_id>/edit/", methods=["GET", "POST"])
@login_required(role="USER")
def cables_edit_one(cable_id):
    if request.method == "GET":
        c = Cable.query.get(cable_id)
        f = CableForm()
        f.setupChoices()
        f.controller_a_id.default=c.controller_a_id
        f.controller_b_id.default=c.controller_b_id
        f.size.default=c.size
        f.process()
        return render_template("cables/edit.html", form = f, cable = c)

    f = CableForm(request.form)
    c = Cable.query.get(cable_id)

    #Validoidaan CableFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan cables/edit.html sivu
    #virheviestin kera.
    f.setupChoices()
    if not f.validate():
        return render_template("cables/edit.html", form = f, cable = c)
    nameNotEdited = True
    if(c.name != f.name.data):
        nameNotEdited = False
    if not f.validate2(nameNotEdited):
        return render_template("cables/edit.html", form = f, cable = c)

    
    if(c.name != f.name.data):
        log = Changelog(current_user.id, "Cable", "name", c.id, "Update", c.name, f.name.data)
        db.session().add(log)  
        c.name = f.name.data
    if(c.note != f.note.data):
        log = Changelog(current_user.id, "Cable", "note", c.id, "Update", c.note, f.note.data)
        db.session().add(log)  
        c.note = f.note.data
    if(c.controller_a_id != f.controller_a_id.data):
        log = Changelog(current_user.id, "Cable", "controller_a_id", c.id, "Update", c.controller_a_id, f.controller_a_id.data)
        db.session().add(log)  
        c.controller_a_id = f.controller_a_id.data
    if(c.controller_b_id != f.controller_b_id.data):
        log = Changelog(current_user.id, "Cable", "controller_b_id", c.id, "Update", c.controller_b_id, f.controller_b_id.data)
        db.session().add(log)  
        c.controller_b_id = f.controller_b_id.data

    db.session().commit()

    return redirect(url_for("cables_index"))


#Kuunnellaan osoitteeseen /cables/<cable_id>/delete/ tulevia
#POST-pyyntöjä. Poistetaan parametrina tulevaa <cable_id> vastaava
#Kaapeli tietokannasta ja uudelleenohjataan käyttäjä osoitteeseen
#/cables
@app.route("/cables/<cable_id>/delete/", methods=["POST"])
@login_required(role="USER")
def cables_delete(cable_id): 
    log = Changelog(current_user.id, "Cable", "", cable_id, "Delete", Cable.query.get(cable_id).name, "")
    db.session().add(log)

    for t in Thread.query.filter_by(cable_id = cable_id):
        Thread.query.filter_by(cable_id=cable_id).delete()
    
    Cable.query.filter_by(id=cable_id).delete()   
    db.session().commit()
    
    return redirect(url_for("cables_index"))
