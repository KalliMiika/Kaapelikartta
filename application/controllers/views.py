from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.controllers.models import Controller
from application.controllers.forms import ControllerForm
from application.changelog.models import Changelog
from application.crossconnections.models import Crossconnection
from application.cables.models import Cable
from application.threads.models import Thread

#Kuunnellaan osoitteeseen /controllers tulevia GET-Pyyntöjä
#Palautetaan controllers/list.html näkymä, 
#jolle annetaan "Select * from Controller"-kyselyn tulos
@app.route("/controllers", methods=["GET"])
def controllers_index():
    return render_template("controllers/list.html", controllers = Controller.findAll())


#Kuunnellaan osoitteeseen /controllers/new/ tulevia GET-Pyyntöjä
#Palautetaan controllers/new.html sivu, parametriksi annetaan
#controllers/forms.py määrittelemät elementit
@app.route("/controllers/new/")
@login_required(role="USER")
def controllers_form():
    return render_template("controllers/new.html", form = ControllerForm())


#Kuunnellaan osoitteeseen /controllers/<controller_id>/view/
@app.route("/controllers/<controller_id>/view/", methods=["GET"])
def controllers_view_one(controller_id):
    c = Controller.query.get(controller_id)
    ham = []
    ccs = Crossconnection.query.filter_by(controller_id=controller_id)
    for cc in ccs:
        thread_a = None
        cable_a = None
        data_a = None
        thread_a = None
        if cc.thread_a_id > 0:
            thread_a = Thread.query.get(cc.thread_a_id)
            cable_a = Cable.query.get(thread_a.cable_id).name
            data_a = Thread.query.get(cc.thread_a_id).data
            thread_a = Thread.query.get(cc.thread_a_id).socket_a
        thread_b = None
        cable_b = None
        data_b = None
        thread_b = None
        if cc.thread_b_id > 0:
            thread_b = Thread.query.get(cc.thread_b_id)
            cable_b = Cable.query.get(thread_b.cable_id).name
            data_b = Thread.query.get(cc.thread_b_id).data
            thread_b = Thread.query.get(cc.thread_b_id).socket_a
        ham.append({
            "id":cc.id,
            "cable_a":cable_a, "cable_b":cable_b,
            "thread_a":thread_a, "thread_b":thread_b,
            "data_a":data_a, "data_b":data_b,
            "device_a":cc.device_a, "device_b":cc.device_b
        })
    return render_template("controllers/view.html", controller = c, ham = ham)


#Kuunnellaan osoitteeseen /controllers/<controller_id> tulevia 
#GET- ja POST -Pyyntöjä
#Get -Pyynöille: 
#Palautetaan <controller_id>:n määrittelemää risteyskojetta vastaava
#controllers/edit.html sivu, parametriksi annetaan
#controllers/forms.py määrittelemät elementit
#Post -Pyynnöille:
#Etsitään <controller_id>:tä vastaava risteyskoju tietokannasta ja
#päivitetään sen tiedot POST-Pyynnön mukana tulleilla syötteillä.
#Päivitetään lopuksi muunneltu risteyskoje tietokantaan ja
#uudelleenohjataan käyttäjä osoitteeseen /controllers
@app.route("/controllers/<controller_id>/edit/", methods=["GET", "POST"])
@login_required(role="USER")
def controllers_edit_one(controller_id):
    if request.method == "GET":
        return render_template("controllers/edit.html", form = ControllerForm(), controller = Controller.query.get(controller_id))
    
    f = ControllerForm(request.form)
    c = Controller.query.get(controller_id)

    #Validoidaan ControllerFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan controllers/edit.html sivu
    #virheviestin kera.
    if not f.validate():
        return render_template("controllers/edit.html", form = f, controller = Controller.query.get(controller_id))
    nameNotEdited = True
    if(c.name != f.name.data):
        nameNotEdited = False
    if not f.validate2(nameNotEdited):
        return render_template("controllers/edit.html", form = f, controller = c)


    if(c.name != f.name.data):
        log = Changelog(current_user.id, "Controller", "name", c.id, "Update", c.name, f.name.data)
        db.session().add(log)
        c.name = f.name.data
    if(c.note != f.note.data):
        log = Changelog(current_user.id, "Controller", "note", c.id, "Update", c.note, f.note.data)
        db.session().add(log)
        c.note = f.note.data
    if(c.x != f.x.data):
        log = Changelog(current_user.id, "Controller", "x", c.id, "Update", c.x, f.x.data)
        db.session().add(log)
        c.x = f.x.data
    if(c.y != f.y.data):
        log = Changelog(current_user.id, "Controller", "y", c.id, "Update", c.y, f.y.data)
        db.session().add(log)        
        c.y = f.y.data


    db.session().commit()

    return redirect(url_for("controllers_index"))


#Kuunnellaan osoitteeseen /controllers/ tulevia POST-Pyyntöjä
#Syötteestä kerätään risteyskojeelle nimi, viesti, x ja y koordinaatit
#ja lisätään se lopuksi tietokantaan  ja uudelleenohjataan 
#käyttäjä osoitteeseen /controllers
@app.route("/controllers/", methods=["POST"])
@login_required(role="USER")
def controllers_create():
    f = ControllerForm(request.form)

    #Validoidaan ControllerFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan controllers/new.html sivu
    #virheviestin kera.
    if not f.validate():
        return render_template("controllers/new.html", form = f)
    if not f.validate2(False):
        return render_template("controllers/new.html", form = f)

    c = Controller(f.name.data, f.note.data, f.x.data, f.y.data)
    db.session().add(c)
    db.session().commit()

    log = Changelog(current_user.id, "Controller", "", c.id, "Create", "", "")
    db.session().add(log)
    db.session().commit()
    
    return redirect(url_for("controllers_index"))


#Kuunnellaan osoitteeseen /controllers/<controller_id>/delete/ tulevia
#POST-pyyntöjä. Poistetaan parametrina tulevaa <controller_id> vastaava
#Risteyskoje tietokannasta ja uudelleenohjataan käyttäjä osoitteeseen
#/controllers
@app.route("/controllers/<controller_id>/delete/", methods=["POST"])
@login_required(role="USER")
def controllers_delete(controller_id): 
    log = Changelog(current_user.id, "Controller", "", 0, "Delete", Controller.query.get(controller_id).name, "")

    for c in Cable.query.filter_by(controller_a_id = controller_id):
        log2 = Changelog(current_user.id, "Cable", "", 0, "Delete", Cable.query.get(c.id).name, "")

        for t in Thread.query.filter_by(cable_id = c.id):
            Changelog.deleteByTableAndId("Thread", t.id)
            db.session().commit()

        Changelog.deleteByTableAndId("Cable", c.id)
        Thread.query.filter_by(cable_id=c.id).delete()
        Cable.query.filter_by(id=c.id).delete()
        db.session().add(log2) 
        db.session().commit()

    for c in Cable.query.filter_by(controller_b_id = controller_id):
        log2 = Changelog(current_user.id, "Cable", "", 0, "Delete", Cable.query.get(c.id).name, "")

        for t in Thread.query.filter_by(cable_id = c.id):
            Changelog.deleteByTableAndId("Thread", t.id)
            db.session().commit()
            
        Changelog.deleteByTableAndId("Cable", c.id)
        Thread.query.filter_by(cable_id=c.id).delete()
        Cable.query.filter_by(id=c.id).delete()
        db.session().add(log2)
        db.session().commit() 

    Changelog.deleteByTableAndId("Controller", controller_id)
    Controller.query.filter_by(id=controller_id).delete()
    db.session().add(log)   
    db.session().commit()
    
    return redirect(url_for("controllers_index"))