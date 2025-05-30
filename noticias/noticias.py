import flask
import jinja2
import flask_login
import sirope
from models.noticia import Noticia
from models.usuario import Usuario

noticiasb = flask.Blueprint("noticias", __name__, template_folder="templates", static_folder="static")

srp = sirope.Sirope()




@noticiasb.route("/")
def noticias_page():

    noticias = list(srp.load_all(Noticia))
    noticias.sort(key=lambda x: x.ID, reverse=True)
    print("session", flask_login.current_user)
    return flask.render_template("noticias.html", noticias=noticias, sesion = Usuario.current_user() != None)

@noticiasb.route("/<int:noticia_id>/")
def noticia_page(noticia_id):
    noticiasdb = srp.load_all(Noticia)
    noticia = next((n for n in noticiasdb if n.ID == noticia_id), None)
    arrcom = []
    
    for comentario in noticia.comentarios:
        arrcom.append(srp.load(comentario))
    if noticia:
        return flask.render_template("noticia.html", noticia=noticia, sesion =  Usuario.current_user() != None, usuario = Usuario.current_user(), comentarios = arrcom)
    else:
        return flask.abort(404)
    
@noticiasb.route("/b/")
def busqueda():
    query = flask.request.args.get("q")
    if query is None:
        return flask.abort(404)
    if not query:
        return flask.redirect("/noticias")
    
    noticias = srp.load_all(Noticia)
    resultados = [n for n in noticias if query.lower() in n.titulo.lower() or query.lower() in n.subtitulo.lower()]
    return flask.render_template("noticias_busqueda.html", noticias = resultados, sesion = Usuario.current_user() != None, busqueda = query)

@noticiasb.route("/publicar/")
def publicar():
    return flask.render_template("crear_noticia.html", sesion = Usuario.current_user() != None)