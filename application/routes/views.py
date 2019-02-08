from flask import redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db
from application.threads.models import Thread
from application.cables.models import Cable

#Kuunnellaan osoitteeseen /routes tulevia GET-Pyyntöjä
#Palautetaan routes/list.html näkymä, 
#jolle annetaan Thread.find_routes()-kyselyn tulos
@app.route("/routes", methods=["GET"])
def routes_index():
    routes = Thread.find_routes()
    return render_template("routes/list.html", routes = routes)

#
@app.route("/routes/<route>/", methods=["GET"])
def routes_view_one(route):
    route = Thread.get_route(route)
    return render_template("routes/view.html", route = route)

