from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.controllers.models import Controller
from application.cables.models import Cable
from application.threads.models import Thread
from application.crossconnections.models import Crossconnection
from application.crossconnections.forms import CrossconnectionForm
from application.changelog.models import Changelog

#Kuunnellaan osoitteeseen /crossconnections/<controller_id>/create/ 
#tulevia GET ja POST -Pyyntöjä
#GET-Pyynnöille:
#   Palautetaan <controller_id>:n määrittelemää risteyskojetta vastaava
#   crossconnections/new.html sivu, parametriksi annetaan
#   crossconnections/forms.py määrittelemät elementit
#POST -Pyynnöistä:
#   Kerätään talteen tarvittavat tiedot uuden Ristikytkennän
#   tallentamiseen tietokantaan.
@app.route("/crossconnections/<controller_id>/create/", methods=["GET", "POST"])
@login_required(role="USER")
def crossconnections_create(controller_id):
    if request.method == "GET":
        f = CrossconnectionForm()
        f.setupChoices(controller_id)
        c = Controller.query.get(controller_id)
        return render_template("crossconnections/new.html", form = f, controller = c)

    f = CrossconnectionForm(request.form)
    f.setupChoices(controller_id)
    if not f.validate():
        c = Controller.query.get(controller_id)
        return render_template("crossconnections/new.html", form = f, controller = c)
    if not f.validate2():
        c = Controller.query.get(controller_id)
        return render_template("crossconnections/new.html", form = f, controller = c)
    
    cc = Crossconnection(controller_id, f.thread_a_id.data, f.thread_b_id.data, f.device_a.data, f.device_b.data)
    db.session().add(cc)
    db.session().commit()

    log = Changelog(current_user.id, "Crossconnection", "", cc.id, "Create", "", "")
    db.session().add(log)
    db.session().commit()

    return redirect(url_for("controllers_view_one", controller_id = controller_id))

#Kuunnellaan osoitteeseen /crossconnections/<crossconnection_id>/edit/ tulevia GET- ja POST-Pyyntöjä
#GET-Pyynnöille:
#   Palautetaan <crossconnection_id>:n määrittelemää kaapelia vastaava
#   crossconnections/edit.html sivu, parametriksi annetaan
#   crossconnections/forms.py määrittelemät elementit
#POST-Pyynnöille:
#   Etsitään <crossconnection_id>:tä vastaava ristikytkentä tietokannasta ja
#   päivitetään sen tiedot POST-Pyynnön mukana tulleilla parametreilla.
#   Päivitetään lopuksi muunneltu ristikytkentä tietokantaan ja
#   uudelleenohjataan käyttäjä osoitteeseen /controllers/<controller_id>/view/
@app.route("/crossconnections/<crossconnection_id>/edit/", methods=["GET", "POST"])
@login_required(role="USER")
def crossconnections_edit_one(crossconnection_id):
    if request.method == "GET":
        c = Crossconnection.query.get(crossconnection_id)
        f = CrossconnectionForm()
        f.setupChoices(c.controller_id)
        f.thread_a_id.default=c.thread_a_id
        f.thread_b_id.default=c.thread_b_id
        f.process()
        return render_template("crossconnections/edit.html", form = f, crossconnection = c)

    f = CrossconnectionForm(request.form)
    c = Crossconnection.query.get(crossconnection_id)
    #Validoidaan CrossconnectionFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan cables/edit.html sivu
    #virheviestin kera.
    f.setupChoices(c.controller_id)
    if not f.validate():
        return render_template("crossconnections/edit.html", form = f, crossconnection = c)
    if not f.validate2():
        return render_template("crossconnections/edit.html", form = f, crossconnection = c)
    
    if(c.thread_a_id != f.thread_a_id.data):
        log = Changelog(current_user.id, "Crossconnection", "thread_a_id", c.id, "Update", c.thread_a_id, f.thread_a_id.data)
        db.session().add(log)  
        c.thread_a_id = f.thread_a_id.data
    if(c.thread_b_id != f.thread_b_id.data):
        log = Changelog(current_user.id, "Crossconnection", "thread_b_id", c.id, "Update", c.thread_b_id, f.thread_b_id.data)
        db.session().add(log)  
        c.thread_b_id = f.thread_b_id.data
    if(c.device_a != f.device_a.data):
        log = Changelog(current_user.id, "Crossconnection", "device_a", c.id, "Update", c.device_a, f.device_a.data)
        db.session().add(log)  
        c.device_a = f.device_a.data
    if(c.device_b != f.device_b.data):
        log = Changelog(current_user.id, "Crossconnection", "device_b", c.id, "Update", c.device_b, f.device_b.data)
        db.session().add(log)  
        c.device_b = f.device_b.data

    db.session().commit()

    return redirect(url_for("controllers_view_one", controller_id = c.controller_id))

#Kuunnellaan osoitteeseen /crossconnections/<crossconnection_id>/delete/ tulevia
#POST-pyyntöjä. Poistetaan parametrina tulevaa <crossconnection_id> vastaava
#ristikytkentä tietokannasta ja uudelleenohjataan käyttäjä osoitteeseen
#/controllers/<controller_id>/view/
@app.route("/crossconnections/<crossconnection_id>/delete/", methods=["POST"])
@login_required(role="USER")
def crossconnections_delete(crossconnection_id): 
    c = Crossconnection.query.get(crossconnection_id)
    controller_id = c.controller_id
    log = None
    if c.thread_a_id == 0:
        cable_b = Cable.query.get(Thread.query.get(c.thread_b_id).cable_id)
        log = Changelog(current_user.id, "Crossconnection", "", 0, "Delete", " -- "+cable_b.name + "/" +str(Thread.query.get(c.thread_b_id).socket_a), "")
        
    elif c.thread_b_id == 0:
        cable_a = Cable.query.get(Thread.query.get(c.thread_a_id).cable_id)
        log = Changelog(current_user.id, "Crossconnection", "", 0, "Delete", cable_a.name + "/" +str(Thread.query.get(c.thread_a_id).socket_a) + " -- ", "")
    else:
        cable_a = Cable.query.get(Thread.query.get(c.thread_a_id).cable_id)
        cable_b = Cable.query.get(Thread.query.get(c.thread_b_id).cable_id)
        log = Changelog(current_user.id, "Crossconnection", "", 0, "Delete", cable_a.name + "/" +str(Thread.query.get(c.thread_a_id).socket_a) + " -- "+cable_b.name + "/" +str(Thread.query.get(c.thread_b_id).socket_a), "")
    
    Crossconnection.query.filter_by(id=c.id).delete()
    db.session().add(log)   
    db.session().commit()
    return redirect(url_for("controllers_view_one", controller_id = controller_id))