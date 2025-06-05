
from http.client import HTTPResponse
import os
import flask
import jinja2
import flask_login
import sirope
from models.comentario import Comentario
from models.noticia import Noticia
from models.ids import NoticiaID
from models.usuario import Usuario






apib = flask.Blueprint("api", __name__, template_folder="templates", static_folder="static")

srp = sirope.Sirope()

idunique = None



idunique = srp.find_first(NoticiaID, lambda x: True)
if idunique is None:
    idunique = NoticiaID()
    srp.save(idunique)
print("API initialized with NoticiaID:", idunique.ID)

def update_noticia_id():
    global idunique
    #srp.delete(idunique.__oid__)
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
    update_noticia_id()
    return flask.redirect("/noticias")

@apib.route("/l/logout", methods = ["POST"])
def logout():
    flask_login.logout_user()
    flask.session.modified = True
    return flask.redirect("/noticias")

@apib.route("/d/noticia/<int:id>", methods = ["DELETE"])
def delete_noticia(id):
    noticia = srp.find_first(Noticia, lambda x: x.ID == id)
    for i in noticia.comentarios:
        srp.delete(i.__oid__)
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
        flask.flash("Invalid username or password")  # Flash an error message
        return flask.redirect("/users")  # Redirect to login page if authentication fails

@apib.route("/l/delete/<id>", methods=["DELETE"])
def delete_user(id):
    user = srp.find_first(Usuario, lambda x: x.id == id)
    if user:
        user.delete()  # Mark the user as deleted
        srp.save(user)
        return flask.jsonify({"status": "success", "message": "User deleted successfully"}), 200
    else:
        return flask.jsonify({"status": "error", "message": "User not found"}), 404

@apib.route("/l/update/<id>", methods=["POST"])
def update_user(id):
    user = srp.find_first(Usuario, lambda x: x.id == id)
    if user:
        if flask.request.form.get("email"):
            user.email = flask.request.form.get("email")
        if flask.request.form.get("password"):
            user.set_password(flask.request.form.get("password"))
        srp.save(user)

        return flask.redirect("/noticias")  # Redirect to noticias page after updating user

@apib.route("/l/checkname", methods=["POST"])
def check_username():
    #username = flask.request.json.get("username")
    username = flask.request.args.get("username")
    user = Usuario.find(srp, username)
    if user:
        
        return flask.jsonify({"status": "error", "exists": "true"}), 400
    else:
        return flask.jsonify({"status": "success", "exists": "false"}), 200
    

        

@apib.route("/c/comentario/<noticia_id>", methods=["POST"])
def comentar_endpoint(noticia_id):
    contenido = flask.request.form.get("contenido")
    if Usuario.current_user() is None:
        flask.abort(403)
    else:
        periodistac = Usuario.current_user().id
    
    noticia = srp.find_first(Noticia, lambda x: x.ID == int(noticia_id))
    if not noticia:
        return flask.jsonify({"status": "error", "message": "Noticia no encontrada"}), 404

    print(type(contenido), type(periodistac))
    comentario = Comentario(contenido, periodistac, noticia.getnxtcmntid())
    oid = srp.save(comentario)
    noticia.add_comentario(oid)
    srp.save(noticia)
    return flask.redirect(f"/noticias/{noticia_id}")  # Redirect to the noticia page after commenting

@apib.route("/d/comentario/<noticia_id>/<int:comentario_id>", methods=["DELETE"])
def delete_comentario_endpoint(noticia_id, comentario_id):
    noticia = srp.find_first(Noticia, lambda x: x.ID == int(noticia_id))
    if not noticia:
        return flask.jsonify({"status": "error", "message": "Noticia no encontrada"}), 404

    comentario = srp.find_first(Comentario, lambda x: x.ID == comentario_id)
    if not comentario:
        return flask.jsonify({"status": "error", "message": "Comentario no encontrado"}), 404

    if noticia.remove_comentario(comentario.__oid__):
        srp.delete(comentario.__oid__)
        srp.save(noticia)
        return flask.jsonify({"status": "success", "message": "Comentario eliminado"}), 200
    else:
        return flask.jsonify({"status": "error", "message": "No se pudo eliminar el comentario"}), 500
    
@apib.route("/update/comentario/<int:comentario_id>", methods=["POST"])
def update_comentario_endpoint(comentario_id):
    current_url = flask.request.url
    comentario = srp.find_first(Comentario, lambda x: x.ID == comentario_id)
    if not comentario:
        return flask.jsonify({"status": "error", "message": "Comentario no encontrado"}), 404

    contenido = flask.request.form.get("contenido")
    if contenido:
        comentario.contenido = contenido
        srp.save(comentario)

    return  flask.redirect(f"/noticias/{flask.request.form['noticia_id']}")  # Redirect to the current page after updating the comment


