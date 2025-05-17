
import flask
import jinja2
import flask_login
import sirope
from models.noticia import Noticia
from models.usuario import Usuario

apib = flask.Blueprint("api", __name__, template_folder="templates", static_folder="static")

srp = sirope.Sirope()

@apib.route("/c/noticia", methods = ["POST"])
def publicar_endpoint():
    titulo = flask.request.form.get("titulo")
    subtitulo = flask.request.form.get("subtitulo")
    contenido = flask.request.form.get("contenido")
    if Usuario.current_user() == None:
        flask.abort(403)
    else:
        periodistac = Usuario.current_user().id
    srp.save(Noticia(titulo, subtitulo, contenido, periodista=periodistac))
    return flask.redirect("/noticias")

@apib.route("/l/logout", methods = ["POST"])
def logout():
    flask_login.logout_user()
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
    email = flask.request.form.get("username")
    password = flask.request.form.get("password")

    # Check if the user already exists
    if Usuario.find(srp, email):
        return flask.jsonify({"status": "error", "message": "User already exists"}), 400

    # Create a new user and save it
    new_user = Usuario(email, password)
    srp.save(new_user)
    return flask.jsonify({"status": "success", "message": "User registered successfully"}), 201

@apib.route("/l/login", methods=["POST"])
def login():
    email = flask.request.form.get("username")
    password = flask.request.form.get("password")
    
    # Find the user in the database
    user = Usuario.find(srp, email)  # Assuming `Usuario.find` is implemented to retrieve a user by email
    
    if user and user.check_password(password):  # Validate the password
        flask_login.login_user(user)  # Log in the user
        flask.session.modified = True  # Mark the session as modified to ensure it is saved
        print("User session", flask_login.current_user.id)
    
        return flask.redirect("/noticias")
    else:
        return flask.redirect("/login")  # Redirect to login page if authentication fails