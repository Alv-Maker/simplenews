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
        return flask.send_from_directory(loginb.static_folder, "login.html")
    
@loginb.route("/register")
def register_page():
    if Usuario.current_user() != None:
        return flask.redirect("/noticias")
    else:
        return flask.send_from_directory(loginb.static_folder, "register.html")