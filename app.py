from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cadastro.sqlite3"

Session(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    nomeusuario = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(15), nullable=False)

    def __init__(self, nomeusuario, senha):
        self.nomeusuario = nomeusuario
        self.senha = senha

@app.route('/')
def index():
  return render_template('index.html')


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nomeusuario = request.form["nomeusuario"]
        senha = request.form["senha"]
        user = User(nomeusuario, senha)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("registrar.html")

@app.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "POST":
        nomeusuario = request.form["nomeusuario"]
        senha = request.form["senha"]
        user = User.query.filter_by(nomeusuario=nomeusuario, senha=senha).first()
        if user:
            session["user"] = user.id
            return redirect(url_for("perfil"))
        else:
            return redirect(url_for("login"))
  return render_template("login.html")

@app.route("/perfil")
def perfil():
    user_id = session.get("user")
    if user_id:
        user = User.query.get(user_id)
        return render_template("perfil.html", nomeusuario = user.nomeusuario)
    else:
        return redirect(url_for("login"))

@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)