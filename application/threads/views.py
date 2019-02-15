from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.threads.models import Thread
from application.threads.forms import ThreadForm
from application.changelog.models import Changelog

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
@login_required(role="USER")
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

    if(t.number_a != f.number_a.data):
        log = Changelog(current_user.id, "Thread", "number_a", t.id, "Update", t.number_a, f.number_a.data)
        db.session().add(log)  
        t.number_a = f.number_a.data
    if(t.number_b != f.number_b.data):
        log = Changelog(current_user.id, "Thread", "number_b", t.id, "Update", t.number_b, f.number_b.data)
        db.session().add(log)  
        t.number_b = f.number_b.data
    if(t.socket_a != f.socket_a.data):
        log = Changelog(current_user.id, "Thread", "socket_a", t.id, "Update", t.socket_a, f.socket_a.data)
        db.session().add(log)  
        t.socket_a = f.socket_a.data
    if(t.socket_b != f.socket_b.data):
        log = Changelog(current_user.id, "Thread", "socket_b", t.id, "Update", t.socket_b, f.socket_b.data)
        db.session().add(log)  
        t.socket_b = f.socket_b.data
    if(t.data != f.data.data):
        log = Changelog(current_user.id, "Thread", "data", t.id, "Update", t.data, f.data.data)
        db.session().add(log)  
        t.data = f.data.data
    if(t.note != f.note.data):
        log = Changelog(current_user.id, "Thread", "note", t.id, "Update", t.note, f.note.data)
        db.session().add(log)  
        t.note = f.note.data

    db.session().commit()
    
    return redirect(url_for("cables_view_one", cable_id=t.cable_id))
