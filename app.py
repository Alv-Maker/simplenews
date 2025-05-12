import flask
import jinja2
import flask_login
import sirope
from models.noticia import Noticia
from noticias.noticias import noticiasb
from users.login import loginb
from models.usuario import Usuario


app = flask.Flask(__name__)
app.secret_key = "supersecretkey"  # Cambiar esto a una clave secreta más segura en la entrea


app.register_blueprint(noticiasb, url_prefix="/noticias")
app.register_blueprint(loginb, url_prefix="/login")

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


lm = flask_login.LoginManager()
lm.init_app(app)





@app.route("/")
def index():
    return flask.send_from_directory(app.static_folder, "index.html")



"""
Understanding the API:

/api/c/<entity>: creating a new entity (e.g., news, user, etc.)
/api/l/<action>: login action (e.g., login, logout)

"""


@app.route("/api/c/noticia", methods = ["POST"])
def publicar_endpoint():
    titulo = flask.request.form.get("titulo")
    subtitulo = flask.request.form.get("subtitulo")
    contenido = flask.request.form.get("contenido")
    srp.save(Noticia(titulo, subtitulo, contenido, periodista="Redaccion"))
    return flask.redirect("/noticias")

@app.route("/api/l/logout", methods = ["POST"])
def logout():
    flask_login.logout_user()
    return flask.send_from_directory("/noticias")

@app.route("/api/d/noticia/<int:id>", methods = ["DELETE"])
def delete_noticia(id):
    noticia = srp.find_first(Noticia, lambda x: x.ID == id)
    if srp.delete(noticia.__oid__):
        return flask.jsonify({"status": "success", "message": "Noticia eliminada"}), 200
    else:
        return flask.jsonify({"status": "error", "message": "Noticia no encontrada"}), 404
    

#@app.errorhandler(404)
#def not_found(code):
#    return flask.abort(404)
@lm.user_loader
def user_loader(email):
    return Usuario.find(srp, email)

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")

@app.route("/api/l/register", methods=["POST"])
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

@app.route("/api/l/login", methods=["POST"])
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


if __name__ == "__main__":
    app.run(debug=True)