
from http.client import HTTPResponse
import flask
import jinja2
import flask_login
import sirope
from models.noticia import Noticia
from models.noticiaid import NoticiaID
from models.usuario import Usuario
import signal

signal.signal(signal.SIGINT, lambda s, f: handle_exit(s, f))
signal.signal(signal.SIGTERM, lambda s, f: handle_exit(s, f))
signal.signal(signal.SIGQUIT, lambda s, f: handle_exit(s, f))

apib = flask.Blueprint("api", __name__, template_folder="templates", static_folder="static")

srp = sirope.Sirope()

idunique = srp.find_first(NoticiaID, lambda x : True)


if idunique == None:
    idunique = NoticiaID()
    srp.save(idunique)

@apib.route("/c/noticia", methods = ["POST"])
def publicar_endpoint():
    titulo = flask.request.form.get("titulo")
    subtitulo = flask.request.form.get("subtitulo")
    contenido = flask.request.form.get("contenido")
    if Usuario.current_user() == None:
        flask.abort(403)
    else:
        periodistac = Usuario.current_user().id
    srp.save(Noticia(titulo, subtitulo, contenido, periodistac, idunique))
    return flask.redirect("/noticias")

@apib.route("/l/logout", methods = ["POST"])
def logout():
    flask_login.logout_user()
    flask.session.modified = True
    return flask.redirect("/noticias")

@apib.route("/d/noticia/<int:id>", methods = ["DELETE"])
def delete_noticia(id):
    noticia = srp.find_first(Noticia, lambda x: x.ID == id)
    if srp.delete(noticia.__oid__):
        return flask.jsonify({"status": "success", "message": "Noticia eliminada"}), 200
    else:
        return flask.jsonify({"status": "error", "message": "Noticia no encontrada"}), 404
    

#@app.errorhandler(404)
#def not_found(code):
#    return flask.abort(404)

@apib.route("/l/register", methods=["POST"])
def register():
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")
    username = flask.request.form.get("username")

    # Check if the user already exists
    if Usuario.find(srp, username):
        return flask.redirect("/users/register")  # Redirect to registration page if user exists

    # Create a new user and save it
    new_user = Usuario(email, password, username)
    srp.save(new_user)
    return flask.redirect("/users")  # Redirect to login page after registration

@apib.route("/l/login", methods=["POST"])
def login():
    username = flask.request.form.get("username")
    password = flask.request.form.get("password")
    
    # Find the user in the database
    user = Usuario.find(srp, username)  # Assuming `Usuario.find` is implemented to retrieve a user by email
    
    if user and user.check_password(password):  # Validate the password
        flask_login.login_user(user)  # Log in the user
        flask.session.modified = True  # Mark the session as modified to ensure it is saved
        print("User session", flask_login.current_user.id)
    
        return flask.redirect("/noticias")
    else:
        return flask.redirect("/users")  # Redirect to login page if authentication fails
    
@apib.route("/l/checkname", methods=["POST"])
def check_username():
    #username = flask.request.json.get("username")
    username = flask.request.args.get("username")
    user = Usuario.find(srp, username)
    if user:
        print(user.id)
        return flask.jsonify({"status": "error", "exists": "true"}), 400
    else:
        return flask.jsonify({"status": "success", "exists": "false"}), 200
    
def handle_exit(signum, frame):
    ls = list(srp.load_all(NoticiaID))
    for i in ls:
        srp.delete(i.__oid__)
    srp.save(idunique)
    exit(0)