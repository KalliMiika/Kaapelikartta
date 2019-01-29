from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app
from application.auth.models import User
from application.auth.forms import LoginForm

#Kuunnellaan osoitteeseen /auth/login tulevia GET- ja POST-pyyntöjä
#   GET-pyynnöille palautetaan auth/loginform.html sisäänkirjautumissivu, 
#parametriksi annetaan auth/forms.py määrittelemät elementit
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
def auth_logout():
    #Käyttäjä kirjataan ulos flask_login:n 
    #tarjoamalla logout_user metodilla
    logout_user()

    return redirect(url_for("index"))