from flask import redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db
from application.threads.models import Thread
from application.threads.forms import ThreadForm

#Kuunnellaan osoitteeseen /threads/<thread_id>/edit/ tulevia GET- ja POST-Pyyntöjä
#GET-Pyynnöille:
#   Palautetaan <thread_id>:n määrittelemää säiettä vastaava
#   threads/edit.html sivu, parametriksi annetaan
#   threads/forms.py määrittelemät elementit
#POST-Pyynnöille:
#   Etsitään <thread_id>:tä vastaava säie tietokannasta ja
#   päivitetään sen tiedot POST-Pyynnön mukana tulleilla syötteillä.
#   Päivitetään lopuksi muunneltu säie tietokantaan ja
#   uudelleenohjataan käyttäjä osoitteeseen "täytä"
@app.route("/threads/<thread_id>/edit/", methods=["GET", "POST"])
@login_required
def threads_edit_one(thread_id):
    if request.method == "GET":
        f = ThreadForm()
        t = Thread.query.get(thread_id)
        return render_template("threads/edit.html", form = f, thread = t)

    f = ThreadForm(request.form)
    t = Thread.query.get(thread_id)

    #Validoidaan ThreadFormin sisältämien kenttien datat, jos
    #niissä on häikkää, niin palautetaan threads/edit.html sivu
    #virheviestin kera.
    if not f.validate():
        return render_template("threads/edit.html", form = f, thread = t)

    t.number_a = f.number_a.data
    t.number_b = f.number_b.data
    t.socket_a = f.socket_a.data
    t.socket_b = f.socket_b.data
    t.data = f.data.data
    t.note = f.note.data

    db.session().commit()

    return redirect(url_for("cables_view_one", cable_id=t.cable_id))
