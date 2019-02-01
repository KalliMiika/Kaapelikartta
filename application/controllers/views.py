from flask import redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db
from application.controllers.models import Controller
from application.controllers.forms import ControllerForm

#Kuunnellaan osoitteeseen /controllers tulevia GET-Pyyntöjä
#Palautetaan controllers/list.html näkymä, 
# jolle annetaan "Select * from Controller"-kyselyn tulos
@app.route("/controllers", methods=["GET"])
def controllers_index():
    return render_template("controllers/list.html", controllers = Controller.query.all())

#Kuunnellaan osoitteeseen /controllers/new/ tulevia GET-Pyyntöjä
#Palautetaan controllers/new.html sivu, parametriksi annetaan
#controllers/forms.py määrittelemät elementit
@app.route("/controllers/new/")
@login_required
def controllers_form():
    return render_template("controllers/new.html", form = ControllerForm())


#Kuunnellaan osoitteeseen /controllers/<controller_id> tulevia GET-Pyyntöjä
#Palautetaan <controller_id>:n määrittelemää risteyskojetta vastaava
# controllers/edit.html sivu, parametriksi annetaan
#controllers/forms.py määrittelemät elementit
@app.route("/controllers/<controller_id>/", methods=["GET"])
@login_required
def controllers_view_one(controller_id):
    return render_template("controllers/edit.html", form = ControllerForm(), controller = Controller.query.get(controller_id))

#Kuunnellaan osoitteeseen /controllers/<controller_id> tulevia POST-Pyyntöjä
#Etsitään <controller_id>:tä vastaava risteyskoju tietokannasta ja
# päivitetään sen tiedot POST-Pyynnön mukana tulleilla syötteillä.
#Päivitetään lopuksi muunneltu risteyskoje tietokantaan ja
# uudelleenohjataan käyttäjä osoitteeseen /controllers
@app.route("/controllers/<controller_id>/", methods=["POST"])
@login_required
def controllers_edit_one(controller_id):
    form = ControllerForm(request.form)

    #Validoidaan ControllerFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan controllers/edit.html sivu
    #virheviestin kera.
    if not form.validate():
        return render_template("controllers/edit.html", form = form, controller = Controller.query.get(controller_id))

    c = Controller.query.get(controller_id)

    c.name = form.name.data
    c.note = form.note.data
    c.x = form.x.data
    c.y = form.y.data

    db.session().commit()

    return redirect(url_for("controllers_index"))

#Kuunnellaan osoitteeseen /controllers/ tulevia POST-Pyyntöjä
#Syötteestä kerätään risteyskojeelle nimi, viesti, x ja y koordinaatit
#ja lisätään se lopuksi tietokantaan  ja uudelleenohjataan 
# käyttäjä osoitteeseen /controllers
@app.route("/controllers/", methods=["POST"])
@login_required
def controllers_create():
    form = ControllerForm(request.form)

    #Validoidaan ControllerFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan controllers/new.html sivu
    #virheviestin kera.
    if not form.validate():
        return render_template("controllers/new.html", form = form)

    c = Controller(form.name.data, form.note.data, form.x.data, form.y.data)
    
    db.session().add(c)
    db.session().commit()
    
    return redirect(url_for("controllers_index"))

@app.route("/controllers/<controller_id>/delete/", methods=["POST"])
@login_required
def controllers_delete(controller_id):
    Controller.query.filter_by(id=controller_id).delete()
    db.session().commit()
    
    return redirect(url_for("controllers_index"))