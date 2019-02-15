from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.controllers.models import Controller
from application.controllers.forms import ControllerForm
from application.changelog.models import Changelog

#Kuunnellaan osoitteeseen /controllers tulevia GET-Pyyntöjä
#Palautetaan controllers/list.html näkymä, 
#jolle annetaan "Select * from Controller"-kyselyn tulos
@app.route("/controllers", methods=["GET"])
def controllers_index():
    return render_template("controllers/list.html", controllers = Controller.query.all())

#Kuunnellaan osoitteeseen /controllers/new/ tulevia GET-Pyyntöjä
#Palautetaan controllers/new.html sivu, parametriksi annetaan
#controllers/forms.py määrittelemät elementit
@app.route("/controllers/new/")
@login_required(role="USER")
def controllers_form():
    return render_template("controllers/new.html", form = ControllerForm())


#Kuunnellaan osoitteeseen /controllers/<controller_id> tulevia GET-Pyyntöjä
#Palautetaan <controller_id>:n määrittelemää risteyskojetta vastaava
#controllers/edit.html sivu, parametriksi annetaan
#controllers/forms.py määrittelemät elementit
@app.route("/controllers/<controller_id>/", methods=["GET"])
@login_required(role="USER")
def controllers_view_one(controller_id):
    return render_template("controllers/edit.html", form = ControllerForm(), controller = Controller.query.get(controller_id))

#Kuunnellaan osoitteeseen /controllers/<controller_id> tulevia POST-Pyyntöjä
#Etsitään <controller_id>:tä vastaava risteyskoju tietokannasta ja
#päivitetään sen tiedot POST-Pyynnön mukana tulleilla syötteillä.
#Päivitetään lopuksi muunneltu risteyskoje tietokantaan ja
#uudelleenohjataan käyttäjä osoitteeseen /controllers
@app.route("/controllers/<controller_id>/", methods=["POST"])
@login_required(role="USER")
def controllers_edit_one(controller_id):
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
    log = Changelog(current_user.id, "Controller", "", controller_id, "Delete", "", "")
    db.session().add(log)

    Controller.query.filter_by(id=controller_id).delete()   
    db.session().commit()
    
    return redirect(url_for("controllers_index"))