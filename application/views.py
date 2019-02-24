from flask import redirect, render_template, request, url_for
from application import app, db

from application.controllers.models import Controller
from application.cables.models import Cable

@app.route("/")
def index():
    cs = Controller.query.all()
    controllers = []
    for c in cs:
        controllers.append({
            "id":c.id,
            "name":c.name,
            "style":"top: "+str(c.y)+"px; left: "+str(c.x)+"px;"
        })
    cables = []
    for c in Cable.query.all():
        con_a = Controller.query.get(c.controller_a_id)
        con_b = Controller.query.get(c.controller_b_id)
        cables.append({
            "id":c.id,
            "name":c.name,
            "x1":con_a.x,
            "y1":con_a.y,
            "x2":con_b.x,
            "y2":con_b.y
        })
    return render_template("index.html", controllers = Controller.query.all(), cables = cables)