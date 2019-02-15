from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.changelog.models import Changelog
from application.changelog.forms import SearchForm

#Kuunnellaan osoitteeseen /changelog tulevia GET-Pyyntöjä
#Palautetaan changelog/list.html näkymä, 
#jolle annetaan "Select * from Changelog"-kyselyn tulos
@app.route("/changelog", methods=["GET"])
def changelog_index():
    f = SearchForm()
    f.setupChoices()
    return render_template("changelog/list.html", changes = Changelog.query.all(), form = f)

#Kuunnellaan osoitteeseen /changelog tulevia POST-Pyyntöjä
#Palautetaan changelog/list.html näkymä,
#jolle annetaan parametrina tulevan seachformin sisällön
#määrittelevän tietokantakyselyn tulos
@app.route("/changelog", methods=["POST"])
def changelog_search():
    f = SearchForm(request.form)
    if f.modified_by.data != "" and f.targetTable.data != "" and f.target.data != "":
        changes = Changelog.findByUserAndTableAndId(f.modified_by.data, f.targetTable.data, f.target.data)
        f.setupChoices()
        f.setupTarget(f.targetTable.data)
        f.targetTable.default = f.targetTable.data
        return render_template("changelog/list.html", changes = changes, form = f)
    elif f.modified_by.data != "" and f.targetTable.data != "":
        changes = Changelog.findByUserAndTable(f.modified_by.data, f.targetTable.data)
        f.setupChoices()
        f.setupTarget(f.targetTable.data)
        f.targetTable.default = f.targetTable.data
        return render_template("changelog/list.html", changes = changes, form = f)
    elif f.modified_by.data != "":
        changes = Changelog.findByUser(f.modified_by.data)
        f.setupChoices()
        return render_template("changelog/list.html", changes = changes, form = f)
    elif f.targetTable.data != "":
        changes = Changelog.findByTable(f.targetTable.data)
        f.setupChoices()
        f.setupTarget(f.targetTable.data)
        f.targetTable.default = f.targetTable.data
        return render_template("changelog/list.html", changes = changes, form = f)
    else:
        changes = Changelog.query.all()
        f.setupChoices()
        return render_template("changelog/list.html", changes = changes, form = f)


        
