from application import app, db
from flask import redirect, render_template, request, url_for
from application.controllers.models import Controller

#Kuunnellaan osoitteeseen /controllers tulevia GET-Pyyntöjä
#Palautetaan controllers/list.html näkymä, 
# jolle annetaan "Select * from Controller"-kyselyn tulos
@app.route("/controllers", methods=["GET"])
def controllers_index():
    return render_template("controllers/list.html", controllers = Controller.query.all())

#Kuunnellaan osoitteeseen /controllers/new/ tulevia GET-Pyyntöjä
#Palautetaan controllers/new.html sivu
@app.route("/controllers/new/")
def controllers_form():
    return render_template("controllers/new.html")


#Kuunnellaan osoitteeseen /controllers/<controller_id> tulevia GET-Pyyntöjä
#Palautetaan <controller_id>:n määrittelemää risteyskojetta vastaava
# controllers/edit.html sivu.
@app.route("/controllers/<controller_id>/", methods=["GET"])
def controllers_view_one(controller_id):
    return render_template("controllers/edit.html", controller = Controller.query.get(controller_id))

#Kuunnellaan osoitteeseen /controllers/<controller_id> tulevia POST-Pyyntöjä
#Etsitään <controller_id>:tä vastaava risteyskoju tietokannasta ja
# päivitetään sen tiedot POST-Pyynnön mukana tulleilla syötteillä.
#Päivitetään lopuksi muunneltu risteyskoje tietokantaan ja
# uudelleenohjataan käyttäjä osoitteeseen /controllers
@app.route("/controllers/<controller_id>/", methods=["POST"])
def controllers_edit_one(controller_id):
    c = Controller.query.get(controller_id)

    c.name = request.form.get("name")
    c.note = request.form.get("note")
    c.x = request.form.get("x")
    c.y = request.form.get("y")

    db.session().commit()
    return redirect(url_for("controllers_index"))

#Kuunnellaan osoitteeseen /controllers/ tulevia POST-Pyyntöjä
#Syötteestä kerätään risteyskojeelle nimi, viesti, x ja y koordinaatit
#ja lisätään se lopuksi tietokantaan
@app.route("/controllers/", methods=["POST"])
def controllers_create():
    c = Controller(request.form.get("name"), request.form.get("note"), request.form.get("x"), request.form.get("y"))
    
    db.session().add(c)
    db.session().commit()
    
    return redirect(url_for("controllers_index"))