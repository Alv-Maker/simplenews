import flask
import jinja2
import flask_login
import sirope
from models.noticia import Noticia

noticiasb = flask.Blueprint("noticias", __name__, template_folder="templates", static_folder="static")

srp = sirope.Sirope()
appdata = {"session": True}


@noticiasb.route("/")
def noticias_page():
    noticias = list(srp.load_all(Noticia))
    noticias.sort(key=lambda x: x.ID, reverse=True)
    print("session", appdata["session"])
    return flask.render_template("noticias.html", noticias=noticias, sesion = appdata["session"])

@noticiasb.route("/<int:noticia_id>/")
def noticia_page(noticia_id):
    noticias = srp.load_all(Noticia)
    noticia = next((n for n in noticias if n.ID == noticia_id), None)
    if noticia:
        return flask.render_template("noticia.html", noticia=noticia, sesion = appdata["session"])
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
    return flask.render_template("noticias.html", noticias = resultados)

@noticiasb.route("/publicar/")
def publicar():
    return flask.send_from_directory(noticiasb.static_folder, "crear-noticia.html")