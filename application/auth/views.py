from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm
from application.changelog.models import Changelog

#Kuunnellaan osoitteeseen /auth/login tulevia GET- ja POST-pyyntöjä
#   GET-pyynnöille palautetaan auth/loginform.html sisäänkirjautumissivu, 
#parametriksi annetaan auth/forms.py LoginForm määrittelemät elementit
#   Post-pyynnöistä kerätään talteen auth/forms.py määrittelemän
#LoginForm olion sisältämät käyttäjätiedot, joiden perusteella
#etsitään auth/models.py määritelty käyttäjätili tietokannasta ja 
#kirjataan käyttäjä sisään. Mikäli tunnuksia vastaavaa käyttäjätiliä
#ei löydy, uudelleenohjataan käyttäjä osoitteeseen /auth/login
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    # mahdolliset validoinnit

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "No such username or password")

    #Käyttäjä kirjataan sisään flask_login:n 
    #tarjoamalla login_user metodilla
    login_user(user)
    
    return redirect(url_for("index"))

#"/auth/logout" osoitteeseen tulevat pyynnöt
#kirjaavat käyttäjän ulos
@app.route("/auth/logout")
@login_required(role="USER")
def auth_logout():
    #Käyttäjä kirjataan ulos flask_login:n 
    #tarjoamalla logout_user metodilla
    logout_user()

    return redirect(url_for("index"))

#Kuunnellaan osoitteeseen /auth/register tulevia GET- ja POST -pyyntöjä
#   Get-Pyynnöille palautetaan auth/new.html rekisteröintilomake
#parametriksi annetaan RegisterForm
#   Post-Pyynnöistä kerätään talteen auth/forms.py määrittelemän
#RegisterForm olion sisältämät käyttäjätiedot, joiden perusteella
#Luodaan uusi käyttäjä tietokantaan ja kirjataan käyttäjä sisään. 
#Mikäli rekisteröinnissä tapahtuu virhe, (esim käyttäjänimi on jo 
#käytössä) uudelleenohjataan käyttäjä osoitteeseen /auth/register
@app.route("/auth/register", methods=["GET", "POST"])
@login_required(role="ADMIN")
def auth_register():
    if request.method == "GET":
        return render_template("auth/new.html", form = RegisterForm())

    form = RegisterForm(request.form)

    #Validoidaan RegisterFormin sisältämien kenttien datat, jos
    #niissä on häikkää, palautetaan auth/new.html sivu
    #virheviestin kera
    if not form.validate():
        return render_template("auth/new.html", form = form)
    #Validoidaan uniikki käyttäjätunnus, jos käyttäjätunnus on
    #käytössä, palautetaan auth/new.html sivu virheviestin kera
    if not form.validateUsername():
        return render_template("auth/new.html", form = form)


    #Luodaan uusi käyttäjä LoginFormista kerätyn datan perusteella
    #default käyttäjätaso on peruskäyttäjä "user"
    u = User(form.name.data, form.username.data, form.password.data, "user")
    db.session().add(u)
    db.session().commit()
    
    log = Changelog(current_user.id, "Account", "", u.id, "Create", "", "")
    db.session().add(log)
    db.session().commit()

    return redirect(url_for("controllers_index"))
