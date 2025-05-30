import flask
import jinja2
import flask_login
import sirope
from models.noticia import Noticia
from models.usuario import Usuario

loginb = flask.Blueprint("users", __name__, template_folder="templates", static_folder="static")

srp = sirope.Sirope()



@loginb.route("/")
def login_page():
    if Usuario.current_user() != None:
        return flask.redirect("/noticias")
    else:
        if flask.get_flashed_messages():
            error = flask.get_flashed_messages().pop(0)
        else:
            error = ""
        return flask.render_template("login.html",error=error)
    
@loginb.route("/register")
def register_page():
    if Usuario.current_user() != None:
        return flask.redirect("/noticias")
    else:
        return flask.send_from_directory(loginb.static_folder, "register.html")

@loginb.route("/profile")
def profile_page():
    if Usuario.current_user() == None:
        flask.flash("Debes iniciar sesión para acceder a tu perfil")
        return flask.redirect("/login")
    else:
        user = Usuario.current_user()
        return flask.render_template("profile.html", usuario=user)
    
