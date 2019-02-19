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
# 
@app.route("/crossconnections/<controller_id>/create/", methods=["GET", "POST"])
def crossconnections_create(controller_id):
    if request.method == "GET":
        f = CrossconnectionForm()
        f.setupChoices()
        return render_template("crossconnections/new.html", form = f, controller_id = controller_id)

    f = CrossconnectionForm(request.form)
    f.setupChoices()
    if not f.validate():
        return render_template("crossconnections/new.html", form = f, controller_id = controller_id)
    if not f.validate2(False):
        return render_template("crossconnections/new.html", form = f, controller_id = controller_id)
    
    cc = Crossconnection(controller_id, f.thread_a_id.data, f.thread_b_id.data, f.device_a.data, f.device_b.data)
    db.session().add(cc)
    db.session().commit()

    log = Changelog(current_user.id, "Crossconnection", "", cc.id, "Create", "", "")
    db.session().add(log)
    db.session().commit()

    return redirect(url_for("index"))