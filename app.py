import flask
import jinja2
import flask_login
import sirope
from models.noticia import Noticia
from noticias.noticias import noticiasb
from users.users import loginb
from api.api import apib
from models.usuario import Usuario
import json

with open("config/appconfig.json") as config_file:
    config = json.load(config_file)

app = flask.Flask(__name__)
app.secret_key = config["SECRET_KEY"]  # Cambiar esto a una clave secreta más segura en la entrega


app.register_blueprint(noticiasb, url_prefix="/noticias")
app.register_blueprint(loginb, url_prefix="/users")
app.register_blueprint(apib, url_prefix="/api")


srp = sirope.Sirope()


lm = flask_login.LoginManager()
lm.init_app(app)


@app.route("/")
def index():
    return flask.send_from_directory(app.static_folder, "index.html")

@app.route("/about")
def about():
    return flask.render_template("about.html", sesion = Usuario.current_user())


@app.errorhandler(405)
def method_not_allowed(e):
    return flask.send_from_directory(app.static_folder, "405page.html"), 403

@app.errorhandler(404)
def page_not_found(e):
    return flask.send_from_directory(app.static_folder, "404page.html"), 404

@app.before_request
def before_request():
    if(flask.request.path.startswith("/static") and not flask.request.path.startswith("/static/img")):
        return flask.send_from_directory(app.static_folder, "404page.html"), 404
    
@app.errorhandler(500)
def internal_server_error(e):
    return flask.send_from_directory(app.static_folder, "500page.html"), 500




@lm.user_loader
def user_loader(email):
    return Usuario.find(srp, email)

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/noticias")




if __name__ == "__main__":
    app.run(debug=True)