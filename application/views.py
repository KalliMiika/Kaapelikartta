from flask import redirect, render_template, request, url_for
from application import app, db

from application.controllers.models import Controller

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
    return render_template("index.html", controllers = Controller.query.all())