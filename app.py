import flask
import jinja2
import flask_login
import sirope
from models.noticia import Noticia
from noticias.noticias import noticiasb


app = flask.Flask(__name__)


app.register_blueprint(noticiasb, url_prefix="/noticias")

noticias = [Noticia("Cae la bolsa", "La bolsa española cae un 10%", "La bolsa ha caído un 10% en la última semanaLos mercados financieros han experimentado una fuerte corrección en los últimos días, con una caída acumulada superior al 10% en la última semana. La incertidumbre económica y las tensiones comerciales han sido factores clave en este desplome, afectando a los principales índices bursátiles.\
\n\nEl S&P 500 ha perdido un 1.4% en la jornada más reciente, mientras que el Dow Jones cayó un 1.45% y el Nasdaq un 2%. La volatilidad ha sido extrema, con oscilaciones de cientos de puntos en cuestión de horas.\
\n\nLos analistas atribuyen esta caída a la escalada de aranceles impuesta por el gobierno de EE.UU., lo que ha generado preocupación entre los inversores sobre el impacto en el comercio global. Además, los rendimientos de los bonos del Tesoro han disminuido, reflejando el pesimismo sobre el futuro económico.\
\n\nA pesar de los datos alentadores sobre inflación y desempleo, el mercado sigue reaccionando con nerviosismo. Los expertos advierten que, si la incertidumbre persiste, podríamos ver nuevas correcciones en los próximos días.\
\n\nLos inversores ahora observan con atención los próximos movimientos de los bancos centrales y las decisiones políticas que podrían influir en la recuperación del mercado. ¿Será este el inicio de una tendencia bajista prolongada o una oportunidad de compra?", None),
            Noticia("Sube el precio del petróleo", "El precio del petróleo sube un 5%", "El precio del petróleo ha subido un 5% en la última semana", None),
           Noticia("La inflación se dispara", "La inflación se dispara un 2%", "La inflación se ha disparado un 2% en la última semana", None),
           Noticia("El desempleo aumenta", "El desempleo aumenta un 1%", "El desempleo ha aumentado un 1% en la última semana", None)]

srp = sirope.Sirope()
#srp.save(noticias[0])
#srp.save(noticias[1])
#srp.save(noticias[2])
#srp.save(noticias[3])



appdata = {"session": True}

@app.route("/")
def index():
    return flask.send_from_directory(app.static_folder, "index.html")






@app.route("/api/c/noticia", methods = ["POST"])
def publicar_endpoint():
    titulo = flask.request.form.get("titulo")
    subtitulo = flask.request.form.get("subtitulo")
    contenido = flask.request.form.get("contenido")
    srp.save(Noticia(titulo, subtitulo, contenido, "Redaccion"))
    return flask.redirect("/noticias")

@app.route("/api/l/logout", methods = ["POST"])
def logout():
    appdata["session"] = False
    return flask.send_from_directory("/noticias")


#@app.errorhandler(404)
#def not_found(code):
#    return flask.abort(404)



if __name__ == "__main__":
    app.run(debug=True)